from typing import List, Dict, Any
from pydantic import BaseModel
from ..llm.base import LLMClient

class VerificationResult(BaseModel):
    is_sufficient: bool
    final_answer: str
    missing_info: str

class VerifierAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def verify(self, original_query: str, execution_results: List[Dict[str, Any]]) -> VerificationResult:
        system_prompt = """You are a Verifier Agent.
Review the Original Query and the Execution Results.
Determine if the results are sufficient to answer the query.
If yes, provide a Final Answer.
If no, explain what is missing.

Return a JSON object matching the VerificationResult schema.
"""
        results_str = ""
        for res in execution_results:
            results_str += f"Step {res.get('step_id')}: Tool {res.get('tool')} -> {res.get('output')}\n"

        user_content = f"""Original Query: {original_query}

Execution Results:
{results_str}
"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        return self.llm.chat(messages, response_format=VerificationResult)
