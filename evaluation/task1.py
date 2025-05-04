from model import ModelManager
import json
import logging
import concurrent.futures
import os
import re
from pathlib import Path
from base_task import GenericEvaluationTask

# Define permutation constants
PERMUTATIONS = [
    ['A', 'B', 'C', 'D'],
    ['D', 'A', 'B', 'C'],
    ['C', 'D', 'A', 'B'],
    ['B', 'C', 'D', 'A']
]

class SarcasmUnderstanding(GenericEvaluationTask):
    """
    Wrapper for the original evaluation process as a reusable task class.
    Can be used in different scenarios with different model names, prompt paths, and custom evaluation methods.
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
            prompt_path: System prompt file path
            model_name: Model name
            data_file: Test data file path
            output_file: Result save file path
            enable_multithread: Whether to enable multi-threaded processing
        """
        super().__init__(task_name, prompt_path, model, data_file, output_file, without_context, without_circulaeval)
    def filter_data(self, dataset):
        """
        Filter the dataset, keep samples that need evaluation
        """
        filtered_data = []
        for data in dataset:
            if data["Answer"] != "":
                filtered_data.append(data)
        return filtered_data
    
    def evaluate_question(self, data, system_prompt):

        single_results = []
        if self.without_circulaeval:
            # Directly evaluate a single question
            result = self.evaluate_permutation_func(data, system_prompt, ["A", "B", "C", "D"], self.manager)
            single_results.append(result)
        else:
            # Evaluate all permutations
            for perm in PERMUTATIONS:
                result = self.evaluate_permutation_func(data, system_prompt, perm, self.manager)
                single_results.append(result)
        
        return {
            "question_id": data["id"],
            "results": single_results
        }
    
    def evaluate_permutation_func(self, data, system_prompt, perm, manager):
        """
        Evaluate a single permutation
        The specific logic needs to be implemented in subclasses
        """
        # construct the prompt using the permutation
        question = data["question"]


        context = data["comments"]
        # change the order of the options according to the permutation
        option_A = data[perm[0]]
        option_B = data[perm[1]]
        option_C = data[perm[2]]
        option_D = data[perm[3]]

        # mapping original options to permuted options
        mapping = {
            perm[0]: "A",
            perm[1]: "B",
            perm[2]: "C",
            perm[3]: "D"
        }
        original_answer = data["Answer"].upper()
        mapping_answer = [mapping[option] for option in original_answer]
        mapping_answer = "".join(mapping_answer)
            
        # Generate user prompt
        context = context[-1] if self.without_context else context
        user_prompt = f"'context'：{context}\n'question'：{question}\n'A'：{option_A}\n'B'：{option_B}\n'C'：{option_C}\n'D'：{option_D}"

        content, response_tokens, prompt_tokens = manager.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            # structed="multiple choice",
        )
        result = {
            "question_id": data["id"],
            "original_answer": mapping_answer,
            "permutation": perm,
            "content": content,
            "response_tokens": response_tokens,
            "prompt_tokens": prompt_tokens
        }
        return result
    
    def calculate_metrics(self, results):

        total_attempts = 0
        correct_attempts = 0

        for single_question in results:
            single_results = single_question["results"]
            correct = True
            for result in single_results:
                # if set(result["content"].strip()) != set(result["original_answer"]):
                #     correct = False
                #     break
                model_choices = set(re.findall(r'[A-Da-d]', result["content"].upper()))
                correct_choices = set(result["original_answer"].upper())
                if model_choices != correct_choices:
                    correct = False
                    break
            if correct:
                total_attempts += 1
                correct_attempts += 1
            else:
                total_attempts += 1
        accuracy = correct_attempts / total_attempts if total_attempts > 0 else 0
        return total_attempts, correct_attempts, accuracy

