import logging
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/processed/sales_transactions_clean.csv"
CHARTS = ROOT / "outputs/charts"
TABLES = ROOT / "outputs/tables"
EXCEL_OUTPUT = ROOT / "outputs/sales_insights_summary.xlsx"

# -----------------------------------------------------------------------------
# Matplotlib Styling Helper (Executive Dark Theme)
# -----------------------------------------------------------------------------
def apply_executive_theme(fig, ax):
    """Applies a modern executive dark theme matching the Power BI palette."""
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#131C2E')
    ax.tick_params(colors='#94A3B8', labelsize=10)
    for spine in ax.spines.values():
        spine.set_color('#1E293B')
        spine.set_linewidth(1.2)
    ax.grid(True, linestyle='--', alpha=0.35, color='#334155')

def format_inr_millions(x, pos):
    """Format tick numbers as Indian Rupees in Millions."""
    if x >= 1e7:
        return f"₹{x*1e-7:.1f}Cr"
    elif x >= 1e6:
        return f"₹{x*1e-6:.1f}M"
    elif x >= 1e3:
        return f"₹{x*1e-3:.0f}K"
    return f"₹{x:.0f}"

# -----------------------------------------------------------------------------
# Analysis Functions
# -----------------------------------------------------------------------------
def generate_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Generates overall KPIs and saves to CSV."""
    logger.info("Generating KPIs...")
    kpis = pd.DataFrame([{
        "total_sales": df.sales_amount.sum(),
        "total_profit": df.profit.sum(),
        "total_orders": df.order_id.nunique(),
        "units_sold": df.quantity.sum(),
        "profit_margin": df.profit.sum() / df.sales_amount.sum() if df.sales_amount.sum() > 0 else 0,
        "avg_order_value": df.sales_amount.sum() / df.order_id.nunique() if df.order_id.nunique() > 0 else 0
    }])
    kpis.to_csv(TABLES / "kpi_summary.csv", index=False)
    return kpis

def analyze_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Generates monthly sales & profit trend and saves styled chart/table."""
    logger.info("Analyzing monthly trends...")
    monthly = df.groupby("year_month", as_index=False).agg(
        sales=("sales_amount", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique")
    ).sort_values("year_month").reset_index(drop=True)
    monthly.to_csv(TABLES / "monthly_sales.csv", index=False)

    fig, ax = plt.subplots(figsize=(12, 5.5))
    apply_executive_theme(fig, ax)

    x = np.arange(len(monthly))
    ax.plot(x, monthly.sales, color="#38BDF8", linewidth=2.8, marker="o", markersize=6, label="Total Sales", zorder=4)
    ax.fill_between(x, monthly.sales, color="#38BDF8", alpha=0.15, zorder=2)

    ax.plot(x, monthly.profit, color="#10B981", linewidth=2.4, marker="s", markersize=5, label="Total Profit", zorder=4)
    ax.fill_between(x, monthly.profit, color="#10B981", alpha=0.20, zorder=2)

    ax.set_title("Monthly Sales & Profit Performance Trend", fontsize=14, fontweight="bold", color="#F8FAFC", pad=15)
    ax.set_xlabel("Month", fontsize=11, fontweight="medium", color="#94A3B8", labelpad=10)
    ax.set_ylabel("Amount (INR)", fontsize=11, fontweight="medium", color="#94A3B8", labelpad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(monthly.year_month, rotation=45, ha="right", color="#CBD5E1")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_inr_millions))
    
    legend = ax.legend(loc="upper left", facecolor="#131C2E", edgecolor="#1E293B", labelcolor="#F8FAFC", fontsize=10)
    legend.get_frame().set_alpha(0.9)
    plt.tight_layout()
    plt.savefig(CHARTS / "monthly_sales_trend.png", dpi=200)
    plt.close()
    return monthly

def analyze_category(df: pd.DataFrame) -> pd.DataFrame:
    """Generates category performance and saves styled chart/table."""
    logger.info("Analyzing category performance...")
    category = df.groupby("category", as_index=False).agg(
        sales=("sales_amount", "sum"), 
        profit=("profit", "sum"), 
        units=("quantity", "sum")
    ).sort_values("sales", ascending=True).reset_index(drop=True)
    category["profit_margin"] = category.profit / category.sales
    category.to_csv(TABLES / "category_performance.csv", index=False)

    fig, ax = plt.subplots(figsize=(11, 5.5))
    apply_executive_theme(fig, ax)

    y_pos = np.arange(len(category))
    bars = ax.barh(y_pos, category.sales, color="#38BDF8", height=0.6, edgecolor="#0284C7", linewidth=1.2, zorder=3)

    # Annotate bars with Sales & Profit Margin
    for bar, (_, row) in zip(bars, category.iterrows()):
        width = bar.get_width()
        margin_pct = row["profit_margin"] * 100
        label_text = f" {format_inr_millions(width, None)}  |  Margin: {margin_pct:.1f}%"
        ax.text(width + (category.sales.max() * 0.015), bar.get_y() + bar.get_height()/2, 
                label_text, va="center", ha="left", color="#F8FAFC", fontsize=9.5, fontweight="semibold")

    ax.set_title("Sales & Profit Margin by Product Category", fontsize=14, fontweight="bold", color="#F8FAFC", pad=15)
    ax.set_xlabel("Total Sales (INR)", fontsize=11, fontweight="medium", color="#94A3B8", labelpad=10)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(category.category, color="#CBD5E1", fontsize=11)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_inr_millions))
    ax.set_xlim(0, category.sales.max() * 1.35)

    plt.tight_layout()
    plt.savefig(CHARTS / "category_sales.png", dpi=200)
    plt.close()
    return category

