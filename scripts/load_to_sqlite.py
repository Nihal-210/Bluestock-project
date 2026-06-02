import pandas as pd
from sqlalchemy import create_engine
engine = create_engine(
    "sqlite:///bluestock_mf.db"
)

print("Database created successfully.")

fund_master = pd.read_csv(
    "data/processed/01_fund_master_cleaned.csv"
)

nav_history = pd.read_csv(
    "data/processed/02_nav_history_cleaned.csv"
)

aum = pd.read_csv(
    "data/processed/03_aum_by_fund_house_cleaned.csv"
)

sip = pd.read_csv(
    "data/processed/04_monthly_sip_inflows_cleaned.csv"
)

category = pd.read_csv(
    "data/processed/05_category_inflows_cleaned.csv"
)

folio = pd.read_csv(
    "data/processed/06_industry_folio_count_cleaned.csv"
)

performance = pd.read_csv(
    "data/processed/07_scheme_performance_cleaned.csv"
)

transactions = pd.read_csv(
    "data/processed/08_investor_transactions_cleaned.csv"
)

portfolio = pd.read_csv(
    "data/processed/09_portfolio_holdings_cleaned.csv"
)

benchmark = pd.read_csv(
    "data/processed/10_benchmark_indices_cleaned.csv"
)

fund_master.to_sql(
    "dim_fund",
    engine,
    if_exists="replace",
    index=False
)

nav_history.to_sql(
    "fact_nav",
    engine,
    if_exists="replace",
    index=False
)

aum.to_sql(
    "fact_aum",
    engine,
    if_exists="replace",
    index=False
)

sip.to_sql(
    "fact_sip_industry",
    engine,
    if_exists="replace",
    index=False
)

performance.to_sql(
    "fact_performance",
    engine,
    if_exists="replace",
    index=False
)

transactions.to_sql(
    "fact_transactions",
    engine,
    if_exists="replace",
    index=False
)

portfolio.to_sql(
    "fact_portfolio",
    engine,
    if_exists="replace",
    index=False
)

print("All datasets loaded successfully.")

source_counts = {
    "dim_fund": len(fund_master),
    "fact_nav": len(nav_history),
    "fact_aum": len(aum),
    "fact_sip_industry": len(sip),
    "fact_performance": len(performance),
    "fact_transactions": len(transactions),
    "fact_portfolio": len(portfolio)
}
db_counts = {}

for table in source_counts.keys():

    query = f"""
    SELECT COUNT(*) AS cnt
    FROM {table}
    """

    db_counts[table] = pd.read_sql(
        query,
        engine
    ).iloc[0]["cnt"]

comparison = pd.DataFrame({

    "Table": source_counts.keys(),

    "Source_Rows": source_counts.values(),

    "Database_Rows": [
        db_counts[t]
        for t in source_counts.keys()
    ]
})

comparison["Match"] = (
    comparison["Source_Rows"]
    ==
    comparison["Database_Rows"]
)

comparison
comparison.to_csv(
    "reports/sqlite_row_validation.csv",
    index=False
)