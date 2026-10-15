"""CSV OHLC input helpers."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional

from .models import Bar


def validate_bars(bars: Iterable[Bar]) -> None:
    previous: Optional[datetime] = None
    for bar in bars:
        if previous is not None and bar.timestamp <= previous:
            raise ValueError("bars must be strictly increasing by timestamp")
        previous = bar.timestamp


def load_bars_csv(path: str, symbol: str) -> List[Bar]:
    """Load timestamp,open,high,low,close[,volume] rows in chronological order."""
    bars: List[Bar] = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"timestamp", "open", "high", "low", "close"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("CSV must contain timestamp, open, high, low, close")
        for line, row in enumerate(reader, start=2):
            try:
                timestamp = datetime.fromisoformat(row["timestamp"])
                bars.append(Bar(timestamp, symbol, float(row["open"]), float(row["high"]),
                                float(row["low"]), float(row["close"]), float(row.get("volume") or 0)))
            except (TypeError, ValueError) as exc:
                raise ValueError("invalid CSV row {}: {}".format(line, exc)) from exc
    validate_bars(bars)
    return bars
