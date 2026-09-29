import requests
import pandas as pd
import os


# ============================================================
# CONFIGURATION
# ============================================================

LATITUDE = 28.531346
LONGITUDE = 77.190156

START_DATE = "2025-03-01"
END_DATE = "2025-08-31"

OUTPUT_FILE = "data/raw/weather/weather_hourly.csv"


# ============================================================
# API URL
# ============================================================

URL = "https://archive-api.open-meteo.com/v1/archive"


# ============================================================
# WEATHER VARIABLES
# ============================================================

HOURLY_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "wind_direction_10m",
    "precipitation",
    "surface_pressure",
    "boundary_layer_height"
]


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)


# ============================================================
# API PARAMETERS
# ============================================================

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "start_date": START_DATE,
    "end_date": END_DATE,
    "hourly": ",".join(HOURLY_VARIABLES),
    "timezone": "Asia/Kolkata",
    "temperature_unit": "celsius",
    "wind_speed_unit": "ms",
    "precipitation_unit": "mm",
    "timeformat": "iso8601"
}


# ============================================================
# REQUEST DATA
# ============================================================

print("Downloading historical weather data...")

response = requests.get(
    URL,
    params=params
)

print("Status code:", response.status_code)

if response.status_code != 200:
    print("ERROR:")
    print(response.text)
    exit()


# ============================================================
# PARSE RESPONSE
# ============================================================

data = response.json()

print("\nWeather location returned by API:")
print("Latitude:", data.get("latitude"))
print("Longitude:", data.get("longitude"))
print("Elevation:", data.get("elevation"))
print("Timezone:", data.get("timezone"))


# ============================================================
# CONVERT TO DATAFRAME
# ============================================================

hourly = data.get("hourly")

if hourly is None:
    print("ERROR: No hourly data returned.")
    exit()


df = pd.DataFrame(hourly)


# ============================================================
# CONVERT TIMESTAMP
# ============================================================

df["time"] = pd.to_datetime(df["time"])


# Rename timestamp column

df = df.rename(
    columns={
        "time": "datetime_local"
    }
)


# ============================================================
# SORT
# ============================================================

df = df.sort_values(
    "datetime_local"
).reset_index(drop=True)


# ============================================================
# SAVE RAW WEATHER DATA
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print("\n========================================")
print("WEATHER DOWNLOAD COMPLETE")
print("========================================")

print("\nNumber of rows:", len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head().to_string())

print("\nLast 5 rows:")
print(df.tail().to_string())

print("\nMissing values:")
print(df.isna().sum())

print("\nDate range:")
print(df["datetime_local"].min())
print("to")
print(df["datetime_local"].max())

print("\nSaved to:")
print(OUTPUT_FILE)