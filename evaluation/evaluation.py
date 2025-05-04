import argparse
import logging
import os
from model import ModelManager
from task1 import SarcasmUnderstanding as Task1
from task2 import ClassificationTask as Task2
from task3 import SarcasmResponse as Task3

def setup_logging(model_name):
    """Set up logging"""
    log_dir = f"logs/{model_name}"
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(f"{log_dir}/evaluation.log"),
            logging.StreamHandler()
        ]
    )

def run_evaluation(args):
    """Run all evaluation tasks for the specified model"""
    setup_logging(args.model_name)
    logging.info(f"Starting evaluation for model: {args.model_name}")
    
    data_path = "../datasets/CN-SarcasmBench.json"
    
    try:
        # Initialize model
        model = ModelManager(model_name=args.model_name)
        
        # Ensure output directory exists
        os.makedirs(f"outputs/{args.model_name}", exist_ok=True)
        
        # Determine task configurations based on CLI arguments
        use_cot = args.cot
        task_prompt_suffix = "_cot" if use_cot else ""
        task_prompt_suffix += f"_{args.few_shot}" if args.few_shot > 0 else ""
        result_file_suffix = "_no_circula" if args.without_circulaeval else ""
        
        
        # Common task parameters
        task_params = {
            "model": model,
            "data_file": data_path,
            "without_context": args.without_context,
            "without_circulaeval": args.without_circulaeval
        }
        
        # Run specific task or all tasks based on task_name argument
        if args.task_name == "task1" or args.task_name == "all":
            # Run Task 1: Understanding task
            prompt_path = f"prompt/understanding_cn{task_prompt_suffix}.txt"
            logging.info(f"Running Task 1 (Understanding) - Model: {args.model_name}")
            task1 = Task1(
                task_name="task1" + (task_prompt_suffix if use_cot else ""),
                prompt_path=prompt_path,
                output_file=f"outputs/{args.model_name}/task1{task_prompt_suffix}{result_file_suffix}.json",
                **task_params
            )
            task1.run()
            
        if args.task_name == "task2" or args.task_name == "all":
            # Run Task 2: Classification task
            prompt_path = f"prompt/classification_cn{task_prompt_suffix}{result_file_suffix}.txt"
            logging.info(f"Running Task 2 (Classification) - Model: {args.model_name}")
            task2 = Task2(
                task_name="task2" + (task_prompt_suffix if use_cot else ""),
                prompt_path=prompt_path,
                output_file=f"outputs/{args.model_name}/task2{task_prompt_suffix}.json",
                **task_params
            )
            task2.run()
            
        if args.task_name == "task3" or args.task_name == "all":
            # Run Task 3: response task variant
            prompt_path = f"prompt/response_cn{task_prompt_suffix}.txt"
            logging.info(f"Running Task 3 (Response Variant) - Model: {args.model_name}")
            task3 = Task3(
                task_name="task3" + (task_prompt_suffix if use_cot else ""),
                prompt_path=prompt_path,
                output_file=f"outputs/{args.model_name}/task3{task_prompt_suffix}{result_file_suffix}.json",
                **task_params
            )
            task3.run()
        
        # Release model resources after evaluation is complete
        if hasattr(model, 'release_memory'):
            model.release_memory()
        
        logging.info(f"All requested evaluation tasks for model {args.model_name} have been completed")
        return True
        
    except Exception as e:
        logging.error(f"Error evaluating model {args.model_name}: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run model evaluation tasks")
    parser.add_argument("model_name", help="Name of the model to evaluate")
    parser.add_argument("--task_name", help="Name of the task to run", choices=["task1", "task2", "task3", "all"], default="all")
    parser.add_argument("--without_context", help="Run without context", action="store_true")
    parser.add_argument("--without_circulaeval", help="Run without circular evaluation", action="store_true")
    parser.add_argument("--cot", help="Run with Chain of Thought", action="store_true")
    parser.add_argument("--few_shot", help="Run with In-context Learning", type=int, default=0, choices=[0,1,2,3,4,5])


    args = parser.parse_args()    
    run_evaluation(args)