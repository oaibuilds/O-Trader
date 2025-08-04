# strategies/rsi_strategy.py
import requests
import pandas as pd
from collections import deque
import json

# 🔧 Load config
with open("config.json") as f:
    config = json.load(f)

symbol = config["symbol"]
buy_rsi = config["buy_rsi"]
sell_rsi = config["sell_rsi"]

price_history = deque(maxlen=100)

def get_price():
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    r = requests.get(url)
    price = float(r.json()["price"])
    price_history.append(price)
    return price

def compute_rsi(prices, period=14):
    if len(prices) < period:
        return None
    series = pd.Series(prices)
    delta = series.diff().dropna()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def decide_action(price, position_open):
    """Buy if RSI < buy_rsi and no open position. Sell if RSI > sell_rsi and has position."""
    rsi = compute_rsi(list(price_history))
    if rsi is None:
        return "HOLD", None
    if rsi < buy_rsi and not position_open:
        return "BUY", rsi
    elif rsi > sell_rsi and position_open:
        return "SELL", rsi
    return "HOLD", rsi
