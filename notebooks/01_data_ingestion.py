"""
data_ingestion.py
=================
Day 1 — Bluestock MF Capstone
Loads all 10 provided CSV datasets, prints diagnostics (.shape, .dtypes, .head()),
notes anomalies, and saves a structured ingestion summary.
"""

import os
import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# ─────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_DIR = os.path.join(BASE_DIR, "data", "raw","downloaded files")
PROC_DIR = os.path.join(BASE_DIR, "data", "processed","downloaded files")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROC_DIR, exist_ok=True)


# ─────────────────────────────────────────────
# Dataset registry
# ─────────────────────────────────────────────
DATASETS = {
    "fund_master"          : "01_fund_master.csv",
    "nav_history"          : "02_nav_history.csv",
    "aum_by_fund_house"    : "03_aum_by_fund_house.csv",
    "monthly_sip_inflow"   : "04_monthly_sip_inflows.csv",
    "category_inflow"      : "05_category_inflows.csv",
    "industry_folio_count" : "06_industry_folio_count.csv",
    "scheme_performance"   : "07_scheme_performance.csv",
    "investor_transactions": "08_investor_transactions.csv",
    "portfolio_holdings"   : "09_portfolio_holdings.csv",
    "benchmark_index"      : "10_benchmark_indices.csv",
}

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
SEPARATOR = "=" * 70

def section(title: str) -> None:
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


def load_dataset(name: str, filename: str) -> pd.DataFrame | None:
    """Load a single CSV and return a DataFrame, or None on failure."""
    path = os.path.join(RAW_DIR, filename)
    if not os.path.exists(path):
        print(f"  [MISSING] {path} — file not found, skipping.")
        return None
    df = pd.read_csv(path, low_memory=False)
    return df


def inspect_dataset(name: str, df: pd.DataFrame) -> dict:
    """
    Print shape, dtypes, head(3), missing-value summary, and basic
    anomaly flags.  Returns a summary dict for the final report.
    """
    section(f"Dataset: {name}  ({df.shape[0]:,} rows × {df.shape[1]} cols)")

    # --- Shape ---
    print(f"\n  Shape   : {df.shape}")

    # --- dtypes ---
    print("\n  dtypes:")
    for col, dtype in df.dtypes.items():
        print(f"    {col:<40} {str(dtype)}")

    # --- Head ---
    print("\n  head(3):")
    print(df.head(3).to_string(index=False))

    # --- Missing values ---
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if missing.empty:
        print("\n  Missing values  : None")
    else:
        print("\n  Missing values (non-zero):")
        for col, cnt in missing.items():
            pct = cnt / len(df) * 100
            print(f"    {col:<40} {cnt:>6} ({pct:.1f}%)")

    # --- Duplicate rows ---
    dup_count = df.duplicated().sum()
    print(f"\n  Duplicate rows  : {dup_count}")

    # --- Basic anomaly flags ---
    anomalies = []
    for col in df.select_dtypes(include=[np.number]).columns:
        if (df[col] < 0).any():
            neg = (df[col] < 0).sum()
            anomalies.append(f"  ⚠  Negative values in '{col}': {neg} rows")
    if anomalies:
        print("\n  Anomaly flags:")
        for a in anomalies:
            print(a)
    else:
        print("  Anomaly flags   : None detected")

    return {
        "name"        : name,
        "rows"        : df.shape[0],
        "cols"        : df.shape[1],
        "missing_cols": missing.to_dict(),
        "duplicates"  : int(dup_count),
        "anomalies"   : anomalies,
    }


def explore_fund_master(df: pd.DataFrame) -> None:
    """Print unique values for key categorical columns in fund_master."""
    section("Fund Master — Categorical Exploration")
    for col in ["fund_house", "category", "sub_category", "risk_grade"]:
        if col in df.columns:
            vals = df[col].dropna().unique()
            print(f"\n  {col} ({len(vals)} unique):")
            for v in sorted(vals):
                print(f"    • {v}")


