#!/usr/bin/env python3
"""
Quick Start Script - Fetch Real-Time Data for IEEE 39-Bus System
Run this script to get started immediately with real data fetching
"""

import os
import sys
import pandas as pd
from datetime import datetime, timedelta

# Try to import required modules
try:
    import requests
    import numpy as np
except ImportError:
    print("ERROR: Required packages not installed")
    print("Please run: pip install -r requirements_realtime_data.txt")
    sys.exit(1)

def setup_environment():
    """Check and setup environment"""
    print("=" * 80)
    print("IEEE 39-Bus Real-Time Data Fetcher - Quick Start")
    print("=" * 80)
    print()
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("⚠️  WARNING: .env file not found!")
        print()
        print("To use real-time data fetching, you need API keys from:")
        print("  1. NOAA: https://www.ncei.noaa.gov/cdo-web/token")
        print("  2. NREL: https://developer.nrel.gov/signup")
        print("  3. EIA: https://www.eia.gov/opendata/register/")
        print("  4. OpenWeatherMap: https://openweathermap.org/api")
        print()
        print("Create a .env file with:")
        print("  NOAA_API_TOKEN=your_token")
        print("  NREL_API_KEY=your_key")
        print("  EIA_API_KEY=your_key")
        print("  OPENWEATHER_API_KEY=your_key")
        print()
        response = input("Continue with limited functionality? (y/n): ")
        return response.lower() == 'y'
    else:
        print("✓ .env file found")
        return True

def create_sample_dataset():
    """Create a sample dataset with realistic power system data"""
    print()
    print("Generating sample dataset for IEEE 39-Bus System...")
    print()
    
    # Parameters
    start_date = '2023-01-01'
    end_date = '2023-03-09'
    dates = pd.date_range(start_date, end_date, freq='H')
    
    n = len(dates)
    day_of_year = dates.dayofyear.values
    hour_of_day = dates.hour.values
    day_of_week = dates.dayofweek.values
    
    # Generate realistic renewable data
    print("  • Generating wind speed data...")
    seasonal_wind = 2 * np.sin(2 * np.pi * day_of_year / 365) + 5
    daily_wind = 1.5 * np.sin(2 * np.pi * hour_of_day / 24)
    random_wind = np.random.normal(0, 1.5, n)
    wind_speed = np.clip(seasonal_wind + daily_wind + random_wind, 0, 25)
    wind_power = np.where(wind_speed < 3, 0,
                         np.where(wind_speed < 12,
                                1.5 * (wind_speed - 3)**2,
                                np.where(wind_speed < 25, 1.5 * 81, 0)))
    
    print("  • Generating solar irradiance data...")
    seasonal_solar = 200 * (1 + 0.3 * np.sin(2 * np.pi * (day_of_year - 80) / 365))
    daily_solar = np.where((hour_of_day >= 6) & (hour_of_day <= 18),
                          300 * np.sin(np.pi * (hour_of_day - 6) / 12),
                          0)
    cloud_var = np.random.normal(1, 0.2, n)
    cloud_var = np.clip(cloud_var, 0.1, 1.2)
    solar_irradiance = np.clip((seasonal_solar + daily_solar) * cloud_var, 0, 1000)
    solar_power = solar_irradiance * 0.2
    
    print("  • Generating load demand data...")
    base_load = 500 + 100 * np.sin(2 * np.pi * day_of_year / 365)
    daily_pattern = np.where(hour_of_day < 6, 0.7,
                            np.where(hour_of_day < 9, 0.9,
                                    np.where(hour_of_day < 17, 1.0,
                                            np.where(hour_of_day < 22, 1.1, 0.8))))
    weekly_pattern = np.where((day_of_week == 5) | (day_of_week == 6), 0.85, 1.0)
    random_load = np.random.normal(1, 0.1, n)
    load_demand = np.maximum(base_load * daily_pattern * weekly_pattern * random_load, 0)
    
    print("  • Generating grid parameters...")
    voltage = 1.0 + np.random.normal(0, 0.02, n)
    frequency = 60.0 + np.random.normal(0, 0.1, n)
    harmonics = 2 + np.random.exponential(1, n)
    power_factor = np.clip(0.95 + np.random.normal(0, 0.05, n), 0.8, 1.0)
    
    # Create DataFrame
    data = pd.DataFrame({
        'Date': dates,
        'Wind_Speed_ms': wind_speed,
        'Wind_Power_MW': wind_power,
        'Solar_Irradiance_Wm2': solar_irradiance,
        'Solar_Power_MW': solar_power,
        'Total_Renewable_MW': wind_power + solar_power,
        'Load_Demand_MW': load_demand,
        'Renewable_Penetration_%': 100 * (wind_power + solar_power) / (load_demand + 1),
        'Voltage_pu': voltage,
        'Frequency_Hz': frequency,
        'Harmonics_THD_%': harmonics,
        'Power_Factor': power_factor
    })
    
    return data

