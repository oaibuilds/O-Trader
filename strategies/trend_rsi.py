# strategies/trend_rsi.py
import pandas as pd
from logic.trend import is_uptrend, is_downtrend


prices = []

def rsi(prices: pd.Series, period: int = 14) -> float:
    if len(prices) < period + 1:
        return None
    delta = prices.diff().dropna()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean().iloc[-1]
    avg_loss = loss.rolling(window=period).mean().iloc[-1]
    return 100.0 if avg_loss == 0 else 100 - (100 / (1 + avg_gain / avg_loss))

def decide_action(price: float, position_open: bool, config: dict):
    global prices
    prices.append(price)
    if len(prices) > 100:
        prices = prices[-100:]

    series = pd.Series(prices)
    rsi_val = rsi(series, 14)
    if rsi_val is None:
        return "HOLD", None, "UNKNOWN"

    trend_window = config.get("trend_window", 5)
    trend = (
        "UP" if is_uptrend(series, trend_window)
        else "DOWN" if is_downtrend(series, trend_window)
        else "SIDEWAYS"
    )

    if not position_open and rsi_val < config.get("buy_rsi", 35) and trend == "UP":
        return "BUY", rsi_val, trend
    elif position_open and rsi_val > config.get("sell_rsi", 65) and trend == "DOWN":
        return "SELL", rsi_val, trend
    else:
        return "HOLD", rsi_val, trend
