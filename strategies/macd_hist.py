import pandas as pd
from utils.trend import is_uptrend, is_downtrend

prices = []

def compute_macd(series, fast=12, slow=26, signal=9):
    if len(series) < slow + signal:
        return None, None, None  
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line
    return macd_line.iloc[-1], signal_line.iloc[-1], hist.iloc[-1]

def decide_action(price: float, position_open: bool, config: dict):
    global prices
    prices.append(price)
    if len(prices) > 200:
        prices.pop(0)

    series = pd.Series(prices)
    macd, signal_line, hist = compute_macd(series)

    if hist is None:
        return "HOLD", None, "UNKNOWN"

    min_macd = config.get("min_macd", 0.001)
    trend = "UP" if hist > 0 else "DOWN" if hist < 0 else "SIDEWAYS"

    if hist > min_macd and not position_open:
        return "BUY", hist, trend
    elif hist < -min_macd and position_open:
        return "SELL", hist, trend
    else:
        return "HOLD", hist, trend
