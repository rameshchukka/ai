import asyncio
from langgraph_sdk import get_client


async def invoke_retrieval_assistant():
    # Initialize the LangGraph client
    # Replace <DEPLOYMENT_URL> with your actual LangGraph deployment URL
    deployment_url = "http://localhost:2024"
    client = get_client(url=deployment_url)

    try:
        # Create a new thread
        thread = await client.threads.create(
            # Optional: Add metadata if needed
            metadata={
                "user_id": "example_user",
                "session": "retrieval_session"
            }
        )

        # Prepare the input for the retrieval graph
        input_data = {
            # You can add additional state keys if your graph expects them
            "query": "What is this document about?",
        }

        # Invoke the assistant on the created thread
        # Replace "retrieval_graph" with your actual assistant ID
        async for event in client.runs.stream(
            thread_id=thread["thread_id"],
            assistant_id="retrieval_graph",
            input=input_data,
            stream_mode="updates"  # Stream updates as they occur
        ):
            # Process and print each event
            print(f"Receiving event of type: {event.event}")
            print(event.data)
            print("\n")

    except Exception as e:
        print(f"An error occurred: {e}")

# If you're running this in a script, you'll need to use asyncio to run the async function

asyncio.run(invoke_retrieval_assistant())
