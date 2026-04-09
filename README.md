# Alfarabi Street

Our workspace for IMC Prosperity 4. Everything here supports one goal: write trading algorithms, test them, and submit.

## Setup

```
pip install -r requirements.txt
```

This installs pandas, numpy, and matplotlib for local analysis. The actual submission uses only Python stdlib — no external packages allowed.

## Project layout

```
datamodel.py           Competition types (TradingState, Order, OrderDepth, etc.)
utils/data_loader.py   Load round data from CSVs
strategies/base.py     Base class for strategies
strategies/            Your strategies go here
visualizer/            Plotting tools (WIP)
backtest/              Backtesting engine (WIP)
build/submission.py    Packs a strategy into a single file for upload
data/                  Round data (CSVs)
```

## How to work on a strategy

1. Create a new file in `strategies/`, e.g. `strategies/my_algo.py`
2. Extend `BaseStrategy` and implement `run()`:

```python
from datamodel import Order, TradingState
from strategies.base import BaseStrategy

class MyAlgo(BaseStrategy):
    def run(self, state: TradingState):
        orders = {}
        # your logic here
        return orders, 0, ""
```

`run()` receives the current market state and returns three things:
- `orders`: dict of symbol -> list of `Order` objects
- `conversions`: int, usually 0
- `trader_data`: string, persists between calls (use it to carry state across ticks)

`BaseStrategy` gives you some helpers: `self.get_position()`, `self.get_mid_price()`, `self.get_best_bid_ask()`. Check `strategies/base.py` for details.

See `strategies/example_mm.py` for a working example.

## Loading data

```python
from utils.data_loader import load_prices, load_trades, load_round

# single day
prices = load_prices(round_num=0, day=-1)
trades = load_trades(round_num=0, day=-1)

# all days in a round
prices, trades = load_round(round_num=0)
```

Round 0 is the tutorial round. Future rounds go into `data/round_1/`, `data/round_2/`, etc.

## Building a submission

The competition expects a single `.py` file with a `Trader` class. The build script handles this:

```
python3 -m build.submission strategies/my_algo.py -o submission.py
```

This concatenates `datamodel.py` and your strategy into one file, renames your class to `Trader`, and inlines any base class helpers you used. Upload the resulting `submission.py` to the platform.

## What's not done yet

- **Visualizer** (`visualizer/plots.py`) — function stubs are there, needs implementation
- **Backtester** (`backtest/runner.py`) — planned integration with [jmerle's backtester](https://github.com/jmerle/imc-prosperity-3-backtester) or a custom one
