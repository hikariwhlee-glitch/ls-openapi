"""Exercise the published LSFutureClient facade against read-only LS APIs."""
from __future__ import annotations

import os
import sys
from typing import Any

from ls_openapi import LSAPIError, LSFutureClient


def rows(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        return [value]
    return value if isinstance(value, list) else []


def fail_detail(exc: Exception) -> str:
    if not isinstance(exc, LSAPIError):
        return type(exc).__name__
    payload = exc.payload if isinstance(exc.payload, dict) else {}
    code = str(payload.get("rsp_cd", "")).strip()
    return f"LS API 오류 {code}".strip()


def main() -> int:
    code = os.getenv("LS_FUTURES_CODE", "A016C000").strip()
    client: LSFutureClient | None = None
    try:
        client = LSFutureClient(timeout=15)
        print(f"SDK 인스턴스 생성: {type(client).__name__}")
        quote = client.market.quote(code)
        quote_block = quote.get("t2111OutBlock")
        if not isinstance(quote_block, dict):
            raise RuntimeError("t2111 현재가 응답 블록이 없습니다.")
        price = str(quote_block.get("price", "")).strip()
        print(f"성공: client.market.quote({code})" + (f", 현재가 {price}" if price else ""))

        orderbook = client.market.orderbook(code)
        book_block = orderbook.get("t2112OutBlock")
        if not isinstance(book_block, dict):
            raise RuntimeError("t2112 호가 응답 블록이 없습니다.")
        bid = str(book_block.get("bidho1", "")).strip()
        ask = str(book_block.get("offerho1", "")).strip()
        print(f"성공: client.market.orderbook({code}), 매수1 {bid or '-'}, 매도1 {ask or '-'}")

        balance = client.account.balance()
        summary = balance.get("t0441OutBlock")
        positions = balance.get("t0441OutBlock1")
        if not isinstance(summary, dict) or "t0441OutBlock1" not in balance:
            raise RuntimeError("t0441 잔고 응답 구조가 올바르지 않습니다.")
        position_count = len(rows(positions))
        print(f"성공: client.account.balance(), 잔고 응답 행 {position_count}건 (계좌 상세값은 출력하지 않음)")
        print("실제 LS API SDK 조회 검증 성공: 현재가, 호가, 잔고 3/3")
        return 0
    except Exception as exc:
        detail = fail_detail(exc)
        print(f"실제 LS API SDK 조회 검증 실패: {detail}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
