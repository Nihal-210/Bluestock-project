"""
Master Execution Script
-----------------------
Orchestrates the BlueStock Mutual Fund Analytics pipeline.
"""

import os
import sys
import subprocess


def run_python_script(script_path):
    """Execute a Python script."""

    print(f"\nExecuting: {script_path}")
    print("-" * 60)

    try:
        subprocess.run(
            [sys.executable, script_path],
            check=True
        )

        print("\n" + "-" * 60)
        print(f"SUCCESS: {os.path.basename(script_path)} completed.")
        print("-" * 60)

    except subprocess.CalledProcessError as e:
        print("\n" + "-" * 60)
        print(f"ERROR while executing {script_path}")
        print(f"Return Code: {e.returncode}")
        print("-" * 60)

    except FileNotFoundError:
        print(f"Python executable not found: {sys.executable}")

    except Exception as e:
        print(f"Unexpected Error: {e}")


def main():

    print("=" * 60)
    print("BlueStock Mutual Fund Analytics Pipeline")
    print("=" * 60)

    # Directory containing this file
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to scripts/live_nav_fetch.py
    live_nav_script = os.path.join(
        base_dir,
        "scripts",
        "live_nav_fetch.py"
    )

    if os.path.exists(live_nav_script):
        run_python_script(live_nav_script)
    else:
        print(f"\nWARNING: Script not found")
        print(live_nav_script)

    print("\n" + "=" * 60)
    print("JUPYTER NOTEBOOK EXECUTION ORDER")
    print("=" * 60)

    notebooks = [
        "01_data_ingestion.ipynb",
        "02_data_cleaning.ipynb",
        "03_EDA_Analysis.ipynb",
        "04_Performance_Analytics.ipynb",
        "05_Advanced_Analytics.ipynb"
    ]

    for idx, notebook in enumerate(notebooks, start=1):
        print(f"{idx}. {notebook}")

    print("\n" + "=" * 60)
    print("RECOMMENDER SYSTEM")
    print("=" * 60)
    print("Run using:")
    print("python scripts/recommender.py")
    print("=" * 60)


if __name__ == "__main__":
    main()