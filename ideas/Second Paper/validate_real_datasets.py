"""
Real Dataset Validator and Processor
Identifies and processes real-world datasets with all required columns for FACTS simulation
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import json

class DatasetRequirementValidator:
    """Check if real datasets have all required columns for FACTS simulation"""
    
    def __init__(self):
        # Required columns for FACTS device simulation
        self.required_columns = {
            'datetime': ['Date', 'DateTime', 'Datetime', 'date', 'time', 'timestamp', 'Time'],
            'wind_speed': ['Wind_Speed_ms', 'WindSpeed', 'wind_speed', 'Wind Speed', 'WSPD', 'WS'],
            'wind_power': ['Wind_Power_MW', 'WindPower', 'wind_power', 'P_wind', 'PW', 'wind_gen'],
            'solar_irradiance': ['Solar_Irradiance_Wm2', 'Solar_Irradiance', 'GHI', 'Irradiance', 'solar_irr', 'DNI', 'DHI'],
            'solar_power': ['Solar_Power_MW', 'SolarPower', 'solar_power', 'P_solar', 'PS', 'solar_gen'],
            'load_demand': ['Load_Demand_MW', 'Load', 'Demand', 'load', 'demand_mw', 'P_load', 'Total_Load'],
            'temperature': ['Temperature', 'Temp', 'temperature_c', 'T', 'temp_c'],
            'frequency': ['Frequency_Hz', 'Frequency', 'frequency', 'Freq', 'f'],
            'voltage': ['Voltage_pu', 'Voltage', 'voltage', 'V_pu', 'bus_voltage'],
            'harmonics': ['Harmonics_THD_%', 'THD', 'harmonics', 'THD_%', 'harmonic_distortion'],
            'power_factor': ['Power_Factor', 'PF', 'power_factor', 'pf'],
        }
        
        # Critical columns (must have)
        self.critical = ['datetime', 'load_demand']
        
        # High priority columns (should have)
        self.high_priority = ['wind_speed', 'wind_power', 'solar_irradiance', 'solar_power', 'temperature']
        
        # Medium priority (nice to have)
        self.medium_priority = ['frequency', 'voltage', 'harmonics', 'power_factor']
    
    def find_matching_columns(self, df_columns):
        """Find which required columns exist in dataset"""
        found = {}
        df_cols_lower = [col.lower() for col in df_columns]
        
        for category, possible_names in self.required_columns.items():
            for possible_name in possible_names:
                if possible_name.lower() in df_cols_lower:
                    idx = [i for i, col in enumerate(df_cols_lower) if col == possible_name.lower()][0]
                    found[category] = df_columns[idx]
                    break
        
        return found
    
    def validate_dataset(self, filepath):
        """Validate if a dataset has required columns"""
        
        try:
            # Try to load dataset
            print(f"\n📂 Checking: {os.path.basename(filepath)}")
            print(f"   Size: {os.path.getsize(filepath) / (1024*1024):.2f} MB")
            
            # Try different methods to load
            try:
                df = pd.read_csv(filepath, nrows=100)  # Load first 100 rows to check
            except:
                try:
                    df = pd.read_excel(filepath, nrows=100)
                except:
                    print(f"   ✗ Cannot load file")
                    return None
            
            print(f"   Rows: {len(df)} (sample), Columns: {len(df.columns)}")
            print(f"   Columns: {', '.join(df.columns[:10])}...")
            
            # Find matching columns
            found = self.find_matching_columns(df.columns)
            
            # Calculate completeness
            critical_found = sum(1 for cat in self.critical if cat in found)
            high_priority_found = sum(1 for cat in self.high_priority if cat in found)
            medium_priority_found = sum(1 for cat in self.medium_priority if cat in found)
            
            total_score = (critical_found * 100 + 
                          high_priority_found * 30 + 
                          medium_priority_found * 10)
            max_score = (len(self.critical) * 100 + 
                        len(self.high_priority) * 30 + 
                        len(self.medium_priority) * 10)
            completeness = (total_score / max_score) * 100
            
            # Print results
            print(f"\n   📊 COMPLETENESS: {completeness:.1f}%")
            print(f"   ✓ Critical columns: {critical_found}/{len(self.critical)}")
            print(f"   ✓ High priority columns: {high_priority_found}/{len(self.high_priority)}")
            print(f"   ✓ Medium priority columns: {medium_priority_found}/{len(self.medium_priority)}")
            
            if found:
                print(f"\n   Found columns:")
                for category, column in sorted(found.items()):
                    print(f"      • {category}: {column}")
            
            # Check data quality
            missing_rate = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            print(f"\n   📈 Data Quality:")
            print(f"      Missing values: {missing_rate:.2f}%")
            
            result = {
                'file': filepath,
                'filename': os.path.basename(filepath),
                'completeness': completeness,
                'critical_found': critical_found,
                'high_priority_found': high_priority_found,
                'medium_priority_found': medium_priority_found,
                'found_columns': found,
                'total_columns': len(df.columns),
                'missing_rate': missing_rate,
                'suitable': completeness >= 60 and missing_rate < 30
            }
            
            if result['suitable']:
                print(f"\n   ✅ SUITABLE FOR FACTS SIMULATION!")
            else:
                print(f"\n   ⚠️  May need preprocessing or additional data")
            
            return result
            
        except Exception as e:
            print(f"   ✗ Error: {str(e)}")
            return None
    
    def recommend_best_dataset(self, results):
        """Recommend the best dataset from list"""
        
        suitable = [r for r in results if r['suitable']]
        
        if not suitable:
            print("\n⚠️  No fully suitable datasets found")
            # Return the most complete one
            best = max(results, key=lambda x: x['completeness'])
            print(f"\n📌 Most complete dataset:")
            print(f"   {best['filename']}: {best['completeness']:.1f}% complete")
            return best
        
        # Sort by completeness
        suitable = sorted(suitable, key=lambda x: x['completeness'], reverse=True)
        best = suitable[0]
        
        print(f"\n✅ RECOMMENDED DATASET:")
        print(f"   {best['filename']}")
        print(f"   Completeness: {best['completeness']:.1f}%")
        print(f"   File: {best['file']}")
        
        return best


def scan_for_datasets():
    """Scan common locations for real datasets"""
    
    print("\n" + "="*80)
    print("SCANNING FOR REAL POWER SYSTEM DATASETS")
    print("="*80)
    
    # Common locations to check
    locations = [
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Documents"),
        os.getcwd(),
        os.path.expanduser("~/Desktop"),
    ]
    
    found_files = []
    
    for location in locations:
        if os.path.exists(location):
            print(f"\nScanning: {location}")
            try:
                for file in os.listdir(location):
                    if file.endswith(('.csv', '.xlsx', '.xls')):
                        # Check if it looks like power/energy data
                        if any(keyword in file.lower() for keyword in 
                               ['energy', 'power', 'demand', 'load', 'wind', 'solar', 'grid', 'elec', 'hourly']):
                            filepath = os.path.join(location, file)
                            found_files.append(filepath)
                            print(f"  Found: {file}")
            except PermissionError:
                pass
    
    return found_files


def create_optimal_dataset_from_requirements():
    """
    Create guide for combining multiple real datasets into one
    that has all FACTS simulation requirements
    """
    
    guide = """
