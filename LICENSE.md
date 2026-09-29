MIT License

Copyright (c) 2026 khushishahs02 and contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

# Time-Lagged Modeling and Short-Term Forecasting of Urban Air Pollution

## Data Provenance, Licensing, and Authenticity

This project investigates the temporal relationship between urban air pollution, meteorological conditions, and regional satellite-detected fire activity, with a focus on short-term PM2.5 forecasting.
The project uses three independent authoritative/open data sources:
* **OpenAQ** — hourly air-quality observations
* **Open-Meteo** — historical hourly meteorological data
* **NASA FIRMS** — satellite-detected active-fire/thermal-anomaly observations from VIIRS NOAA-20

No traffic, financial, synthetic, or Kaggle-derived dataset is used in the final project.

### 1. Dataset Overview

| Dataset | Source | Product / API | Period | Role |
| :--- | :--- | :--- | :--- | :--- |
| PM2.5 | OpenAQ | Sensor hourly aggregation API | Mar–Nov 2025 | Primary pollution target |
| NO2 | OpenAQ | Sensor hourly aggregation API | Mar–Nov 2025 | Secondary pollutant / predictor |
| Weather | Open-Meteo | Historical Weather API | Mar–Nov 2025 | Meteorological predictors |
| Fire activity | NASA FIRMS | VIIRS NOAA-20 Standard Processing | Mar–Nov 2025 | Regional fire predictors |

The analytical study period is: **1 March 2025 – 30 November 2025**
The raw datasets are retained separately. They are not modified to manufacture observations or replace source measurements.

### 2. Air Quality Data — OpenAQ

