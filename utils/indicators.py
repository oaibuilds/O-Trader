import pandas as pd

def compute_ema(prices, period):
    if len(prices) < period:
        return None
    return pd.Series(prices).ewm(span=period, adjust=False).mean().iloc[-1]

def compute_macd(prices, fast_period=12, slow_period=26, signal_period=9):
    if len(prices) < slow_period + signal_period:
        return None, None
    fast_ema = pd.Series(prices).ewm(span=fast_period, adjust=False).mean()
    slow_ema = pd.Series(prices).ewm(span=slow_period, adjust=False).mean()
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    return macd_line.iloc[-1], signal_line.iloc[-1]

def compute_rsi(prices: pd.Series, period: int = 14) -> float:
    if len(prices) < period + 1:
        return None
    delta = prices.diff().dropna()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean().iloc[-1]
    avg_loss = loss.rolling(window=period).mean().iloc[-1]
    return 100.0 if avg_loss == 0 else 100 - (100 / (1 + avg_gain / avg_loss))

def compute_macd(series, fast=12, slow=26, signal=9):
    if len(series) < slow + signal:
        return None, None, None
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line
    return macd_line.iloc[-1], signal_line.iloc[-1], hist.iloc[-1]
