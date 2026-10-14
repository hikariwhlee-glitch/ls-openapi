"""국내 선물/옵션 정상 주문 요청 (CFOAT00100).

이 함수는 호출 즉시 주문 요청을 제출합니다. 이 모듈의 import나 LSClient 생성만으로는
주문이 전송되지 않습니다. 자동 재시도는 하지 않으며, 응답은 서버 원문 그대로 반환합니다.
"""

from __future__ import annotations

import math
from typing import Optional

from .client import LSClient, TRResponse

FUTUREOPTION_ORDER_PATH = "/futureoption/order"
TR_FUTUREOPTION_NORMAL_ORDER = "CFOAT00100"


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
    """선물/옵션 정상 주문을 제출합니다 (TR CFOAT00100).

    호출하면 실제 연결된 계좌에 주문 요청이 전송됩니다. 별도의 확인 대화상자나
    자동 재시도는 없습니다. 주문 전송 없이 요청 형식만 시험하려면 mock 세션을 사용하세요.

    side_code와 price_type_code는 포털에서 확인한 코드 문자열을 그대로 넘깁니다.
    공식 주문 필드 코드표는 확인되지 않았으므로 이 함수에서 코드 의미를 추측하거나
    매핑하지 않습니다. 응답은 해석하지 않고 TRResponse.body에 원본 그대로 담깁니다.
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
    return client.post_tr(
        FUTUREOPTION_ORDER_PATH,
        TR_FUTUREOPTION_NORMAL_ORDER,
        body,
        mac_address=mac_address,
    )
