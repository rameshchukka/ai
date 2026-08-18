"""
Demo: idfc-coder SDK driving Atlassian (Jira/Confluence) + self-hosted
Bitbucket in a single multi-turn session.

WHAT THIS DEMO SHOWS
---------------------
1. Agent reads a Jira ticket for context               (Atlassian MCP - built-in)
2. Agent pulls the linked Confluence design doc         (Atlassian MCP - built-in)
3. Agent checks open PRs in the relevant Bitbucket repo (Bitbucket MCP - mcp.demo.json)
4. Everything runs in `phase="plan"` so it's read-only for the demo —
   safe to run live without risk of the agent changing anything.

BEFORE RUNNING
---------------
    cp .env.demo.example .env.demo      # fill in real values in .env.demo
    set -a; source .env.demo; set +a    # load them into this shell
    pip install idfc-coder --index-url \
        https://artifactory.idfcfirstbank.com/artifactory/api/pypi/idfc-pypi-local/simple
    python demo_atlassian_bitbucket.py

Edit the three constants below (JIRA_TICKET, BITBUCKET_WORKSPACE/REPO) to
match whatever you want to show live.
"""

import asyncio
import json
import os

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

# ---- Edit these for your demo ----
JIRA_TICKET = "PROJ-1234"
BITBUCKET_PROJECT = "PROJ"
BITBUCKET_REPO = "backend-api"
# -----------------------------------


def render(msg) -> None:
    if isinstance(msg, AssistantMessage):
        for block in msg.content:
            if isinstance(block, TextBlock):
                print(block.text, end="")
            elif isinstance(block, ToolUseBlock):
                print(f"\n  → calling tool: {block.name}({block.input})")

    elif isinstance(msg, ToolMessage):
        for block in getattr(msg, "content", []) or []:
            if isinstance(block, ToolResultBlock):
                status = "ERROR" if block.is_error else "ok"
                preview = str(block.content)[:200]
                print(f"    [{status}] {preview}")

    elif isinstance(msg, ResultMessage):
        print(f"\n\n-- done: {msg.num_turns} turns, {msg.duration_ms}ms --\n")


async def main() -> None:
    # sanity check before burning demo time on a missing token
    required = ["AD_USERNAME", "AD_PASSWORD", "ATLASSIAN_API_TOKEN",
                "BITBUCKET_URL", "BITBUCKET_TOKEN"]
    missing = [v for v in required if not os.environ.get(v)]
    if missing:
        raise SystemExit(f"Missing env vars: {', '.join(missing)} — source .env.demo first")

    opts = IDFCCoderOptions(
        cwd=os.getcwd(),
        phase="plan",                       # read-only for the demo
        mcp_config="./mcp.demo.json",        # adds the Bitbucket MCP server
        max_steps=50,
    )

    async with IDFCCoderClient(opts) as client:
        print(f"\n=== Step 1: Read Jira ticket {JIRA_TICKET} ===")
        async for msg in client.query(
            f"Look up Jira ticket {JIRA_TICKET}. Summarize the description, "
            f"acceptance criteria, and any linked Confluence pages."
        ):
            render(msg)

        print("\n=== Step 2: Pull the linked Confluence design doc ===")
        async for msg in client.query(
            "Open the Confluence page you just found and summarize the "
            "design approach in 5 bullet points."
        ):
            render(msg)

        print(f"\n=== Step 3: Check Bitbucket repo {BITBUCKET_PROJECT}/{BITBUCKET_REPO} ===")
        async for msg in client.query(
            f"List open pull requests in the {BITBUCKET_PROJECT}/{BITBUCKET_REPO} "
            f"Bitbucket repository. Flag any that look related to {JIRA_TICKET}."
        ):
            render(msg)

        print("\n=== Step 4: Tie it together ===")
        async for msg in client.query(
            "Based on the ticket, the design doc, and the open PRs, is this "
            "feature already in progress? Give a one-paragraph status summary."
        ):
            render(msg)


if __name__ == "__main__":
    asyncio.run(main())
