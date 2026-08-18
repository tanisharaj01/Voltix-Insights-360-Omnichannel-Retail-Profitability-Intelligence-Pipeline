import logging
from pathlib import Path
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/raw/sales_transactions_raw.csv"
OUTPUT = ROOT / "data/processed/sales_transactions_clean.csv"

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the raw sales transactions DataFrame.
    """
    logger.info("Starting data cleaning process...")
    
    # Strip whitespace from string columns
    str_cols = ["state", "city", "region", "channel", "category", "product", "payment_mode"]
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()
            
    # Standardize specific values
    if "state" in df.columns:
        df["state"] = df["state"].replace({"delhi": "Delhi"})
        
    # Drop duplicates based on order_id
    initial_rows = len(df)
    df = df.drop_duplicates(subset=["order_id"], keep="first")
    logger.info(f"Dropped {initial_rows - len(df)} duplicate orders.")

    # Fill missing values
    if "city" in df.columns:
        df["city"] = df["city"].fillna("Unknown")
    if "payment_mode" in df.columns:
        df["payment_mode"] = df["payment_mode"].fillna("Unknown")

    # Feature engineering: Dates
    if "order_date" in df.columns:
        df["year"] = df["order_date"].dt.year
        df["month_num"] = df["order_date"].dt.month
        df["month"] = df["order_date"].dt.strftime("%b")
        df["quarter"] = "Q" + df["order_date"].dt.quarter.astype(str)
        df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
        
    # Feature engineering: Financials
    if all(c in df.columns for c in ["quantity", "unit_price", "discount_pct", "profit", "sales_amount"]):
        df["gross_sales_before_discount"] = df["quantity"] * df["unit_price"]
        df["discount_amount"] = df["gross_sales_before_discount"] * df["discount_pct"]
        df["profit_margin"] = df["profit"] / df["sales_amount"]

    # Sort and reset index
    if "order_date" in df.columns and "order_id" in df.columns:
        df = df.sort_values(["order_date", "order_id"]).reset_index(drop=True)
        
    logger.info("Data cleaning completed.")
    return df

def main():
    """Main execution function."""
    try:
        logger.info(f"Loading raw data from {INPUT}")
        df = pd.read_csv(INPUT, parse_dates=["order_date"])
        
        cleaned_df = clean_data(df)
        
        # Ensure output directory exists
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        
        cleaned_df.to_csv(OUTPUT, index=False)
        logger.info(f"Saved {len(cleaned_df):,} clean rows to {OUTPUT}")
    except FileNotFoundError:
        logger.error(f"Input file not found: {INPUT}")
    except Exception as e:
        logger.error(f"An error occurred during data cleaning: {e}")

if __name__ == "__main__":
    main()
