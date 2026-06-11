"""
Advanced Mutual Fund Recommender System
--------------------------------------
Features:
1. Risk-based filtering
2. AUM filtering
3. Composite scoring
4. Category diversification
5. Explainable recommendations
"""

import pandas as pd
import numpy as np
import os


def normalize(series):
    """Min-Max Normalization"""
    if series.max() == series.min():
        return pd.Series([1] * len(series), index=series.index)

    return (series - series.min()) / (series.max() - series.min())


def recommend_funds(risk_appetite, top_n=3):
    """
    Recommend top mutual funds based on:
    - Risk Appetite
    - Sharpe Ratio
    - CAGR
    - AUM
    - Expense Ratio
    """

    print(f"\nSearching best funds for '{risk_appetite}' investors...")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)

    master_path = os.path.join(
        base_dir,
        "data",
        "processed",
        "01_fund_master_cleaned.csv"
    )

    scorecard_path = os.path.join(
        base_dir,
        "reports",
        "fund_scorecard.csv"
    )

    if not os.path.exists(master_path):
        print("Fund Master file missing.")
        return

    if not os.path.exists(scorecard_path):
        print("Scorecard file missing.")
        return

    # ---------------------------------------------------
    # Load Data
    # ---------------------------------------------------
    fund_master = pd.read_csv(master_path)
    fund_scores = pd.read_csv(scorecard_path)

    # Standardize columns
    fund_master.columns = (
        fund_master.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    fund_scores.columns = (
        fund_scores.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # ---------------------------------------------------
    # Dynamic Columns
    # ---------------------------------------------------
    common_col = (
        "scheme_name"
        if "scheme_name" in fund_scores.columns
        else "amfi_code"
    )

    risk_col = next(
        (c for c in fund_master.columns if "risk" in c),
        None
    )

    sharpe_col = next(
        (c for c in fund_scores.columns if "sharpe" in c),
        None
    )

    cagr_col = next(
        (c for c in fund_scores.columns if "cagr" in c),
        None
    )

    expense_col = next(
        (c for c in fund_scores.columns if "expense" in c),
        None
    )

    category_col = next(
        (
            c for c in fund_master.columns
            if "category" in c
        ),
        None
    )

    aum_col = next(
        (
            c for c in fund_master.columns
            if "aum" in c
        ),
        None
    )

    # ---------------------------------------------------
    # Merge
    # ---------------------------------------------------
    merge_cols = [common_col]

    for col in [risk_col, category_col, aum_col]:
        if col:
            merge_cols.append(col)

    merged = pd.merge(
        fund_scores,
        fund_master[merge_cols],
        on=common_col,
        how="inner"
    )

    # ---------------------------------------------------
    # Risk Mapping
    # ---------------------------------------------------
    risk_appetite = risk_appetite.strip().title()

    risk_mapping = {
        "Low": [
            "Low",
            "Low To Moderate"
        ],
        "Moderate": [
            "Moderate",
            "Moderately High"
        ],
        "High": [
            "High",
            "Very High"
        ]
    }

    if risk_appetite not in risk_mapping:
        print("Choose Low / Moderate / High")
        return

    merged[risk_col] = (
        merged[risk_col]
        .astype(str)
        .str.strip()
        .str.title()
    )

    filtered = merged[
        merged[risk_col].isin(
            risk_mapping[risk_appetite]
        )
    ].copy()

    if filtered.empty:
        print("No matching funds found.")
        return

    # ---------------------------------------------------
    # AUM Filter
    # ---------------------------------------------------
    if aum_col:
        filtered[aum_col] = pd.to_numeric(
            filtered[aum_col],
            errors="coerce"
        )

        threshold = filtered[aum_col].quantile(0.25)

        filtered = filtered[
            filtered[aum_col] >= threshold
        ]

    # ---------------------------------------------------
    # Numeric Conversion
    # ---------------------------------------------------
    for col in [sharpe_col, cagr_col, expense_col]:
        if col:
            filtered.loc[:, col] = pd.to_numeric(
                filtered[col],
                errors="coerce"
)

    # ---------------------------------------------------
    # Composite Score
    # ---------------------------------------------------
    filtered["sharpe_score"] = normalize(
        filtered[sharpe_col]
    )

    filtered["cagr_score"] = normalize(
        filtered[cagr_col]
    )

    if aum_col:
        filtered["aum_score"] = normalize(
            filtered[aum_col]
        )
    else:
        filtered["aum_score"] = 0

    if expense_col:
        filtered["expense_score"] = 1 - normalize(
            filtered[expense_col]
        )
    else:
        filtered["expense_score"] = 0

    filtered["recommendation_score"] = (
        0.40 * filtered["sharpe_score"] +
        0.30 * filtered["cagr_score"] +
        0.20 * filtered["aum_score"] +
        0.10 * filtered["expense_score"]
    )

    # ---------------------------------------------------
    # Category Diversification
    # ---------------------------------------------------
    if category_col:
        filtered = (
            filtered
            .sort_values(
                "recommendation_score",
                ascending=False
            )
            .drop_duplicates(
                subset=category_col
            )
        )

    # ---------------------------------------------------
    # Top Funds
    # ---------------------------------------------------
    recommendations = (
        filtered
        .sort_values(
            "recommendation_score",
            ascending=False
        )
        .head(top_n)
        .copy()
    )

    # ---------------------------------------------------
    # Explainability
    # ---------------------------------------------------
    explanations = []

    for _, row in recommendations.iterrows():

        reasons = []

        if row["sharpe_score"] > 0.7:
            reasons.append(
                "Strong risk-adjusted returns"
            )

        if row["cagr_score"] > 0.7:
            reasons.append(
                "High historical CAGR"
            )

        if row["aum_score"] > 0.7:
            reasons.append(
                "Large AUM indicates investor trust"
            )

        if expense_col and row["expense_score"] > 0.7:
            reasons.append(
                "Low expense ratio"
            )

        explanations.append(
            " | ".join(reasons)
        )

    recommendations["why_recommended"] = explanations

    # ---------------------------------------------------
    # Display
    # ---------------------------------------------------
    display_cols = [
        common_col,
        risk_col,
        "recommendation_score",
        sharpe_col
    ]

    if cagr_col:
        display_cols.append(cagr_col)

    if aum_col:
        display_cols.append(aum_col)

    if expense_col:
        display_cols.append(expense_col)

    display_cols.append("why_recommended")

    print("\nTop Recommended Funds")
    print("-" * 120)

    print(
        recommendations[display_cols]
        .round(2)
        .to_string(index=False)
    )

    print("-" * 120)

    return recommendations


if __name__ == "__main__":

    print("=" * 60)
    print("Bluestock Advanced Mutual Fund Recommender")
    print("=" * 60)

    risk = input(
        "\nEnter Risk Appetite (Low/Moderate/High): "
    )

    recommend_funds(risk)