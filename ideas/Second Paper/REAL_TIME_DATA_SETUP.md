# Real-Time Power Systems Data Fetcher - Setup & Configuration Guide

## Overview

This guide explains how to set up and use the real-time data fetcher to collect actual operational data from various online sources for your IEEE 39-Bus power system simulation with FACTS device control.

## Table of Contents
1. [Installation](#installation)
2. [API Keys Configuration](#api-keys-configuration)
3. [Data Sources Overview](#data-sources-overview)
4. [Usage Examples](#usage-examples)
5. [Troubleshooting](#troubleshooting)

---

## Installation

### Step 1: Install Python Dependencies

```bash
pip install -r requirements_realtime_data.txt
```

### Step 2: Create Environment File

Create a `.env` file in your project directory to store API keys securely:

```bash
# Windows PowerShell
New-Item -Path .env -ItemType File

# macOS/Linux
touch .env
```

Add the following to your `.env` file (replace with your actual keys):

```
NOAA_API_TOKEN=your_noaa_token_here
NREL_API_KEY=your_nrel_api_key_here
EIA_API_KEY=your_eia_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

---

## API Keys Configuration

### 1. NOAA API Token

**Purpose**: Historical wind speed and weather data  
**Website**: https://www.ncei.noaa.gov/cdo-web/webservices/v2/

**Steps to obtain token**:
1. Visit https://www.ncei.noaa.gov/cdo-web/token
2. Sign in or create account
3. Enter your email
4. Click "Request Token"
5. Check email for activation link
6. Copy token to `.env` file

**Data Available**:
- Average wind speed (AWND)
- Maximum/minimum temperatures
- Precipitation
- Snow depth
- Historical climate data

---

### 2. NREL API Key

**Purpose**: Solar irradiance and wind resource data  
**Website**: https://developer.nrel.gov/

**Steps to obtain key**:
1. Visit https://developer.nrel.gov/signup
2. Fill registration form
3. Verify email
4. Create new API key from dashboard
5. Copy key to `.env` file

**Data Available**:
- PVWatts solar power estimates
- Wind resource atlas data
- National Solar Radiation Database (NSRDB)
- Solar power monthly/hourly estimates
- Irradiance data (GHI, DHI, DNI)

---

### 3. EIA API Key

**Purpose**: Electricity load demand and consumption data  
**Website**: https://www.eia.gov/opendata/

**Steps to obtain key**:
1. Visit https://www.eia.gov/opendata/register/
2. Fill registration form
3. EIA will email your API key
4. Copy key to `.env` file

**Data Available**:
- Net electricity generation by fuel type
- Total electricity demand by region
- Renewable energy generation
- Coal, natural gas, nuclear production
- Capacity by region

**Series IDs for Common Regions**:
- US Total: `ELEC.CONS.ALL.US-ALL.A`
- New England: `ELEC.CONS.ALL.NE-ALL.A`
- California: `ELEC.CONS.ALL.CAL-ALL.A`
- Texas: `ELEC.CONS.ALL.TEX-ALL.A`
- Mid-Atlantic: `ELEC.CONS.ALL.MAT-ALL.A`

---

### 4. OpenWeatherMap API Key

**Purpose**: Real-time weather data and forecasts  
**Website**: https://openweathermap.org/api

**Steps to obtain key**:
1. Visit https://openweathermap.org/api
2. Click "Sign Up" or "Log In"
3. Create account or sign in
4. Go to API keys section
5. Copy default API key to `.env` file

**Data Available**:
- Current weather conditions
- Weather forecasts (5, 7, or 14 day)
- Hourly data
- Wind speed and direction
- Cloud coverage
- Precipitation
- Temperature and humidity

---

## Data Sources Overview

### Wind Speed Data

| Source | Type | Resolution | Coverage | Best For |
|--------|------|-----------|----------|----------|
| NOAA NCEI | Historical | Daily | Global | Long-term historical analysis |
| NREL Wind Toolkit | Resource map | Monthly | US | Wind resource assessment |
| OpenWeatherMap | Real-time/Forecast | 3-hourly | Global | Forecast accuracy |

**Recommended Usage**:
- Use NOAA for historical baseline (2+ years of data)
- Use NREL for resource estimation
- Use OpenWeatherMap for real-time monitoring

### Solar Irradiance Data

| Source | Type | Resolution | Coverage | Best For |
|--------|------|-----------|----------|----------|
| NREL NSRDB | Historical/Typical | Hourly | US | Accurate solar modeling |
| NREL PVWatts | Modeled | Monthly/Hourly | Global | System performance |
| OpenWeatherMap | Real-time | Current + 7-day | Global | Real-time forecasting |

**Recommended Usage**:
- Use NREL NSRDB for detailed solar modeling
- Use PVWatts for quick system sizing
- Use OpenWeatherMap for real-time cloud tracking

### Load Demand Data

| Source | Type | Resolution | Coverage | Best For |
|--------|------|-----------|----------|----------|
| EIA | Historical | Annual/Monthly | US | Long-term trends |
| ISO-NE | Real-time | 5-minute | New England | Current demand |
| MISO | Real-time | Real-time | Midwest | Real-time grid status |

**Recommended Usage**:
- Use EIA for annual planning
- Use ISO-NE for operational data (New England region)
- Use MISO for Midwest region

### Grid Frequency & Voltage

| Source | Type | Resolution | Coverage | Best For |
|--------|------|-----------|----------|----------|
| GridStatus | Historical | Minute | Global | Frequency analysis |
| ISO-NE API | Real-time | Real-time | New England | Current frequency |
| PJM API | Real-time | Real-time | Mid-Atlantic | Current frequency |

**Recommended Usage**:
- Use GridStatus for historical analysis
- Use ISO-RTO APIs for current operational status

---

## Usage Examples

### Example 1: Fetch Combined Dataset for Your IEEE 39-Bus System

```python
from fetch_real_time_data import RealTimeDataFetcher

# Initialize fetcher
fetcher = RealTimeDataFetcher()

# Fetch combined dataset for your study period
data = fetcher.fetch_combined_dataset(
    start_date='2023-01-01',
    end_date='2023-03-09',
    frequency='H'  # Hourly data
)

# Display summary
print(data.describe())

# Save to CSV
fetcher.save_datasets(data, prefix='ieee39_real_time_')
```

### Example 2: Fetch Only Wind Data from NOAA

```python
from fetch_real_time_data import RealTimeDataFetcher

fetcher = RealTimeDataFetcher()

# Fetch wind data for New England (42.5°N, 72.5°W)
wind_data = fetcher.fetch_wind_data_noaa(
    latitude=42.5,
    longitude=-72.5,
    start_date='2023-01-01',
    end_date='2023-03-09'
)

# Display first few rows
print(wind_data.head(10))

# Save to CSV
wind_data.to_csv('wind_data_real_new_england.csv', index=False)
```

### Example 3: Fetch Solar Data from NREL

```python
from fetch_real_time_data import RealTimeDataFetcher

fetcher = RealTimeDataFetcher()

# Fetch solar data for Connecticut (41.5°N, 70.8°W)
solar_data = fetcher.fetch_solar_data_nrel(
    latitude=41.5,
    longitude=70.8,
    api_key='YOUR_NREL_API_KEY'
)

# Display data
print(solar_data)

# Save to CSV
solar_data.to_csv('solar_data_real_connecticut.csv', index=False)
```

### Example 4: Fetch Real-Time Grid Data from ISO-NE

```python
from fetch_real_time_data import RealTimeDataFetcher

fetcher = RealTimeDataFetcher()

# Get current grid status (frequency, demand, wind generation)
iso_data = fetcher.fetch_iso_rto_data('ISONE')

# Display current conditions
print(iso_data)

# Save to CSV
iso_data.to_csv('isone_realtime_current.csv', index=False)
```

### Example 5: Fetch Load Demand from EIA

```python
from fetch_real_time_data import RealTimeDataFetcher

fetcher = RealTimeDataFetcher()

# Fetch historical load for US
load_data = fetcher.fetch_load_demand_eia(region='US')

# Display data
print(load_data)

# Save to CSV
load_data.to_csv('us_load_demand_historical.csv', index=False)
```

### Example 6: Fetch Grid Frequency Data

```python
from fetch_real_time_data import RealTimeDataFetcher

fetcher = RealTimeDataFetcher()

# Fetch historical frequency data
freq_data = fetcher.fetch_grid_frequency_data(country='US')

# Display data
print(freq_data.head(20))

# Save to CSV
freq_data.to_csv('us_grid_frequency_historical.csv', index=False)
```

---

## Integrating with Your Python Implementation

### Modified python_implementation.py

Replace the synthetic data generation with real data:

```python
# OLD: Synthetic data generation
# data_gen = DataGenerator(duration_hours=8760)
# data = data_gen.generate_complete_dataset()

# NEW: Real data fetching
from fetch_real_time_data import RealTimeDataFetcher

fetcher = RealTimeDataFetcher()
data = fetcher.fetch_combined_dataset(
    start_date='2023-01-01',
    end_date='2023-03-09',
    frequency='H'
)

# Continue with FACTS device simulation using real data
# ... rest of your code ...
```

---

## Data Quality Considerations

### Missing Data Handling

```python
import pandas as pd
import numpy as np

# Option 1: Forward fill (propagate last known value)
data_filled = data.fillna(method='ffill')

# Option 2: Linear interpolation
data_filled = data.interpolate(method='linear')

# Option 3: Drop missing values
data_clean = data.dropna()

# Option 4: Forward fill then backward fill
data_filled = data.fillna(method='ffill').fillna(method='bfill')
```

### Data Normalization

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# StandardScaler: mean=0, std=1
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data[['Wind_Speed_ms', 'Solar_Irradiance_Wm2']])

# MinMaxScaler: range [0, 1]
scaler = MinMaxScaler()
data_normalized = scaler.fit_transform(data)
```

### Outlier Detection

```python
# Remove outliers beyond 3 standard deviations
z_scores = np.abs((data - data.mean()) / data.std())
data_clean = data[(z_scores < 3).all(axis=1)]
```

---

## Troubleshooting

### Issue 1: "API Key Invalid" Error

**Solution**:
1. Verify key is correct in `.env` file
2. Check for extra whitespace or special characters
3. Verify key hasn't expired
4. Regenerate key from provider website

### Issue 2: "Connection Timeout" Error

**Solution**:
```python
import requests

# Increase timeout (example: 60 seconds)
response = requests.get(url, timeout=60)

# Implement retry logic
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
```

### Issue 3: "Rate Limit Exceeded" Error

**Solution**:
```python
import time

# Add delay between API calls
for location in locations:
    data = fetch_data(location)
    time.sleep(1)  # 1 second delay

# Or use API batch requests if available
```

### Issue 4: "No Data Available" for Specific Location

**Solution**:
1. Check if location has historical data
2. Try nearby location (±0.5° latitude/longitude)
3. Adjust time period to available range
4. Use synthetic data as fallback

---

## Best Practices

### 1. Cache API Responses

```python
import json
from datetime import datetime, timedelta

cache_file = 'data_cache.json'

def get_with_cache(url, cache_expiry_hours=24):
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache = json.load(f)
            if datetime.now() - datetime.fromisoformat(cache['timestamp']) < timedelta(hours=cache_expiry_hours):
                return cache['data']
    
    # Fetch new data
    response = requests.get(url)
    data = response.json()
    
    # Save to cache
    with open(cache_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'data': data
        }, f)
    
    return data
```

### 2. Monitor API Usage

```python
import logging

# Set up logging
logging.basicConfig(filename='data_fetch.log', level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Fetching data from {url}")
logger.error(f"Error: {error_message}")
```

### 3. Implement Error Recovery

```python
def fetch_with_fallback(primary_source, fallback_source):
    try:
        return fetch_from_source(primary_source)
    except Exception as e:
        logger.warning(f"Primary source failed: {e}")
        try:
            return fetch_from_source(fallback_source)
        except Exception as e2:
            logger.error(f"Fallback also failed: {e2}")
            return generate_synthetic_data()
```

---

## Additional Resources

### Documentation Links
- [NOAA CDO Web Services](https://www.ncei.noaa.gov/cdo-web/webservices/v2/)
- [NREL Developer Network](https://developer.nrel.gov/)
- [EIA Open Data](https://www.eia.gov/opendata/)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [ISO-NE Webservices](https://webservices.iso-ne.com/)

### Example Datasets
- [Kaggle: Power Systems Datasets](https://www.kaggle.com/datasets?search=power+system)
- [UCI ML Repository: Energy Data](https://archive.ics.uci.edu/ml/datasets.php?format=&task=&att=&area=&numAtt=&numIns=&type=&sort=&view=table&order=ascending)

### Related Research
- IEEE Power Systems datasets
- NREL publications on solar/wind integration
- FERC data on grid operations

---

## Questions or Issues?

For more information or to report issues:
1. Check API provider documentation
2. Review API rate limits and quotas
3. Verify network connectivity
4. Check `.env` file configuration
5. Review logs in `data_fetch.log`

---

**Last Updated**: 2024  
**Version**: 1.0  
**For**: IEEE 39-Bus System with FACTS Device Control Study
