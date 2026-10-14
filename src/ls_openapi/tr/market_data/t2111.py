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
    """선물/옵션 현재가(t2111)를 조회하고 원본 응답을 반환합니다."""
    if not isinstance(focode, str) or not focode.strip():
        raise ValueError("focode(선물/옵션 종목코드)는 비어 있을 수 없습니다.")
    body = build_in_block(TR_CD, {"focode": focode.strip()})
    return client.post_tr(PATH, TR_CD, body, mac_address=mac_address)
