# O-Trader

**O-Trader** is a modular and extensible framework for algorithmic trading simulation and strategy development. It is part of **The O Project**, an initiative focused on AI-driven systems for automating tasks.

---

## 🧠 Project Vision

This system is designed with scalability and clarity in mind:

- Simulate and validate trading strategies with real or synthetic data.
- Support multiple plug-in strategies and logic modules.
- Integrate GPT-based agents and advanced analyzers over time.
- Maintain full auditability and exportability of trades and results.
- Transition smoothly from **paper trading** to **real-time trading** via APIs.

---

## 📁 Project Structure

```
O-Trader/
│
├── analyzer/               # Tools for trade analysis and reporting
├── core/                   # Simulation engine, wallet logic, logs
├── data/                   # Historical market data or API responses
├── logic/                  # Signal generators, indicators, and shared logic
├── strategies/             # Custom strategies (trend_rsi, future ones)
├── tests/                  # Unit tests
├── utils/                  # Utility functions
│
├── config.json             # Global config file
├── main.py                 # Project entry point
├── logger.py               # Logging helper
├── simulator.py            # Trading simulator core
├── trades.csv              # Generated trades log
├── requirements.txt        # Python dependencies
├── .env / .env.template    # Environment variables (API keys, etc.)
```

---

## ✅ Current Status

- [x] Core simulation logic implemented
- [x] Plug-in strategy system working
- [x] First strategy: `trend_rsi`
- [x] Trade logs saved to CSV
- [ ] Binance API integration pending
- [ ] GPT-based trading agents (planned)

---

## 🚀 How to Run

```bash
git clone https://github.com/oaibuilds/O-Trader.git
cd O-Trader
pip install -r requirements.txt
python main.py
```

You can adjust parameters in `config.json` such as initial balance, polling intervals, thresholds, etc.

---

## 📊 Sample Output

```
Total Trades      : 27
Buy Trades        : 13
Sell Trades       : 13
Final Balance     : 999.99 USDT
Net PnL           : -0.00088%
Win Rate          : 48%
```

> Simulation uses neutral conditions (no slippage or fees).

---

## ➕ Add a New Strategy

1. Create a new Python file inside `strategies/`.
2. Define a function `generate_signal(data: dict) -> str`.
3. It should return `"BUY"`, `"SELL"` or `"HOLD"`.
4. Register your strategy in `main.py`.

---

## 🧠 Roadmap (Next Steps)

- 🔜 Binance API integration (real trading)
- 🔜 Agent GPTs for trade reasoning and adaptation
- 🔜 Real-time backtest dashboard
- 🔜 Strategy benchmarking system
- 🔜 Telegram or Discord alerts

---

## 🌐 The O Project

> `O-Trader` is a core module of **The O Project**, focused on long-term intelligence, autonomy and global capital leverage.

Learn more soon at: [oaibuilds.com](https://oaibuilds.com)

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for more info.
