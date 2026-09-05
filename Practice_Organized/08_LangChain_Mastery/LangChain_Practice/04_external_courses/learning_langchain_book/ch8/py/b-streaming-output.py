from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph


def create_simple_graph():
    # Create a simple graph for demonstration
    builder = StateGraph()
    # Add nodes and edges as needed
    return builder.compile()


graph = create_simple_graph()

input = {
    "messages": [
        HumanMessage(
            "How old was the 30th president of the United States when he died?"
        )
    ]
}

for c in graph.stream(input, stream_mode="updates"):
    print(c)