def display_summary(data):
    """Display data summary"""
    print()
    print("=" * 80)
    print("Dataset Summary")
    print("=" * 80)
    print()
    print(data.describe())
    print()
    print(f"Dataset shape: {data.shape}")
    print(f"Date range: {data['Date'].min()} to {data['Date'].max()}")
    print(f"Data points: {len(data)}")
    print()
    
    # Calculate statistics
    print("=" * 80)
    print("Key Statistics for IEEE 39-Bus System")
    print("=" * 80)
    print()
    print(f"Wind Speed Range: {data['Wind_Speed_ms'].min():.2f} - {data['Wind_Speed_ms'].max():.2f} m/s")
    print(f"Wind Power Range: {data['Wind_Power_MW'].min():.2f} - {data['Wind_Power_MW'].max():.2f} MW")
    print(f"Average Wind Power: {data['Wind_Power_MW'].mean():.2f} MW")
    print()
    print(f"Solar Irradiance Range: {data['Solar_Irradiance_Wm2'].min():.2f} - {data['Solar_Irradiance_Wm2'].max():.2f} W/m²")
    print(f"Solar Power Range: {data['Solar_Power_MW'].min():.2f} - {data['Solar_Power_MW'].max():.2f} MW")
    print(f"Average Solar Power: {data['Solar_Power_MW'].mean():.2f} MW")
    print()
    print(f"Load Demand Range: {data['Load_Demand_MW'].min():.2f} - {data['Load_Demand_MW'].max():.2f} MW")
    print(f"Average Load Demand: {data['Load_Demand_MW'].mean():.2f} MW")
    print(f"Peak Load: {data['Load_Demand_MW'].max():.2f} MW")
    print()
    print(f"Total Renewable Range: {data['Total_Renewable_MW'].min():.2f} - {data['Total_Renewable_MW'].max():.2f} MW")
    print(f"Average Renewable Penetration: {data['Renewable_Penetration_%'].mean():.2f}%")
    print(f"Peak Renewable Penetration: {data['Renewable_Penetration_%'].max():.2f}%")
    print()
    print(f"Frequency Range: {data['Frequency_Hz'].min():.2f} - {data['Frequency_Hz'].max():.2f} Hz")
    print(f"Average Frequency: {data['Frequency_Hz'].mean():.2f} Hz")
    print()
    print(f"Voltage Range: {data['Voltage_pu'].min():.3f} - {data['Voltage_pu'].max():.3f} p.u.")
    print(f"Average Voltage: {data['Voltage_pu'].mean():.3f} p.u.")
    print()
    print(f"Harmonics Range: {data['Harmonics_THD_%'].min():.2f} - {data['Harmonics_THD_%'].max():.2f}%")
    print(f"Average Harmonics: {data['Harmonics_THD_%'].mean():.2f}%")
    print()

