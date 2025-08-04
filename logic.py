import json
import importlib

with open("config.json") as f:
    config = json.load(f)

symbol = config["symbol"]
strategy_name = config["strategy"]
strategy_module = importlib.import_module(f"strategies.{strategy_name}")
decide_action = strategy_module.decide_action
get_price = strategy_module.get_price