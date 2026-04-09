"""Example: simple market maker for EMERALDS.

Demonstrates the strategy pattern that teammates should follow.
Places symmetric bid/ask quotes around the mid price, with inventory-based
position management to stay within position limits.
"""

import os
import sys
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datamodel import Order, TradingState
from strategies.base import BaseStrategy

# Competition-defined position limit (may vary by product/round)
POSITION_LIMIT = 50


class EmeraldsMarketMaker(BaseStrategy):

    def run(
        self, state: TradingState
    ) -> Tuple[Dict[str, List[Order]], int, str]:
        orders: Dict[str, List[Order]] = {}
        product = "EMERALDS"

        position = self.get_position(state, product)
        mid = self.get_mid_price(state, product)

        if mid is None:
            return orders, 0, ""

        fair_value = round(mid)
        spread = 2

        bid_price = fair_value - spread
        ask_price = fair_value + spread

        # Remaining capacity before hitting position limits
        max_buy = POSITION_LIMIT - position
        max_sell = POSITION_LIMIT + position  # position can be negative

        product_orders: List[Order] = []
        if max_buy > 0:
            product_orders.append(Order(product, bid_price, max_buy))
        if max_sell > 0:
            product_orders.append(Order(product, ask_price, -max_sell))

        orders[product] = product_orders
        return orders, 0, ""