def analyze_product_margin_matrix(df: pd.DataFrame) -> None:
    """Generates Sales vs Profit Margin scatter matrix chart to flag margin leakage."""
    logger.info("Analyzing product margin matrix...")
    product = df.groupby("product", as_index=False).agg(
        sales=("sales_amount", "sum"),
        profit=("profit", "sum"),
        units=("quantity", "sum")
    )
    product["profit_margin"] = product.profit / product.sales

    fig, ax = plt.subplots(figsize=(11, 6))
    apply_executive_theme(fig, ax)

    # Color code by healthy vs at risk margin (threshold 18%)
    colors = ["#10B981" if m >= 0.18 else "#EF4444" for m in product["profit_margin"]]
    sizes = np.clip(product["units"] * 0.4, 60, 400)

    scatter = ax.scatter(product["sales"], product["profit_margin"] * 100, 
                         s=sizes, c=colors, alpha=0.85, edgecolors="#F8FAFC", linewidth=0.8, zorder=3)

    # Benchmark threshold line
    ax.axhline(18, color="#F59E0B", linestyle=":", linewidth=1.5, label="18% Target Margin Benchmark", zorder=2)

    # Annotate key outliers
    for _, row in product.iterrows():
        if row["profit_margin"] < 0.18 or row["sales"] > product["sales"].quantile(0.85):
            ax.annotate(row["product"], (row["sales"], row["profit_margin"] * 100),
                        xytext=(6, 5), textcoords="offset points", color="#E2E8F0", fontsize=8.5, fontweight="medium")

    ax.set_title("Product Portfolio: Revenue vs Profit Margin Matrix", fontsize=14, fontweight="bold", color="#F8FAFC", pad=15)
    ax.set_xlabel("Total Sales", fontsize=11, color="#94A3B8", labelpad=10)
    ax.set_ylabel("Profit Margin (%)", fontsize=11, color="#94A3B8", labelpad=10)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_inr_millions))
    ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    
    legend = ax.legend(loc="lower right", facecolor="#131C2E", edgecolor="#1E293B", labelcolor="#F8FAFC", fontsize=9.5)
    legend.get_frame().set_alpha(0.9)
    plt.tight_layout()
    plt.savefig(CHARTS / "product_margin_matrix.png", dpi=200)
    plt.close()

def analyze_dimensions(df: pd.DataFrame) -> dict:
    """Generates performance tables for region, product, and customer."""
    logger.info("Analyzing region, product, and customer dimensions...")
    # Region
    region = df.groupby("region", as_index=False).agg(
        sales=("sales_amount", "sum"), profit=("profit", "sum"),
        orders=("order_id", "nunique")).sort_values("sales", ascending=False)
    region["profit_margin"] = region.profit / region.sales
    region.to_csv(TABLES / "region_performance.csv", index=False)

    # Product
    product = df.groupby("product", as_index=False).agg(
        sales=("sales_amount", "sum"), profit=("profit", "sum"), units=("quantity", "sum")
    ).sort_values("sales", ascending=False)
    product["profit_margin"] = product.profit / product.sales
    product.to_csv(TABLES / "product_performance.csv", index=False)

    # Customer
    customer = df.groupby("customer_id", as_index=False).agg(
        sales=("sales_amount", "sum"), profit=("profit", "sum"),
        orders=("order_id", "nunique")).sort_values("sales", ascending=False)
    customer.to_csv(TABLES / "customer_performance.csv", index=False)

    return {"region": region, "product": product, "customer": customer}

def export_excel_workbook(kpis, monthly, category, dimensions) -> None:
    """Exports all summary tables into a clean multi-tab Excel workbook."""
    logger.info(f"Exporting Excel summary report to {EXCEL_OUTPUT}...")
    with pd.ExcelWriter(EXCEL_OUTPUT, engine="openpyxl") as writer:
        kpis.to_excel(writer, sheet_name="KPI_Overview", index=False)
        monthly.to_excel(writer, sheet_name="Monthly_Trends", index=False)
        category.to_excel(writer, sheet_name="Category_Performance", index=False)
        dimensions["region"].to_excel(writer, sheet_name="Region_Performance", index=False)
        dimensions["product"].to_excel(writer, sheet_name="Product_Performance", index=False)
        dimensions["customer"].head(100).to_excel(writer, sheet_name="Top100_Customers", index=False)
    logger.info("Excel workbook exported successfully.")

def main():
    """Main execution function."""
    try:
        logger.info(f"Loading cleaned data from {INPUT}")
        df = pd.read_csv(INPUT, parse_dates=["order_date"])
        
        # Ensure output directories exist
        CHARTS.mkdir(parents=True, exist_ok=True)
        TABLES.mkdir(parents=True, exist_ok=True)
        
        kpis = generate_kpis(df)
        monthly = analyze_monthly_trend(df)
        category = analyze_category(df)
        analyze_product_margin_matrix(df)
        dimensions = analyze_dimensions(df)
        export_excel_workbook(kpis, monthly, category, dimensions)
        
        logger.info("Sales analysis completed successfully with executive visual reports.")
    except FileNotFoundError:
        logger.error(f"Input file not found: {INPUT}. Please run clean_data.py first.")
    except Exception as e:
        logger.error(f"An error occurred during analysis: {e}")

if __name__ == "__main__":
    main()
