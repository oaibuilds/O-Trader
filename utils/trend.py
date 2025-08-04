import pandas as pd

def is_uptrend(prices: pd.Series, window: int = 5) -> bool:
    """
    Returns True if the average of the last `window` prices is increasing.
    """
    if len(prices) < window + 1:
        return False
    return prices.iloc[-window:].mean() > prices.iloc[-(window+1):-1].mean()

def is_downtrend(prices: pd.Series, window: int = 5) -> bool:
    """
    Returns True if the average of the last `window` prices is decreasing.
    """
    if len(prices) < window + 1:
        return False
    return prices.iloc[-window:].mean() < prices.iloc[-(window+1):-1].mean()
