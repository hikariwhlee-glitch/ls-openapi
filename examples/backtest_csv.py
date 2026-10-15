"""Run a simple moving-average strategy over sample OHLC data."""

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
    parser = argparse.ArgumentParser()
    parser.add_argument("csv")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--multiplier", type=float, required=True)
    parser.add_argument("--tick-size", type=float, required=True)
    parser.add_argument("--margin", type=float, default=0)
    parser.add_argument("--fee", type=float, default=0)
    args = parser.parse_args()

    bars = load_bars_csv(args.csv, args.symbol)
    spec = ContractSpec(args.symbol, args.multiplier, args.tick_size, args.margin, args.fee)
    result = run_backtest(bars, spec, moving_average_signal)
    print("bars={} trades={}".format(len(bars), len(result.trades)))
    print("final_equity={:,.0f}".format(result.final_equity))
    print("total_return={:.2%} max_drawdown={:.2%}".format(result.total_return, result.max_drawdown))


if __name__ == "__main__":
    main()
