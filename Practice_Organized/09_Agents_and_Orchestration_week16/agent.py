"""
agent.py
Week 16 - Part A, Step 2-3: The agent loop

Implements a portable ReAct-style loop: the model receives the task plus a
scratchpad of what's happened so far, and responds with ONE JSON action per
turn - either a tool call or a final answer. This works identically across
Gemini, OpenRouter, and mock mode since it only needs call_llm(system, user),
not provider-specific function-calling APIs.

Run: python agent.py
"""

import json
from llm_client import call_llm
from tools import TOOLS

MAX_ITERATIONS = 6


def build_system_prompt() -> str:
    tool_descriptions = "\n".join(
        f"- {name}: {spec['description']}\n"
        f"  input schema: {spec['input_model'].model_json_schema()['properties']}"
        for name, spec in TOOLS.items()
    )

    return f"""You are a support agent that solves tasks by calling tools step by step.

Available tools:
{tool_descriptions}

On EVERY turn, respond with ONLY valid JSON (no markdown fences, no explanation) in ONE
of these two shapes:

To call a tool:
{{"thought": "brief reasoning", "action": "tool_name", "action_input": {{...}}}}

To give your final answer once you have enough information:
{{"thought": "brief reasoning", "action": "final_answer", "answer": "your answer to the user"}}

Only call one tool per turn. Use the observation from each tool call to decide your next
step. If a tool returns an error, do not call the same tool with the same bad input again -
adjust your approach or explain the problem in your final answer.
"""


def parse_action(raw_text: str) -> dict:
    """Defensive JSON parsing for the agent's action - same discipline as
    Week 14's parse_llm_json(), applied to agent actions instead of data
    extraction."""
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[len("json"):].lstrip("\n")
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        return {"error": "invalid_json", "detail": str(e), "raw": raw_text}


def execute_tool(action: str, action_input: dict) -> dict:
    if action not in TOOLS:
        return {"error": f"Unknown tool '{action}'. Available tools: {list(TOOLS.keys())}"}

    spec = TOOLS[action]
    try:
        validated_input = spec["input_model"](**action_input)
    except Exception as e:
        return {"error": f"Invalid input for tool '{action}': {e}"}

    return spec["function"](**validated_input.model_dump())


def run_agent(task: str, max_iterations: int = MAX_ITERATIONS, verbose: bool = True) -> str:
    system_prompt = build_system_prompt()
    scratchpad = ""

    for iteration in range(1, max_iterations + 1):
        user_prompt = f"Task: {task}\n\n{scratchpad}\nWhat is your next action?"

        raw_response = call_llm(system_prompt, user_prompt, temperature=0.0)
        parsed = parse_action(raw_response)

        if verbose:
            print(f"\n--- Iteration {iteration} ---")
            print("Raw model output:", raw_response)

        if "error" in parsed:
            scratchpad += f"\n[System note: your last response wasn't valid JSON - {parsed['error']}. Try again.]\n"
            continue

        thought = parsed.get("thought", "")
        action = parsed.get("action")

        if action == "final_answer":
            answer = parsed.get("answer", "(no answer provided)")
            if verbose:
                print(f"Thought: {thought}")
                print(f"Final answer: {answer}")
            return answer

        action_input = parsed.get("action_input", {})
        observation = execute_tool(action, action_input)

        if verbose:
            print(f"Thought: {thought}")
            print(f"Action: {action}({action_input})")
            print(f"Observation: {observation}")

        scratchpad += (
            f"\nThought: {thought}\n"
            f"Action: {action}\n"
            f"Action Input: {json.dumps(action_input)}\n"
            f"Observation: {json.dumps(observation)}\n"
        )

    return (
        f"[MAX ITERATIONS ({max_iterations}) REACHED] The agent could not complete this "
        f"task in the allotted steps. This is the guard working as intended - failing "
        f"loudly and stopping, rather than looping forever."
    )


if __name__ == "__main__":
    print("=" * 60)
    print("Test 1: single-tool task")
    print("=" * 60)
    result = run_agent("Look up the account details for customer cust_001.")
    print("\nRESULT:", result)

    print("\n" + "=" * 60)
    print("Test 2: multi-tool task")
    print("=" * 60)
    result = run_agent(
        "A customer says their laptop stand from order ord_1001 arrived damaged. "
        "Look up the order, check refund eligibility, and tell me what should happen next."
    )
    print("\nRESULT:", result)
