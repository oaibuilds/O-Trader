import csv
import importlib
import json
from datetime import datetime
import time
from core.wallet import Wallet
from colorama import init, Fore
from trade_limiter import TradeLimiter
from logic.data_fetcher import get_price
from core.qty_logic import calculate_qty

# 📥 Config
with open("config.json") as f:
    config = json.load(f)

symbol = config["symbol"]
strategy_name = config["strategy"]
base_qty = config.get("base_qty", 10)

wallet = Wallet(balance=1000.0)
limiter = TradeLimiter(max_trades_per_minute=5)

strategy_module = importlib.import_module(f"strategies.{strategy_name}")

# 💾 Inicializa archivo de trades
with open("trades.csv", mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        datetime.utcnow(), "INIT", symbol, "-", 0,
        wallet.balance, strategy_name, "-", 0, "-"
    ])

if __name__ == "__main__":
    while True:
        price = get_price(symbol)
        position_open = len(wallet.positions) > 0
        action, signal, trend = strategy_module.decide_action(price, position_open, config)

        if not limiter.can_trade():
            action = "HOLD"
            signal = "LIMIT"
            trend = "-"

        qty = calculate_qty(signal, strategy_name, base_qty) if action == "BUY" else 0

        color = Fore.GREEN if action == "BUY" else Fore.RED if action == "SELL" else Fore.LIGHTBLACK_EX
        info = f"Signal: {signal:.5f}" if isinstance(signal, float) else f"{signal}"
        print(color + f"[{symbol}] Price: {price:.5f} | {info} | Trend: {trend} | Qty: {qty} | Action: {action} | Balance: {wallet.balance:.5f}")

        wallet.update(action, price, symbol, qty, strategy_name, signal)
        time.sleep(config.get("polling_interval", 60))
