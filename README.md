# Mutual Fund Analytics — Day 1: Data Ingestion

## Project Structure

```
mutual_fund_project/
├── data/
│   ├── raw/            # Raw CSVs & JSONs fetched from mfapi.in
│   └── processed/      # Cleaned, enriched DataFrames
├── notebooks/          # Jupyter EDA notebooks
├── sql/                # SQL scripts
├── dashboard/          # Dashboard files (Plotly/Dash)
├── reports/            # Generated text/PDF reports
├── data_ingestion.py   # Main EDA & validation script
├── live_nav_fetch.py   # Live NAV fetcher (mfapi.in)
├── requirements.txt    # Python dependencies
└── setup.sh            # One-time project setup script
```

## Quickstart

```bash
# 1. Setup (installs deps + git init)
bash setup.sh

# 2. Fetch live NAV data
python live_nav_fetch.py

# 3. Run ingestion & EDA
python data_ingestion.py
```

## Data Sources

All data fetched live from **[mfapi.in](https://api.mfapi.in)** — a free, public Mutual Fund API for India.

| Endpoint | Description |
|---|---|
| `GET /mf/all` | Full fund master list (all AMFI scheme codes + names) |
| `GET /mf/{scheme_code}` | NAV history for a specific scheme |

## Schemes Tracked (Day 1)

| Scheme | AMFI Code |
|---|---|
| HDFC Top 100 Direct | 125497 |
| SBI Bluechip | 119551 |
| ICICI Bluechip | 120503 |
| Nippon Large Cap | 118632 |
| Axis Bluechip | 119092 |
| Kotak Bluechip | 120841 |

## Deliverables — Day 1

- [x] `data_ingestion.py` — EDA on all raw CSVs, fund master exploration, AMFI code validation
- [x] `live_nav_fetch.py` — Live NAV fetch for HDFC + 5 key schemes
- [x] `requirements.txt` — All Python dependencies
- [x] `setup.sh` — Folder structure init + git setup
- [x] `reports/data_quality_summary.txt` — Generated after running `data_ingestion.py`
