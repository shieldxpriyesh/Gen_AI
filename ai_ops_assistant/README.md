# AI Operations Assistant

A local multi-agent system that plans, executes, and validates natural language tasks using real APIs.

## Architecture

The system follows a **Planner-Executor-Verifier** multi-agent architecture:

1.  **Planner Agent**: Analyzes the user's natural language request and generates a step-by-step execution plan (JSON). It selects the appropriate tools for each step.
2.  **Executor Agent**: Iterates through the plan, invoking the specific tools (Weather, GitHub) with the generated arguments. It collects output from each step.
3.  **Verifier Agent**: Reviews the execution results against the original query.
    *   **Feedback Loop**: If the results are insufficient (e.g., missing data), it provides specific feedback to the Planner. The Planner then generates a refined plan to address the missing information (up to 3 retries).
    *   **Success**: It formats the final structured answer.

### Agents & Tools
*   **Planner**: Uses LLM to create logical plans.
*   **Executor**: Routes commands to `WeatherTool` and `GitHubTool`.
*   **Verifier**: Uses LLM to validate completeness and correctness.

## Integrated APIs

1.  **Open-Meteo API**: Fetches real-time weather data (No API key required).
2.  **GitHub API**: Searches for repositories using the public search endpoint.

---

## Setup Instructions

### 1. Prerequisites
*   Python 3.8+
*   An OpenAI API Key

### 2. Installation
Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory (or `ai_ops_assistant/`) based on `.env.example`:

```bash
cp .env.example .env
```

**Required Variable:**
```ini
OPENAI_API_KEY=sk-proj-...  # Your actual OpenAI API Key
```

---

## Running the Project

Run the assistant using the CLI entry point:

```bash
# Basic usage
python3 -m ai_ops_assistant.main --query "Find the weather in Tokyo and the most popular python repo"

# Run with Mock LLM (if you don't have an API key)
python3 -m ai_ops_assistant.main --query "Find the weather in Tokyo" --mock
```

---

## Example Prompts

Here are 3-5 prompts to test the system's capabilities:

1.  **Multi-tool usage**:
    > "Find the current temperature in London and search for the 'requests' library on GitHub."

2.  **Weather only**:
    > "What is the weather code and wind speed in Paris right now?"

3.  **GitHub only (Sorting)**:
    > "Find the top 3 most starred repositories related to 'machine learning'."

4.  **Complex / Ambiguous (Tests Verifier)**:
    > "Check the weather in New York."
    *(If the tool returns error or partial data, the Verifier should trigger a retry).*

---

## Known Limitations / Tradeoffs

1.  **Context Window**: The current implementation sends full history in retries. For very long conversations, this could hit token limits (though unlikely for single-turn tasks).
2.  **Tool Simplicity**: The tools are wrappers around specific API endpoints. Extending to *any* API would require a more generic OpenAPI tool loader.
3.  **GitHub Rate Limits**: Unauthenticated GitHub API requests are rate-limited (60/hour). Heavy usage might require adding a GitHub Token.
4.  **Mock LLM**: The `--mock` mode uses hardcoded responses for specific queries (Tokyo/Python). It does not generalize to other queries without code modification.
