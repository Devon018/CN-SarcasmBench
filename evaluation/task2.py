from model import ModelManager
import json
import logging
import concurrent.futures
import os
import re
from pathlib import Path
from base_task import GenericEvaluationTask


class ClassificationTask(GenericEvaluationTask):
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
        without_context: bool = False,     # Whether to use context or not
        without_circulaeval: bool = False  # Whether to use circular evaluation or not
    ):
        """
        Args:
            task_name: Task name
            prompt_path: Path to system prompt file
            model_name: Model name
            data_file: Path to test data file
            output_file: Path to save results
            enable_multithread: Whether to enable multithreaded processing
        """
        super().__init__(task_name, prompt_path, model, data_file, output_file, without_context, without_circulaeval)
       
        self.classification_map = { 
            "overstatement": "夸张",
            "understatement": "淡化",
            "contradiction": "反语",
            "fact": "事实",
            "metaphor": "比喻",
            "incongruity": "荒谬",
            "roleplay": "角色扮演"
        }
    def filter_data(self, dataset):
        """
        Filter the dataset, keeping only samples that need evaluation
        """
        filtered_data = []
        for data in dataset:
            if data["classification"] != "undefined":
                filtered_data.append(data)
        return filtered_data
    
    def evaluate_question(self, data, system_prompt):
        perm = None
        result = self.evaluate_permutation_func(data, system_prompt, perm, self.manager)
        
        return {
            "question_id": data["id"],
            "results": result
        }
    
    def evaluate_permutation_func(self, data, system_prompt, perm, manager):
        """
        Evaluate a single permutation
        Specific logic needs to be implemented in subclasses
        """
        # construct the prompt using the permutation
        context = data["comments"]

        # Generate user prompt
        context = context[-1] if self.without_context else context
        user_prompt = f"'context'：{context}"
        content, response_tokens, prompt_tokens = manager.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            # structed="classification",
        )
        result = {
            "question_id": data["id"],
            "original_answer": self.classification_map[data["classification"]],
            "content": content,
            "response_tokens": response_tokens,
            "prompt_tokens": prompt_tokens
        }
        return result
    
    def calculate_metrics(self, results):
        """
        Calculate evaluation metrics
        """
        total_attempts = 0
        correct_attempts = 0

        for single_question in results:
            result = single_question["results"]
            total_attempts += 1
            if result['original_answer'] in result["content"].strip():
                correct_attempts += 1
        accuracy = correct_attempts / total_attempts if total_attempts > 0 else 0
        return total_attempts, correct_attempts, accuracy

