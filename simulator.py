# simulator.py
import csv
import importlib
import pandas as pd
from core.wallet import Wallet
from logic.data_fetcher import load_config
from logic.logic import symbol
from core.qty_logic import calculate_qty

# ⚙️ Carga configuración
config = load_config()
strategy_name = config["strategy"]
strategy_module = importlib.import_module(f"strategies.{strategy_name}")

# 💰 Simulación de wallet
wallet = Wallet(balance=1000.0)
base_qty = 10

# 📈 Cargar precios desde CSV real (ajústalo si usas otra fuente)
df = pd.read_csv(f"data/{symbol}_historical.csv")
prices = df["close"].tolist()

# 📊 Guardar resultados
results = []

for i, price in enumerate(prices):
    position_open = len(wallet.positions) > 0
    action, signal, trend = strategy_module.decide_action(price, position_open, config)
    qty = calculate_qty(signal, strategy_name, base_qty) if action == "BUY" else 0

    wallet.update(action, price, symbol, qty, strategy_name, signal)

    results.append({
        "index": i,
        "price": price,
        "action": action,
        "signal": signal,
        "trend": trend,
        "balance": wallet.balance
    })

# 💾 Exportar resultados para análisis posterior
with open("simulation_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("✅ Simulación completada. Resultados guardados en simulation_results.csv")
