def calculate_qty(signal: float, strategy: str, base_qty: int = 10) -> int:
    """
    Devuelve la cantidad a operar basada en la señal y la estrategia activa.

    :param signal: valor de señal entregado por la estrategia (puede ser RSI, MACD histograma, etc.)
    :param strategy: nombre de la estrategia (ej: 'trend_rsi', 'ema_crossover', 'macd_hist')
    :param base_qty: cantidad base (por defecto 10)
    :return: cantidad ajustada
    """
    if signal is None:
        return base_qty

    if strategy == "trend_rsi":
        if signal < 20:
            return base_qty * 3
        elif signal < 30:
            return base_qty * 2
        else:
            return base_qty

    elif strategy == "ema_crossover":
        abs_signal = abs(signal)
        if abs_signal > 0.1:
            return base_qty * 3
        elif abs_signal > 0.05:
            return base_qty * 2
        else:
            return base_qty

    elif strategy == "macd_hist":
        abs_signal = abs(signal)
        if abs_signal > 1.0:
            return base_qty * 3
        elif abs_signal > 0.5:
            return base_qty * 2
        else:
            return base_qty

    else:
        # Estrategia desconocida → usar cantidad base
        return base_qty
