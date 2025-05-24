import pandas as pd
import pytest
from scripts.validate_data import validate_data

def test_no_nulls():
    df = pd.DataFrame({"Date": ["2024-01-01"], "Close": [150]})
    df.to_csv("data/test_sample.csv", index=False)
    try:
        validate_data("data/test_sample.csv")
    except Exception as e:
        pytest.fail(f"Validation raised an error: {e}")