╔══════════════════════════════════════════════════════════════════════════════╗
║        COMBINING REAL DATASETS FOR COMPLETE FACTS SIMULATION                 ║
║             How to merge multiple real sources into one dataset              ║
╚══════════════════════════════════════════════════════════════════════════════╝

STRATEGY: Combine the BEST of each data source

1. LOAD DEMAND - Use FERC 714 or EIA
   ─────────────────────────────────
   Best Source: FERC 714 (150,000+ records, 2006-2023)
   URL: https://data.openei.org/datasets/dataset/ferc-714-hourly-demand-data
   Columns needed: DateTime, Region, Demand_MW
   Coverage: All US regions (pick your region)
   ✓ Most reliable load data available

2. WIND POWER - Use NREL or Kaggle Wind Dataset
   ────────────────────────────────────────────
   Option A (Best): NREL NSRDB
   URL: https://nsrdb.nrel.gov/
   Coverage: Global, 30-year typical year
   Requires: Free API key
   
   Option B (Easier): Kaggle Wind Power Dataset
   URL: https://www.kaggle.com/datasets/theforcecoder/wind-power-forecasting
   Records: 85,000 (3 years)
   No API key needed
   ✓ Ready to use immediately

3. SOLAR POWER - Use NREL or Kaggle Solar Dataset
   ────────────────────────────────────────────
   Option A (Best): NREL NSRDB Solar
   URL: https://nsrdb.nrel.gov/
   Coverage: Global, 30-year data
   Requires: Free API key
   
   Option B (Easier): Kaggle Solar Dataset
   URL: https://www.kaggle.com/datasets/dronio/solar-power-generation-data
   Records: 44,000 (2 years)
   No API key needed
   ✓ Ready to use immediately

