"""Small deterministic next-bar-open backtest engine."""

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
    """Simulate target-position signals at the next bar open.

    P&L is mark-to-market on the provided price series. This works for futures prices
    and option premium series when the caller supplies the right multiplier. Signals
    formed after a bar close execute at the next bar open. Margin is a fixed per-contract
    cash check, not an exchange margin model. Expiry/assignment is intentionally omitted.
    """
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
    peak = initial_cash
    max_drawdown = 0.0

    for index, bar in enumerate(bars):
        if index > 0:
            target = int(signal(index - 1, bars[:index]))
            delta = target - quantity
            if delta:
                raw_price = bar.open + (slippage_ticks * contract.tick_size * (1 if delta > 0 else -1))
                # Round in the adverse direction so fills always respect the configured tick.
                price = (math.ceil(raw_price / contract.tick_size - 1e-12) if delta > 0
                         else math.floor(raw_price / contract.tick_size + 1e-12)) * contract.tick_size
                old_quantity = quantity
                closing = min(abs(delta), abs(old_quantity)) if old_quantity and delta * old_quantity < 0 else 0
                realized = (price - average_price) * (1 if old_quantity > 0 else -1) * closing * contract.multiplier
                cash += realized
                new_quantity = target
                opening = abs(delta) - closing
                if opening and abs(new_quantity) * contract.margin_per_contract > cash:
                    raise ValueError(f"insufficient cash for margin at {bar.timestamp.isoformat()}")
                if opening:
                    if old_quantity == 0 or old_quantity * new_quantity < 0:
                        average_price = price
                    elif old_quantity * delta > 0:
                        average_price = (abs(old_quantity) * average_price + abs(delta) * price) / abs(new_quantity)
                if new_quantity == 0:
                    average_price = 0.0
                fee = abs(delta) * contract.fee_per_contract_per_side
                cash -= fee
                trades.append(Trade(bar.timestamp, contract.symbol, "buy" if delta > 0 else "sell",
                                    abs(delta), price, fee, realized))
                quantity = new_quantity

        equity = cash + quantity * (bar.close - average_price) * contract.multiplier
        peak = max(peak, equity)
        max_drawdown = max(max_drawdown, (peak - equity) / peak if peak else 0.0)
        curve.append((bar.timestamp, equity))

    final_equity = curve[-1][1]
    return BacktestResult(initial_cash, cash, final_equity, final_equity / initial_cash - 1,
                          max_drawdown, tuple(trades), tuple(curve))
