from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver


def main():
    # Create a simple graph
    builder = StateGraph()
    # Add nodes and edges as needed
    graph = builder.compile(checkpointer=MemorySaver())

    config = {"configurable": {"thread_id": "1"}}

    history = [state for state in graph.get_state_history(config)]

    print("History states:", len(history))

    # replay a past state
    if len(history) >= 3:
        result = graph.invoke(None, history[2].config)
        print("Replayed state result:", result)


if __name__ == "__main__":
    main()
