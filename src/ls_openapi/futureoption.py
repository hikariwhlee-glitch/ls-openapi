"""국내 선물/옵션 시세 조회.

현재 구현: ``t2111`` 선물/옵션현재가(시세)조회

근거: 사용자가 제공한 ``t2111`` 호출 샘플 (경로, 헤더, InBlock). 공식 TR 명세 원문이 아니라
샘플이므로 응답(OutBlock) 필드, 필수 여부, 초당 호출 제한은 **확인되지 않았습니다**.
그래서 응답은 해석하지 않고 서버가 준 JSON을 그대로 돌려줍니다.
``docs/api-inventory.md`` 에 확인 상태를 정리해 두었습니다.
"""

from __future__ import annotations

from typing import Optional

from .client import LSClient, TRResponse, build_in_block

FUTUREOPTION_MARKET_DATA_PATH = "/futureoption/market-data"
TR_CURRENT_PRICE = "t2111"


def fetch_current_price(
    client: LSClient,
    focode: str,
    *,
    mac_address: Optional[str] = None,
) -> TRResponse:
    """선물/옵션 현재가(``t2111``)를 조회합니다.

    ``focode`` 는 선물/옵션 종목코드입니다. 종목코드 형식과 현재 거래 중인 코드는
    이 저장소에서 확인되지 않았으므로 값을 검사하지 않고 그대로 보냅니다
    (비어 있는 값만 거부합니다). 응답 본문은 ``TRResponse.body`` 에 원본 그대로 담깁니다.
    """
    if not isinstance(focode, str) or not focode.strip():
        raise ValueError("focode(선물/옵션 종목코드)는 비어 있을 수 없습니다.")
    body = build_in_block(TR_CURRENT_PRICE, {"focode": focode.strip()})
    return client.post_tr(
        FUTUREOPTION_MARKET_DATA_PATH,
        TR_CURRENT_PRICE,
        body,
        mac_address=mac_address,
    )