**Source**
The PM2.5 and NO2 datasets were retrieved programmatically from the official OpenAQ API v3.
* Official source: [https://openaq.org/](https://openaq.org/)
* API documentation: [https://docs.openaq.org/](https://docs.openaq.org/)

OpenAQ API documentation identifies the platform as an open-access source of global air-quality data and states that it aggregates measurements from government agencies and other public sources.
The project uses the OpenAQ hourly sensor resource: `/v3/sensors/{sensor_id}/hours`
This endpoint provides hourly aggregated sensor observations.

**PM2.5**
* OpenAQ sensor ID: 12235312
* Parameter: PM2.5
* Unit: µg/m³
* API resource: `https://api.openaq.org/v3/sensors/12235312/hours`
* The data was requested for: `2025-03-01T00:00:00Z` through `2025-11-30T23:59:59Z`

The downloaded observations contain: sensor ID, parameter, concentration value, unit, UTC aggregation start, UTC aggregation end, local aggregation start, local aggregation end.
The OpenAQ records are hourly aggregation windows rather than instantaneous measurements.

**NO2**
* OpenAQ sensor ID: 12235309
* Parameter: NO2
* Unit: ppb
* API resource: `https://api.openaq.org/v3/sensors/12235309/hours`
* The data was requested for: `2025-03-01T00:00:00Z` through `2025-11-30T23:59:59Z`
* The same hourly aggregation-window fields are retained.

**OpenAQ Licensing**
OpenAQ states that its platform provides access to air-quality data from multiple original providers and that users are responsible for complying with the applicable terms of the original data providers. OpenAQ also requires attribution to OpenAQ when using OpenAQ services.
OpenAQ's licensing documentation states that the platform's data licenses include information on attribution, modification, redistribution, commercial use, and share-alike requirements. OpenAQ's published guidance also states that it shares air-sensor data under CC BY 4.0 or data that is free of copyright restrictions.

**Required attribution**
For this project, the appropriate attribution is:
*Air-quality data accessed through OpenAQ, using the OpenAQ API, with attribution to the original data provider(s) as identified by OpenAQ metadata.*
The project does not claim that OpenAQ itself operates the physical monitoring sensor.

**OpenAQ Authenticity and Provenance**
The PM2.5 and NO2 values are not synthetically generated.
They were obtained directly through the official OpenAQ API using the corresponding sensor IDs and date filters.
The repository preserves the source sensor ID and the original API-derived timestamps so that the observations can be traced back to the OpenAQ platform.
OpenAQ itself notes that it does not represent all air-quality monitoring data worldwide and that its data consists of measurements it has discovered or has been introduced to and that are publicly available.
Therefore, this project describes the data as: *"air-quality observations accessed through OpenAQ"* rather than claiming that OpenAQ is the original measurement agency.

### 3. Meteorological Data — Open-Meteo

**Source**
Historical hourly meteorological data was obtained from the official Open-Meteo Historical Weather API.
* Official source: [https://open-meteo.com/](https://open-meteo.com/)
* Historical Weather API documentation: [https://open-meteo.com/en/docs/historical-weather-api](https://open-meteo.com/en/docs/historical-weather-api)

The requested location corresponds to the Delhi study area used for the air-quality analysis.

**Variables**
The weather dataset contains: datetime_local, temperature_2m, relative_humidity_2m, wind_speed_10m, wind_direction_10m, precipitation, surface_pressure, boundary_layer_height.
These variables are used as meteorological predictors in the pollution analysis and forecasting models.

**Temporal Coverage**
The final weather dataset is intended to cover: 1 March 2025 – 30 November 2025. Weather data is retained at hourly resolution.

**Important Spatial Note**
Open-Meteo provides gridded/model-based historical weather data. Therefore, the weather observations should not be described as measurements from the physical OpenAQ air-quality station. The project uses the nearest applicable Open-Meteo grid/model location for the study area. Any coordinate/grid metadata returned by the Open-Meteo API should be retained in the project metadata.

**Open-Meteo Licensing**
Open-Meteo states that its weather data relies on open data licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). Attribution is required, modifications must be indicated, and use and redistribution are permitted under the license terms.
The Open-Meteo API/software itself has separate licensing considerations; this project uses the weather data, not the Open-Meteo server software.

**Required attribution**
*Weather data provided by Open-Meteo, based on open meteorological data sources and licensed under CC BY 4.0.*
The exact upstream weather model/reanalysis source should also be retained in the API metadata associated with the downloaded dataset.

### 4. Satellite Fire Data — NASA FIRMS

**Source**
Fire activity data was obtained from NASA's: Fire Information for Resource Management System (FIRMS)
* Official source: [https://firms.modaps.eosdis.nasa.gov/](https://firms.modaps.eosdis.nasa.gov/)

NASA FIRMS provides active-fire and thermal-anomaly products from MODIS, VIIRS and Landsat instruments. NASA provides archived historical fire data and explicitly advises users performing scientific analysis to use the standard science-quality products.

**Product**
The project uses: VIIRS NOAA-20 Standard Processing
* Product identifier: VIIRS_NOAA20_SP
* Satellite: NOAA-20 / JPSS-1
* Instrument: VIIRS — Visible Infrared Imaging Radiometer Suite
* Spatial resolution: approximately 375 m for the VIIRS I-band fire product.
NASA's official FIRMS documentation identifies NOAA-20 VIIRS as a 375 m active-fire product and provides its temporal coverage.

**Spatial Coverage**
The fire data was downloaded for the regional bounding box:
West: 74°E South: 27°N East: 79°E North: 31°N
This region covers Delhi and surrounding areas of northern India relevant to the regional-fire/pollution analysis.

**Temporal Coverage**
The project uses: 1 March 2025 – 30 November 2025
The FIRMS API supports the VIIRS_NOAA20_SP standard-processing product.

**Variables**
The downloaded FIRMS observations contain fields including: latitude, longitude, bright_ti4, scan, track, acq_date, acq_time, satellite, instrument, confidence, version, bright_ti5, frp, daynight, type.
NASA defines these fields in the official VIIRS fire-product documentation.

**Interpretation of Fire Detections**
A FIRMS observation is a satellite-detected active-fire/thermal-anomaly pixel.
It should not automatically be interpreted as:
* a confirmed agricultural fire,
* a confirmed crop-residue-burning event,
* a complete representation of all fires on the ground, or
* proof that smoke from that detection reached Delhi.

NASA explicitly warns that satellite-derived active-fire/thermal anomalies have limited accuracy and may originate from fire, hot smoke, agriculture or other sources. Cloud cover can also obscure detections.
Therefore, this project uses the term: *"satellite-detected fire activity"* rather than treating every detection as a confirmed crop-burning event.
Where the type attribute is used, NASA defines:
0 = presumed vegetation fire, 1 = active volcano, 2 = other static land source, 3 = offshore detection

**Fire Radiative Power**
The frp field represents Fire Radiative Power (FRP).
NASA defines FRP as pixel-integrated fire radiative power measured in megawatts (MW).
FRP is therefore used in this project as a measure of the intensity of detected fire activity, not as a direct measurement of emitted PM2.5.

**NASA FIRMS Licensing and Usage**
NASA's Science Data Portal states that scientific data may have specific licenses or usage notices in their metadata; for NASA-led mission observations without a restrictive notice, NASA describes such data as CC0, while encouraging citation of the original source. Users should nevertheless follow the specific product's documentation and attribution requirements.

**Recommended attribution**
*NASA FIRMS VIIRS NOAA-20 Standard Processing active fire data.*
The project should cite NASA FIRMS and the specific VIIRS NOAA-20 product documentation.

### 5. Dataset Authenticity
The project intentionally uses data obtained from the organizations that publish or officially distribute the underlying datasets.

| Component | Authentic source |
| :--- | :--- |
| PM2.5 | OpenAQ official API |
| NO2 | OpenAQ official API |
| Weather | Open-Meteo official API |
| Fire activity | NASA FIRMS official API |

* No values are manually entered into the raw datasets.
* No synthetic observations are added to the raw datasets.
* No Kaggle mirror is used as the source of the final datasets.
* No third-party GitHub repository is used as the source of the final raw observations.

### 6. Reproducibility
The raw datasets were obtained programmatically.
The project maintains download scripts under: `scripts/`
The scripts specify:
* source API
* sensor/product identifier
* date range
* geographic bounding box where applicable
* API parameters
* output location
* pagination logic
* duplicate handling

API credentials are intentionally excluded from the repository. API keys must never be committed to GitHub or included in this README.

### 7. Raw Data Policy
The `data/raw/` directory contains source-derived observations.
Raw files should not be manually edited.
Data cleaning, temporal alignment, feature engineering, aggregation and lag construction should be performed in separate processing scripts.

Recommended structure:
```
data/
├── raw/
│   ├── air_quality/
│   │   ├── pm25_hourly_mar_nov.csv
│   │   └── no2_hourly_mar_nov.csv
│   ├── weather/
│   │   └── weather_hourly_mar_nov.csv
│   └── fires/
│       └── firms_noaa20_2025_mar_nov.csv
└── processed/
    └── master_hourly.csv
```

### 8. Data Processing Policy
The following transformations are considered project preprocessing rather than source-data replacement:
* Converting timestamps to a common time zone/convention.
* Aligning hourly air-quality observations with hourly meteorological observations.
* Removing duplicate records.
* Handling missing observations.
* Creating lagged pollution variables.
* Creating lagged weather variables.
* Converting wind direction into sine/cosine components.
* Aggregating FIRMS detections into hourly/regional fire-activity features.
* Creating distance-based fire features.
* Creating forecasting targets at 1-hour, 3-hour, 6-hour, 12-hour and 24-hour horizons.

The original source-derived values remain preserved in the raw datasets.

### 9. Research Use of the Data
The combined dataset is designed to investigate:
* **Research Question 1:** How strongly do previous PM2.5 and NO2 levels predict subsequent PM2.5 concentrations?
* **Research Question 2:** Which meteorological conditions and time lags are associated with subsequent changes in urban PM2.5 and NO2?
* **Research Question 3:** Is regional satellite-detected fire activity temporally associated with subsequent changes in Delhi PM2.5?
* **Research Question 4:** Does adding meteorological and regional fire information improve short-term PM2.5 forecasting compared with using pollution history alone?

### 10. Important Scientific Limitations
The dataset supports temporal association and forecasting analysis. It does not, by itself, establish causal relationships.
In particular:
* FIRMS detections do not prove that a specific fire caused an observed PM2.5 increase.
* FIRMS observations are satellite detections and are affected by satellite overpass timing and cloud cover.
* Absence of a FIRMS detection does not necessarily mean that no fire existed.
* OpenAQ is an aggregation platform and the original measurement provider should be acknowledged where identified.
* Open-Meteo weather data represents gridded/model-based meteorological information rather than a measurement from the pollution sensor itself.
* Weather and fire observations may have different spatial representations from the air-quality station.
* Temporal alignment and lag selection can affect observed relationships.

Consequently, conclusions should be phrased in terms of association, temporal relationships and predictive performance, rather than direct causation.

### 11. Citation and Attribution Summary

**OpenAQ**
OpenAQ. OpenAQ API and aggregated air-quality data.
* Official documentation: [https://docs.openaq.org/](https://docs.openaq.org/)
* Terms of Use: [https://docs.openaq.org/about/terms](https://docs.openaq.org/about/terms)
* Licenses: [https://docs.openaq.org/resources/licenses](https://docs.openaq.org/resources/licenses)

**Open-Meteo**
Open-Meteo. Historical Weather API.
* Official website: [https://open-meteo.com/](https://open-meteo.com/)
* Historical Weather API: [https://open-meteo.com/en/docs/historical-weather-api](https://open-meteo.com/en/docs/historical-weather-api)
* Weather data licensing: CC BY 4.0

**NASA FIRMS**
NASA Earth Science Data and Information System / Land, Atmosphere Near real-time Capability for EOS (LANCE). Fire Information for Resource Management System (FIRMS).
* Official website: [https://firms.modaps.eosdis.nasa.gov/](https://firms.modaps.eosdis.nasa.gov/)
* VIIRS active-fire product documentation: [https://firms.modaps.eosdis.nasa.gov/content/descriptions/FIRMS_VIIRS_Firehotspots.html](https://firms.modaps.eosdis.nasa.gov/content/descriptions/FIRMS_VIIRS_Firehotspots.html)
* Archive Download: [https://firms.modaps.eosdis.nasa.gov/download/](https://firms.modaps.eosdis.nasa.gov/download/)
* Product used: VIIRS NOAA-20 Standard Processing (VIIRS_NOAA20_SP)

### 12. Final Attribution Statement
This project uses:
Air-quality observations accessed through OpenAQ; historical meteorological data accessed through Open-Meteo; and VIIRS NOAA-20 Standard Processing active-fire observations distributed through NASA FIRMS.
All source organizations are credited according to their published documentation and licensing/usage requirements.
The project does not claim ownership of the original source datasets.
The project-specific contribution consists of data retrieval, validation, temporal/spatial alignment, feature engineering, statistical analysis, forecasting models and derived analytical outputs.
