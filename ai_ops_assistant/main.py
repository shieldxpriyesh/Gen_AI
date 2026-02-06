import argparse
import sys
from ai_ops_assistant.llm.openai_client import OpenAIClient
from ai_ops_assistant.llm.mock_client import MockLLMClient
from ai_ops_assistant.tools.weather import WeatherTool
from ai_ops_assistant.tools.github import GitHubTool
from ai_ops_assistant.agents.planner import PlannerAgent
from ai_ops_assistant.agents.executor import ExecutorAgent
from ai_ops_assistant.agents.verifier import VerifierAgent

def main():
    parser = argparse.ArgumentParser(description="AI Operations Assistant")
    parser.add_argument("--query", type=str, required=True, help="Natural language task to perform")
    parser.add_argument("--model", type=str, default="gpt-4o", help="OpenAI model to use")
    parser.add_argument("--mock", action="store_true", help="Use mock LLM instead of OpenAI")
    args = parser.parse_args()

    print(f"🚀 Starting AI Operations Assistant for query: '{args.query}'\n")

    try:
        if args.mock:
            print("⚠️ USING MOCK LLM")
            llm = MockLLMClient()
        else:
            llm = OpenAIClient(model=args.model)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    tools = [WeatherTool(), GitHubTool()]
    
    planner = PlannerAgent(llm, tools)
    executor = ExecutorAgent(tools)
    verifier = VerifierAgent(llm)

    current_attempt = 0
    feedback = ""

    while current_attempt < max_retries:
        if current_attempt > 0:
            print(f"\n🔄 Attempt {current_attempt + 1}/{max_retries}: Retrying with feedback...")
            args.query = f"Original Query: {args.query}\nPrevious Attempt Feedback: {feedback}"

     
        print("🧠 Planner Agent: Thinking...")
        try:
            plan = planner.create_plan(args.query)
            print("📋 Plan created:")
            for step in plan.steps:
                print(f"  {step.id}. {step.description} (Tool: {step.tool_name})")
        except Exception as e:
            print(f"❌ Planning failed: {e}")
            sys.exit(1)

        print("\n⚙️ Executor Agent: Working...")
        results = executor.execute_plan(plan)
        
        print("\n✅ Verifier Agent: Checking details...")
        verification = verifier.verify(args.query, results)

        if verification.is_sufficient:
            print("\n" + "="*50)
            print("FINAL RESULT")
            print("="*50)
            print(verification.final_answer)
            return
        else:
            print("⚠️ Result might be incomplete.")
            print("Analysis:", verification.missing_info)
            feedback = verification.missing_info
            current_attempt += 1

    print("\n" + "="*50)
    print("FINAL RESULT (Partial)")
    print("="*50)
    print("Exceeded max retries. Partial answer:")
    print(verification.final_answer)

if __name__ == "__main__":
    main()
