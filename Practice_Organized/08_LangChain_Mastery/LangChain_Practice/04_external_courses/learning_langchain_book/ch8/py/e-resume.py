from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver


async def main():
    # Create a simple graph
    builder = StateGraph()
    # Add nodes and edges as needed
    graph = builder.compile(checkpointer=MemorySaver())

    config = {"configurable": {"thread_id": "1"}}

    output = graph.astream(None, config, interrupt_before=["tools"])

    async for c in output:
        print(c)  # do something with the output


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
