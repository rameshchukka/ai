# Libraries for MCP client, LLM handling, and async operations
import asyncio
import json
import sys
from pathlib import Path
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import (
    Root,
    TextContent,
    CreateMessageResult,
    CreateMessageRequestParams,
    ListRootsResult,
)

# Configuration
SERVER_SCRIPT = str(Path(__file__).parent / "server.py")
PROJECT_DIR = Path(__file__).parent.resolve()

# StdioServerParameters launches "python server.py" via stdin/stdout
server_params = StdioServerParameters(
    command=sys.executable,  # Use same interpreter that runs this script
    args=[SERVER_SCRIPT],
)

# ROOTS — Tell the server which directories it can access
async def list_roots(context) -> ListRootsResult:
    """Limit the server's file access to this project directory."""
    return ListRootsResult(roots=[Root(uri=f"file://{PROJECT_DIR}", name=PROJECT_DIR.name)])

# Anthropic client used to fulfill sampling requests from the server
anthropic_client = Anthropic()

# SAMPLING — Handle LLM requests delegated from the server
async def handle_sampling(context, params: CreateMessageRequestParams) -> CreateMessageResult:
    """Run a Claude LLM call on behalf of the server and return the result."""
    # Extract the prompt text from the first sampling message
    prompt = params.messages[0].content.text

    print(f"\n[Sampling] Server requested LLM task:")
    print(f"  Prompt preview: {prompt[:150]}...")

    response = anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=params.maxTokens or 200,
        messages=[{"role": "user", "content": prompt}],
    )

    response_text = response.content[0].text
    print(f"  LLM Response: {response_text[:100]}...")

    return CreateMessageResult(
        role="assistant",
        content=TextContent(type="text", text=response_text),
        model="claude-sonnet-4-20250514",
    )

# HELPER — Call a tool on an already-open session and return parsed JSON
async def call_tool(session: ClientSession, tool_name: str, arguments: dict) -> dict:
    """Call a tool on the given session and return the parsed JSON result."""
    result = await session.call_tool(tool_name, arguments=arguments)
    # The server always returns a single TextContent item
    return json.loads(result.content[0].text)

# CONNECTION & DISCOVERY
async def verify_connection(session: ClientSession):
    """Verify all expected tools and resources exist on the given session."""
    print("=" * 60)
    print("MCP Connection Verification")
    print("=" * 60)

    # list_tools() sends a "tools/list" JSON-RPC request to the server
    tools_result = await session.list_tools()
    tool_names = [tool.name for tool in tools_result.tools]
    print("--- START SCREENSHOT ---")
    print(f"\nDiscovered {len(tool_names)} tools:")
    for tool in tools_result.tools:
        print(f"  - {tool.name}: {tool.description[:80]}...")

    assert "get_restaurant_info" in tool_names, "FAIL: get_restaurant_info not found!"
    assert "recommend_by_vibe" in tool_names, "FAIL: recommend_by_vibe not found!"
    assert "get_review" in tool_names, "FAIL: get_review not found!"
    print("\nAll required tools verified!")

    # list_resources() discovers data endpoints the server exposes
    resources_result = await session.list_resources()
    print(f"\nDiscovered {len(resources_result.resources)} resources:")
    for resource in resources_result.resources:
        print(f"  - {resource.uri}: {resource.name}")

    roots_result = await list_roots(None)
    print(f"\nConfigured {len(roots_result.roots)} roots:")
    for root in roots_result.roots:
        print(f"  - {root.name}: {root.uri}")

    print("--- END SCREENSHOT ---")

# DEMOS — Call each tool through the MCP protocol
async def demo_get_restaurant_info(session: ClientSession):
    """Demo: Look up a restaurant by name."""
    print("\n" + "-" * 60)
    print("Demo: get_restaurant_info('Iron & Embers')")
    print("-" * 60)

    data = await call_tool(session, "get_restaurant_info", {"restaurant_name": "Iron & Embers"})
    print(json.dumps(data, indent=2))

async def demo_recommend_by_vibe(session: ClientSession):
    """Demo: Find restaurants by vibe keyword."""
    print("\n" + "-" * 60)
    print("Demo: recommend_by_vibe('moody')")
    print("-" * 60)

    data = await call_tool(session, "recommend_by_vibe", {"vibe": "moody"})
    print(f"Vibe: {data['vibe_searched']}")
    print(f"Structured matches: {len(data['structured_matches'])}")
    for match in data["structured_matches"]:
        print(f"  - {match['name']} ({match['cuisine']}) - {match['rating']}/5")
    print(f"Raw text excerpts: {len(data['raw_text_excerpts'])}")

async def demo_get_review(session: ClientSession):
    """Demo: Retrieve a restaurant review."""
    print("\n" + "-" * 60)
    print("Demo: get_review('Iron & Embers')")
    print("-" * 60)

    data = await call_tool(session, "get_review", {"restaurant_name": "Iron & Embers"})
    print(json.dumps(data, indent=2))

# Main Entry Point
async def main():
    """Run all demos sequentially using a single shared MCP session."""
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read,
            write,
            sampling_callback=handle_sampling,
            list_roots_callback=list_roots,
        ) as session:
            await session.initialize()

            await demo_get_restaurant_info(session)
            await demo_recommend_by_vibe(session)
            await demo_get_review(session)
            await verify_connection(session)

if __name__ == "__main__":
    asyncio.run(main())
