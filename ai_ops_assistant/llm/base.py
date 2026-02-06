from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class LLMClient(ABC):
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], response_format: Optional[Any] = None) -> Any:
        pass
