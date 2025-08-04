# strategies/ema_crossover.py
import pandas as pd
from collections import deque
from logic.trend import is_uptrend, is_downtrend


price_history = deque(maxlen=200)

def compute_ema(prices, period):
    if len(prices) < period:
        return None
    return pd.Series(prices).ewm(span=period, adjust=False).mean().iloc[-1]

def decide_action(price: float, position_open: bool, config: dict):
    global price_history
    price_history.append(price)

    ema_fast = config.get("ema_fast", 12)
    ema_slow = config.get("ema_slow", 26)
    min_signal = config.get("min_signal", 0.01)

    if len(price_history) < max(ema_fast, ema_slow):
        return "HOLD", None, "UNKNOWN"

    fast = compute_ema(price_history, ema_fast)
    slow = compute_ema(price_history, ema_slow)

    if fast is None or slow is None:
        return "HOLD", None, "UNKNOWN"

    signal = fast - slow
    trend = "UP" if signal > 0 else "DOWN" if signal < 0 else "SIDEWAYS"

    if signal > min_signal and not position_open:
        return "BUY", signal, trend
    elif signal < -min_signal and position_open:
        return "SELL", signal, trend
    else:
        return "HOLD", signal, trend
