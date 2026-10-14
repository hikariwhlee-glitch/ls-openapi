"""선물/옵션 취소주문 TR CFOAT00300."""

from __future__ import annotations

from typing import Optional

from ...client import LSClient, TRResponse

PATH = "/futureoption/order"
TR_CD = "CFOAT00300"


def cancel_futures_option_order(
    client: LSClient,
    instrument_code: str,
    original_order_number: int,
    quantity: int,
    *,
    mac_address: Optional[str] = None,
) -> TRResponse:
    """선물/옵션 기존 주문을 취소합니다.

    요청값 검증 후 전달된 값 그대로 CFOAT00300에 보냅니다. 호출하면 연결된
    계좌의 주문이 취소될 수 있으며, 자동 재시도하지 않습니다.
    """
    if not isinstance(instrument_code, str) or not instrument_code.strip():
        raise ValueError("종목코드는 비어 있을 수 없는 문자열이어야 합니다.")
    if (
        isinstance(original_order_number, bool)
        or not isinstance(original_order_number, int)
        or original_order_number <= 0
    ):
        raise ValueError("원주문번호는 양의 정수여야 합니다.")
    if (
        isinstance(quantity, bool)
        or not isinstance(quantity, int)
        or quantity <= 0
    ):
        raise ValueError("취소수량은 양의 정수여야 합니다.")

    body = {
        "CFOAT00300InBlock1": {
            "FnoIsuNo": instrument_code.strip(),
            "OrgOrdNo": original_order_number,
            "CancQty": quantity,
        }
    }
    return client.post_tr(PATH, TR_CD, body, mac_address=mac_address)
