"""선물/옵션 정정주문 TR CFOAT00200."""

from __future__ import annotations

import math
from typing import Optional

from ...client import LSClient, TRResponse

PATH = "/futureoption/order"
TR_CD = "CFOAT00200"


def modify_futures_option_order(
    client: LSClient,
    instrument_code: str,
    original_order_number: int,
    price_type_code: str,
    order_price: float,
    quantity: int,
    *,
    mac_address: Optional[str] = None,
) -> TRResponse:
    """선물/옵션 기존 주문을 정정합니다.

    요청값 검증 후 전달된 값 그대로 CFOAT00200에 보냅니다. 호출하면 연결된
    계좌의 주문이 변경될 수 있으며, 자동 재시도하지 않습니다.
    """
    if not isinstance(instrument_code, str) or not instrument_code.strip():
        raise ValueError("종목코드는 비어 있을 수 없는 문자열이어야 합니다.")
    if (
        isinstance(original_order_number, bool)
        or not isinstance(original_order_number, int)
        or original_order_number <= 0
    ):
        raise ValueError("원주문번호는 양의 정수여야 합니다.")
    if not isinstance(price_type_code, str) or not price_type_code.strip():
        raise ValueError("호가유형코드는 비어 있을 수 없는 문자열이어야 합니다.")
    if (
        isinstance(quantity, bool)
        or not isinstance(quantity, int)
        or quantity <= 0
    ):
        raise ValueError("정정수량은 양의 정수여야 합니다.")
    if (
        isinstance(order_price, bool)
        or not isinstance(order_price, (int, float))
        or not math.isfinite(float(order_price))
        or order_price < 0
    ):
        raise ValueError("정정가격은 0 이상의 유한한 숫자여야 합니다.")

    body = {
        "CFOAT00200InBlock1": {
            "FnoIsuNo": instrument_code.strip(),
            "OrgOrdNo": original_order_number,
            "FnoOrdprcPtnCode": price_type_code.strip(),
            "FnoOrdPrc": order_price,
            "MdfyQty": quantity,
        }
    }
    return client.post_tr(PATH, TR_CD, body, mac_address=mac_address)
