import requests
import pandas as pd
from io import StringIO
from pathlib import Path
from datetime import datetime, timedelta
import time


# ============================================================
# SETTINGS
# ============================================================

MAP_KEY = "api-key"

SOURCE = "VIIRS_NOAA20_SP"

# FIRMS area format:
# west, south, east, north
AREA = "74,27,79,31"

START_DATE = datetime(2025, 3, 1)
END_DATE = datetime(2025, 11, 30)

# FIRMS area API allows up to 5 days per request.
CHUNK_DAYS = 5


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = PROJECT_DIR / "data" / "raw" / "fires"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "firms_noaa20_2025_mar_nov.csv"


# ============================================================
# DOWNLOAD FUNCTION
# ============================================================

def download_chunk(start_date, days):

    date_string = start_date.strftime("%Y-%m-%d")

    url = (
        f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
        f"{MAP_KEY}/{SOURCE}/{AREA}/{days}/{date_string}"
    )

    print()
    print("=" * 60)
    print(f"Downloading: {date_string}")
    print(f"Days: {days}")
    print(f"Source: {SOURCE}")
    print("=" * 60)

    response = requests.get(url, timeout=120)

    print("Status code:", response.status_code)

    if response.status_code != 200:
        print("ERROR:")
        print(response.text)
        return None

    df = pd.read_csv(StringIO(response.text))

    print("Rows downloaded:", len(df))

    return df


# ============================================================
# MAIN DOWNLOAD
# ============================================================

all_data = []

current_date = START_DATE

while current_date <= END_DATE:

    remaining_days = (END_DATE - current_date).days + 1

    days = min(CHUNK_DAYS, remaining_days)

    df = download_chunk(current_date, days)

    if df is not None and not df.empty:
        all_data.append(df)

    current_date += timedelta(days=days)

    # Small pause to avoid hammering the API
    time.sleep(1)


# ============================================================
# CHECK RESULTS
# ============================================================

if not all_data:

    print("\nNo data was downloaded.")
    raise SystemExit


print("\nCombining downloaded chunks...")

final_df = pd.concat(all_data, ignore_index=True)

print("Rows before duplicate removal:", len(final_df))


# ============================================================
# REMOVE DUPLICATES
# ============================================================

# A fire detection is identified using its important
# spatial/time/satellite attributes.

duplicate_columns = [
    "latitude",
    "longitude",
    "acq_date",
    "acq_time",
    "satellite"
]

final_df = final_df.drop_duplicates(
    subset=duplicate_columns
).reset_index(drop=True)


print("Rows after duplicate removal:", len(final_df))


# ============================================================
# SORT
# ============================================================

final_df = final_df.sort_values(
    by=["acq_date", "acq_time", "latitude", "longitude"]
).reset_index(drop=True)


# ============================================================
# SAVE RAW DATA
# ============================================================

final_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 60)
print("DOWNLOAD COMPLETE")
print("=" * 60)

print("Total rows:", len(final_df))

print(
    "Date range:",
    final_df["acq_date"].min(),
    "to",
    final_df["acq_date"].max()
)

print(
    "Latitude range:",
    final_df["latitude"].min(),
    "to",
    final_df["latitude"].max()
)

print(
    "Longitude range:",
    final_df["longitude"].min(),
    "to",
    final_df["longitude"].max()
)

print(
    "Total FRP:",
    round(final_df["frp"].sum(), 2)
)

print(
    "Mean FRP:",
    round(final_df["frp"].mean(), 2)
)

print()
print("Saved to:")
print(OUTPUT_FILE)