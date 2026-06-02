"""
live_nav_fetch.py
-----------------
Fetches live NAV data from mfapi.in for:
  - HDFC Top 100 Direct (125497)
  - SBI Bluechip (119551)
  - ICICI Bluechip (120503)
  - Nippon Large Cap (118632)
  - Axis Bluechip (119092)
  - Kotak Bluechip (120841)

Saves each scheme's NAV history as a raw CSV in data/raw/.
Also saves a combined CSV with all schemes.
"""

import requests
import pandas as pd
import json
import os
import time
from datetime import datetime

BASE_URL = "https://api.mfapi.in/mf"
RAW_DIR = os.path.join(os.path.dirname(__file__), "data", "raw","data fetched")
os.makedirs(RAW_DIR, exist_ok=True)

SCHEMES = {
    125497: "HDFC_Top100_Direct",
    119551: "SBI_Bluechip",
    120503: "ICICI_Bluechip",
    118632: "Nippon_LargeCap",
    119092: "Axis_Bluechip",
    120841: "Kotak_Bluechip",
}


def fetch_nav(scheme_code: int) -> dict:
    """Fetch NAV data for a single scheme code. Returns parsed JSON."""
    url = f"{BASE_URL}/{scheme_code}"
    print(f"  Fetching: {url}")
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.json()


def parse_nav_response(raw: dict, scheme_code: int, scheme_name: str) -> pd.DataFrame:
    """
    Parse mfapi.in JSON response into a clean DataFrame.

    Response structure:
        {
          "meta": { "fund_house": ..., "scheme_type": ..., "scheme_category": ...,
                    "scheme_code": ..., "scheme_name": ... },
          "data": [ {"date": "DD-MM-YYYY", "nav": "123.456"}, ... ],
          "status": "SUCCESS"
        }
    """
    meta = raw.get("meta", {})
    nav_records = raw.get("data", [])

    df = pd.DataFrame(nav_records)
    df.rename(columns={"date": "nav_date", "nav": "nav_value"}, inplace=True)

    # Parse date and convert NAV to float
    df["nav_date"] = pd.to_datetime(df["nav_date"], format="%d-%m-%Y")
    df["nav_value"] = pd.to_numeric(df["nav_value"], errors="coerce")

    # Attach metadata columns
    df["scheme_code"] = scheme_code
    df["scheme_name"] = scheme_name
    df["fund_house"] = meta.get("fund_house", "")
    df["scheme_type"] = meta.get("scheme_type", "")
    df["scheme_category"] = meta.get("scheme_category", "")

    df.sort_values("nav_date", inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def save_raw_csv(df: pd.DataFrame, scheme_name: str) -> str:
    """Save a scheme's NAV DataFrame as CSV in data/raw/."""
    filename = f"nav_{scheme_name}.csv"
    path = os.path.join(RAW_DIR, filename)
    df.to_csv(path, index=False)
    print(f"    Saved: {path}  ({len(df)} rows)")
    return path


def print_summary(df: pd.DataFrame, scheme_name: str):
    """Print basic summary stats for a scheme."""
    print(f"\n  --- {scheme_name} ---")
    print(f"  Shape       : {df.shape}")
    print(f"  Date range  : {df['nav_date'].min().date()} → {df['nav_date'].max().date()}")
    print(f"  Latest NAV  : {df['nav_value'].iloc[-1]:.4f}")
    print(f"  Min NAV     : {df['nav_value'].min():.4f}")
    print(f"  Max NAV     : {df['nav_value'].max():.4f}")
    print(f"  Null values : {df['nav_value'].isna().sum()}")


def main():
    print("=" * 60)
    print("  LIVE NAV FETCH  |  mfapi.in")
    print(f"  Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    all_dfs = []

    for code, name in SCHEMES.items():
        print(f"\n[{code}] {name}")
        try:
            raw = fetch_nav(code)

            # Save raw JSON response as well
            json_path = os.path.join(RAW_DIR, f"raw_{name}.json")
            with open(json_path, "w") as f:
                json.dump(raw, f, indent=2)
            print(f"    Raw JSON saved: {json_path}")

            df = parse_nav_response(raw, code, name)
            print_summary(df, name)
            save_raw_csv(df, name)
            all_dfs.append(df)

        except requests.exceptions.RequestException as e:
            print(f"    ERROR fetching {code}: {e}")

        time.sleep(0.5)  # polite delay between requests

    # Combined CSV
    if all_dfs:
        combined = pd.concat(all_dfs, ignore_index=True)
        combined_path = os.path.join(RAW_DIR, "nav_all_schemes_combined.csv")
        combined.to_csv(combined_path, index=False)
        print(f"\n[Combined] Saved {len(combined)} total rows → {combined_path}")

    print("\n" + "=" * 60)
    print("  NAV fetch complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
