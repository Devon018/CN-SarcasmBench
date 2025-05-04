from model import ModelManager
import json
import logging
import concurrent.futures
import os
import re
from pathlib import Path

# Define permutation constants
PERMUTATIONS = [
    ['A', 'B', 'C', 'D'],
    ['D', 'A', 'B', 'C'],
    ['C', 'D', 'A', 'B'],
    ['B', 'C', 'D', 'A']
]

class GenericEvaluationTask:
    """
    Wraps the original evaluation process into a reusable task class.
    Can be used in different scenarios with different model names, prompt paths and custom evaluation methods.
    Supports checkpoint resumption.
    """
    def __init__(
        self,
        task_name: str,
        prompt_path: str,
        model: ModelManager,
        data_file: str,
        output_file: str,
        enable_multithread: bool = False,  # Whether to enable multithreading
        without_context: bool = False,     # Whether to use context
        without_circulaeval: bool = False, # Whether to use circular evaluation
    ):
        """
        Args:
            task_name: Task name
            prompt_path: System prompt file path
            model_name: Model name
            data_file: Test data file path
            output_file: Result save file path
            enable_multithread: Whether to enable multithreaded processing
            without_context: Whether to disable context usage
            without_circulaeval: Whether to disable circular evaluation
            few_shot: Number of samples for few-shot learning
        """
        self.task_name = task_name
        self.prompt_path = prompt_path
        self.model_name = model
        self.data_file = data_file
        self.output_file = output_file
        self.without_context = without_context
        self.without_circulaeval = without_circulaeval
        
        # Intermediate result file
        self.checkpoint_file = f"{os.path.splitext(self.output_file)[0]}_checkpoint.json"

        # Initialize model
        self.manager = model
        self.system_prompt = self.load_system_prompt()
    
    def filter_data(self, dataset):
        """
        Filter dataset, retain samples to be evaluated
        """
        raise NotImplementedError("Please implement specific filtering logic in subclass")
    
    def evaluate_permutation_func(self, data, system_prompt, perm, manager):
        """
        Evaluate a single permutation
        Specific logic needs to be implemented in subclass
        """
        raise NotImplementedError("Please implement specific evaluation logic in subclass")
        
    def load_and_process_data(self) -> list:
        """Load and return multiple-choice test data"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        dataset = self.filter_data(dataset)
        return dataset

    def load_system_prompt(self) -> str:
        """Load system prompt text"""
        with open(self.prompt_path, 'r', encoding='utf-8') as f:
            return f.read()

    def evaluate_question(self, data: dict, system_prompt: str) -> dict:
        """
        Test all permutations for a single question
        Sequential processing, without multithreading
        """
        # Sequential processing of permutations
        raise NotImplementedError("Please implement specific evaluation logic in subclass")

    
    def load_checkpoint(self):
        """Load checkpoint file to get processed results"""
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                    checkpoint_data = json.load(f)
                logging.info(f"Checkpoint data loaded, containing {len(checkpoint_data['details'])} processed questions")
                return checkpoint_data.get('details', [])
            except Exception as e:
                logging.warning(f"Failed to load checkpoint file: {str(e)}, will start from beginning")
        return []
    
    def save_checkpoint(self, results):
        """Save checkpoint file"""
        os.makedirs(os.path.dirname(self.checkpoint_file), exist_ok=True)
        total_attempts, correct_attempts, accuracy = self.calculate_metrics(results)
        try:
            # Calculate current statistics
            
            checkpoint_data = {
                "task": self.task_name,
                "statistics": {
                    "total_questions": len(results),
                    "total_attempts": total_attempts,
                    "correct_attempts": correct_attempts,
                    "accuracy": f"{accuracy:.2%}"
                },
                "details": results
            }
            
            with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)
            
            logging.info(f"Checkpoint data saved, total of {len(results)} questions")
        except Exception as e:
            logging.error(f"Failed to save checkpoint file: {str(e)}")

    def calculate_metrics(self, results):
        raise NotImplementedError("Please implement specific evaluation metrics calculation logic in subclass")
    
    def filter_data(self, dataset):
        """
        Filter data
        Specific logic needs to be implemented in subclass
        """
        raise NotImplementedError("Please implement specific filtering logic in subclass")
    
    def run(self, max_questions: int = 0):
        """
        Run evaluation and save results
        Use multithreading based on enable_multithread setting
        Supports checkpoint resumption
        """
        # Ensure log directory exists
        if os.path.exists(self.output_file):
            print("Task already completed, skipping...")
            return 
        log_dir = f"./output/{self.task_name}"
        os.makedirs(log_dir, exist_ok=True)
        
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(f"{log_dir}/evaluation.log", mode='w'),
                logging.StreamHandler()
            ]
        )

        # Load checkpoint data
        results = self.load_checkpoint()
        processed_ids = {r["question_id"] for r in results}
        
        # Load data and system prompt
        dataset = self.load_and_process_data()
        system_prompt = self.load_system_prompt()

        # Filter out processed questions
        unprocessed_dataset = [data for data in dataset if data["id"] not in processed_ids]
        logging.info(f"Skipped {len(processed_ids)} processed questions, {len(unprocessed_dataset)} questions remaining")
        
        # Process only first n questions for demonstration, this limit can be removed
        if max_questions > 0:
            # Process only the first max_questions from remaining unprocessed questions
            subset = unprocessed_dataset[:max_questions]
        else:
            # Process all unprocessed questions
            subset = unprocessed_dataset
        # Process questions sequentially
        for data in subset:
            question_id = data["id"]
            try:
                result = self.evaluate_question(data, system_prompt)
                results.append(result)
                logging.info(f"Question {question_id} completed")
                
                # Save checkpoint after each question
                self.save_checkpoint(results)
            except Exception as e:
                logging.error(f"Question {question_id} evaluation failed: {str(e)}")

        total_attempts, correct_attempts, accuracy = self.calculate_metrics(results)

        # Save final results
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "task": self.task_name,
                "statistics": {
                    "total_questions": len(results),
                    "total_attempts": total_attempts,
                    "correct_attempts": correct_attempts,
                    "accuracy": f"{accuracy:.2%}"
                },
                "details": results
            }, f, ensure_ascii=False, indent=2)
        
        # Delete checkpoint file after all questions are processed
        if len(unprocessed_dataset) == len(subset):
            try:
                if os.path.exists(self.checkpoint_file):
                    os.remove(self.checkpoint_file)
                    logging.info("Task completed, checkpoint file deleted")
            except Exception as e:
                logging.warning(f"Failed to delete checkpoint file: {str(e)}")