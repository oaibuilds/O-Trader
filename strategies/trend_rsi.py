import pandas as pd
from utils.trend import is_uptrend, is_downtrend
from utils.indicators import compute_rsi

prices = []

def decide_action(price: float, position_open: bool, config: dict):
    global prices
    prices.append(price)
    if len(prices) > 100:
        prices = prices[-100:]

    series = pd.Series(prices)
    rsi_val = compute_rsi(series, period=14)
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
