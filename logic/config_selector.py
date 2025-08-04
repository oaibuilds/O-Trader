import json

PRESETS = {
    "trend_rsi": {
        "strategy": "trend_rsi",
        "polling_interval": 2,
        "buy_rsi": 35,
        "sell_rsi": 65,
        "ema_fast": 9,
        "ema_slow": 21,
        "trend_window": 5
    },
    "ema_crossover": {
        "strategy": "ema_crossover",
        "polling_interval": 2,
        "ema_fast": 9,
        "ema_slow": 21,
        "min_signal": 0.001
    },
    "macd_hist": {
        "strategy": "macd_hist",
        "polling_interval": 2,
        "min_macd": 0.001
    }
}

SYMBOLS = ["DOGEUSDT", "ETHUSDT", "SOLUSDT", "BTCUSDT"]

def select_config():
    print("\n📊 Available Strategies:")
    for i, name in enumerate(PRESETS, 1):
        print(f"{i}. {name}")

    choice = int(input("\nChoose a strategy [1/2/...]: ")) - 1
    key = list(PRESETS.keys())[choice]
    config = PRESETS[key]

    print("\n💱 Available Symbols:")
    for i, s in enumerate(SYMBOLS, 1):
        print(f"{i}. {s}")
    sym_choice = int(input("\nChoose a symbol [1/2/...]: ")) - 1
    config["symbol"] = SYMBOLS[sym_choice]

    config["max_positions"] = 3
    config["take_profit_pct"] = 0.02
    config["stop_loss_pct"] = 0.01

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    print(f"\n✅ Config saved for strategy: {key} on symbol: {config['symbol']}\n")

if __name__ == "__main__":
    select_config()
