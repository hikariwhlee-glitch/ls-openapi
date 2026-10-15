"""Deterministic next-bar-open OHLC backtest engine."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Sequence, Tuple

from .models import Bar, ContractSpec, Trade

Signal = Callable[[int, Sequence[Bar]], int]


@dataclass(frozen=True)
class BacktestResult:
    initial_cash: float
    final_cash: float
    final_equity: float
    total_return: float
    max_drawdown: float
    trades: Tuple[Trade, ...]
    equity_curve: Tuple[Tuple[object, float], ...]


def run_backtest(
    bars: Sequence[Bar], contract: ContractSpec, signal: Signal, *,
    initial_cash: float = 10_000_000, slippage_ticks: float = 0,
) -> BacktestResult:
    """Run a single-symbol target-position backtest using next-bar-open fills."""
    if initial_cash <= 0:
        raise ValueError("initial_cash must be positive")
    if slippage_ticks < 0:
        raise ValueError("slippage_ticks cannot be negative")
    if any(bar.symbol != contract.symbol for bar in bars):
        raise ValueError("all bars must match the contract symbol")
    for previous, current in zip(bars, bars[1:]):
        if current.timestamp <= previous.timestamp:
            raise ValueError("bars must be strictly increasing by timestamp")
    if not bars:
        return BacktestResult(initial_cash, initial_cash, initial_cash, 0.0, 0.0, (), ())

    cash, quantity, average_price = initial_cash, 0, 0.0
    trades = []
    curve = []
    peak, max_drawdown = initial_cash, 0.0

    for index, bar in enumerate(bars):
        if index:
            target = int(signal(index - 1, bars[:index]))
            delta = target - quantity
            if delta:
                raw = bar.open + slippage_ticks * contract.tick_size * (1 if delta > 0 else -1)
                price = (math.ceil(raw / contract.tick_size - 1e-12) if delta > 0
                         else math.floor(raw / contract.tick_size + 1e-12)) * contract.tick_size
                old_quantity = quantity
                closing = min(abs(delta), abs(old_quantity)) if old_quantity and delta * old_quantity < 0 else 0
                realized = (price - average_price) * (1 if old_quantity > 0 else -1) * closing * contract.multiplier
                cash += realized
                opening = abs(delta) - closing
                if opening and abs(target) * contract.margin_per_contract > cash:
                    raise ValueError("insufficient cash for margin at {}".format(bar.timestamp.isoformat()))
                if opening:
                    if old_quantity == 0 or old_quantity * target < 0:
                        average_price = price
                    elif old_quantity * delta > 0:
                        average_price = (abs(old_quantity) * average_price + abs(delta) * price) / abs(target)
                if target == 0:
                    average_price = 0.0
                fee = abs(delta) * contract.fee_per_contract_per_side
                cash -= fee
                trades.append(Trade(bar.timestamp, contract.symbol, "buy" if delta > 0 else "sell",
                                    abs(delta), price, fee, realized))
                quantity = target

        equity = cash + quantity * (bar.close - average_price) * contract.multiplier
        peak = max(peak, equity)
        max_drawdown = max(max_drawdown, (peak - equity) / peak if peak else 0.0)
        curve.append((bar.timestamp, equity))

    final_equity = curve[-1][1]
    return BacktestResult(initial_cash, cash, final_equity, final_equity / initial_cash - 1,
                          max_drawdown, tuple(trades), tuple(curve))
