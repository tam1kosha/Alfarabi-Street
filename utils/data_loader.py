"""Load competition CSV data into pandas DataFrames and native datamodel objects."""

import os
from typing import Dict, List, Optional, Tuple

import pandas as pd

# Add project root to path so datamodel can be imported
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datamodel import OrderDepth, Trade

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Maps round number to directory name
_ROUND_DIR_MAP = {
    0: "tutorial round",
}


def _resolve_round_dir(round_num: int, data_dir: str = DATA_DIR) -> str:
    """Map round number to actual directory path."""
    dir_name = _ROUND_DIR_MAP.get(round_num, f"round_{round_num}")
    path = os.path.join(data_dir, dir_name)
    if not os.path.isdir(path):
        # Try alternative naming
        alt_name = f"round_{round_num}"
        alt_path = os.path.join(data_dir, alt_name)
        if os.path.isdir(alt_path):
            return alt_path
        raise FileNotFoundError(
            f"No data directory found for round {round_num}. "
            f"Tried: {path}, {alt_path}"
        )
    return path


def _find_csv(round_dir: str, file_type: str, day: int) -> str:
    """Find CSV file matching the pattern {file_type}_round_N_day_{day}.csv."""
    for fname in os.listdir(round_dir):
        if fname.startswith(file_type) and f"day_{day}" in fname and fname.endswith(".csv"):
            return os.path.join(round_dir, fname)
    raise FileNotFoundError(
        f"No {file_type} CSV found for day {day} in {round_dir}"
    )


def list_rounds(data_dir: str = DATA_DIR) -> List[str]:
    """Return available round directory names."""
    if not os.path.isdir(data_dir):
        return []
    return sorted(
        d for d in os.listdir(data_dir)
        if os.path.isdir(os.path.join(data_dir, d)) and not d.startswith(".")
    )


def list_days(round_num: int, data_dir: str = DATA_DIR) -> List[int]:
    """Return sorted day numbers available for a round."""
    round_dir = _resolve_round_dir(round_num, data_dir)
    days = set()
    for fname in os.listdir(round_dir):
        if "day_" in fname and fname.endswith(".csv"):
            # Extract day number from filename like prices_round_0_day_-1.csv
            part = fname.split("day_")[1].replace(".csv", "")
            try:
                days.add(int(part))
            except ValueError:
                continue
    return sorted(days)


def load_prices(round_num: int, day: int, data_dir: str = DATA_DIR) -> pd.DataFrame:
    """Load prices CSV into a DataFrame.

    Returns DataFrame with columns: day, timestamp, product, bid_price_1..3,
    bid_volume_1..3, ask_price_1..3, ask_volume_1..3, mid_price, profit_and_loss.
    """
    round_dir = _resolve_round_dir(round_num, data_dir)
    path = _find_csv(round_dir, "prices", day)
    return pd.read_csv(path, sep=";")


def load_trades(round_num: int, day: int, data_dir: str = DATA_DIR) -> pd.DataFrame:
    """Load trades CSV into a DataFrame.

    Returns DataFrame with columns: timestamp, buyer, seller, symbol, currency,
    price, quantity.
    """
    round_dir = _resolve_round_dir(round_num, data_dir)
    path = _find_csv(round_dir, "trades", day)
    return pd.read_csv(path, sep=";")


def load_round(
    round_num: int, data_dir: str = DATA_DIR
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load all days for a round, concatenated.

    Returns (prices_df, trades_df) with all days combined.
    """
    days = list_days(round_num, data_dir)
    if not days:
        raise FileNotFoundError(f"No data found for round {round_num}")

    prices_frames = []
    trades_frames = []
    for day in days:
        try:
            prices_frames.append(load_prices(round_num, day, data_dir))
        except FileNotFoundError:
            pass
        try:
            trades_frames.append(load_trades(round_num, day, data_dir))
        except FileNotFoundError:
            pass

    prices_df = pd.concat(prices_frames, ignore_index=True) if prices_frames else pd.DataFrame()
    trades_df = pd.concat(trades_frames, ignore_index=True) if trades_frames else pd.DataFrame()
    return prices_df, trades_df


def prices_to_order_depth(prices_row: pd.Series) -> OrderDepth:
    """Convert a single row of price data into an OrderDepth object.

    Args:
        prices_row: A single row from the prices DataFrame.

    Returns:
        OrderDepth with buy_orders and sell_orders populated.
    """
    od = OrderDepth()
    for i in range(1, 4):
        bid_price = prices_row.get(f"bid_price_{i}")
        bid_vol = prices_row.get(f"bid_volume_{i}")
        if pd.notna(bid_price) and pd.notna(bid_vol):
            od.buy_orders[int(bid_price)] = int(bid_vol)

        ask_price = prices_row.get(f"ask_price_{i}")
        ask_vol = prices_row.get(f"ask_volume_{i}")
        if pd.notna(ask_price) and pd.notna(ask_vol):
            # Sell orders have negative volume in the competition format
            od.sell_orders[int(ask_price)] = -int(ask_vol)

    return od


def trades_to_trade_list(
    trades_df: pd.DataFrame,
    timestamp: Optional[int] = None,
    symbol: Optional[str] = None,
) -> List[Trade]:
    """Convert trades DataFrame rows to a list of Trade objects.

    Args:
        trades_df: Trades DataFrame.
        timestamp: If provided, filter to this timestamp only.
        symbol: If provided, filter to this symbol only.
    """
    df = trades_df
    if timestamp is not None:
        df = df[df["timestamp"] == timestamp]
    if symbol is not None:
        df = df[df["symbol"] == symbol]

    trades = []
    for _, row in df.iterrows():
        trades.append(
            Trade(
                symbol=row["symbol"],
                price=int(row["price"]),
                quantity=int(row["quantity"]),
                buyer=str(row.get("buyer", "")),
                seller=str(row.get("seller", "")),
                timestamp=int(row["timestamp"]),
            )
        )
    return trades
