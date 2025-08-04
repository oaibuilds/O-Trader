from logger import log_trade_extended
from datetime import datetime
import json

with open("config.json") as f:
    config = json.load(f)


class Wallet:
    def __init__(self, balance, max_positions=3):
        self.balance = balance
        self.positions = []  # List of dicts: {"entry": float, "qty": float, "time": str}
        self.max_positions = max_positions

        # Configurable risk management
        self.take_profit_pct = config.get("take_profit_pct", 0.02)  # +2%
        self.stop_loss_pct = config.get("stop_loss_pct", 0.01)      # -1%

    def update(self, action, price, symbol, qty, strategy, signal):
        now = datetime.utcnow().isoformat()
        pnl = 0.0

        # Asegurar que signal sea un float con 2 decimales
        try:
            signal = round(float(signal), 2)
        except (ValueError, TypeError):
            signal = -1.0

        closed_positions = []
        for i, pos in enumerate(self.positions):
            entry = pos["entry"]
            delta = price - entry
            delta_pct = delta / entry

            if delta_pct >= self.take_profit_pct:
                pnl = delta * pos["qty"]
                proceeds = pos["qty"] * price
                self.balance += proceeds
                log_trade_extended(now, "SELL", symbol, price, pos["qty"], self.balance, strategy, signal, pnl, trend="TP")
                closed_positions.append(i)

            elif delta_pct <= -self.stop_loss_pct:
                pnl = delta * pos["qty"]
                proceeds = pos["qty"] * price
                self.balance += proceeds
                log_trade_extended(now, "SELL", symbol, price, pos["qty"], self.balance, strategy, signal, pnl, trend="SL")
                closed_positions.append(i)

        for i in reversed(closed_positions):
            self.positions.pop(i)

        if action == "BUY" and len(self.positions) < self.max_positions:
            cost = qty * price
            self.balance -= cost
            self.positions.append({"entry": price, "qty": qty, "time": now})
            log_trade_extended(now, "BUY", symbol, price, qty, self.balance, strategy, signal, pnl=0.0)

        elif action == "SELL" and self.positions:
            pos = self.positions.pop(0)
            entry = pos["entry"]
            proceeds = pos["qty"] * price
            pnl = (price - entry) * pos["qty"]
            self.balance += proceeds
            log_trade_extended(now, "SELL", symbol, price, pos["qty"], self.balance, strategy, signal, pnl, trend="MANUAL")
