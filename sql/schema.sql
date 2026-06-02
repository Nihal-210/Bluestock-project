CREATE TABLE dim_fund (

    amfi_code INTEGER PRIMARY KEY,

    fund_house TEXT,

    category TEXT,

    expense_ratio REAL
);

CREATE TABLE dim_date (

    date_id INTEGER PRIMARY KEY,

    date DATE,

    year INTEGER,

    month INTEGER,

    quarter INTEGER,

    is_weekday INTEGER
);

CREATE TABLE fact_nav (

    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,

    amfi_code INTEGER,

    date DATE,

    nav REAL,

    FOREIGN KEY(amfi_code)
    REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_transactions (

    tx_id INTEGER PRIMARY KEY AUTOINCREMENT,

    investor_id TEXT,

    amfi_code INTEGER,

    transaction_date DATE,

    amount_inr REAL,

    transaction_type TEXT,

    state TEXT,

    FOREIGN KEY(amfi_code)
    REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_performance (

    perf_id INTEGER PRIMARY KEY AUTOINCREMENT,

    amfi_code INTEGER,

    return_1yr_pct REAL,

    return_3yr_pct REAL,

    return_5yr_pct REAL,

    expense_ratio_pct REAL,

    FOREIGN KEY(amfi_code)
    REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_aum (

    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,

    fund_house TEXT,

    date DATE,

    aum_crore REAL
);