"""Run the small CSV futures/options-premium backtest example."""

from __future__ import annotations

import argparse

from ls_openapi.backtest import ContractSpec, run_backtest
from ls_openapi.backtest.data import load_bars_csv


def moving_average_signal(index, history):
    closes = [bar.close for bar in history]
    if len(closes) < 6:
        return 0
    short_average = sum(closes[-3:]) / 3
    long_average = sum(closes[-6:]) / 6
    return 1 if short_average > long_average else 0


def main() -> None:
    parser = argparse.ArgumentParser(description="CSV domestic derivatives backtest example")
    parser.add_argument("csv", help="CSV with timestamp,open,high,low,close[,volume]")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--multiplier", type=float, required=True, help="contract point value")
    parser.add_argument("--tick-size", type=float, required=True)
    parser.add_argument("--margin", type=float, required=True, help="fixed cash check per contract")
    parser.add_argument("--fee", type=float, default=0, help="fee per contract per side")
    args = parser.parse_args()
    bars = load_bars_csv(args.csv, args.symbol)
    spec = ContractSpec(args.symbol, args.multiplier, args.tick_size, args.margin, args.fee)
    result = run_backtest(bars, spec, moving_average_signal)
    print(f"bars={len(bars)} trades={len(result.trades)}")
    print(f"final_equity={result.final_equity:,.0f}")
    print(f"total_return={result.total_return:.2%} max_drawdown={result.max_drawdown:.2%}")


if __name__ == "__main__":
    main()
