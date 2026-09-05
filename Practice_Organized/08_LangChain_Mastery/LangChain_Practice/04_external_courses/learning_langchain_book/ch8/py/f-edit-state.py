from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver


def main():
    # Create a simple graph
    builder = StateGraph()
    # Add nodes and edges as needed
    graph = builder.compile(checkpointer=MemorySaver())

    config = {"configurable": {"thread_id": "1"}}

    state = graph.get_state(config)
    print("Current state:", state)

    # something you want to add or replace
    update = {}

    graph.update_state(config, update)
    print("State updated")


if __name__ == "__main__":
    main()
