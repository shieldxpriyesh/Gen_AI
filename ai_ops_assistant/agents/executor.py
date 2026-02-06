from typing import List, Dict, Any
from .planner import Plan
from ..tools.base import BaseTool

class ExecutorAgent:
    def __init__(self, tools: List[BaseTool]):
        self.tools_map = {t.name: t for t in tools}

    def execute_plan(self, plan: Plan) -> List[Dict[str, Any]]:
        results = []
        for step in plan.steps:
            tool = self.tools_map.get(step.tool_name)
            if not tool:
                results.append({
                    "step_id": step.id,
                    "error": f"Tool {step.tool_name} not found"
                })
                continue

            print(f"Executing step {step.id}: {step.description} using {step.tool_name}...")
            tool_output = tool.execute(**step.tool_args)
            results.append({
                "step_id": step.id,
                "tool": step.tool_name,
                "output": tool_output
            })
        return results