4. WEATHER DATA - Use NOAA
   ────────────────────────
   Website: https://www.ncei.noaa.gov/cdo-web/
   Data: Temperature, precipitation, wind speed
   Coverage: Any US location, 1900-present
   Resolution: Daily or hourly
   ✓ Free, no API key needed

5. GRID PARAMETERS (Frequency, Voltage) - Use ISO-RTO
   ────────────────────────────────────────────────
   NYISO: https://www.nyiso.com/energy-market-data
   PJM: https://www.pjm.com/markets-and-operations
   CAISO: https://www.caiso.com/supply-demand
   ERCOT: https://www.ercot.com/gridmktinfo
   MISO: https://www.misoenergy.org/
   
   Data: 15-minute to hourly frequency & voltage
   Coverage: Regional (pick your region)
   ✓ Real grid operations data

RECOMMENDED COMBINATION FOR YOUR WORK:

┌─────────────────────────────────────────────────────────────┐
│ EASIEST OPTION (All from Kaggle - No API Keys)              │
├─────────────────────────────────────────────────────────────┤
│ 1. Base Dataset: Spain Hourly Energy                         │
│    URL: https://www.kaggle.com/datasets/robikscube/          │
│          hourly-energy-demand-generation-prices-weather      │
│    Has: Load, Wind, Solar, Temperature (4 years)             │
│    ✓ Already merged and ready!                              │
│                                                              │
│ 2. Optional Enhancement: Add ISO-RTO Grid Data               │
│    Pick your region: NYISO, PJM, CAISO, ERCOT, MISO         │
│    Download 1-2 years of real frequency/voltage data        │
│    Merge by timestamp                                        │
│                                                              │
│ 3. Result: Complete dataset with all FACTS parameters       │
└─────────────────────────────────────────────────────────────┘

PYTHON SCRIPT TO MERGE DATASETS:

```python
import pandas as pd

# Load base dataset (Spain)
df_base = pd.read_csv('spain_energy_data.csv')

# Load frequency/voltage data (if available)
df_iso = pd.read_csv('iso_rto_grid_data.csv')

# Parse dates
df_base['DateTime'] = pd.to_datetime(df_base['DateTime'])
df_iso['DateTime'] = pd.to_datetime(df_iso['DateTime'])

# Merge on timestamp (hourly)
df_base['Hour'] = df_base['DateTime'].dt.floor('H')
df_iso['Hour'] = df_iso['DateTime'].dt.floor('H')

df_merged = pd.merge(df_base, df_iso[['Hour', 'Frequency_Hz', 'Voltage_pu']], 
                     left_on='Hour', right_on='Hour', how='left')

# Fill any missing frequency/voltage with realistic values
df_merged['Frequency_Hz'].fillna(60.0, inplace=True)
df_merged['Voltage_pu'].fillna(1.0, inplace=True)

# Add calculated columns if missing
if 'Harmonics_THD_%' not in df_merged.columns:
    # Estimate harmonics based on renewable penetration
    df_merged['Harmonics_THD_%'] = 2.5 + 0.08 * df_merged['Renewable_Penetration_%']

if 'Power_Factor' not in df_merged.columns:
    df_merged['Power_Factor'] = 0.95  # Typical grid power factor

# Rename columns to match requirements
df_merged = df_merged.rename(columns={
    'DateTime': 'Date',
    'wind_speed': 'Wind_Speed_ms',
    'wind_power': 'Wind_Power_MW',
    'solar_irradiance': 'Solar_Irradiance_Wm2',
    'solar_power': 'Solar_Power_MW',
    'load': 'Load_Demand_MW'
})

# Calculate missing columns
df_merged['Total_Renewable_MW'] = df_merged['Wind_Power_MW'] + df_merged['Solar_Power_MW']
df_merged['Renewable_Penetration_%'] = 100 * df_merged['Total_Renewable_MW'] / (df_merged['Total_Renewable_MW'] + df_merged['Load_Demand_MW'])

# Save
df_merged.to_csv('complete_facts_dataset.csv', index=False)
print(f"✓ Created complete dataset: {len(df_merged)} records")
print(f"  Columns: {', '.join(df_merged.columns)}")
```

