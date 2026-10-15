"""Daily futures/options chart TR t8466 mapped to backtest bars."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from ...backtest.models import Bar
from ...client import LSClient, TRResponse, build_in_block

PATH = "/futureoption/market-data"
TR_CD = "t8466"


def fetch_daily_bars(
    client: LSClient,
    shcode: str,
    *,
    end_date: str = "99999999",
    start_date: str = "",
    count: int = 500,
    compressed: bool = False,
    cts_date: str = "",
    tr_cont: str = "N",
    tr_cont_key: str = "",
    mac_address: Optional[str] = None,
) -> tuple[TRResponse, List[Bar]]:
    """Fetch one t8466 daily-chart page and convert it to chronological bars.

    The caller controls pagination using response.tr_cont, response.tr_cont_key,
    and the returned t8466OutBlock.cts_date. The API guide lists a 1 request/sec
    limit. No automatic request loop or sleep is performed.
    """
    if not isinstance(shcode, str) or len(shcode.strip()) != 8:
        raise ValueError("shcode must be an 8-character instrument code")
    shcode = shcode.strip()
    if not isinstance(end_date, str) or (end_date != "99999999" and not _is_yyyymmdd(end_date)):
        raise ValueError("end_date must be YYYYMMDD or 99999999")
    if start_date and not _is_yyyymmdd(start_date):
        raise ValueError("start_date must be empty or YYYYMMDD")
    if cts_date and not _is_yyyymmdd(cts_date):
        raise ValueError("cts_date must be empty or YYYYMMDD")
    max_count = 2000 if compressed else 500
    if isinstance(count, bool) or not isinstance(count, int) or not 1 <= count <= max_count:
        raise ValueError(f"count must be between 1 and {max_count}")
    if tr_cont not in ("Y", "N"):
        raise ValueError("tr_cont must be Y or N")

    fields = {
        "shcode": shcode,
        "gubun": "2",  # daily
        "qrycnt": count,
        "sdate": start_date,
        "edate": end_date,
        "cts_date": cts_date,
        "comp_yn": "Y" if compressed else "N",
    }
    response = client.post_tr(
        PATH, TR_CD, build_in_block(TR_CD, fields),
        tr_cont=tr_cont, tr_cont_key=tr_cont_key, mac_address=mac_address,
    )

    rows = response.body.get("t8466OutBlock1")
    if not isinstance(rows, list):
        raise ValueError("t8466 response is missing the t8466OutBlock1 array")
    bars = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("t8466OutBlock1 contains a non-object row")
        try:
            date = datetime.strptime(str(row["date"]), "%Y%m%d")
            bars.append(Bar(date, shcode, float(row["open"]), float(row["high"]),
                            float(row["low"]), float(row["close"]),
                            float(row.get("jdiff_vol") or 0)))
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"invalid t8466 daily bar: {exc}") from exc
    bars.sort(key=lambda bar: bar.timestamp)
    return response, bars


def _is_yyyymmdd(value: str) -> bool:
    if len(value) != 8 or not value.isdigit():
        return False
    try:
        datetime.strptime(value, "%Y%m%d")
    except ValueError:
        return False
    return True
