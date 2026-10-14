"""선물/옵션 현재가 호가 조회 TR t2112."""

from __future__ import annotations

from typing import Optional

from ...client import LSClient, TRResponse, build_in_block

PATH = "/futureoption/market-data"
TR_CD = "t2112"


def fetch_orderbook(
    client: LSClient,
    shcode: str,
    *,
    mac_address: Optional[str] = None,
) -> TRResponse:
    """선물/옵션 호가(t2112)를 조회하고 원본 응답을 반환합니다."""
    if not isinstance(shcode, str) or len(shcode.strip()) != 8:
        raise ValueError("shcode(선물/옵션 종목코드)는 8자리여야 합니다.")
    body = build_in_block(TR_CD, {"shcode": shcode.strip()})
    return client.post_tr(PATH, TR_CD, body, mac_address=mac_address)
