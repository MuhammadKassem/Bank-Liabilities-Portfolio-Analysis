import pandas as pd
from pathlib import Path
import sqlite3


print(
    "\n"
    "=======================================================================\n"
    "======= Bank Misr Liability Portfolio Analysis - Case Study ============\n"
    "=======================================================================\n"
)

print(
    "==========================================================================\n"
    " All data used in this case study was synthetically generated using Python\n"
    "==========================================================================\n"
)


print("================ Q_1 Database Path and Connection ==================")

BASE_DIR = Path(r"D:\BM_Liability_CaseStudy")
DB_PATH = BASE_DIR / "data" / "liability_analysis.db"

if not DB_PATH.exists():
    raise FileNotFoundError(f"Database not found: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)

try:
    df_accounts = pd.read_sql_query("SELECT * FROM accounts", conn)
    df_customers = pd.read_sql_query("SELECT * FROM customers", conn)
    df_products = pd.read_sql_query("SELECT * FROM products", conn)
    df_monthly_balances = pd.read_sql_query(
        "SELECT * FROM monthly_balances", conn
    )
finally:
    conn.close()

print("================= Database Connected ====================")


print("================ Q_2 Deposit Balance Analysis ==================")

product_balance = (
    df_monthly_balances.groupby("product_type")["closing_balance_egp"]
    .sum()
    .sort_values(ascending=False)
)

print("Deposit balance analysis:\n", product_balance)


print("================ Q_3 Total Interest by Product Type ==================")

product_interest = (
    df_monthly_balances.groupby("product_type")["interest_egp"]
    .sum()
    .sort_values(ascending=False)
)

print("Total interest by product type:\n", product_interest)


print("================ Q_4 Total Interest by Banking Product ==================")

bank_product_merge0 = df_monthly_balances.merge(
    df_accounts[["account_id", "product_id"]],
    on="account_id",
    how="inner"
)

bank_product_merge1 = bank_product_merge0.merge(
    df_products[["product_id", "product_name"]],
    on="product_id",
    how="inner"
)

bank_product_interest = (
    bank_product_merge1.groupby("product_name")["interest_egp"]
    .sum()
    .sort_values(ascending=False)
)

print("Banking product interest analysis:\n", bank_product_interest)


print("================ Q_5 Monthly Balance Growth ==================")

monthly_balance = (
    df_monthly_balances.groupby("month")["closing_balance_egp"]
    .sum()
    .sort_index()
)

monthly_analysis = pd.DataFrame({
    "total_balance": monthly_balance,
    "monthly_change": monthly_balance.diff(),
    "monthly_growth_pct": monthly_balance.pct_change() * 100
})

print(monthly_analysis.tail(6))


print("================ Q_6 Annual Portfolio Growth ==================")

dec_2024 = monthly_balance.loc["2024-12-01"]
dec_2025 = monthly_balance.loc["2025-12-01"]

yoy_growth = ((dec_2025 - dec_2024) / dec_2024) * 100

print(f"December 2024 Balance: {dec_2024:,.2f} EGP")
print(f"December 2025 Balance: {dec_2025:,.2f} EGP")
print(f"YoY Growth: {yoy_growth:.2f}%")


print("================ Q_7 Annual Product Portfolio Growth ==================")

monthly_product = (
    df_monthly_balances
    .merge(
        df_accounts[["account_id", "product_id"]],
        on="account_id",
        how="inner"
    )
    .merge(
        df_products[["product_id", "product_name"]],
        on="product_id",
        how="inner"
    )
)

product_balance_dec_24 = (
    monthly_product[monthly_product["month"] == "2024-12-01"]
    .groupby("product_name")["closing_balance_egp"]
    .sum()
)

product_balance_dec_25 = (
    monthly_product[monthly_product["month"] == "2025-12-01"]
    .groupby("product_name")["closing_balance_egp"]
    .sum()
)

product_balance_growth = product_balance_dec_25 - product_balance_dec_24
product_YoY_growth = (
    (product_balance_dec_25 - product_balance_dec_24)
    / product_balance_dec_24
) * 100

product_yoy_analysis = pd.DataFrame({
    "balance_dec_2024": product_balance_dec_24,
    "balance_dec_2025": product_balance_dec_25,
    "balance_change": product_balance_growth,
    "yoy_growth_pct": product_YoY_growth
})

print(product_yoy_analysis)


print("================ Q_8 Product Contribution to Portfolio Growth ==================")

product_yoy_analysis["growth_contribution_pct"] = (
    product_yoy_analysis["balance_change"]
    / product_yoy_analysis["balance_change"].sum()
) * 100

print(
    product_yoy_analysis.sort_values(
        "growth_contribution_pct",
        ascending=False
    )
)


print("================ Q_9 Portfolio Composition Analysis ==================")

product_composition = pd.DataFrame({
    "balance_dec_2025": product_balance_dec_25
})

product_composition["portfolio_share_pct"] = (
    product_composition["balance_dec_2025"]
    / product_composition["balance_dec_2025"].sum()
) * 100

print(product_composition)


print("================ Q_10 Customer Portfolio Analysis ==================")

customer_dec_25 = df_monthly_balances[
    df_monthly_balances["month"] == "2025-12-01"
]

customer_balance = (
    customer_dec_25.groupby("customer_id")["closing_balance_egp"]
    .sum()
)

top_customers = customer_balance.sort_values(ascending=False).head(10)

print(top_customers)


print("================ Q_11 Customer Concentration Analysis ==================")

total_portfolio = customer_balance.sum()
top_10_balance = top_customers.sum()

top_10_concentration_pct = (
    top_10_balance / total_portfolio
) * 100

print(f"Total Portfolio: {total_portfolio:,.2f} EGP")
print(f"Top 10 Balance: {top_10_balance:,.2f} EGP")
print(f"Top 10 Customers Concentration: {top_10_concentration_pct:.2f}%")


print("================ Q_12 Top 10 Customers by Product ==================")

customer_product_dec_25 = (
    customer_dec_25
    .merge(
        df_accounts[["account_id", "product_id"]],
        on="account_id",
        how="inner"
    )
    .merge(
        df_products[["product_id", "product_name"]],
        on="product_id",
        how="inner"
    )
)

customer_product_balance = (
    customer_product_dec_25
    .groupby(["product_name", "customer_id"])["closing_balance_egp"]
    .sum()
    .reset_index()
)

top_customers_by_product = (
    customer_product_balance
    .sort_values(
        ["product_name", "closing_balance_egp"],
        ascending=[True, False]
    )
    .groupby("product_name")
    .head(10)
)

print(top_customers_by_product)


print("================ Q_13 Customer Segmentation by Balance ==================")

customer_segmentation = customer_balance.reset_index()

customer_segmentation["balance_segment"] = pd.cut(
    customer_segmentation["closing_balance_egp"],
    bins=[0, 10000, 50000, float("inf")],
    labels=["Low", "Medium", "High"],
    right=False
)

segment_counts = customer_segmentation["balance_segment"].value_counts()

segment_pct = (
    customer_segmentation["balance_segment"]
    .value_counts(normalize=True)
    .mul(100)
)

print(segment_counts)
print(segment_pct)


print("================ Q_14 Product Mix by Customer Segment ==================")

customer_product_segment = (
    customer_product_dec_25
    .merge(
        customer_segmentation[["customer_id", "balance_segment"]],
        on="customer_id",
        how="left"
    )
)

segment_by_product = (
    customer_product_segment
    .groupby(["product_name", "balance_segment"])["customer_id"]
    .nunique()
    .reset_index(name="customer_count")
)

segment_pivot = segment_by_product.pivot(
    index="product_name",
    columns="balance_segment",
    values="customer_count"
).fillna(0)

print(segment_pivot)


print("================ Q_15 Portfolio Performance Analysis ==================")

portfolio_summary = {
    "total_portfolio_dec_2025": total_portfolio,
    "top_10_customers_balance": top_10_balance,
    "top_10_customers_concentration_pct": top_10_concentration_pct,
    "yoy_portfolio_growth_pct": yoy_growth
}

portfolio_summary_df = pd.DataFrame(
    list(portfolio_summary.items()),
    columns=["metric", "value"]
)

print(portfolio_summary_df)
