import os
from openai import OpenAI
import requests
from typing import Tuple, List, Dict, Optional, Union
import json
import logging
import yaml
try:
    from vllm import LLM, SamplingParams
    from vllm.sampling_params import GuidedDecodingParams
except ImportError:
    pass  # vLLM might not be installed if only using API models

class ModelManager:
    """
    A class to manage different LLM models using their respective APIs or local deployment.
    Supports:
    - OpenAI API models (GPT-4o, GPT-o1)
    - DeepSeek API models (deepseek-r1)
    - Local models via vLLM deployment (including Qwen models)
    """
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, base_url: Optional[str] = None, config_path: str = "config.yaml"):
        """
        Initialize the model manager.
        
        Args:
            model_name: Name of the model to use
            api_key: API key for the respective service
            base_url: Base URL for API calls (if different from default)
            config_path: Path to the configuration file
        """
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url
        self.config = self._load_config(config_path)
        self.model_type = self._determine_model_type()
        self.client = None
        self.vllm_model = None
        self.tokenizer = None
        
        self._setup_client()
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            logging.warning(f"Failed to load config from {config_path}: {e}")
            return {}
    
    def _determine_model_type(self) -> str:
        """Determine the type of model based on model name."""
        if self.model_name.startswith(("gpt-4o", "gpt-o1")):
            return "openai"
        elif "deepseek-r1" in self.model_name:
            return "deepseek"
        else:
            # Qwen models also fall under local vLLM deployment
            return "vllm"
    
    def _setup_client(self):
        """Set up the appropriate client based on model type."""
        if self.model_type == "openai":
            api_config = self.config.get("api", {}).get("openai", {})
            self.client = OpenAI(
                api_key=self.api_key or os.environ.get("OPENAI_API_KEY"),
                base_url=self.base_url or api_config.get("base_url", "https://api.openai.com/v1")
            )
        elif self.model_type == "deepseek":
            api_config = self.config.get("api", {}).get("deepseek", {})
            self.client = OpenAI(
                api_key=self.api_key or os.environ.get("DEEPSEEK_API_KEY"),
                base_url=self.base_url or api_config.get("base_url", "https://api.deepseek.com/v1")
            )
        elif self.model_type == "vllm":
            try:
                # Get vLLM configuration
                vllm_config = self.config.get("vllm", {})
                inference_config = vllm_config.get("inference", {})
                
                # Initialize vLLM model
                model_dtype = inference_config.get("dtype", "auto")

                tensor_parallel_size = inference_config.get("tensor_parallel_size", 1)
                max_model_len = inference_config.get("max_tokens", 1024)
                
                logging.info(f"Loading vLLM model: {self.model_name}")
                model_path = os.path.join(vllm_config.get("path", "../Models/"), self.model_name)
                
                self.vllm_model = LLM(
                    model=model_path,
                    tensor_parallel_size=tensor_parallel_size,
                    dtype=model_dtype,
                    trust_remote_code=True,
                    max_model_len=max_model_len,
                    gpu_memory_utilization=inference_config.get("gpu_memory_utilization", 0.9)
                )
                logging.info("vLLM model loaded successfully.")
            except NameError:
                raise ImportError("vLLM is not installed. Please install it to use local models.")
    
    def generate(self, system_prompt: str, user_prompt: str, context: Optional[List[Dict]] = None, 
                 temperature: Optional[float] = None, seed: Optional[int] = None, structed = None) -> Tuple[str, int, int]:
        """
        Generate a response from the model.
        
        Args:
            system_prompt: System prompt
            user_prompt: User prompt
            context: Additional conversation context
            temperature: Sampling temperature (overrides config)
            seed: Random seed (overrides config)
            structed: If specified, uses guided decoding for structured outputs
            
        Returns:
            Tuple of (content, response_tokens, prompt_tokens)
        """
        messages = [
                {'role': 'user', 'content': system_prompt+"\n"+ user_prompt}
            ]
        
        # Add context if provided
        if context:
            messages = context + messages

        # For OpenAI/DeepSeek models:
        if self.model_type in ["openai", "deepseek"]:
            api_config = self.config.get("api", {}).get(self.model_type, {})
            
            # Use provided parameters or fall back to config values
            temp = temperature if temperature is not None else api_config.get("temperature", 0.7)
            random_seed = seed if seed is not None else self.config.get("evaluation", {}).get("seed", 42)
            max_tokens = api_config.get("max_tokens", 1024)
            top_p = api_config.get("top_p", 0.9)
            
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temp,
                seed=random_seed,
                max_tokens=max_tokens,
                top_p=top_p
            )
            content = completion.choices[0].message.content
            response_tokens = completion.usage.completion_tokens
            prompt_tokens = completion.usage.prompt_tokens

        # For local vLLM models (including Qwen):
        elif self.model_type == "vllm":
            vllm_config = self.config.get("vllm", {}).get("inference", {})
            
            # Use provided parameters or fall back to config values
            temp = temperature if temperature is not None else vllm_config.get("temperature", 0.7)
            random_seed = seed if seed is not None else self.config.get("evaluation", {}).get("seed", 42)
            max_tokens = vllm_config.get("max_tokens", 1024)
            top_p = vllm_config.get("top_p", 0.9)
            top_k = vllm_config.get("top_k", 50)
            presence_penalty = vllm_config.get("presence_penalty", 0.0)
            frequency_penalty = vllm_config.get("frequency_penalty", 0.0)
            
            sampling_params_kwargs = {
                "temperature": temp,
                "seed": random_seed,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "top_k": top_k,
                "presence_penalty": presence_penalty,
                "frequency_penalty": frequency_penalty
            }
            
            sampling_params = SamplingParams(**sampling_params_kwargs)
            outputs = self.vllm_model.chat(messages, sampling_params)
            prompt_tokens = len(outputs[0].prompt_token_ids)
            response_tokens = len(outputs[0].outputs[0].token_ids)
            content = outputs[0].outputs[0].text
        
        content = content.split('</think>')[-1].strip()
        return content, response_tokens, prompt_tokens
    