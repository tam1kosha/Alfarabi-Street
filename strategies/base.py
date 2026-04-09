"""Base class for all trading strategies."""

import os
import sys
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datamodel import Order, OrderDepth, TradingState


class BaseStrategy(ABC):
    """Abstract base for strategy development.

    All strategies extend this class during development.
    For submission, the build script extracts the logic into a standalone Trader class.

    The run() method signature matches the competition's Trader.run() exactly:
        - Input: TradingState
        - Output: (orders_dict, conversions, trader_data)
    """

    @abstractmethod
    def run(
        self, state: TradingState
    ) -> Tuple[Dict[str, List[Order]], int, str]:
        """Called each timestamp with the current market state.

        Args:
            state: Current market state including order depths, positions, trades.

        Returns:
            orders: Dict mapping symbol -> list of Order objects.
            conversions: Number of conversions to request (0 if unused).
            trader_data: Serialized state string to persist between calls.
        """
        raise NotImplementedError

    # --- Helpers (convenience methods for strategy development) ---

    def get_position(self, state: TradingState, product: str) -> int:
        """Current position for a product (0 if none)."""
        return state.position.get(product, 0)

    def get_mid_price(self, state: TradingState, product: str) -> float | None:
        """Compute mid price from best bid and ask."""
        od = state.order_depths.get(product)
        if od is None or not od.buy_orders or not od.sell_orders:
            return None
        best_bid = max(od.buy_orders.keys())
        best_ask = min(od.sell_orders.keys())
        return (best_bid + best_ask) / 2

    def get_best_bid_ask(
        self, state: TradingState, product: str
    ) -> Tuple[int | None, int | None]:
        """Return (best_bid, best_ask) from order depth."""
        od = state.order_depths.get(product)
        if od is None:
            return None, None
        best_bid = max(od.buy_orders.keys()) if od.buy_orders else None
        best_ask = min(od.sell_orders.keys()) if od.sell_orders else None
        return best_bid, best_ask

    def get_order_depth_volume(
        self, state: TradingState, product: str
    ) -> Tuple[int, int]:
        """Return (total_bid_volume, total_ask_volume) for a product."""
        od = state.order_depths.get(product)
        if od is None:
            return 0, 0
        bid_vol = sum(od.buy_orders.values())
        ask_vol = sum(abs(v) for v in od.sell_orders.values())
        return bid_vol, ask_vol
