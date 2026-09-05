import asyncio
from contextlib import aclosing

from langchain.schema import HumanMessage
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver


async def main():
    # Create a simple graph
    builder = StateGraph()
    # Add nodes and edges as needed
    graph = builder.compile(checkpointer=MemorySaver())

    event = asyncio.Event()

    input = {
        "messages": [
            HumanMessage(
                "How old was the 30th president of the United States when he died?"
            )
        ]
    }

    config = {"configurable": {"thread_id": "1"}}

    async with aclosing(graph.astream(input, config)) as stream:
        async for chunk in stream:
            if event.is_set():
                break
            else:
                print(chunk)  # do something with the output

    # Simulate interruption after 2 seconds
    await asyncio.sleep(2)
    event.set()


if __name__ == "__main__":
    asyncio.run(main())
