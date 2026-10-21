"""Domain-oriented convenience facade over the raw LS TR client.

Most helpers return LS response dictionaries unchanged; instrument search returns
a compact list of matching name/code candidates. Use LSOpenAPI.call for any TR
that does not yet have a convenience method.
"""
from __future__ import annotations

from datetime import date
import re
from typing import Any, Literal

from .client import LSAPIError, LSOpenAPI
from .websocket import LSWebSocket


def _normalize_instrument_text(value: str) -> str:
    """Normalize Korean/English symbol names and remove generic product words."""
    normalized = re.sub(r"[\\W_]+", "", value.casefold())
    normalized = normalized.replace("kospi200", "코스피200").replace("kosdaq150", "코스닥150")
    for word in ("futures", "future", "options", "option", "선물", "옵션"):
        normalized = normalized.replace(word, "")
    return normalized


class MarketData:
    """Domestic futures/options market-data helpers."""

    def __init__(self, client: LSOpenAPI):
        self._client = client

    def search_instruments(
        self,
        query: str,
        *,
        instrument_type: Literal["futures", "options"] = "futures",
        limit: int = 20,
    ) -> dict[str, Any]:
        """Search index futures/options master lists by name or symbol code.

        Futures use t9943; options use t9944. Multiple contracts are returned
        as candidates so the caller can choose the intended expiry/strike.
        """
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty instrument name or code")
        if instrument_type not in {"futures", "options"}:
            raise ValueError("instrument_type must be 'futures' or 'options'")
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 100:
            raise ValueError("limit must be an integer from 1 to 100")

        if instrument_type == "futures":
            tr_code, output_block, params = "t9943", "t9943OutBlock", {"gubun": "V"}
        else:
            tr_code, output_block, params = "t9944", "t9944OutBlock", {"dummy": ""}

        normalized_query = _normalize_instrument_text(query)
        if not normalized_query:
            raise ValueError("query must include an instrument name or symbol code")

        response = self._client.call(tr_code, params)
        rows = response.get(output_block, [])
        if not isinstance(rows, list):
            raise RuntimeError(f"{tr_code} response did not contain an array in {output_block}")

        matches = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            name = str(row.get("hname", "")).strip()
            code = str(row.get("shcode", "")).strip()
            extended_code = str(row.get("expcode", "")).strip()
            searchable = _normalize_instrument_text(f"{name} {code} {extended_code}")
            if normalized_query in searchable:
                matches.append(
                    {
                        "name": name,
                        "code": code,
                        "extended_code": extended_code,
                    }
                )

        return {
            "query": query,
            "instrument_type": instrument_type,
            "master_tr": tr_code,
            "match_count": len(matches),
            "returned_count": min(len(matches), limit),
            "results": matches[:limit],
        }

    def quote(self, code: str) -> dict[str, Any]:
        """Get the current quote (t2111) for a futures/options code."""
        return self._client.call("t2111", {"focode": code})

    def orderbook(self, code: str) -> dict[str, Any]:
        """Get the current order book (t2112) for a futures/options code."""
        return self._client.call("t2112", {"shcode": code})

    def tick_chart(
        self,
        code: str,
        *,
        count: int = 200,
        interval: int = 1,
        end_date: str | None = None,
        start_date: str = "",
        start_time: str = "",
        end_time: str = "",
        compressed: bool = False,
    ) -> dict[str, Any]:
        """Get tick/minute chart data (t8464); dates use YYYYMMDD."""
        if count < 1:
            raise ValueError("count must be positive")
        if interval < 1:
            raise ValueError("interval must be positive")
        today = date.today().strftime("%Y%m%d")
        params = {
            "shcode": code,
            "ncnt": interval,
            "qrycnt": count,
            "nday": 0,
            "sdate": start_date,
            "stime": start_time,
            "edate": end_date or today,
            "etime": end_time,
            "cts_date": "",
            "cts_time": "",
            "comp_yn": "Y" if compressed else "N",
        }
        return self._client.call("t8464", params)


