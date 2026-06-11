# 📈 Mutual Fund Analytics Platform

An end-to-end Mutual Fund Analytics and Business Intelligence platform built using Python, SQL, and Power BI.

The project analyzes mutual fund performance, investor behavior, SIP trends, AUM growth, and portfolio diversification using real-world mutual fund datasets.

---

## 🎯 Project Overview

This project transforms raw mutual fund data into actionable business insights through:

- Data Cleaning & ETL Pipelines
- Financial Performance Analysis
- Investor Analytics
- Risk & Return Evaluation
- Interactive Dashboards
- Automated Reporting

The platform enables investors, analysts, and fund houses to make data-driven decisions.

---

## 📊 Key Features

### Industry Analytics
- AUM Growth Analysis
- SIP Inflow Tracking
- Folio Growth Trends
- Category-wise Inflow Analysis

### Fund Performance Analytics
- CAGR Calculation
- Alpha & Beta Analysis
- Sharpe Ratio
- Sortino Ratio
- Maximum Drawdown

### Investor Analytics
- Age Group Analysis
- Gender Distribution
- State-wise Participation
- T30 vs B30 Comparison

### Portfolio Analytics
- Sector Allocation
- Correlation Analysis
- Diversification Insights

---

## 🏗️ System Architecture

```text
Raw Data Sources
        │
        ▼
   ETL Pipeline
        │
        ▼
 Data Warehouse
        │
        ▼
 Analytics Engine
        │
        ▼
 Dashboards & Reports
```

---

## 📂 Datasets Used

| Dataset | Description |
|----------|------------|
| Fund Master | Scheme metadata |
| NAV History | Historical NAV data |
| AUM Data | Fund house AUM |
| SIP Inflows | Monthly SIP statistics |
| Category Inflows | Category-wise investments |
| Folio Count | Investor participation |
| Scheme Performance | Risk-return metrics |
| Investor Transactions | Demographic analysis |
| Portfolio Holdings | Sector allocation |
| Benchmark Indices | Market benchmark data |

---

## 📈 Analytics Performed

### Exploratory Data Analysis
- NAV Trend Analysis
- AUM Growth Analysis
- SIP Trend Analysis
- Investor Demographics

### Performance Analysis
- Daily Returns
- CAGR
- Alpha
- Beta
- Sharpe Ratio
- Sortino Ratio

### Risk Analysis
- Maximum Drawdown
- Correlation Matrix
- Portfolio Diversification

---

## 📊 Dashboard Overview

The Power BI dashboard contains:

### Industry Overview
- Total AUM
- SIP Inflows
- Folio Growth

### Fund Performance
- NAV Trends
- Alpha & Beta Comparison
- Risk-Return Analysis

### Investor Analytics
- Age Distribution
- Gender Split
- Geographic Analysis

### Portfolio Analytics
- Sector Allocation
- Correlation Heatmap

---

## 📁 Repository Structure
```text
📦bluestock_mf_capstone
 ┣ 📂data
 ┃ ┣ 📂raw                         # Immutable source assets & live API extractions
 ┃ ┃ ┣ 📜01_fund_master.csv
 ┃ ┃ ┣ 📜02_nav_history.csv
 ┃ ┃ ┣ 📜... (Other raw datasets)
 ┃ ┃ ┗ 📜125497_HDFC_TOP_100_live.csv
 ┃ ┣ 📂processed                   # Standardized, cleaned, and filled datasets
 ┃ ┃ ┣ 📜clean_nav_history.csv
 ┃ ┃ ┗ 📜clean_transaction.csv
 ┃ ┣ 📂db                          # SQLite Star Schema warehouse engine
 ┃ ┃ ┗ 📜bluestock_mf.db
 ┣ 📂notebooks                     # Sequential pipeline processing environments
 ┃ ┣ 📜01_data_ingestion.ipynb
 ┃ ┣ 📜02_data_cleaning.ipynb
 ┃ ┣ 📜03_EDA_Analysis.ipynb
 ┃ ┣ 📜04_Performance_Analytics.ipynb
 ┃ ┣ 📜05_Advanced_Analytics.ipynb
 ┣ 📂scripts                       # Production automation & execution apps
 ┃ ┣ 📜live_nav_fetch.py
 ┃ ┣ 📜recommender.py
 ┣ 📂sql                           # Structural warehouse creation logic
 ┃ ┣ 📜schema.sql
 ┃ ┣ 📜queries.sql
 ┣ 📂dashboard                     # Front-end business intelligence binaries
 ┃ ┣ 📜bluestock_mf_dashboard.pbix
 ┣ 📂reports                       # Exported analytical metrics, visuals & PDFs
 ┃ ┣ 📜fund_scorecard.csv
 ┃ ┣ 📜var_cvar_reports.csv
 ┃ ┣ 📜sector_hhi_chart.png
 ┃ ┣ 📜Dashboard - Page1.png
 ┃ ┣ 📜Final_Report.pdf
 ┃ ┗ 📜README.md
 ┃ ┗ 📜Bluestock_MF_Presentation.pptx # Fintech investment presentation deck
 ┣ 📜requirements.txt              # Standard system dependencies
 ┣ 📜data_dictionary.md            # Warehouse data model catalog
 ┣ 📜run_pipeline.py               # Absolute path automation master controller
 ┗ 📜 README.md
```
---

## 🛠️ Tech Stack

### Programming
- Python

### Libraries
- Pandas
- NumPy
- Matplotlib
- Seaborn

### Database
- SQLite

### Visualization
- Power BI

---

## 🚀 Getting Started

Clone the repository:

```bash
git clone <repository-url>
cd mutual-fund-analytics
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the pipeline:

```bash
python run_pipeline.py
```

---

## 📌 Key Insights

- SIP inflows crossed ₹31,000 Cr
- Folio count nearly doubled
- Young investors dominate participation
- SBI MF leads industry AUM
- Positive Alpha observed across multiple schemes
- Diversification opportunities identified through correlation analysis

---

## 🔮 Future Enhancements

- Live NAV Integration
- AI-based Fund Recommendation Engine
- Portfolio Optimization
- Predictive Analytics
- Automated Reporting

---

## 👨‍💻 Author

**Nihal Chadha**

B.Tech Electronics & Communication Engineering  
Delhi Technological University

---
