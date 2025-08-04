import csv
from datetime import datetime
import time
from logic import get_price, decide_action, symbol, config
from wallet import Wallet
from colorama import init, Fore
from trade_limiter import TradeLimiter

init(autoreset=True)

wallet = Wallet(balance=1000.0)
base_qty = 10
strategy_name = config["strategy"]
limiter = TradeLimiter(max_trades_per_minute=5)

# 💾 Guardar estado inicial (balance 1000.00) en el CSV
with open("trades.csv", mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        datetime.utcnow(),  # timestamp
        "INIT",             # acción
        symbol,
        "-",                # precio
        0,                  # cantidad
        wallet.balance,     # balance inicial
        strategy_name,
        "-",                # signal
        0,                  # pnl
        "-"                 # trend
    ])

def calculate_qty(signal: float) -> int:
    if signal is None:
        return base_qty
    elif signal < 25:
        return base_qty * 3
    elif signal < 30:
        return base_qty * 2
    else:
        return base_qty

if __name__ == "__main__":
    while True:
        price = get_price()
        action, signal, trend = decide_action(price, len(wallet.positions) > 0, config)

        if not limiter.can_trade():
            action = "HOLD"
            signal = "LIMIT"
            trend = "-"

        qty = calculate_qty(signal) if action == "BUY" else 0

        color = Fore.GREEN if action == "BUY" else Fore.RED if action == "SELL" else Fore.LIGHTBLACK_EX
        info = f"Signal: {signal:.5f}" if isinstance(signal, float) else f"{signal}"
        print(color + f"[{symbol}] Price: {price:.5f} | {info} | Trend: {trend} | Qty: {qty} | Action: {action} | Balance: {wallet.balance:.5f}")

        wallet.update(action, price, symbol, qty, strategy_name, signal)
        time.sleep(config.get("polling_interval", 60))
