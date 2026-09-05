from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    filter_messages,
)

# Sample messages
messages = [
    SystemMessage(content="you are a good assistant", id="1"),
    HumanMessage(content="example input", id="2", name="example_user"),
    AIMessage(content="example output", id="3", name="example_assistant"),
    HumanMessage(content="real input", id="4", name="bob"),
    AIMessage(content="real output", id="5", name="alice"),
]

# Filter for human messages
human_messages = filter_messages(messages, include_types="human")
print("Human messages:", human_messages)

# Filter to exclude certain names
excluded_names = filter_messages(
    messages, exclude_names=["example_user", "example_assistant"]
)
print("\nExcluding example names:", excluded_names)

# Filter by types and IDs
filtered_messages = filter_messages(
    messages, include_types=["human", "ai"], exclude_ids=["3"]
)
print("\nFiltered by types and IDs:", filtered_messages)
