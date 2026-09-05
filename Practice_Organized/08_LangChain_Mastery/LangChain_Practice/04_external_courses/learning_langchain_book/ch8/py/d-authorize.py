from langchain.schema import HumanMessage
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver


async def main():
    # Create a simple graph
    builder = StateGraph()
    # Add nodes and edges as needed
    graph = builder.compile(checkpointer=MemorySaver())

    input = {
        "messages": [
            HumanMessage(
                "How old was the 30th president of the United States when he died?"
            )
        ]
    }

    config = {"configurable": {"thread_id": "1"}}

    output = graph.astream(input, config, interrupt_before=["tools"])

    async for c in output:
        print(c)  # do something with the output


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
