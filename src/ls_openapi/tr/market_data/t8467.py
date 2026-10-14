"""지수선물 마스터 조회 TR t8467."""

from __future__ import annotations

from typing import Optional

from ...client import LSClient, TRResponse, build_in_block

PATH = "/futureoption/market-data"
TR_CD = "t8467"


def fetch_index_futures_master(
    client: LSClient,
    gubun: str = "",
    *,
    mac_address: Optional[str] = None,
) -> TRResponse:
    """지수선물 종목 마스터(t8467)를 조회하고 원본 응답을 반환합니다.

    gubun: V(변동성), S(섹터), Q(코스닥150). 그 밖의 값은 코스피200 선물입니다.
    """
    if not isinstance(gubun, str) or len(gubun) > 1:
        raise ValueError("gubun은 빈 값 또는 한 글자여야 합니다.")
    body = build_in_block(TR_CD, {"gubun": gubun})
    return client.post_tr(PATH, TR_CD, body, mac_address=mac_address)
