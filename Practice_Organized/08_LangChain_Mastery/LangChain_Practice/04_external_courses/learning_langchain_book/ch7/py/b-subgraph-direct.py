from typing import TypedDict

from langgraph.graph import START, StateGraph


# Define the state types for parent and subgraph
class State(TypedDict):
    foo: str  # this key is shared with the subgraph


class SubgraphState(TypedDict):
    foo: str  # this key is shared with the parent graph
    bar: str


# Define subgraph
def subgraph_node(state: SubgraphState):
    # note that this subgraph node can communicate with the parent graph via the shared "foo" key
    return {"foo": state["foo"] + "bar"}


subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node("subgraph_node", subgraph_node)
# Additional subgraph setup would go here
subgraph = subgraph_builder.compile()

# Define parent graph
builder = StateGraph(State)
builder.add_node("subgraph", subgraph)
builder.add_edge(START, "subgraph")
# Additional parent graph setup would go here
graph = builder.compile()

# Example usage
initial_state = {"foo": "hello"}
result = graph.invoke(initial_state)
print(f"Result: {result}")  # Should append "bar" to the foo value
