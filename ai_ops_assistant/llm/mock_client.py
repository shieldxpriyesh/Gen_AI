from typing import List, Dict, Any, Optional
from .base import LLMClient
from ..agents.planner import Plan, PlanStep
from ..agents.verifier import VerificationResult

class MockLLMClient(LLMClient):
    def chat(self, messages: List[Dict[str, str]], response_format: Optional[Any] = None) -> Any:
        last_message = messages[-1]["content"] if messages else ""
        system_prompt = messages[0]["content"] if messages else ""

        print(f"🤖 Mock LLM received request. System prompt start: '{system_prompt[:30]}...'")

        if "Planner Agent" in system_prompt:
            return Plan(
                steps=[
                    PlanStep(
                        id=1,
                        description="Fetch current weather for Tokyo",
                        tool_name="get_weather",
                        tool_args={"city": "Tokyo"}
                    ),
                    PlanStep(
                        id=2,
                        description="Search for popular Python repositories",
                        tool_name="search_github_repos",
                        tool_args={"query": "python", "sort": "stars"}
                    )
                ]
            )
        
        if "Verifier Agent" in system_prompt:
            return VerificationResult(
                is_sufficient=True,
                final_answer="The weather in Tokyo is [Mock Data] and the most popular Python repo is [Mock Data].",
                missing_info=""
            )

        return "Mock response"
