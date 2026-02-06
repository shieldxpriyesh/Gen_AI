from typing import List, Optional
from pydantic import BaseModel
from ..llm.base import LLMClient
from ..tools.base import BaseTool

class PlanStep(BaseModel):
    id: int
    description: str
    tool_name: str
    tool_args: dict

class Plan(BaseModel):
    steps: List[PlanStep]

class PlannerAgent:
    def __init__(self, llm: LLMClient, tools: List[BaseTool]):
        self.llm = llm
        self.tools = tools

    def create_plan(self, user_query: str) -> Plan:
        tools_desc = "\n".join([f"- {t.name}: {t.description}" for t in self.tools])
        
        system_prompt = f"""You are a Planner Agent.
Your goal is to create a step-by-step plan to answer the user's query.
You have access to the following tools:
{tools_desc}

Return a valid JSON object matching the Plan schema.
Each step should specify which tool to use and the arguments for it.
If no tool is needed for a step (e.g. final synthesis), you can use a hypothetical 'synthesize' tool or just describe it, but ideally map to available tools.
However, for this assignment, we mostly want to plan tool calls.
"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]

        return self.llm.chat(messages, response_format=Plan)
