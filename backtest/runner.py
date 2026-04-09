"""Backtester integration stub.

TODO: Implement backtesting engine. Options:

1. Integrate with jmerle's backtester (recommended for quick start):
       pip install prosperity3bt
       prosperity3bt submission.py 0
   GitHub: jmerle/imc-prosperity-3-backtester
   (Check for prosperity-4 version when available)

2. Build a custom backtester using utils/data_loader.py:
   - Reconstruct TradingState from CSV data at each timestamp
   - Feed to strategy's run() method
   - Track positions, PnL, and order fills

Planned interface:
    run_backtest(strategy_path, round_num, days) -> BacktestResult
    compare_strategies(paths, round_num) -> comparison DataFrame

BacktestResult should contain:
    - pnl_series: Dict[str, List[float]]  (per-product PnL over time)
    - total_pnl: float
    - trades_executed: List[Trade]
    - position_history: Dict[str, List[int]]
"""
