"""선물/옵션 정상주문 TR CFOAT00100."""

from __future__ import annotations

import math
from typing import Optional

from ...client import LSClient, TRResponse

PATH = "/futureoption/order"
TR_CD = "CFOAT00100"


def submit_futures_option_order(
    client: LSClient,
    instrument_code: str,
    side_code: str,
    price_type_code: str,
    order_price: float,
    quantity: int,
    *,
    mac_address: Optional[str] = None,
) -> TRResponse:
    """선물/옵션 정상 주문(CFOAT00100)을 제출합니다.

    인수는 주문 요청에 그대로 반영합니다. 시세 확인, 틱 보정, 가격 선택은 하지
    않습니다. 호출하면 실제 연결된 계좌로 주문이 제출되며 자동 재시도하지 않습니다.
    응답 본문은 TRResponse.body에 서버 원문 그대로 담깁니다.
    """
    values = (
        ("종목코드", instrument_code),
        ("매매구분코드", side_code),
        ("호가유형코드", price_type_code),
    )
    for label, value in values:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("{}는 비어 있을 수 없는 문자열이어야 합니다.".format(label))

    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("주문수량은 양의 정수여야 합니다.")

    if (
        isinstance(order_price, bool)
        or not isinstance(order_price, (int, float))
        or not math.isfinite(float(order_price))
        or order_price < 0
    ):
        raise ValueError("주문가격은 0 이상의 유한한 숫자여야 합니다.")

    body = {
        "CFOAT00100InBlock1": {
            "FnoIsuNo": instrument_code.strip(),
            "BnsTpCode": side_code.strip(),
            "FnoOrdprcPtnCode": price_type_code.strip(),
            "FnoOrdPrc": order_price,
            "OrdQty": quantity,
        }
    }
    return client.post_tr(PATH, TR_CD, body, mac_address=mac_address)
