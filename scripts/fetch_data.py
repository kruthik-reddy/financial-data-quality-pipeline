import pandas as pd
import requests
from datetime import datetime
import os

def fetch_stock_data(symbol="AAPL"):
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1=1672531200&period2=1704067200&interval=1d&events=history"
    df = pd.read_csv(url)
    df.to_csv(f"data/{symbol}_raw.csv", index=False)
    print(f"{symbol} data saved at data/{symbol}_raw.csv")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    fetch_stock_data()
