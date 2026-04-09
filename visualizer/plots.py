"""Visualization stub.

TODO: Implement these plotting functions using matplotlib.
Use utils/data_loader.py to load data, then visualize.

Example usage (once implemented):
    from utils.data_loader import load_prices, load_trades
    from visualizer.plots import plot_price_series

    prices = load_prices(round_num=0, day=-1)
    plot_price_series(prices, product="EMERALDS")

Planned functions:

    plot_price_series(prices_df, product)
        Mid price over time with bid/ask bands.

    plot_spread(prices_df, product)
        Bid-ask spread over time.

    plot_order_book_snapshot(prices_df, product, timestamp)
        Depth chart at a single point in time.

    plot_trade_volume(trades_df, symbol)
        Volume bars over time.

    plot_pnl(prices_df, product)
        Cumulative profit_and_loss curve.

    plot_comparison(prices_df, products)
        Overlay mid prices of multiple products (normalized).
"""
