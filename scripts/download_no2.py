import requests
import pandas as pd
import os
import time

# ============================================================
# CONFIGURATION
# ============================================================

API_KEY = "api-key"

SENSOR_ID = 12235309

START_DATE = "2025-03-01T00:00:00Z"
END_DATE = "2025-11-30T23:59:59Z"

BASE_URL = f"https://api.openaq.org/v3/sensors/{SENSOR_ID}/hours"

# Save as a NEW file first
OUTPUT_FILE = "data/raw/air_quality/no2_hourly_mar_nov.csv"


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)


# ============================================================
# API HEADERS
# ============================================================

headers = {
    "X-API-Key": API_KEY
}


# ============================================================
# DOWNLOAD DATA
# ============================================================

all_records = []

page = 1
limit = 1000

while True:

    print(f"\nDownloading page {page}...")

    params = {
        "datetime_from": START_DATE,
        "datetime_to": END_DATE,
        "limit": limit,
        "page": page
    }

    response = requests.get(
        BASE_URL,
        headers=headers,
        params=params
    )

    print("Status:", response.status_code)

    if response.status_code != 200:
        print("ERROR:")
        print(response.text)
        break

    data = response.json()

    results = data.get("results", [])

    print("Records received:", len(results))

    if not results:
        break

    all_records.extend(results)

    print(
        "Records downloaded so far:",
        len(all_records)
    )

    if len(results) < limit:
        break

    page += 1

    time.sleep(0.2)


# ============================================================
# CHECK RESULTS
# ============================================================

print("\n========================================")
print("DOWNLOAD COMPLETE")
print("========================================")

print("Total records:", len(all_records))

if not all_records:
    print("No records were downloaded.")
    exit()


# ============================================================
# CONVERT TO DATAFRAME
# ============================================================

rows = []

for record in all_records:

    period = record.get("period", {})

    datetime_from = period.get(
        "datetimeFrom",
        {}
    )

    datetime_to = period.get(
        "datetimeTo",
        {}
    )

    parameter = record.get(
        "parameter",
        {}
    )

    rows.append({
        "sensor_id": SENSOR_ID,
        "parameter": parameter.get("name"),
        "value": record.get("value"),
        "unit": parameter.get("units"),
        "datetime_from_utc": datetime_from.get("utc"),
        "datetime_to_utc": datetime_to.get("utc"),
        "datetime_from_local": datetime_from.get("local"),
        "datetime_to_local": datetime_to.get("local"),
    })


df = pd.DataFrame(rows)


# ============================================================
# CONVERT TIMESTAMPS
# ============================================================

df["datetime_from_utc"] = pd.to_datetime(
    df["datetime_from_utc"],
    utc=True
)

df["datetime_to_utc"] = pd.to_datetime(
    df["datetime_to_utc"],
    utc=True
)

df["datetime_from_local"] = pd.to_datetime(
    df["datetime_from_local"]
)

df["datetime_to_local"] = pd.to_datetime(
    df["datetime_to_local"]
)


# ============================================================
# SORT
# ============================================================

df = df.sort_values(
    "datetime_from_utc"
).reset_index(drop=True)


# ============================================================
# REMOVE DUPLICATE HOURLY WINDOWS
# ============================================================

df = df.drop_duplicates(
    subset=[
        "datetime_from_utc",
        "datetime_to_utc"
    ]
).reset_index(drop=True)


# ============================================================
# SAVE
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n========================================")
print("FINAL DATASET SUMMARY")
print("========================================")

print("\nFirst 5 rows:")
print(df.head().to_string())

print("\nLast 5 rows:")
print(df.tail().to_string())

print("\nNumber of rows:", len(df))

print("\nDate range:")
print(
    df["datetime_from_utc"].min(),
    "to",
    df["datetime_to_utc"].max()
)

print("\nMissing values:")
print(df.isna().sum())

print("\nNO2 statistics:")
print(df["value"].describe())

print("\nNumber of values <= 0:")
print((df["value"] <= 0).sum())

print("\nOutput file:")
print(OUTPUT_FILE)