class Account:
    """Domestic futures/options account read helpers."""

    def __init__(self, client: LSOpenAPI):
        self._client = client

    def balance(self, *, continuation_key: str = "", continuation: bool = False) -> dict[str, Any]:
        """Get account balance and positions (t0441)."""
        return self._client.call(
            "t0441",
            {"cts_expcode": "", "cts_medocd": ""},
            continuation_key=continuation_key,
            continuation=continuation,
        )

    def orders(
        self,
        *,
        code: str = "",
        filled: Literal["0", "1", "2"] = "0",
        sort: Literal["1", "2"] = "1",
        continuation_key: str = "",
        continuation: bool = False,
    ) -> dict[str, Any]:
        """Get executions/open orders (t0434)."""
        return self._client.call(
            "t0434",
            {
                "expcode": code,
                "chegb": filled,
                "sortgb": sort,
                "cts_ordno": " ",
            },
            continuation_key=continuation_key,
            continuation=continuation,
        )


class Orders:
    """Order, amend and cancel helpers. Disabled unless allow_orders=True."""

    def __init__(self, client: LSOpenAPI):
        self._client = client

    @staticmethod
    def _positive_quantity(quantity: int) -> None:
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
            raise ValueError("quantity must be a positive integer")

    def new(
        self,
        instrument_code: str,
        *,
        side: Literal["buy", "sell"],
        quantity: int,
        price: float,
    ) -> dict[str, Any]:
        """Submit a limit order (CFOAT00100); returns the raw LS response."""
        if not instrument_code.strip():
            raise ValueError("instrument_code is required")
        if side not in {"buy", "sell"}:
            raise ValueError("side must be 'buy' or 'sell'")
        self._positive_quantity(quantity)
        if price <= 0:
            raise ValueError("price must be positive")
        return self._client.call(
            "CFOAT00100",
            {
                "FnoIsuNo": instrument_code,
                "BnsTpCode": "2" if side == "buy" else "1",
                "FnoOrdprcPtnCode": "00",
                "FnoOrdPrc": price,
                "OrdQty": quantity,
            },
        )

    def amend(
        self,
        instrument_code: str,
        original_order_no: int | str,
        *,
        quantity: int,
        price: float,
        price_type: str = "00",
    ) -> dict[str, Any]:
        """Amend an order (CFOAT00200); returns the raw LS response."""
        if not instrument_code.strip():
            raise ValueError("instrument_code is required")
        self._positive_quantity(quantity)
        if price <= 0:
            raise ValueError("price must be positive")
        return self._client.call(
            "CFOAT00200",
            {
                "FnoIsuNo": instrument_code,
                "OrgOrdNo": original_order_no,
                "FnoOrdprcPtnCode": price_type,
                "FnoOrdPrc": price,
                "MdfyQty": quantity,
            },
        )

    def cancel(
        self,
        instrument_code: str,
        original_order_no: int | str,
        *,
        quantity: int,
    ) -> dict[str, Any]:
        """Cancel unfilled quantity (CFOAT00300); returns the raw LS response."""
        if not instrument_code.strip():
            raise ValueError("instrument_code is required")
        self._positive_quantity(quantity)
        return self._client.call(
            "CFOAT00300",
            {
                "FnoIsuNo": instrument_code,
                "OrgOrdNo": original_order_no,
                "CancQty": str(quantity),
            },
        )


class LSFutureClient(LSOpenAPI):
    """Convenient domestic futures/options SDK entry point.

    The raw call and iter_pages methods remain available for the full TR catalog.
    Trading endpoints still require explicit allow_orders=True.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.market = MarketData(self)
        self.account = Account(self)
        self.orders = Orders(self)

    def websocket(self, *, simulated: bool = False) -> LSWebSocket:
        """Create a WebSocket client; call connect() or use it as a context manager."""
        return LSWebSocket(self, simulated=simulated)


__all__ = ["LSFutureClient", "MarketData", "Account", "Orders", "LSAPIError"]
