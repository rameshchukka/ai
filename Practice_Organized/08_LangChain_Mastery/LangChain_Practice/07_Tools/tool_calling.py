from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

# -------------------------------------------------------
# Step 1: Define the tool
# -------------------------------------------------------
@tool
def multiply(a: int, b: int) -> int:
    """Given 2 numbers a and b this tool returns their product"""
    return a * b

# -------------------------------------------------------
# Step 2: Initialize Gemini LLM and bind tools
# -------------------------------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key="AIzaSyAuKkH44_dvmH7dPqRBaUYvHvCy5kJG0oc"
)
llm_with_tools = llm.bind_tools([multiply])

TOOL_MAP = {"multiply": multiply}

# -------------------------------------------------------
# Step 3: First LLM call — model decides if tool is needed
# -------------------------------------------------------
user_message = HumanMessage(content="can you multiply 3 with 1000")
response = llm_with_tools.invoke([user_message])
print("LLM Response:", response)

# -------------------------------------------------------
# Step 4: Check if the LLM requested a tool call
# -------------------------------------------------------
if response.tool_calls:

    tool_messages = []

    for tool_call in response.tool_calls:
        tool_name    = tool_call["name"]     # e.g., "multiply"
        tool_args    = tool_call["args"]     # e.g., {"a": 3, "b": 1000}
        tool_call_id = tool_call["id"]       # unique ID to match result to call

        # -------------------------------------------------------
        # Step 5: Execute the tool locally
        # -------------------------------------------------------
        tool_fn = TOOL_MAP.get(tool_name)
        if not tool_fn:
            print(f"Unknown tool: {tool_name}")
            continue

        result = tool_fn.invoke(tool_args)
        print(f"Tool '{tool_name}' with args {tool_args} → Result: {result}")

        # -------------------------------------------------------
        # Step 6: Wrap result in ToolMessage
        # tool_call_id links this result to the LLM's specific tool request
        # -------------------------------------------------------
        tool_messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call_id
            )
        )

    # -------------------------------------------------------
    # Step 7: Second LLM call — pass full conversation + tool results
    # so the model can generate a natural language final response
    # With * — unpacks and flattens into the list (CORRECT)
    # -------------------------------------------------------
    final_response = llm_with_tools.invoke([
        user_message,     # original user question
        response,         # model's tool call decision
        *tool_messages    # tool execution results
    ])

    print("Final Response:", final_response.content)

else:
    # -------------------------------------------------------
    # No tool needed — model answered directly
    # -------------------------------------------------------
    print("Direct Response:", response.content)