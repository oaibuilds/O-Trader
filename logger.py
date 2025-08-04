import csv
from pathlib import Path

LOG_FILE = "trades.csv"

def log_trade_extended(timestamp, action, symbol, price, qty, balance, strategy, signal, pnl, trend="-"):
    """
    Guarda un trade en formato CSV.
    Campos: timestamp, action, symbol, price, quantity, balance, strategy, signal, pnl, trend
    """

    # Asegurar formato correcto en los campos numéricos
    try:
        signal = round(float(signal), 2)
    except (ValueError, TypeError):
        signal = -1.0  # Valor por defecto si no es float

    row = [
        timestamp,
        action,
        symbol,
        round(price, 5),
        round(qty, 4),
        round(balance, 5),
        strategy,
        signal,
        round(pnl, 5),
        trend
    ]

    # Crear archivo si no existe
    file = Path(LOG_FILE)
    exists = file.exists()

    with open(file, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["timestamp", "action", "symbol", "price", "quantity", "balance", "strategy", "signal", "pnl", "trend"])
        writer.writerow(row)
