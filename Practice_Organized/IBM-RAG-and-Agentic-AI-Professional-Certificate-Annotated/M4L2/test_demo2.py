import asyncio
import json
import sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_SCRIPT = str((Path(__file__).parent / "server.py").resolve())
server_params = StdioServerParameters(command=sys.executable, args=[SERVER_SCRIPT])

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Session initialized", flush=True)
            result = await asyncio.wait_for(
                session.call_tool("recommend_by_vibe", {"vibe": "moody"}),
                timeout=30
            )
            data = json.loads(result.content[0].text)
            print(f"Got {len(data['structured_matches'])} structured matches", flush=True)
            print("DONE", flush=True)

asyncio.run(run())
