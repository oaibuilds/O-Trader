# strategies/trend_rsi.py
import pandas as pd
import numpy as np
import requests
from utils.trend import is_uptrend, is_downtrend
from logic import config, symbol

prices = []

def get_price():
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    return float(response.json()["price"])

def rsi(prices: pd.Series, period: int = 14) -> float:
    if len(prices) < period + 1:
        return None
    delta = prices.diff().dropna()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean().iloc[-1]
    avg_loss = loss.rolling(window=period).mean().iloc[-1]
    return 100.0 if avg_loss == 0 else 100 - (100 / (1 + avg_gain / avg_loss))

def calculate_qty(signal: float, base_qty: int = 10) -> int:
    if signal is None:
        return base_qty
    elif signal < 20:
        return base_qty * 3  # Muy sobrevendido → más fuerte
    elif signal < 30:
        return base_qty * 2
    else:
        return base_qty


def decide_action(price: float, position_open: bool, config: dict):
    global prices
    prices.append(price)
    if len(prices) > 100:
        prices = prices[-100:]

    series = pd.Series(prices)
    rsi_val = rsi(series, 14)
    if rsi_val is None:
        return "HOLD", None, "UNKNOWN"

    trend = "UP" if is_uptrend(series, config.get("trend_window", 5)) else "DOWN" if is_downtrend(series, config.get("trend_window", 5)) else "SIDEWAYS"

    if not position_open and rsi_val < config.get("buy_rsi", 35) and trend == "UP":
        return "BUY", rsi_val, trend
    elif position_open and rsi_val > config.get("sell_rsi", 65) and trend == "DOWN":
        return "SELL", rsi_val, trend
    else:
        return "HOLD", rsi_val, trend
