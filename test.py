import requests

def get_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    r = requests.get(url)
    return float(r.json()['price'])

print("✅ Conexión exitosa")
for symbol in ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT"]:
    print(symbol, "→", get_price(symbol))

