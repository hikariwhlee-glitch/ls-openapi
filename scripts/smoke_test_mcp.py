"""Smoke-test the local MCP server without LS credentials or API calls."""

from __future__ import annotations

import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


EXPECTED_TOOLS = {
    "get_futures_quote",
    "get_futures_orderbook",
    "get_account_balance",
    "get_futures_tick_chart",
}


async def main() -> None:
    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", "ls_openapi.mcp_server"],
        env=os.environ.copy(),
    )
    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.list_tools()

    actual_tools = {tool.name for tool in result.tools}
    missing = EXPECTED_TOOLS - actual_tools
    if missing:
        raise AssertionError(f"MCP server is missing tools: {sorted(missing)}")
    print(f"MCP handshake passed; tools: {', '.join(sorted(actual_tools))}")


if __name__ == "__main__":
    asyncio.run(main())