def validate_amfi_codes(fund_master: pd.DataFrame, nav_history: pd.DataFrame) -> None:
    """Confirm every AMFI code in fund_master exists in nav_history."""
    section("AMFI Code Validation")

    fm_col  = next((c for c in fund_master.columns  if "amfi" in c.lower() or "scheme_code" in c.lower()), None)
    nav_col = next((c for c in nav_history.columns  if "amfi" in c.lower() or "scheme_code" in c.lower()), None)

    if fm_col is None or nav_col is None:
        print(f"  [SKIP] Could not auto-detect AMFI code columns.")
        print(f"         fund_master cols : {list(fund_master.columns)}")
        print(f"         nav_history cols : {list(nav_history.columns)}")
        return

    fm_codes  = set(fund_master[fm_col].dropna().astype(str))
    nav_codes = set(nav_history[nav_col].dropna().astype(str))

    missing_in_nav = fm_codes - nav_codes
    extra_in_nav   = nav_codes - fm_codes

    print(f"\n  fund_master  AMFI codes : {len(fm_codes):,}")
    print(f"  nav_history  AMFI codes : {len(nav_codes):,}")
    print(f"  Codes in FM but NOT nav : {len(missing_in_nav)}")
    print(f"  Extra codes only in nav : {len(extra_in_nav)}")

    if missing_in_nav:
        print("\n  ⚠  Missing from nav_history (first 10):")
        for c in sorted(missing_in_nav)[:10]:
            print(f"    {c}")
    else:
        print("\n  ✓  All fund_master AMFI codes are present in nav_history.")


def save_ingestion_summary(summaries: list[dict]) -> None:
    """Write a JSON + Markdown ingestion summary to data/processed/."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # JSON
    json_path = os.path.join(PROC_DIR, "ingestion_summary.json")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "generated_at": ts,
                "datasets": summaries
            },
            f,
            indent=2
        )

    print(f"\n  Ingestion summary (JSON) saved → {json_path}")

    # Markdown
    md_lines = [
        "# Data Ingestion Summary",
        f"\n_Generated: {ts}_\n",
        "| Dataset | Rows | Cols | Missing Cols | Duplicates | Anomalies |",
        "|---------|------|------|-------------|------------|-----------|",
    ]

    for s in summaries:
        miss = len(s["missing_cols"])
        anom = len(s["anomalies"])

        md_lines.append(
            f"| {s['name']} | {s['rows']:,} | {s['cols']} "
            f"| {miss} | {s['duplicates']} | {anom} |"
        )

    md_path = os.path.join(PROC_DIR, "ingestion_summary.md")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"  Ingestion summary (MD) saved → {md_path}")

# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
def main() -> None:
    print(SEPARATOR)
    print("  Bluestock MF Capstone — Day 1: Data Ingestion")
    print(f"  Run timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(SEPARATOR)

    dataframes: dict[str, pd.DataFrame] = {}
    summaries:  list[dict]              = []

    for name, filename in DATASETS.items():
        df = load_dataset(name, filename)
        if df is None:
            continue
        summary = inspect_dataset(name, df)
        summaries.append(summary)
        dataframes[name] = df

    # ── Fund Master exploration ──────────────────────────────────────
    if "fund_master" in dataframes:
        explore_fund_master(dataframes["fund_master"])

    # ── AMFI code validation ─────────────────────────────────────────
    if "fund_master" in dataframes and "nav_history" in dataframes:
        validate_amfi_codes(dataframes["fund_master"], dataframes["nav_history"])

    # ── Save summary ─────────────────────────────────────────────────
    section("Saving Ingestion Summaries")
    save_ingestion_summary(summaries)

    section("Day 1 — Data Ingestion Complete ✓")
    print(f"  Datasets loaded : {len(dataframes)}/{len(DATASETS)}")
    total_rows = sum(s["rows"] for s in summaries)
    print(f"  Total rows read : {total_rows:,}")


if __name__ == "__main__":
    main()