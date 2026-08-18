"""
Multi-turn conversation example — idfc-coder Python SDK, with MCP tools wired in.

This pattern is for anything that needs conversation state across turns
(the agent remembers what it did in turn 1 when you ask for turn 2),
and for pulling in extra tools (Jira, GitHub, your own internal MCP
server) beyond the built-ins.

Requires the same install + AD_USERNAME/AD_PASSWORD as the one-shot example.
"""

import asyncio

from idfc_coder.sdk import (
    IDFCCoderClient,
    IDFCCoderOptions,
    AssistantMessage,
    ToolMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    ToolResultBlock,
)

# MCP servers can be inline (dict, as below) or a path to an mcp.json file,
# e.g. mcp_config="./mcp.json"
MCP_CONFIG = {
    "mcpServers": {
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {
                # Pull from env rather than hardcoding — never commit real tokens.
                "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}",
            },
        },
        # HTTP-transport MCP server example (internal service):
        "internal-api": {
            "url": "https://mcp.iservebetter.idfcfirstbank.com/sse",
        },
    }
}


def render_message(msg) -> None:
    """Pretty-print any SDK message type to stdout."""
    if isinstance(msg, AssistantMessage):
        for block in msg.content:
            if isinstance(block, TextBlock):
                print(block.text, end="")
            elif isinstance(block, ToolUseBlock):
                print(f"\n  [tool call] {block.name}({block.input})")

    elif isinstance(msg, ToolMessage):
        # result of a tool execution
        for block in getattr(msg, "content", []) or []:
            if isinstance(block, ToolResultBlock):
                status = "ERROR" if block.is_error else "ok"
                print(f"  [tool result: {status}] {block.content!r:.200}")

    elif isinstance(msg, ResultMessage):
        print(
            f"\n\n-- turn complete: {msg.num_turns} turns, "
            f"{msg.duration_ms}ms, error={msg.is_error} --"
        )


async def main() -> None:
    opts = IDFCCoderOptions(
        cwd="/my/project",
        phase="plan",              # start read-only; switch to "execute" once you trust the plan
        mcp_config=MCP_CONFIG,
        max_steps=200,
        model=None,                # None = use default; or set e.g. "MiniMax-M2.5"
    )

    async with IDFCCoderClient(opts) as client:
        async for msg in client.query("What does this project do?"):
            render_message(msg)

        # Conversation state carries over — the agent remembers turn 1.
        async for msg in client.query("Now add tests for the untested modules"):
            render_message(msg)


if __name__ == "__main__":
    asyncio.run(main())
