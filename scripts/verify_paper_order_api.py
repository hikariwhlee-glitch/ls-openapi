"""Run a guarded one-contract LS domestic futures paper order lifecycle check.

This script intentionally performs real order API calls. Run only with a
simulated-trading app key and after reviewing the workflow inputs.
"""
from __future__ import annotations

import os
import sys
import time
from typing import Any

from ls_openapi import LSAPIError, LSOpenAPI


ACK = "I_ACKNOWLEDGE_PAPER_SIMULATED_TRADING"
POLL_ATTEMPTS = 12
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


def wait_order(
    client: LSOpenAPI, short_code: str, order_no: int
) -> dict[str, Any] | None:
    for _ in range(POLL_ATTEMPTS):
        row = find_order(client, short_code, order_no)
        if row is not None:
            return row
        time.sleep(POLL_INTERVAL)
    return None


def order_number(response: dict[str, Any], tr_code: str) -> int:
    block = response.get(f"{tr_code}OutBlock2")
    if isinstance(block, list):
        block = block[0] if block else {}
    if not isinstance(block, dict):
        raise RuntimeError(f"{tr_code} 응답에서 주문번호 블록을 찾지 못했습니다.")
    value = block.get("OrdNo")
    if value in (None, "", 0, "0"):
        raise RuntimeError(f"{tr_code} 응답에 주문번호가 없습니다. 주문 상태를 수동 확인하세요.")
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


def require_open_unfilled(row: dict[str, Any] | None, label: str) -> None:
    if row is None:
        raise RuntimeError(f"{label}: 주문 상태를 확인하지 못했습니다. 중복 주문하지 말고 수동 확인하세요.")
    if number(row, "cheqty") != 0 or number(row, "ordrem") != 1:
        raise RuntimeError(
            f"{label}: 예상한 미체결 1계약 상태가 아닙니다 "
            f"(체결={number(row, 'cheqty'):g}, 미체결={number(row, 'ordrem'):g})."
        )


def cancel_one(client: LSOpenAPI, short_code: str, api_code: str, order_no: int) -> None:
    client.call(
        "CFOAT00300",
        {"FnoIsuNo": api_code, "OrgOrdNo": order_no, "CancQty": 1},
    )
    row = wait_order(client, short_code, order_no)
    if row is None or number(row, "cheqty") != 0 or number(row, "ordrem") != 0:
        raise RuntimeError(
            f"주문 {order_no} 취소 후 미체결 0을 확인하지 못했습니다. 추가 주문 없이 수동 확인하세요."
        )
    print(f"취소 확인: 주문번호 끝자리 {order_no % 10000:04d}, 미체결 0")


