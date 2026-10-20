"""Place one guarded simulated BUY order for a fresh A016C000 long position.

This script submits one real paper order and does not close a filled position.
"""
from __future__ import annotations

import os
import sys
import time
from typing import Any

from ls_openapi import LSAPIError, LSOpenAPI

ACK = "I_ACKNOWLEDGE_PAPER_SIMULATED_TRADING"
POLL_ATTEMPTS = 30
POLL_INTERVAL = 1.0


def rows(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        return [value]
    return value if isinstance(value, list) else []


def number(row: dict[str, Any], key: str) -> float:
    try:
        return float(str(row.get(key, "0")).strip() or 0)
    except (TypeError, ValueError):
        return 0.0


def safe_error(exc: Exception, client: LSOpenAPI) -> str:
    if isinstance(exc, LSAPIError):
        payload = exc.payload if isinstance(exc.payload, dict) else {}
        code = str(payload.get("rsp_cd", "")).strip()
        message = " ".join(str(payload.get("rsp_msg", "")).split())
        for secret in (client.app_key, client.app_secret, client._token):
            if secret:
                message = message.replace(secret, "[redacted]")
        return f"LS API {code}: {message[:180]}" if code or message else "LS API 오류"
    if isinstance(exc, RuntimeError):
        return " ".join(str(exc).split())[:180] or type(exc).__name__
    return type(exc).__name__


def order_rows(client: LSOpenAPI, short_code: str) -> list[dict[str, Any]]:
    result = client.call(
        "t0434",
        {"expcode": short_code, "chegb": "0", "sortgb": "1", "cts_ordno": " "},
    )
    return rows(result.get("t0434OutBlock1"))


def find_order(client: LSOpenAPI, short_code: str, order_no: int) -> dict[str, Any] | None:
    matches = []
    for row in order_rows(client, short_code):
        try:
            current_no = int(float(row.get("ordno", 0)))
            original_no = int(float(row.get("orgordno", 0)))
        except (TypeError, ValueError):
            continue
        if current_no == order_no or original_no == order_no:
            matches.append(row)
    if not matches:
        return None
    return max(matches, key=lambda item: number(item, "sysprocseq"))


def wait_order(client: LSOpenAPI, short_code: str, order_no: int) -> dict[str, Any] | None:
    for _ in range(POLL_ATTEMPTS):
        row = find_order(client, short_code, order_no)
        if row is not None:
            return row
        time.sleep(POLL_INTERVAL)
    return None


def order_number(response: dict[str, Any]) -> int:
    block = response.get("CFOAT00100OutBlock2")
    if isinstance(block, list):
        block = block[0] if block else {}
    if not isinstance(block, dict):
        raise RuntimeError("주문 응답에서 주문번호 블록을 찾지 못했습니다.")
    value = block.get("OrdNo")
    if value in (None, "", 0, "0"):
        raise RuntimeError("주문 응답에 주문번호가 없습니다. 주문 여부를 계좌에서 수동 확인하세요.")
    return int(float(value))


def position(client: LSOpenAPI, short_code: str) -> dict[str, Any] | None:
    result = client.call("t0441", {"cts_expcode": "", "cts_medocd": ""})
    matches = [
        row for row in rows(result.get("t0441OutBlock1"))
        if str(row.get("expcode", "")).strip() == short_code
    ]
    if len(matches) > 1:
        raise RuntimeError("잔고에서 대상 종목이 중복 반환되어 중단합니다.")
    return matches[0] if matches else None


def main() -> int:
    if os.getenv("LS_ORDER_CONFIRM", "") != ACK:
        print("중단: 명시적인 모의투자 주문 확인 문자열이 없습니다.")
        return 2
    short_code = os.getenv("LS_ORDER_TARGET_CODE", "A016C000").strip()
    if short_code != "A016C000":
        print("중단: 이 검증은 A016C000 전용으로 고정되어 있습니다.")
        return 2

    client: LSOpenAPI | None = None
    order_no: int | None = None
    try:
        client = LSOpenAPI(allow_orders=True)
        holding = position(client, short_code)
        if holding is not None and (number(holding, "jqty") > 0 or number(holding, "cqty") > 0):
            raise RuntimeError(
                f"{short_code} 보유 잔고가 이미 있어 신규 롱 주문을 막았습니다 "
                f"(보유 {number(holding, 'jqty'):g}, 청산가능 {number(holding, 'cqty'):g})."
            )
        existing = [row for row in order_rows(client, short_code) if number(row, "ordrem") > 0]
        if existing:
            raise RuntimeError(f"{short_code} 미체결 주문 {len(existing)}건이 있어 신규 주문을 막았습니다.")

        master = client.call("t8467", {"gubun": ""})
        candidates = [
            row for row in rows(master.get("t8467OutBlock"))
            if str(row.get("shcode", "")).strip() == short_code
        ]
        if len(candidates) != 1:
            raise RuntimeError("지수선물 마스터에서 A016C000을 하나의 주문코드로 확인하지 못했습니다.")
        product = candidates[0]
        api_code = str(product.get("expcode", "")).strip() or short_code
        if not (8 <= len(api_code) <= 12):
            raise RuntimeError("마스터에서 주문용 종목코드를 확인하지 못했습니다.")

        quote = client.call("t2112", {"shcode": short_code}).get("t2112OutBlock", {})
        if not isinstance(quote, dict):
            raise RuntimeError("현재 호가 응답 구조가 올바르지 않습니다.")
        ask = number(quote, "offerho1")
        bid = number(quote, "bidho1")
        ladder = sorted({
            number(quote, f"{side}ho{i}")
            for side in ("offer", "bid") for i in range(1, 6)
            if number(quote, f"{side}ho{i}") > 0
        })
        gaps = [right - left for left, right in zip(ladder, ladder[1:]) if right > left]
        if ask <= 0 or bid <= 0 or not gaps:
            raise RuntimeError("유효한 매수1/매도1 호가와 호가 단위를 확인하지 못했습니다.")
        tick = min(gaps)
        limit_price = round(ask + 5 * tick, 8)
        if limit_price <= ask:
            raise RuntimeError("매도1호가보다 5틱 높은 매수 지정가 계산에 실패했습니다.")

        print(
            f"주문 전 확인: {short_code} {str(product.get('hname', '')).strip() or '선물'}, "
            f"매수1 {bid:g}, 매도1 {ask:g}, 호가단위 {tick:g}"
        )
        print(f"신규 매수 지정가 준비: 매도1호가 + 5틱 = {limit_price:g}, 수량 1계약")

        response = client.call(
            "CFOAT00100",
            {
                "FnoIsuNo": api_code,
                "BnsTpCode": "2",
                "FnoOrdprcPtnCode": "00",
                "FnoOrdPrc": limit_price,
                "OrdQty": 1,
            },
        )
        order_no = order_number(response)
        print(f"매수 주문 접수: 주문번호 끝자리 {order_no % 10000:04d}, 수량 1계약")

        state = wait_order(client, short_code, order_no)
        if state is None:
            raise RuntimeError("주문 상태 조회가 되지 않습니다. 중복 주문하지 말고 잔고/미체결을 수동 확인하세요.")
        filled = number(state, "cheqty")
        remaining = number(state, "ordrem")
        if filled < 1 and remaining > 0:
            client.call(
                "CFOAT00300",
                {"FnoIsuNo": api_code, "OrgOrdNo": order_no, "CancQty": remaining},
            )
            state = wait_order(client, short_code, order_no)
            if state is None or number(state, "ordrem") > 0:
                raise RuntimeError("미체결 잔량 취소 여부를 확인하지 못했습니다. 계좌를 수동 확인하세요.")
            raise RuntimeError("제한 시간 내 체결되지 않아 잔량을 취소했습니다.")
        if filled < 1:
            raise RuntimeError(f"체결수량이 1계약 미만입니다 (체결 {filled:g}, 미체결 {remaining:g}).")

        print(f"체결 확인: {filled:g}계약, 체결가 {number(state, 'cheprice'):g}")
        after = position(client, short_code)
        if after is None or number(after, "jqty") < 1:
            raise RuntimeError("주문 체결은 확인했지만 매수 잔고 1계약을 확인하지 못했습니다. 계좌를 확인하세요.")
        side = str(after.get("medosu", "")).strip()
        if side not in {"매수", "1", "B"}:
            raise RuntimeError(f"체결 후 잔고 방향이 매수로 확인되지 않았습니다 ({side or '미확인'}).")
        print(f"롱 잔고 확인: {short_code}, 매수 {number(after, 'jqty'):g}계약")
        print("검증 완료: 신규 매수 → 체결 확인. 새 포지션은 자동 청산하지 않았습니다.")
        return 0
    except Exception as exc:
        detail = safe_error(exc, client) if client is not None else type(exc).__name__
        print(f"검증 중단: {detail}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
