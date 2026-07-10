"""
live_nav_fetch.py
=================
Fetches live NAV history for 6 mutual fund schemes from the MFAPI
(https://api.mfapi.in) and saves each scheme's data as a CSV file
inside the  data/raw/  directory.

Run:
    python live_nav_fetch.py

Output files created (inside data/raw/):
    hdfc_nav.csv
    sbi_nav.csv
    icici_nav.csv
    nippon_nav.csv
    axis_nav.csv
    kotak_nav.csv
"""

import os
import time
import requests
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# 1.  Define the 6 scheme codes (AMFI codes)
# ─────────────────────────────────────────────────────────────────────────────

SCHEMES = {
    "hdfc"   : 125497,
    "sbi"    : 119551,
    "icici"  : 120503,
    "nippon" : 118632,
    "axis"   : 119092,
    "kotak"  : 120841,
}

BASE_URL  = "https://api.mfapi.in/mf/{code}"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "raw")


# ─────────────────────────────────────────────────────────────────────────────
# 2 & 3.  Call MFAPI and parse the JSON response
# ─────────────────────────────────────────────────────────────────────────────

def fetch_nav(scheme_name: str, amfi_code: int) -> dict | None:
    """
    Hit the MFAPI endpoint for one scheme.
    Returns the parsed JSON dict on success, or None on failure.
    """
    url = BASE_URL.format(code=amfi_code)
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; NAVFetcher/1.0)"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()          # raises on 4xx / 5xx
        data = response.json()
        return data
    except requests.exceptions.Timeout:
        print(f"  [ERROR] {scheme_name.upper()} ({amfi_code}) — request timed out.")
    except requests.exceptions.HTTPError as e:
        print(f"  [ERROR] {scheme_name.upper()} ({amfi_code}) — HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] {scheme_name.upper()} ({amfi_code}) — connection error: {e}")
    except ValueError:
        print(f"  [ERROR] {scheme_name.upper()} ({amfi_code}) — could not parse JSON.")
    return None


# ─────────────────────────────────────────────────────────────────────────────
# 4 & 5.  Extract NAV history and convert to DataFrame
# ─────────────────────────────────────────────────────────────────────────────

def build_dataframe(scheme_name: str, amfi_code: int, raw: dict) -> pd.DataFrame:
    """
    Extracts the NAV history list from the API response and returns a
    clean, sorted DataFrame with columns: amfi_code, scheme_name,
    fund_house, date, nav.
    """
    meta        = raw.get("meta", {})
    fund_house  = meta.get("fund_house", "Unknown")
    full_name   = meta.get("scheme_name", scheme_name)
    nav_records = raw.get("data", [])          # list of {"date": "DD-MM-YYYY", "nav": "123.45"}

    df = pd.DataFrame(nav_records)             # columns: date, nav

    # ── type conversions ────────────────────────────────────────────────────
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    df["nav"]  = pd.to_numeric(df["nav"], errors="coerce")

    # ── add metadata columns ─────────────────────────────────────────────────
    df.insert(0, "amfi_code",   amfi_code)
    df.insert(1, "scheme_name", full_name)
    df.insert(2, "fund_house",  fund_house)

    # ── sort oldest → newest ─────────────────────────────────────────────────
    df = df.sort_values("date").reset_index(drop=True)

    return df


# ─────────────────────────────────────────────────────────────────────────────
# 6.  Save each DataFrame as a CSV inside data/raw/
# ─────────────────────────────────────────────────────────────────────────────

def save_csv(df: pd.DataFrame, scheme_name: str, output_dir: str) -> str:
    """Saves the DataFrame to  <output_dir>/<scheme_name>_nav.csv  ."""
    filename = f"{scheme_name}_nav.csv"
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)
    return filepath


# ─────────────────────────────────────────────────────────────────────────────
# 7.  Main — orchestrate everything and print success / failure messages
# ─────────────────────────────────────────────────────────────────────────────

def main():
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("  Live NAV Fetch — MFAPI")
    print("=" * 60)
    print(f"  Output directory : {OUTPUT_DIR}")
    print(f"  Schemes to fetch : {len(SCHEMES)}\n")

    results = {"success": [], "failure": []}

    for scheme_name, amfi_code in SCHEMES.items():
        print(f"Fetching [{scheme_name.upper():8s}]  AMFI code: {amfi_code} ...", end="  ")

        # ── Step 2 & 3: call API + parse JSON ───────────────────────────────
        raw = fetch_nav(scheme_name, amfi_code)

        if raw is None:
            print("FAILED")
            results["failure"].append(scheme_name)
            continue

        # ── Step 4 & 5: extract NAV history + build DataFrame ───────────────
        df = build_dataframe(scheme_name, amfi_code, raw)

        if df.empty:
            print(f"FAILED  (empty data returned by API)")
            results["failure"].append(scheme_name)
            continue

        # ── Step 6: save CSV ─────────────────────────────────────────────────
        filepath = save_csv(df, scheme_name, OUTPUT_DIR)

        # ── Step 7: success message ──────────────────────────────────────────
        date_min = df["date"].min().strftime("%Y-%m-%d")
        date_max = df["date"].max().strftime("%Y-%m-%d")
        print(
            f"OK  |  {len(df):,} rows  |  "
            f"{date_min} → {date_max}  |  "
            f"saved → {os.path.basename(filepath)}"
        )
        results["success"].append(scheme_name)

        time.sleep(0.3)   # polite delay between requests

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"  Done.  {len(results['success'])} succeeded, {len(results['failure'])} failed.")
    if results["success"]:
        print(f"  ✓ Saved : {', '.join(results['success'])}")
    if results["failure"]:
        print(f"  ✗ Failed: {', '.join(results['failure'])}")
    print("=" * 60)


if __name__ == "__main__":
    main()