def main() -> int:
    if os.getenv("LS_ORDER_CONFIRM", "") != ACK:
        print("중단: 명시적인 모의투자 주문 확인 문자열이 없습니다.")
        return 2
    short_code = os.getenv("LS_ORDER_TARGET_CODE", "A016C000").strip()
    if len(short_code) != 8 or not short_code.isalnum():
        print("중단: LS_ORDER_TARGET_CODE는 선물 단축코드 8자리여야 합니다.")
        return 2

    client: LSOpenAPI | None = None
    try:
        client = LSOpenAPI(allow_orders=True)
        holding = position(client, short_code)
        if holding is None:
            raise RuntimeError(f"대상 종목 {short_code}의 보유 잔고가 없습니다.")
        side = str(holding.get("medosu", "")).strip()
        if side not in {"매수", "1", "B"}:
            raise RuntimeError(f"대상 종목의 보유 방향이 매수로 확인되지 않아 중단합니다 ({side or '미확인'}).")
        if number(holding, "jqty") < 1 or number(holding, "cqty") < 1:
            raise RuntimeError("대상 종목의 청산 가능 수량이 1계약 미만입니다.")
        print(
            f"잔고 확인: {short_code}, 매수 보유 {number(holding, 'jqty'):g}계약, "
            f"청산 가능 {number(holding, 'cqty'):g}계약; 검증 주문은 1계약"
        )

        master = client.call("t8467", {"gubun": ""})
        candidates = [
            row for row in rows(master.get("t8467OutBlock"))
            if str(row.get("shcode", "")).strip() == short_code
        ]
        if len(candidates) != 1:
            raise RuntimeError("지수선물 마스터에서 대상 코드를 하나로 매핑하지 못했습니다.")
        product = candidates[0]
        api_code = str(product.get("expcode", "")).strip() or short_code
        if not api_code or not (8 <= len(api_code) <= 12):
            raise RuntimeError("종목 주문코드를 확인하지 못했습니다.")

        quote = client.call("t2112", {"shcode": short_code}).get("t2112OutBlock", {})
        if not isinstance(quote, dict):
            raise RuntimeError("현재 호가 응답 구조가 올바르지 않습니다.")
        offer = number(quote, "offerho1")
        bid = number(quote, "bidho1")
        offer_prices = [number(quote, f"offerho{i}") for i in range(1, 6)]
        bid_prices = [number(quote, f"bidho{i}") for i in range(1, 6)]
        ladder = sorted({price for price in offer_prices + bid_prices if price > 0})
        gaps = [right - left for left, right in zip(ladder, ladder[1:]) if right > left]
        if offer <= 0 or bid <= 0 or not gaps:
            raise RuntimeError("현재 호가와 최소 호가 단위를 확인하지 못했습니다.")
        tick = min(gaps)
        high_limit = round(offer + tick * 10, 8)
        if high_limit <= offer or high_limit <= bid:
            raise RuntimeError("미체결을 기대할 높은 지정가를 계산하지 못했습니다.")
        print(
            f"종목 확인: {str(product.get('hname', '')).strip() or short_code}, "
            f"매도1 {offer:g}, 호가단위 {tick:g}, 검증 지정가 {high_limit:g}"
        )

        existing = [row for row in order_rows(client, short_code) if number(row, "ordrem") > 0]
        if existing:
            raise RuntimeError(f"대상 종목에 기존 미체결 주문 {len(existing)}건이 있어 중단합니다.")

        first = client.call(
            "CFOAT00100",
            {"FnoIsuNo": api_code, "BnsTpCode": "1", "FnoOrdprcPtnCode": "00",
             "FnoOrdPrc": high_limit, "OrdQty": 1},
        )
        first_no = order_number(first, "CFOAT00100")
        print(f"첫 매도 지정가 접수: 가격 {high_limit:g}, 수량 1, 주문번호 끝자리 {first_no % 10000:04d}")
        state = wait_order(client, short_code, first_no)
        if state is None or number(state, "cheqty") != 0:
            raise RuntimeError("첫 주문이 미체결로 확인되지 않았습니다. 두 번째 주문은 보내지 않았습니다.")
        require_open_unfilled(state, "첫 주문")
        cancel_one(client, short_code, api_code, first_no)

        holding = position(client, short_code)
        if holding is None or str(holding.get("medosu", "")).strip() not in {"매수", "1", "B"} or number(holding, "cqty") < 1:
            raise RuntimeError("첫 주문 취소 후 매수 보유분 1계약이 확인되지 않아 재주문을 중단합니다.")

        second = client.call(
            "CFOAT00100",
            {"FnoIsuNo": api_code, "BnsTpCode": "1", "FnoOrdprcPtnCode": "00",
             "FnoOrdPrc": high_limit, "OrdQty": 1},
        )
        second_no = order_number(second, "CFOAT00100")
        print(f"재주문 접수: 가격 {high_limit:g}, 수량 1, 주문번호 끝자리 {second_no % 10000:04d}")
        state = wait_order(client, short_code, second_no)
        require_open_unfilled(state, "재주문")

        amend_quote = client.call("t2112", {"shcode": short_code}).get("t2112OutBlock", {})
        if not isinstance(amend_quote, dict):
            raise RuntimeError("정정 직전 현재 호가 응답 구조가 올바르지 않습니다.")
        amend_bid = number(amend_quote, "bidho1")
        amend_price = round(amend_bid - tick * 5, 8)
        if amend_bid <= 0 or amend_price <= 0:
            raise RuntimeError("정정 직전 매수1호가 또는 5틱 아래 가격을 확인하지 못해 주문 정정을 중단합니다.")
        amended = client.call(
            "CFOAT00200",
            {"FnoIsuNo": api_code, "OrgOrdNo": second_no, "FnoOrdprcPtnCode": "00",
             "FnoOrdPrc": amend_price, "MdfyQty": 1},
        )
        amended_no = order_number(amended, "CFOAT00200")
        print(
            f"현재 매수1호가 {amend_bid:g}보다 5틱 낮은 {amend_price:g}로 지정가 정정 접수: "
            f"원주문 끝자리 {second_no % 10000:04d}, 정정주문 끝자리 {amended_no % 10000:04d}"
        )

        final_state = None
        for _ in range(POLL_ATTEMPTS):
            final_state = find_order(client, short_code, amended_no)
            if final_state and number(final_state, "cheqty") >= 1:
                break
            time.sleep(POLL_INTERVAL)

        if final_state is None:
            raise RuntimeError("현재 매수1호가 정정 후 주문 상태 확인이 안 됩니다. 수동으로 미체결을 확인하세요.")
        if number(final_state, "cheqty") < 1:
            if number(final_state, "ordrem") > 0:
                cancel_one(client, short_code, api_code, amended_no)
            raise RuntimeError("현재 매수1호가 정정 후 체결을 확인하지 못했습니다. 잔여 주문은 취소했습니다.")

        print(f"체결 확인: 체결수량 {number(final_state, 'cheqty'):g}, 체결가격 {number(final_state, 'cheprice'):g}")
        updated = position(client, short_code)
        remaining_position = number(updated, "jqty") if updated else 0
        if remaining_position > number(holding, "jqty") - 1:
            raise RuntimeError("주문 체결은 확인했으나 잔고 감소가 확인되지 않았습니다. 계좌를 다시 확인하세요.")
        print(f"잔고 확인: {short_code} 보유 수량 {remaining_position:g}계약")
        print("모의투자 주문 흐름 검증 완료: 신규 → 취소 → 재주문 → 현재 매수1호가 정정 → 체결")
        return 0
    except Exception as exc:
        detail = safe_error(exc, client) if client is not None else type(exc).__name__
        print(f"검증 중단: {detail}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
