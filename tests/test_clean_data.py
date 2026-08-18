import pandas as pd
import pytest
import sys
from pathlib import Path

# Add src to Python path so we can import our modules
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.clean_data import clean_data

@pytest.fixture
def sample_data():
    """Returns a small DataFrame simulating raw sales data."""
    return pd.DataFrame({
        "order_id": [1, 1, 2, 3],
        "order_date": pd.to_datetime(["2024-01-15", "2024-01-15", "2024-02-10", "2024-03-05"]),
        "state": [" delhi ", "delhi", "maharashtra", "karnataka "],
        "city": ["New Delhi", "New Delhi", None, "Bangalore"],
        "region": ["North", "North", "West", "South"],
        "channel": ["Online", "Online", "Store", "Online"],
        "category": ["Electronics", "Electronics", "Clothing", "Home"],
        "product": ["Laptop", "Laptop", "Shirt", "Table"],
        "payment_mode": [None, None, "Cash", "Card"],
        "quantity": [1, 1, 2, 1],
        "unit_price": [50000, 50000, 1000, 5000],
        "discount_pct": [0.10, 0.10, 0.0, 0.05],
        "profit": [5000, 5000, 500, 1000],
        "sales_amount": [45000, 45000, 2000, 4750]
    })

def test_clean_data(sample_data):
    """Tests the clean_data function."""
    df = clean_data(sample_data)
    
    # 1. Duplicates dropped (order_id 1 is duplicated)
    assert len(df) == 3
    
    # 2. String stripping
    assert df["state"].iloc[0] == "Delhi" # And delhi replacement
    assert df["state"].iloc[2] == "karnataka"
    
    # 3. Fillna
    assert df["city"].iloc[1] == "Unknown"
    assert df["payment_mode"].iloc[0] == "Unknown"
    
    # 4. Dates
    assert df["year"].iloc[0] == 2024
    assert df["month_num"].iloc[1] == 2
    assert df["quarter"].iloc[2] == "Q1"
    
    # 5. Financials
    # order 1 laptop: quantity 1, unit_price 50000
    assert df["gross_sales_before_discount"].iloc[0] == 50000
    assert df["discount_amount"].iloc[0] == 5000
    assert df["profit_margin"].iloc[0] == pytest.approx(5000 / 45000)
