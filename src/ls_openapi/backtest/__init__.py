"""Broker-neutral OHLC backtest primitives for futures and options premium series."""

from .engine import BacktestResult, run_backtest
from .models import Bar, ContractSpec, Trade

__all__ = ["BacktestResult", "Bar", "ContractSpec", "Trade", "run_backtest"]
