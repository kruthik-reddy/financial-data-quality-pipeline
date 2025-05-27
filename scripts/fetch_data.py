import pandas as pd
import yfinance as yf
import os
import argparse
import matplotlib.pyplot as plt

def fetch_and_plot_stock_data(symbol, period=None, start=None, end=None):
    if period:
        df = yf.download(symbol, period=period)
    else:
        df = yf.download(symbol, start=start, end=end)

    os.makedirs("data", exist_ok=True)
    csv_path = f"data/{symbol}_raw.csv"
    df.to_csv(csv_path)
    print(f"{symbol} data saved at {csv_path}")

    if "Close" in df.columns:
        df["Close"].plot(title=f"{symbol} Closing Price", figsize=(10, 4))
        plt.xlabel("Date")
        plt.ylabel("Close Price")
        plt.grid(True)
        plot_path = f"data/{symbol}_closing_plot.png"
        plt.savefig(plot_path)
        plt.close()
        print(f"{symbol} plot saved at {plot_path}")
    else:
        print(f"No 'Close' column found to plot for {symbol}.")

def fetch_multiple(symbols, period=None, start=None, end=None):
    for symbol in symbols:
        fetch_and_plot_stock_data(symbol, period=period, start=start, end=end)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download, clean, and plot stock data.")
    parser.add_argument("--symbols", nargs="+", default=["AAPL"], help="List of stock symbols (e.g., AAPL TSLA MSFT)")
    parser.add_argument("--period", type=str, default=None, help="Data period like 1mo, 6mo, 1y")
    parser.add_argument("--start", type=str, default=None, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default=None, help="End date (YYYY-MM-DD)")
    args = parser.parse_args()

    fetch_multiple(args.symbols, period=args.period, start=args.start, end=args.end)
