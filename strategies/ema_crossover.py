# strategies/ema_crossover.py
import requests
import pandas as pd
from collections import deque
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🔧 Load config
with open("config.json") as f:
    config = json.load(f)

symbol = config.get("symbol", "BTCUSDT")
ema_fast = config.get("ema_fast", 12)
ema_slow = config.get("ema_slow", 26)
min_signal = config.get("min_signal", 0.01)
max_len = max(ema_fast, ema_slow) * 5

# Store price history
price_history = deque(maxlen=max_len)


def get_price():
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        price = float(response.json()["price"])
        price_history.append(price)
        return price
    except (requests.RequestException, KeyError, ValueError) as e:
        logging.error(f"Error fetching price: {e}")
        return None


def compute_ema(prices, period):
    if len(prices) < period:
        return None
    return pd.Series(prices).ewm(span=period, adjust=False).mean().iloc[-1]


def decide_action(price: float, position_open: bool):
    if price is None:
        return "HOLD", None

    if len(price_history) < max(ema_fast, ema_slow):
        logging.info("Not enough data for EMA calculation.")
        return "HOLD", None

    fast = compute_ema(price_history, ema_fast)
    slow = compute_ema(price_history, ema_slow)

    if fast is None or slow is None:
        return "HOLD", None

    signal = fast - slow
    logging.info(f"Price: {price:.2f} | EMA{ema_fast}: {fast:.2f} | EMA{ema_slow}: {slow:.2f} | Signal: {signal:.5f}")

    if signal > min_signal and not position_open:
        return "BUY", signal
    elif signal < -min_signal and position_open:
        return "SELL", signal
    return "HOLD", signal
