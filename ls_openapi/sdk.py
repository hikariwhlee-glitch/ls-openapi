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


def _instrument_tokens(value: str) -> list[str]:
    """Normalize a natural-language instrument query or master name into tokens."""
    text = value.casefold()
    text = re.sub(r"kospi\\s*[-_]?\\s*200|코스피\\s*[-_]?\\s*200", " 코스피200 ", text)
    text = re.sub(r"kosdaq\\s*[-_]?\\s*150|코스닥\\s*[-_]?\\s*150", " 코스닥150 ", text)
    text = re.sub(r"코스피200\\s*위클리\\s*옵션|코스닥150\\s*위클리\\s*옵션|미니\\s*(선물|옵션)|지수\\s*(선물|옵션)|주식\\s*선물|상품\\s*선물|콜\\s*옵션|풋\\s*옵션", lambda m: re.sub(r"\\s+", " ", m.group(0)), text)
    text = re.sub(r"코스피200위클리옵션", "코스피200 위클리 옵션", text)
    text = re.sub(r"코스닥150위클리옵션", "코스닥150 위클리 옵션", text)
    text = re.sub(r"미니(선물|옵션)", r"미니 \\1", text)
    text = re.sub(r"(지수|주식|상품)(선물|옵션)", r"\\1 \\2", text)
    text = re.sub(r"(콜|풋)옵션", r"\\1 옵션", text)
    text = re.sub(r"찾아\\s*줘|찾아\\s*주세요|검색(?:해)?\\s*줘|검색(?:해)?\\s*주세요|조회(?:해)?\\s*줘|조회(?:해)?\\s*주세요|알려\\s*줘|알려\\s*주세요|보여\\s*줘|보여\\s*주세요", " ", text)
    text = re.sub(r"\\b(?:please|find|search|lookup|look|up|show|tell|me|the|contract|instrument)\\b", " ", text)
    text = re.sub(r"[^0-9a-z가-힣]+", " ", text)
    ignored = {
        "선물", "선물형", "future", "futures", "옵션", "option", "options",
        "종목", "코드", "상품코드", "검색", "조회", "알려", "찾아", "주세요",
        "줘", "해줘", "부탁", "부탁해", "관련", "거래", "가능한",
    }
    aliases = {
        "콜": "c", "콜옵션": "c", "call": "c",
        "풋": "p", "풋옵션": "p", "put": "p",
        "mini": "미니", "weekly": "위클리",
        "kospi200": "코스피200", "kosdaq150": "코스닥150",
        "index": "지수", "stock": "주식", "commodity": "상품",
    }
    tokens: list[str] = []
    for token in text.split():
        if token in ignored:
            continue
        token = aliases.get(token, token)
        if token and token not in tokens:
            tokens.append(token)
    return tokens


class MarketData:
    """Domestic futures/options market-data helpers."""

    def __init__(self, client: LSOpenAPI):
        self._client = client

    def search_instruments(
        self,
        query: str,
        *,
        instrument_type: Literal["futures", "options"] = "futures",
        asset_class: Literal["all", "index", "stock", "commodity"] = "all",
        limit: int = 20,
    ) -> dict[str, Any]:
        """Search LS derivative masters by natural-language name, category or code.

        Product families are loaded from LS's index, stock and commodity masters.
        Results are candidates: expiry, strike and contract variant are never
        guessed or silently selected.
        """
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty instrument name or code")
        if instrument_type not in {"futures", "options"}:
            raise ValueError("instrument_type must be 'futures' or 'options'")
        if asset_class not in {"all", "index", "stock", "commodity"}:
            raise ValueError("asset_class must be 'all', 'index', 'stock', or 'commodity'")
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 100:
            raise ValueError("limit must be an integer from 1 to 100")

        query_tokens = _instrument_tokens(query)
        if not query_tokens and not re.search(r"선물|future|옵션|option|파생", query, re.IGNORECASE):
            raise ValueError("query must include a product name, category or symbol code")

        plans: list[tuple[str, dict[str, str], str, str, str]] = []
        if instrument_type == "futures":
            if asset_class in {"all", "index"}:
                plans.extend([
                    ("t9943", {"gubun": ""}, "t9943OutBlock", "index", "지수선물"),
                    ("t9943", {"gubun": "V"}, "t9943OutBlock", "index", "변동성 지수 선물"),
                    ("t9943", {"gubun": "S"}, "t9943OutBlock", "index", "섹터 지수 선물"),
                    ("t8467", {"gubun": "Q"}, "t8467OutBlock", "index", "코스닥150 지수 선물"),
                    ("t8435", {"gubun": "MF"}, "t8435OutBlock", "index", "미니 선물"),
                    ("t8435", {"gubun": "SF"}, "t8435OutBlock", "index", "코스닥150 선물"),
                ])
            if asset_class in {"all", "stock"}:
                plans.append(("t8401", {}, "t8401OutBlock", "stock", "주식 선물"))
            if asset_class in {"all", "commodity"}:
                plans.append(("t8426", {"dummy": ""}, "t8426OutBlock", "commodity", "상품 선물"))
        else:
            if asset_class in {"all", "index"}:
                plans.extend([
                    ("t9944", {"dummy": ""}, "t9944OutBlock", "index", "지수 옵션"),
                    ("t8433", {"dummy": ""}, "t8433OutBlock", "index", "지수옵션"),
                    ("t8435", {"gubun": "MO"}, "t8435OutBlock", "index", "미니 옵션"),
                    ("t8435", {"gubun": "WK"}, "t8435OutBlock", "index", "코스피200 위클리 옵션"),
                    ("t8435", {"gubun": "QW"}, "t8435OutBlock", "index", "코스닥150 위클리 옵션"),
                ])

        matches: list[dict[str, Any]] = []
        seen_codes: set[str] = set()
        called_trs: list[str] = []
        for tr_code, params, output_block, family, product_family in plans:
            if tr_code not in called_trs:
                called_trs.append(tr_code)
            response = self._client.call(tr_code, params)
            rows = response.get(output_block, [])
            if not isinstance(rows, list):
                raise RuntimeError(f"{tr_code} response did not contain an array in {output_block}")
            for row in rows:
                if not isinstance(row, dict):
                    continue
                name = str(row.get("hname", "")).strip()
                code = str(row.get("shcode", "")).strip()
                extended_code = str(row.get("expcode", "")).strip()
                identity = code or extended_code
                if identity and identity in seen_codes:
                    continue
                family_words = {
                    "index": "지수 index",
                    "stock": "주식 개별주식 stock",
                    "commodity": "상품 원자재 commodity",
                }[family]
                searchable = _instrument_tokens(
                    f"{name} {code} {extended_code} {family_words} {product_family}"
                )
                if all(token in searchable for token in query_tokens):
                    if identity:
                        seen_codes.add(identity)
                    matches.append({
                        "name": name,
                        "code": code,
                        "extended_code": extended_code,
                        "asset_class": family,
                        "instrument_type": instrument_type,
                        "product_family": product_family,
                        "master_tr": tr_code,
                    })

        return {
            "query": query,
            "instrument_type": instrument_type,
            "asset_class": asset_class,
            "master_tr": called_trs[0] if len(called_trs) == 1 else None,
            "master_trs": called_trs,
            "match_count": len(matches),
            "returned_count": min(len(matches), limit),
            "unsupported": (
                ["stock options", "commodity options"]
                if instrument_type == "options" and asset_class in {"all", "stock", "commodity"}
                else []
            ),
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
