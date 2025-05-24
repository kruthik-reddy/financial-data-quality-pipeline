import pandas as pd
import logging
import os

logging.basicConfig(filename="data/validation.log", level=logging.INFO)

def validate_data(filepath):
    df = pd.read_csv(filepath)
    issues = []

    if df.isnull().values.any():
        issues.append("Missing values detected")

    if (df["Close"] < 0).any():
        issues.append("Negative closing prices found")

    if df.duplicated().any():
        issues.append("Duplicate rows detected")

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        if df["Date"].isnull().any():
            issues.append("Invalid date formats found")

    if issues:
        logging.info(f"Issues in {filepath}: {issues}")
    else:
        logging.info(f"{filepath} passed all checks")

if __name__ == "__main__":
    validate_data("data/AAPL_raw.csv")
