"""Input and output models for OHLC backtests."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

Side = Literal["buy", "sell"]


@dataclass(frozen=True)
class Bar:
    timestamp: datetime
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0

    def __post_init__(self) -> None:
        if self.low > self.high:
            raise ValueError("low must be <= high")
        if self.low > min(self.open, self.close) or self.high < max(self.open, self.close):
            raise ValueError("OHLC prices must satisfy low <= open/close <= high")
        if self.volume < 0:
            raise ValueError("volume cannot be negative")


@dataclass(frozen=True)
class ContractSpec:
    symbol: str
    multiplier: float
    tick_size: float
    margin_per_contract: float = 0.0
    fee_per_contract_per_side: float = 0.0

    def __post_init__(self) -> None:
        if not self.symbol:
            raise ValueError("symbol is required")
        if self.multiplier <= 0 or self.tick_size <= 0:
            raise ValueError("multiplier and tick_size must be positive")
        if self.margin_per_contract < 0 or self.fee_per_contract_per_side < 0:
            raise ValueError("margin and fee cannot be negative")


@dataclass(frozen=True)
class Trade:
    timestamp: datetime
    symbol: str
    side: Side
    quantity: int
    price: float
    fee: float
    realized_pnl: float
