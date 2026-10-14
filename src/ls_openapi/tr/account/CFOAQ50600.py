"""선물옵션 계좌잔고 및 평가현황3 TR CFOAQ50600."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from ...client import LSClient, TRResponse

PATH = "/futureoption/accno"
TR_CD = "CFOAQ50600"


def fetch_futures_option_balance(
    client: LSClient,
    order_date: str,
    *,
    balance_eval_type: str = "1",
    futures_price_eval_type: str = "1",
    liquidation_quantity_query_type: str = "1",
    mac_address: Optional[str] = None,
) -> TRResponse:
    """선물옵션 계좌잔고 및 평가현황3(CFOAQ50600)을 조회합니다.

    필드명과 기본 코드값은 사용자 제공 호출 샘플을 따릅니다. 코드값의 공식
    의미는 별도 확인이 필요합니다. 응답에는 계좌·잔고 정보가 포함될 수 있습니다.
    """
    if not isinstance(order_date, str):
        raise ValueError("주문일자는 YYYYMMDD 형식의 문자열이어야 합니다.")
    try:
        parsed_date = datetime.strptime(order_date, "%Y%m%d")
    except ValueError as exc:
        raise ValueError("주문일자는 유효한 YYYYMMDD 날짜여야 합니다.") from exc
    if parsed_date.strftime("%Y%m%d") != order_date:
        raise ValueError("주문일자는 YYYYMMDD 형식이어야 합니다.")

    codes = (
        ("잔고평가구분코드", balance_eval_type),
        ("선물가격평가구분코드", futures_price_eval_type),
        ("청산수량조회구분코드", liquidation_quantity_query_type),
    )
    for label, value in codes:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("{}는 비어 있을 수 없는 문자열이어야 합니다.".format(label))

    
body = {
    "CFOAQ50600InBlock1": {
        "OrdDt": order_date,
        "BalEvalTp": balance_eval_type.strip(),
        "FutsPrcEvalTp": futures_price_eval_type.strip(),
        "LqdtQtyQryTp": liquidation_quantity_query_type.strip(),
    }
}

return client.post_tr(
    PATH,
    TR_CD,
    body,
    mac_address=mac_address,
)