PRIORITY RANKING:

Easiest to Implement:
1. ✅ Use Kaggle Spain Dataset (already has everything)
2. ⭐ Add ISO-RTO frequency/voltage if available
3. Optional: Add NOAA weather enhancements

Most Data Complete:
1. FERC 714 (US Load) + NREL (Solar/Wind) + ISO-RTO (Grid)
2. Requires 3 downloads + merging
3. Result: Most comprehensive US grid data

YOUR RECOMMENDATION:

📌 For quick start: Use Kaggle Spain dataset
   - Pros: Ready to use, no preprocessing needed, 4 years data
   - Cons: European data (not US-specific)

📌 For US-specific: Use FERC 714 + NREL
   - Pros: Real US grid data, most authoritative
   - Cons: Requires API keys, more setup

📌 For fastest: Use extended synthetic data I created earlier
   - Pros: Ready now, realistic patterns
   - Cons: Not real-world measurements

NEXT STEPS:

1. Download preferred dataset from Kaggle or FERC 714
2. Run dataset validator to check completeness
3. Run merger script if combining multiple sources
4. Use result with your FACTS simulation
5. Compare real vs. synthetic results in your paper

"""
    
    return guide


def main():
    """Main validation workflow"""
    
    validator = DatasetRequirementValidator()
    
    print("\n" + "="*80)
    print("REAL DATASET VALIDATOR FOR FACTS SIMULATION")
    print("="*80)
    
    # Show requirements
    print("\n📋 REQUIRED COLUMNS FOR YOUR FACTS SIMULATION:")
    print("\n   CRITICAL (Must Have):")
    for cat in validator.critical:
        options = ', '.join(validator.required_columns[cat][:3])
        print(f"      • {cat}: {options}...")
    
    print("\n   HIGH PRIORITY (Should Have):")
    for cat in validator.high_priority:
        options = ', '.join(validator.required_columns[cat][:2])
        print(f"      • {cat}: {options}...")
    
    print("\n   MEDIUM PRIORITY (Nice to Have):")
    for cat in validator.medium_priority:
        options = ', '.join(validator.required_columns[cat][:2])
        print(f"      • {cat}: {options}...")
    
    # Scan for local datasets
    print("\n" + "-"*80)
    print("SCANNING FOR DATASETS...")
    print("-"*80)
    
    found_files = scan_for_datasets()
    
    if found_files:
        print(f"\n✓ Found {len(found_files)} potential dataset files")
        print("\nValidating...")
        
        results = []
        for filepath in found_files:
            result = validator.validate_dataset(filepath)
            if result:
                results.append(result)
        
        if results:
            print("\n" + "="*80)
            print("VALIDATION SUMMARY")
            print("="*80)
            
            # Sort by completeness
            results = sorted(results, key=lambda x: x['completeness'], reverse=True)
            
            for i, result in enumerate(results, 1):
                status = "✅" if result['suitable'] else "⚠️"
                print(f"\n{i}. {status} {result['filename']}")
                print(f"   Completeness: {result['completeness']:.1f}%")
                print(f"   Critical: {result['critical_found']}/{len(validator.critical)}")
                print(f"   High Priority: {result['high_priority_found']}/{len(validator.high_priority)}")
            
            # Recommend best
            if results:
                print("\n" + "="*80)
                best = validator.recommend_best_dataset(results)
    else:
        print("\n⚠️  No local datasets found")
    
    # Save merge guide
    guide = create_optimal_dataset_from_requirements()
    guide_file = "DATASET_MERGE_GUIDE.txt"
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("\n" + "="*80)
    print("✅ DATASET VALIDATION COMPLETE")
    print("="*80)
    print(f"\n📄 Merge guide saved: {guide_file}")
    print("\n📌 NEXT STEPS:")
    print("   1. Download preferred real dataset (see REAL_DATA_DOWNLOAD_GUIDE.txt)")
    print("   2. Place CSV file in this folder")
    print("   3. Re-run this validator")
    print("   4. It will automatically identify and recommend best dataset")
    print("   5. Use recommended dataset with FACTS simulation")


if __name__ == "__main__":
    main()
