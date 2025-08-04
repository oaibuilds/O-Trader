def classify_trend(signal: float) -> str:
    if signal > 0:
        return "UP"
    elif signal < 0:
        return "DOWN"
    return "SIDEWAYS"
