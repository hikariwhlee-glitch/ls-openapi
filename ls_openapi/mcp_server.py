"""Local, read-only MCP server for LS domestic futures/options."""

from __future__ import annotations

from datetime import date
from functools import lru_cache
import os
from typing import Any, Literal

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from .sdk import LSFutureClient

# Load a project-local .env for desktop clients that only pass a working directory.
load_dotenv(os.environ.get("LS_OPENAPI_ENV_FILE") or None)

server = FastMCP("ls-openapi")


@lru_cache(maxsize=1)
def _client() -> LSFutureClient:
    """Create the REST client only when the first tool is called."""
    return LSFutureClient()


@server.tool()
def search_derivative_instruments(
    query: str,
    instrument_type: Literal["auto", "futures", "options"] = "auto",
    asset_class: Literal["all", "index", "stock", "commodity"] = "all",
    limit: int = 20,
) -> dict[str, Any]:
    """Find LS domestic derivatives from a natural-language request.

    Pass the user's product terms and keep meaningful constraints in query
    (for example "코스피200 미니 선물 최근월", "삼성전자 주식선물",
    "금 상품선물", or "코스피200 위클리 400 콜옵션"). Set instrument_type to auto unless the user specifies futures/options; set asset_class from the request to index, stock, commodity or all.
    Futures cover index, single-stock and commodity masters; options currently
    cover index options, including mini and weekly contracts. The LS master data
    does not expose a reliable common expiry/strike schema, so return candidates
    and never silently choose a contract when several match.
    """
    return _client().market.search_instruments(
        query,
        instrument_type=instrument_type,
        asset_class=asset_class,
        limit=limit,
    )


@server.tool()
def get_futures_quote(instrument_code: str) -> dict[str, Any]:
    """Read the latest domestic futures/options quote for a code such as A016C000."""
    return _client().market.quote(instrument_code)


@server.tool()
def get_futures_orderbook(instrument_code: str) -> dict[str, Any]:
    """Read the current domestic futures/options order book for an instrument code."""
    return _client().market.orderbook(instrument_code)


@server.tool()
def get_account_balance() -> dict[str, Any]:
    """Read domestic futures/options account balance and positions.

    This returns private account data to the connected MCP client. Use only with a
    trusted, local Codex installation.
    """
    return _client().account.balance()


@server.tool()
def get_futures_tick_chart(
    instrument_code: str,
    count: int = 200,
    interval: int = 1,
    end_date: str | None = None,
    compressed: bool = False,
) -> dict[str, Any]:
    """Read historical tick/minute chart rows (t8464); dates use YYYYMMDD."""
    if count < 1:
        raise ValueError("count must be positive")
    if interval < 1:
        raise ValueError("interval must be positive")
    params = {
        "shcode": instrument_code,
        "ncnt": interval,
        "qrycnt": count,
        "nday": 0,
        "sdate": "",
        "stime": "",
        "edate": end_date or date.today().strftime("%Y%m%d"),
        "etime": "",
        "cts_date": "",
        "cts_time": "",
        "comp_yn": "Y" if compressed else "N",
    }
    return _client().call("t8464", params)


def main() -> None:
    """Run the server over stdio for Codex and other local MCP hosts."""
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
