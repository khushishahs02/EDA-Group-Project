# Environmental Data Analysis (EDA) Project

This repository contains scripts and data processing pipelines for an Environmental Data Analysis project. The project focuses on collecting and analyzing data regarding air quality (PM2.5, NO2), weather, and wildfires (NASA FIRMS) to study their correlations and environmental impact.

## Project Structure

- `apis/` - (Ignored in git) Contains raw API keys for the data sources.
- `data/`
  - `raw/` - Raw data downloads (Air Quality, Fires, Weather).
  - `processed/` - Cleaned and processed datasets.
- `scripts/` - Python scripts for data collection:
  - `download_pm25.py` - Fetches PM2.5 air quality data.
  - `download_no2.py` - Fetches NO2 air quality data.
  - `download_weather.py` - Fetches meteorological data.
  - `download_firms.py` - Fetches wildfire data using NASA's FIRMS API.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/khushishahs02/EDA-Group-Project.git
   cd EDA-Group-Project
   ```

2. **Environment Setup:**
   Ensure you have Python installed and create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   (Dependencies will be listed in a `requirements.txt` when finalized. Ensure `requests`, `pandas`, etc., are installed to run the scripts.)

4. **API Keys:**
   Create an `apis/` directory in the root if it doesn't exist. Place your API keys in the respective `.txt` files as expected by the scripts (`nasa_firms_api.txt`, `opentransit_api.txt`, `aq_api.txt`).

## Usage

To start data collection, run the scripts located in the `scripts/` directory:
```bash
python scripts/download_weather.py
python scripts/download_pm25.py
```