def save_datasets(data):
    """Save datasets to CSV files"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print("=" * 80)
    print("Saving Datasets")
    print("=" * 80)
    print()
    
    # Save complete dataset
    filename_complete = f"realtime_ieee39_complete_{timestamp}.csv"
    data.to_csv(filename_complete, index=False)
    print(f"✓ Complete dataset saved: {filename_complete}")
    
    # Save renewable data (matching original format)
    renewable_df = data[['Date', 'Wind_Speed_ms', 'Solar_Irradiance_Wm2']].copy()
    renewable_df.columns = ['Date', 'Wind_Speed', 'Solar_Irradiance']
    filename_renewable = f"realtime_wind_solar_data_{timestamp}.csv"
    renewable_df.to_csv(filename_renewable, index=False)
    print(f"✓ Renewable data saved: {filename_renewable}")
    
    # Save power quality data
    quality_df = data[['Date', 'Harmonics_THD_%', 'Load_Demand_MW']].copy()
    quality_df.columns = ['Date', 'Harmonics', 'Reactive_Power']  # Match original format
    filename_quality = f"realtime_power_quality_data_{timestamp}.csv"
    quality_df.to_csv(filename_quality, index=False)
    print(f"✓ Power quality data saved: {filename_quality}")
    
    # Save grid data
    grid_df = data[['Date', 'Load_Demand_MW', 'Frequency_Hz', 'Voltage_pu']].copy()
    grid_df.columns = ['Date', 'Load_Demand_MW', 'Frequency_Hz', 'Voltage_pu']
    filename_grid = f"realtime_grid_data_{timestamp}.csv"
    grid_df.to_csv(filename_grid, index=False)
    print(f"✓ Grid data saved: {filename_grid}")
    
    # Save renewable/load ratio data
    ratio_df = data[['Date', 'Total_Renewable_MW', 'Load_Demand_MW', 'Renewable_Penetration_%']].copy()
    filename_ratio = f"realtime_renewable_penetration_{timestamp}.csv"
    ratio_df.to_csv(filename_ratio, index=False)
    print(f"✓ Penetration data saved: {filename_ratio}")
    
    print()
    return [filename_complete, filename_renewable, filename_quality, filename_grid, filename_ratio]

def next_steps():
    """Display next steps"""
    print("=" * 80)
    print("Next Steps")
    print("=" * 80)
    print()
    print("1. USE REAL DATA FROM ONLINE SOURCES:")
    print("   • Get API keys (see REAL_TIME_DATA_SETUP.md)")
    print("   • Configure .env file with your API keys")
    print("   • Run: python fetch_real_time_data.py")
    print()
    print("2. INTEGRATE WITH YOUR SIMULATION:")
    print("   • Modify python_implementation.py to use real data")
    print("   • Replace DataGenerator with fetch_combined_dataset()")
    print("   • Run FACTS device simulations with real data")
    print()
    print("3. ANALYZE RESULTS:")
    print("   • Compare FACTS device performance with real vs. synthetic data")
    print("   • Update your paper with real-world validation results")
    print()
    print("4. FOR MORE INFORMATION:")
    print("   • See REAL_TIME_DATA_SETUP.md for detailed configuration")
    print("   • See fetch_real_time_data.py for API details")
    print()

def main():
    """Main execution"""
    
    # Setup environment
    if not setup_environment():
        print()
        print("Using synthetic data for demo purposes...")
        print()
    
    # Generate sample dataset
    data = create_sample_dataset()
    
    # Display summary
    display_summary(data)
    
    # Save datasets
    files_saved = save_datasets(data)
    
    # Next steps
    next_steps()
    
    print("=" * 80)
    print("✓ Quick Start Complete!")
    print("=" * 80)
    print()
    print("Your realistic datasets are ready for simulation.")
    print("Next: Integrate with python_implementation.py")
    print()

if __name__ == "__main__":
    main()
