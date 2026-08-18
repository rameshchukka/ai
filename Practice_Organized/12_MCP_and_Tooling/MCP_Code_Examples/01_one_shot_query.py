"""
One-shot query example — idfc-coder Python SDK.

Use this pattern for simple, single-turn asks where you just want
a text answer back (e.g. from a script or notebook).

Requires:
    pip install idfc-coder --index-url \
        https://artifactory.idfcfirstbank.com/artifactory/api/pypi/idfc-pypi-local/simple

Credentials (AD-based auth to the internal LLM) must be set in the
environment before running:
    export AD_USERNAME=your.username
    export AD_PASSWORD='your-password'   # single-quote if it has $ ! ` etc.
"""

import asyncio

from idfc_coder.sdk import query, AssistantMessage, TextBlock


async def main() -> None:
    prompt = "What files are in this project?"

    async for msg in query(prompt=prompt):
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="")

    print()  # trailing newline after streamed output


if __name__ == "__main__":
    asyncio.run(main())
