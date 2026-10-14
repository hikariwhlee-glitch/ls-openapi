"""모의투자에서 네 KOSPI 200 선물 월물을 조회하고 각 1계약 매수 주문을 냅니다.

main의 live-test 워크플로를 codex/document-live-t2111-verified ref로 수동 실행한 경우에만
주문을 전송합니다. LS_LIVE_TEST=1도 함께 필요하며, 일반 pytest나 다른 ref에서는 건너뜁니다.
종목마다 t2111의 price를 다시 조회하고 KRX 호가 단위 0.05포인트를 더해
지정가(BnsTpCode=2, FnoOrdprcPtnCode=00) 매수 1계약을 한 번 전송합니다.
요청 재시도는 없으며, 주문이 체결되거나 미체결 상태로 남을 수 있습니다.
"""
import os
import time
from decimal import Decimal, InvalidOperation

import pytest

from ls_openapi import (
    APIError,
    LSClient,
    Settings,
    TokenManager,
    fetch_current_price,
    submit_futures_option_order,
)

pytestmark = pytest.mark.skipif(
    os.environ.get("LS_LIVE_TEST") != "1"
    or os.environ.get("GITHUB_REF")
    != "refs/heads/codex/document-live-t2111-verified",
    reason="이 실서버 주문은 Codex 브랜치의 수동 Actions 실행에서만 가능합니다",
)

_CONTRACTS = ("A016C000", "A0173000", "A0176000", "A0179000")
_TICK_SIZE = Decimal("0.05")
_PAUSE_BETWEEN_CALLS = 1.1


def _quote_price(client, instrument_code):
    response = fetch_current_price(client, instrument_code)
    body = response.body if isinstance(response.body, dict) else {}
    quote = body.get("t2111OutBlock")
    if (
        body.get("rsp_cd") != "00000"
        or not isinstance(quote, dict)
        or quote.get("focode") != instrument_code
    ):
        raise AssertionError(
            "유효한 현재가 응답이 아닙니다: {} (rsp_cd={!r})".format(
                instrument_code, body.get("rsp_cd")
            )
        )
    try:
        price = Decimal(str(quote["price"]))
    except (KeyError, InvalidOperation, TypeError, ValueError) as exc:
        raise AssertionError(
            "현재가 price를 읽을 수 없습니다: {}".format(instrument_code)
        ) from exc
    if not price.is_finite() or price <= 0:
        raise AssertionError(
            "주문 기준 현재가가 유효하지 않습니다: {}={!r}".format(
                instrument_code, quote.get("price")
            )
        )
    order_price = price + _TICK_SIZE
    if order_price % _TICK_SIZE != 0:
        raise AssertionError(
            "현재가가 호가 단위에 맞지 않습니다: {}={!s}".format(
                instrument_code, price
            )
        )
    return price, order_price


def test_buy_one_contract_for_each_current_month():
    """현재가 + 1틱으로 네 월물에 지정가 매수 주문을 순차 제출합니다."""
    settings = Settings.from_env()
    manager = TokenManager(settings)
    client = LSClient(settings, token_manager=manager)
    accepted = []

    try:
        for index, instrument_code in enumerate(_CONTRACTS):
            if index:
                time.sleep(_PAUSE_BETWEEN_CALLS)

            current_price, order_price = _quote_price(client, instrument_code)
            time.sleep(_PAUSE_BETWEEN_CALLS)

            print(
                "\n[주문 준비] {} 현재가={} / 지정가={} (+{}) / 수량=1".format(
                    instrument_code, current_price, order_price, _TICK_SIZE
                )
            )
            try:
                response = submit_futures_option_order(
                    client,
                    instrument_code=instrument_code,
                    side_code="2",
                    price_type_code="00",
                    order_price=float(order_price),
                    quantity=1,
                )
            except APIError as exc:
                print("[주문 실패] {}: {}".format(instrument_code, exc))
                raise

            body = response.body if isinstance(response.body, dict) else {}
            code = body.get("rsp_cd")
            message = body.get("rsp_msg")
            print("[주문 결과] {} rsp_cd={!r}".format(instrument_code, code))
            if message is not None:
                print("[주문 결과] rsp_msg={}".format(str(message)[:120]))
            for block_name, block in sorted(body.items()):
                if isinstance(block, dict):
                    print(
                        "[주문 결과] {} 필드명={}".format(
                            block_name, sorted(block)
                        )
                    )

            if response.tr_cd != "CFOAT00100" or code != "00000":
                raise AssertionError(
                    "주문 성공 응답을 확인하지 못해 이후 주문을 중단했습니다 "
                    "(종목={}, rsp_cd={!r}, 앞서 접수된 주문={})".format(
                        instrument_code, code, accepted
                    )
                )
            accepted.append((instrument_code, str(order_price)))

        print("\n[요약] 접수 성공: {}".format(accepted))
    finally:
        try:
            result = manager.revoke()
            print(
                "[토큰 폐기] code/message: {} / {}".format(
                    (result or {}).get("code"), (result or {}).get("message")
                )
            )
        except Exception as exc:
            print("[토큰 폐기 실패] {}".format(type(exc).__name__))

    assert len(accepted) == len(_CONTRACTS), (
        "네 월물 모두 주문 접수 성공 응답이 필요합니다: {}".format(accepted)
    )
