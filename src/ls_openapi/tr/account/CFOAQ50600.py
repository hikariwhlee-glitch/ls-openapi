"""선물옵션 계좌잔고 및 평가현황3 TR CFOAQ50600.

근거: 사용자가 제공한 호출 샘플(경로 ``/futureoption/accno``, 헤더, ``CFOAQ50600InBlock1``).
공식 TR 명세 원문이 아니므로 필드 의미, 코드표(``BalEvalTp`` 등), 응답 필드, 초당 호출 제한은
**확인되지 않았습니다**. 응답은 해석하지 않고 서버 JSON을 그대로 돌려줍니다.
응답에는 계좌·잔고 등 민감한 값이 들어 있을 수 있으니 로그나 공개 장소에 출력하지 마세요.
"""

from __future__ import annotations

from typing import Optional

from ...client import LSClient, TRResponse

PATH = "/futureoption/accno"
TR_CD = "CFOAQ50600"
IN_BLOCK = "CFOAQ50600InBlock1"


def _text(label: str, value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("{}는 비어 있을 수 없는 문자열이어야 합니다.".format(label))
    return value.strip()


def fetch_account_balance(
    client: LSClient,
    order_date: str,
    *,
    balance_eval_type: str = "1",
    futures_price_eval_type: str = "1",
    liquidation_qty_query_type: str = "1",
    mac_address: Optional[str] = None,
) -> TRResponse:
    """선물옵션 계좌잔고 및 평가현황(CFOAQ50600)을 조회합니다.

    ``order_date`` 는 ``YYYYMMDD`` 형식입니다(샘플의 ``OrdDt``). 나머지 구분값은 샘플 기본값
    ``"1"`` 이며 코드표는 확인되지 않아 그대로 전달합니다. ``RecCnt`` 는 샘플대로 1입니다.
    계좌는 인증에 쓴 앱키에 연결된 계좌이며 요청 본문에 계좌번호를 넣지 않습니다(샘플 기준).
    응답 본문은 ``TRResponse.body`` 에 원본 그대로 담깁니다.
    """
    date = _text("주문일자(order_date)", order_date)
    if len(date) != 8 or not date.isdigit():
        raise ValueError("주문일자(order_date)는 YYYYMMDD 8자리 숫자여야 합니다.")
    body = {
        IN_BLOCK: {
            "RecCnt": 1,
            "OrdDt": date,
            "BalEvalTp": _text("잔고평가구분", balance_eval_type),
            "FutsPrcEvalTp": _text("선물가격평가구분", futures_price_eval_type),
            "LqtQtyQryTp": _text("청산수량조회구분", liquidation_qty_query_type),
        }
    }
    return client.post_tr(PATH, TR_CD, body, mac_address=mac_address)
