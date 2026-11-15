# Environmental Data Analysis (EDA) Project

This repository contains data collection scripts, datasets, and Jupyter notebooks for an Environmental Data Analysis project. The project explores the relationship between air quality (PM2.5 and NO2), weather conditions, and wildfire activity (NASA FIRMS) to understand their impact on the environment.

## Project Structure

- `apis/` – Contains API keys for the different data sources (ignored by Git).
- `data/`
  - `raw/` – Raw datasets for air quality, fires, and weather.
  - `processed/` – Cleaned and processed datasets used for analysis.
- `scripts/` – Python scripts used for collecting data:
  - `download_pm25.py` – Fetches PM2.5 air quality data.
  - `download_no2.py` – Fetches NO2 air quality data.
  - `download_weather.py` – Collects meteorological data.
  - `download_firms.py` – Fetches wildfire data using NASA's FIRMS API.
- `notebooks/` – Jupyter notebooks containing exploratory data analysis, visualisations, statistical analysis, and predictive modelling.

## Analysis Contributions

The project includes multiple individual and combined analyses:

- **Air Quality Analysis:** Exploration of PM2.5 and NO2 trends, distributions, and patterns.
- **Wildfire Analysis:** Investigation of wildfire activity and its relationship with air pollution.
- **Weather and Pollution Analysis:** Study of how weather conditions influence PM2.5 concentrations in Delhi, including correlation analysis, lag analysis, Granger causality, and regression modelling.
- **Combined Analysis:** Integration of pollution and wildfire datasets to investigate their overall environmental impact.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/khushishahs02/EDA-Group-Project.git
cd EDA-Group-Project
```

### 2. Environment Setup

Ensure Python is installed and create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python libraries:

```bash
pip install numpy pandas matplotlib seaborn scipy statsmodels scikit-learn requests
```

### 4. API Keys

Create an `apis/` directory in the project root if it does not exist. Add the required API keys in their respective `.txt` files as expected by the scripts:

- `nasa_firms_api.txt`
- `opentransit_api.txt`
- `aq_api.txt`

Keep API keys private and do not commit them to GitHub.

## Usage

### Data Collection

To start collecting data, run the scripts from the project root:

```bash
python scripts/download_weather.py
python scripts/download_pm25.py
python scripts/download_no2.py
python scripts/download_firms.py
```

### Running the Analysis

Open the `notebooks/` directory and launch the required Jupyter notebook:

```bash
jupyter notebook
```

Select the notebook you want to explore and run its cells to view the analysis and visualisations.
