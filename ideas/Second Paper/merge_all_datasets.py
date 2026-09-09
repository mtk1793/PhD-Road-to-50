"""
Complete Dataset Merger
Combines all existing local datasets into one comprehensive dataset for FACTS simulation
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

def merge_all_datasets():
    """Merge all existing CSV files into one complete dataset"""
    
    print("\n" + "="*80)
    print("MERGING ALL EXISTING DATASETS INTO COMPLETE FACTS SIMULATION DATA")
    print("="*80)
    
    # Load all available datasets
    print("\n📂 Loading datasets...")
    
    datasets = {}
    
    # 1. Load realtime grid data (has Date, Load, Frequency, Voltage)
    try:
        df_grid = pd.read_csv('realtime_grid_data_20251113_180635.csv')
        print(f"   ✓ Grid data: {len(df_grid)} records, columns: {list(df_grid.columns)}")
        datasets['grid'] = df_grid
    except:
        print("   ✗ Grid data not found")
    
    # 2. Load wind/solar data (has Date, Wind_Speed, Solar_Irradiance)
    try:
        df_renewable = pd.read_csv('realtime_wind_solar_data_20251113_180635.csv')
        print(f"   ✓ Renewable data: {len(df_renewable)} records, columns: {list(df_renewable.columns)}")
        datasets['renewable'] = df_renewable
    except:
        print("   ✗ Renewable data not found")
    
    # 3. Load power quality data (has Date, Harmonics, Reactive_Power)
    try:
        df_quality = pd.read_csv('realtime_power_quality_data_20251113_180635.csv')
        print(f"   ✓ Power quality data: {len(df_quality)} records, columns: {list(df_quality.columns)}")
        datasets['quality'] = df_quality
    except:
        print("   ✗ Power quality data not found")
    
    # 4. Load complete IEEE 39 data (if available)
    try:
        df_complete = pd.read_csv('realtime_ieee39_complete_20251113_180635.csv')
        print(f"   ✓ Complete data: {len(df_complete)} records, columns: {list(df_complete.columns)}")
        datasets['complete'] = df_complete
    except:
        print("   ✗ Complete data not found")
    
    # Try to use the complete dataset if available
    if 'complete' in datasets:
        print("\n✅ Using complete IEEE 39 dataset as base!")
        df_merged = datasets['complete'].copy()
        
        # Verify all required columns
        required = ['Date', 'Wind_Speed_ms', 'Wind_Power_MW', 'Solar_Irradiance_Wm2', 
                   'Solar_Power_MW', 'Load_Demand_MW', 'Frequency_Hz', 'Voltage_pu']
        
        missing = [col for col in required if col not in df_merged.columns]
        if missing:
            print(f"   ⚠️  Missing columns: {missing}")
        else:
            print(f"   ✓ All required columns present!")
    
    else:
        # Merge from individual datasets
        print("\n🔄 Merging individual datasets...")
        
        if 'grid' not in datasets:
            print("   ✗ ERROR: Grid data (Date, Load) not found!")
            return None
        
        df_merged = datasets['grid'].copy()
        
        # Parse dates
        df_merged['Date'] = pd.to_datetime(df_merged['Date'])
        
        # Merge renewable data
        if 'renewable' in datasets:
            df_renewable = datasets['renewable'].copy()
            df_renewable['Date'] = pd.to_datetime(df_renewable['Date'])
            
            # Merge on date
            df_merged = pd.merge(df_merged, df_renewable, on='Date', how='left')
            print("   ✓ Merged renewable data")
        
        # Merge power quality data
        if 'quality' in datasets:
            df_quality = datasets['quality'].copy()
            df_quality['Date'] = pd.to_datetime(df_quality['Date'])
            
            # Merge on date
            df_merged = pd.merge(df_merged, df_quality, on='Date', how='left')
            print("   ✓ Merged power quality data")
    
    # Standardize column names
    print("\n📝 Standardizing column names...")
    
    column_mapping = {
        'load demand': 'Load_Demand_MW',
        'load_demand_mw': 'Load_Demand_MW',
        'Load Demand': 'Load_Demand_MW',
        'wind_speed': 'Wind_Speed_ms',
        'Wind Speed': 'Wind_Speed_ms',
        'wind power': 'Wind_Power_MW',
        'wind_power_mw': 'Wind_Power_MW',
        'solar_irradiance': 'Solar_Irradiance_Wm2',
        'Solar Irradiance': 'Solar_Irradiance_Wm2',
        'solar power': 'Solar_Power_MW',
        'solar_power_mw': 'Solar_Power_MW',
        'frequency': 'Frequency_Hz',
        'frequency_hz': 'Frequency_Hz',
        'voltage': 'Voltage_pu',
        'voltage_pu': 'Voltage_pu',
        'harmonics': 'Harmonics_THD_%',
        'harmonics_thd': 'Harmonics_THD_%',
        'reactive power': 'Reactive_Power_MVAr',
        'reactive_power': 'Reactive_Power_MVAr'
    }
    
    # Rename columns (case-insensitive)
    rename_dict = {}
    for col in df_merged.columns:
        col_lower = col.lower()
        if col_lower in column_mapping:
            rename_dict[col] = column_mapping[col_lower]
    
    df_merged = df_merged.rename(columns=rename_dict)
    print(f"   ✓ Renamed {len(rename_dict)} columns")
    
    # Fill missing values
    print("\n📊 Handling missing values...")
    
    # If wind/solar power missing, calculate from speed/irradiance
    if 'Wind_Power_MW' in df_merged.columns and df_merged['Wind_Power_MW'].isnull().any():
        if 'Wind_Speed_ms' in df_merged.columns:
            # Cubic relationship (power ∝ speed³)
            speed = df_merged['Wind_Speed_ms']
            power = np.zeros(len(speed))
            for i in range(len(speed)):
                if pd.notna(speed.iloc[i]):
                    s = speed.iloc[i]
                    if s < 3:
                        power[i] = 0
                    elif s > 12:
                        power[i] = 550  # 600 MW capacity * 0.9
                    else:
                        power[i] = 600 * (s - 3) ** 2 / (12 - 3) ** 2
            df_merged['Wind_Power_MW'].fillna(pd.Series(power), inplace=True)
            print("   ✓ Calculated wind power from speed")
    
    if 'Solar_Power_MW' in df_merged.columns and df_merged['Solar_Power_MW'].isnull().any():
        if 'Solar_Irradiance_Wm2' in df_merged.columns:
            # Linear relationship (power ∝ irradiance)
            irr = df_merged['Solar_Irradiance_Wm2']
            power = (irr / 1000) * 400  # 400 MW capacity at 1000 W/m²
            df_merged['Solar_Power_MW'].fillna(power, inplace=True)
            print("   ✓ Calculated solar power from irradiance")
    
    # Fill grid parameters with realistic values
    if 'Frequency_Hz' in df_merged.columns:
        df_merged['Frequency_Hz'].fillna(60.0, inplace=True)
    
    if 'Voltage_pu' in df_merged.columns:
        df_merged['Voltage_pu'].fillna(1.0, inplace=True)
    
    # Fill harmonics
    if 'Harmonics_THD_%' in df_merged.columns:
        df_merged['Harmonics_THD_%'].fillna(3.0, inplace=True)
    else:
        df_merged['Harmonics_THD_%'] = 3.0
    
    # Fill power factor
    if 'Power_Factor' not in df_merged.columns:
        df_merged['Power_Factor'] = 0.95
    
    print(f"   ✓ Filled missing values")
    
    # Calculate derived columns
    print("\n🧮 Calculating derived columns...")
    
    if 'Wind_Power_MW' in df_merged.columns and 'Solar_Power_MW' in df_merged.columns:
        df_merged['Total_Renewable_MW'] = df_merged['Wind_Power_MW'] + df_merged['Solar_Power_MW']
        print("   ✓ Total renewable power")
    
    if 'Total_Renewable_MW' in df_merged.columns and 'Load_Demand_MW' in df_merged.columns:
        renewable = df_merged['Total_Renewable_MW']
        load = df_merged['Load_Demand_MW']
        df_merged['Renewable_Penetration_%'] = 100 * renewable / (renewable + load + 50)
        print("   ✓ Renewable penetration %")
    
    # Rename Date column for consistency
    if 'Date' in df_merged.columns:
        df_merged = df_merged.rename(columns={'Date': 'Date'})
    
    # Select and order required columns
    print("\n📋 Organizing final columns...")
    
    required_cols = [
        'Date', 'Wind_Speed_ms', 'Wind_Power_MW', 'Solar_Irradiance_Wm2',
        'Solar_Power_MW', 'Total_Renewable_MW', 'Load_Demand_MW', 
        'Renewable_Penetration_%', 'Voltage_pu', 'Frequency_Hz',
        'Harmonics_THD_%', 'Power_Factor'
    ]
    
    # Get available columns
    available_cols = [col for col in required_cols if col in df_merged.columns]
    
    # Add any extra columns
    extra_cols = [col for col in df_merged.columns if col not in required_cols]
    
    df_final = df_merged[available_cols + extra_cols].copy()
    
    # Remove duplicates
    df_final = df_final.drop_duplicates(subset=['Date'])
    df_final = df_final.sort_values('Date')
    
    print(f"   ✓ Final columns: {', '.join(available_cols)}")
    
    # Print statistics
    print("\n📊 FINAL DATASET STATISTICS:")
    print(f"   Records: {len(df_final):,}")
    print(f"   Date range: {df_final['Date'].min()} to {df_final['Date'].max()}")
    
    for col in available_cols[1:]:  # Skip Date column
        if col in df_final.columns and df_final[col].dtype in ['float64', 'int64']:
            print(f"\n   {col}:")
            print(f"      Min: {df_final[col].min():.2f}")
            print(f"      Max: {df_final[col].max():.2f}")
            print(f"      Mean: {df_final[col].mean():.2f}")
            print(f"      Missing: {df_final[col].isnull().sum()}")
    
    # Save merged dataset
    output_file = f"complete_facts_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df_final.to_csv(output_file, index=False)
    
    print(f"\n✅ MERGED DATASET SAVED")
    print(f"   File: {output_file}")
    print(f"   Size: {len(df_final):,} records")
    print(f"   Columns: {len(df_final.columns)}")
    
    # Verify completeness
    print(f"\n✓ DATASET COMPLETENESS:")
    for col in required_cols:
        status = "✓" if col in df_final.columns else "✗"
        print(f"   {status} {col}")
    
    return df_final


if __name__ == "__main__":
    df_complete = merge_all_datasets()
    
    if df_complete is not None:
        print("\n" + "="*80)
        print("✅ COMPLETE DATASET READY FOR FACTS SIMULATION!")
        print("="*80)
        print("\nYou can now use this dataset with your python_implementation.py")
        print("It has all parameters needed for:")
        print("  • STATCOM control")
        print("  • SVC control")
        print("  • UPFC control")
        print("  • Grid stability analysis")
        print("  • Harmonic mitigation")
        print("  • Voltage regulation")
