import pandas as pd
from scipy.stats import zscore
import matplotlib.pyplot as plt

def analyze_statistics(filepath):
    df = pd.read_csv(filepath)
    df["zscore"] = zscore(df["Close"].fillna(0))
    outliers = df[abs(df["zscore"]) > 3]

    print(f"Outliers:
{outliers[['Date', 'Close', 'zscore']]}")

    df["Close"].plot(title="Stock Closing Prices", figsize=(10, 5))
    plt.savefig("data/closing_price_trend.png")
    print("Trend plot saved to data/closing_price_trend.png")

if __name__ == "__main__":
    analyze_statistics("data/AAPL_raw.csv")
