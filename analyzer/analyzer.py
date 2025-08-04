import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

CSV_FILE = "trades.csv"

def main():
    if not Path(CSV_FILE).exists():
        print("❌ No trades.csv file found. Run the bot first to generate trades.")
        return

    df = pd.read_csv(CSV_FILE, header=None, names=[
        "timestamp", "action", "symbol", "price", "quantity", "balance", "strategy", "signal", "pnl", "trend"
    ])

    if df.empty:
        print("⚠️ trades.csv is empty.")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601")

    df["signal"] = pd.to_numeric(df["signal"], errors="coerce")  # ✅ evita crash si hay strings

    # 📈 KPI Summary
    print("\n📊 TRADE SUMMARY")
    print("-" * 40)
    print(f"Total Trades      : {len(df)}")
    print(f"Buy Trades        : {len(df[df['action'] == 'BUY'])}")
    print(f"Sell Trades       : {len(df[df['action'] == 'SELL'])}")
    print(f"Final Balance     : {df['balance'].iloc[-1]:.2f}")
    print(f"Unique Strategies : {df['strategy'].nunique()}")
    print("-" * 40)

    for strat in df["strategy"].unique():
        sub = df[df["strategy"] == strat]
        print(f"\n🔹 Strategy: {strat}")
        print(f"  Trades: {len(sub)} | Final Balance: {sub['balance'].iloc[-1]:.2f}")
        print(f"  Avg Signal BUY : {sub[sub['action'] == 'BUY']['signal'].mean():.5f}")
        print(f"  Avg Signal SELL: {sub[sub['action'] == 'SELL']['signal'].mean():.5f}")

    # 💰 PROFIT SUMMARY
    initial_balance = df.iloc[0]["balance"]
    final_balance = df["balance"].iloc[-1]
    net_profit = final_balance - initial_balance
    net_profit_pct = (net_profit / initial_balance) * 100
    avg_pnl = df["pnl"].mean()
    win_trades = df[df["pnl"] > 0]
    loss_trades = df[df["pnl"] < 0]
    win_rate = len(win_trades) / len(df[df['action'] == 'SELL']) * 100 if len(df[df['action'] == 'SELL']) > 0 else 0

    print("\n💰 PROFIT SUMMARY")
    print("-" * 40)
    print(f"Initial Balance   : {initial_balance:.5f}")
    print(f"Final Balance     : {final_balance:.5f}")
    print(f"Net Profit ($)    : {net_profit:.5f}")
    print(f"Net Profit (%)    : {net_profit_pct:.5f}%")
    print(f"Avg PnL per trade : {avg_pnl:.5f}")
    print(f"Win Rate (SELLs)  : {win_rate:.5f}%")
    print("-" * 40)

    # Gráficos
    plot_balance(df)
    plot_equity_curve(df)

def plot_balance(df):
    df_plot = df.drop_duplicates(subset="timestamp")[["timestamp", "balance"]]

    plt.figure(figsize=(10, 5))
    plt.plot(df_plot["timestamp"], df_plot["balance"], marker="o", linestyle="-")
    plt.title("📈 Balance Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Balance")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_equity_curve(df):
    df["equity"] = df["pnl"].cumsum() + df.iloc[0]["balance"]
    df.set_index("timestamp", inplace=True)
    df["equity"].plot(title="Equity Curve")
    plt.xlabel("Time")
    plt.ylabel("Equity")
    plt.grid()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
