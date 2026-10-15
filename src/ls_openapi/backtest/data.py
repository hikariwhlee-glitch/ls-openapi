"""CSV input helpers for local futures/options price series."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

from .models import Bar


def validate_bars(bars: Iterable[Bar]) -> None:
    previous: datetime | None = None
    for bar in bars:
        if previous is not None and bar.timestamp <= previous:
            raise ValueError("bars must be strictly increasing by timestamp")
        previous = bar.timestamp


def load_bars_csv(path: str | Path, symbol: str) -> List[Bar]:
    """Load timestamp,open,high,low,close[,volume] rows in chronological order."""
    bars: List[Bar] = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"timestamp", "open", "high", "low", "close"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("CSV must contain columns: timestamp, open, high, low, close")
        for line, row in enumerate(reader, start=2):
            try:
                timestamp = datetime.fromisoformat(row["timestamp"])
                bars.append(Bar(timestamp, symbol, float(row["open"]), float(row["high"]),
                                float(row["low"]), float(row["close"]), float(row.get("volume") or 0)))
            except (TypeError, ValueError) as exc:
                raise ValueError(f"invalid CSV row {line}: {exc}") from exc
    validate_bars(bars)
    return bars
