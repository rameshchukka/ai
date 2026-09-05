from typing import TypedDict
from langgraph.graph import START, StateGraph


class State(TypedDict):
    foo: str


class SubgraphState(TypedDict):
    # none of these keys are shared with the parent graph state
    bar: str
    baz: str


# Define subgraph
def subgraph_node(state: SubgraphState):
    return {"bar": state["bar"] + "baz"}


subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node("subgraph_node", subgraph_node)
subgraph_builder.add_edge(START, "subgraph_node")
# Additional subgraph setup would go here
subgraph = subgraph_builder.compile()


# Define parent graph node that invokes subgraph
def node(state: State):
    # transform the state to the subgraph state
    response = subgraph.invoke({"bar": state["foo"]})
    # transform response back to the parent state
    return {"foo": response["bar"]}


builder = StateGraph(State)
# note that we are using `node` function instead of a compiled subgraph
builder.add_node("node", node)
builder.add_edge(START, "node")
# Additional parent graph setup would go here
graph = builder.compile()

# Example usage
initial_state = {"foo": "hello"}
result = graph.invoke(initial_state)
print(
    f"Result: {result}"
)  # Should transform foo->bar, append "baz", then transform bar->foo
