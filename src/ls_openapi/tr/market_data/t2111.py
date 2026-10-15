"""선물/옵션 현재가 조회 TR t2111."""

from __future__ import annotations

from typing import Optional

from ...client import LSClient, TRResponse, build_in_block

PATH = "/futureoption/market-data"
TR_CD = "t2111"


def fetch_current_price(
    client: LSClient,
    focode: str,
    *,
    mac_address: Optional[str] = None,
) -> TRResponse:
    """선물/옵션 현재가(t2111)를 조회하고 원본 응답을 반환합니다.

    공식 InBlock의 focode 길이는 8자입니다. 길이가 다른 값은 거부합니다.
    """
    if not isinstance(focode, str) or len(focode.strip()) != 8:
        raise ValueError("focode(선물/옵션 종목코드)는 8자리여야 합니다.")
    body = build_in_block(TR_CD, {"focode": focode.strip()})
    return client.post_tr(PATH, TR_CD, body, mac_address=mac_address)
