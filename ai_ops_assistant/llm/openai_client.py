import os
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
from .base import LLMClient
from dotenv import load_dotenv

load_dotenv()

class OpenAIClient(LLMClient):
    def __init__(self, model: str = "gpt-4o"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat(self, messages: List[Dict[str, str]], response_format: Optional[Any] = None) -> Any:
        kwargs = {
            "model": self.model,
            "messages": messages,
        }
        
        try:
            if response_format:
                kwargs["response_format"] = response_format
                response = self.client.beta.chat.completions.parse(**kwargs)
                return response.choices[0].message.parsed
            else:
                response = self.client.chat.completions.create(**kwargs)
                return response.choices[0].message.content
        except Exception as e:
            print(f"Error in LLM call: {e}")
            raise
