"""
Extended Real-Time Dataset Generator
Generates comprehensive datasets spanning multiple years with realistic grid dynamics
Suitable for long-term FACTS device performance evaluation and AI model training
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class ExtendedDatasetGenerator:
    """Generate extended realistic power system datasets (1-5 years of hourly data)"""
    
    def __init__(self):
        self.start_date = datetime(2021, 1, 1)
        self.seed = 42
        np.random.seed(self.seed)
        
    def generate_wind_data(self, num_days=365, capacity_mw=600):
        """
        Generate realistic wind power data with seasonal variation
        Based on typical wind farm generation patterns
        """
        num_hours = num_days * 24
        hours = np.arange(num_hours)
        
        # Seasonal variation (winter stronger winds)
        day_of_year = (hours // 24) % 365
        seasonal_factor = 0.7 + 0.3 * np.sin(2 * np.pi * day_of_year / 365 - np.pi/2)
        
        # Daily variation (more wind at night)
        hourly_factor = 0.5 + 0.5 * np.cos(2 * np.pi * (hours % 24) / 24)
        
        # Random fluctuations
        noise = np.random.normal(0, 0.15, num_hours)
        
        # Wind speed (m/s)
        base_speed = 7.5  # Average wind speed
        wind_speed = base_speed * (seasonal_factor * hourly_factor + noise)
        wind_speed = np.clip(wind_speed, 0, 15)
        
        # Wind power (cubic relationship, cut-in at 3 m/s, cut-out at 12 m/s)
        wind_power = np.zeros(num_hours)
        for i in range(num_hours):
            if wind_speed[i] < 3:
                wind_power[i] = 0
            elif wind_speed[i] > 12:
                wind_power[i] = capacity_mw * 0.9  # Slightly below rated
            else:
                wind_power[i] = capacity_mw * (wind_speed[i] - 3) ** 2 / (12 - 3) ** 2
        
        wind_power = np.clip(wind_power, 0, capacity_mw)
        return wind_speed, wind_power
    
    def generate_solar_data(self, num_days=365, capacity_mw=400):
        """
        Generate realistic solar PV generation with cloud effects
        Based on typical solar farm generation patterns
        """
        num_hours = num_days * 24
        hours = np.arange(num_hours)
        
        # Seasonal variation (more solar in summer)
        day_of_year = (hours // 24) % 365
        seasonal_factor = 0.5 + 0.5 * np.sin(2 * np.pi * day_of_year / 365 + np.pi/2)
        
        # Daily cycle (solar only during daylight)
        hour_of_day = hours % 24
        daily_pattern = np.maximum(0, np.sin(np.pi * (hour_of_day - 6) / 12))
        
        # Cloud cover variation (random intermittency)
        cloud_cover = np.random.beta(2, 5, num_hours)  # More clear days than cloudy
        
        # Solar irradiance (W/m²)
        base_irradiance = 800  # Peak irradiance
        solar_irradiance = base_irradiance * seasonal_factor * daily_pattern * cloud_cover
        
        # Solar power (MW) - assuming ~200 MW per GW at 1000 W/m²
        solar_power = (solar_irradiance / 1000) * capacity_mw
        solar_power = np.clip(solar_power, 0, capacity_mw)
        
        return solar_irradiance, solar_power
    
    def generate_load_data(self, num_days=365, base_load_mw=485):
        """
        Generate realistic electricity load demand with temporal patterns
        Based on typical utility load curves
        """
        num_hours = num_days * 24
        hours = np.arange(num_hours)
        
        # Seasonal variation (summer higher for cooling)
        day_of_year = (hours // 24) % 365
        seasonal_factor = 0.85 + 0.15 * np.sin(2 * np.pi * day_of_year / 365 + np.pi/2)
        
        # Weekly pattern (lower on weekends)
        day_of_week = (hours // 24) % 7
        weekly_factor = np.where(day_of_week < 5, 1.0, 0.9)
        
        # Daily pattern (peak morning and evening)
        hour_of_day = hours % 24
        daily_pattern = 0.6 + 0.3 * np.cos(2 * np.pi * (hour_of_day - 14) / 24) + 0.15 * np.sin(4 * np.pi * (hour_of_day - 8) / 24)
        daily_pattern = np.clip(daily_pattern, 0.5, 1.2)
        
        # Random variations
        noise = np.random.normal(0, 0.05, num_hours)
        
        load = base_load_mw * seasonal_factor * weekly_factor * daily_pattern * (1 + noise)
        load = np.clip(load, base_load_mw * 0.3, base_load_mw * 1.6)
        
        return load
    
    def generate_grid_dynamics(self, num_hours, load_mw, renewable_mw):
        """Generate realistic grid frequency, voltage, and harmonics based on power balance"""
        
        # Frequency deviation based on mismatch (simplified swing equation)
        imbalance = renewable_mw - load_mw
        frequency_deviation = -0.2 * (imbalance / 1000)  # Droop characteristic
        frequency_deviation = np.clip(frequency_deviation, -0.5, 0.5)
        
        # Add transient response and damping
        freq = np.zeros(num_hours)
        freq[0] = 60.0 + frequency_deviation[0]
        for i in range(1, num_hours):
            # Exponential recovery with time constant ~10 seconds (proportional to 1 hour)
            freq[i] = 60.0 + frequency_deviation[i] * 0.3 + freq[i-1] * 0.7
        
        # Add small random oscillations
        freq += np.random.normal(0, 0.02, num_hours)
        freq = np.clip(freq, 59.5, 60.5)
        
        # Voltage regulation (simplified - depends on reactive power)
        voltage = 1.0 - 0.03 * (renewable_mw / 1000) + 0.05 * np.random.normal(0, 1, num_hours)
        voltage = np.clip(voltage, 0.92, 1.08)
        
        # Harmonics increase with renewable penetration (power electronics)
        renewable_pct = 100 * renewable_mw / (renewable_mw + load_mw)
        thd = 2.5 + 0.08 * renewable_pct + 2 * np.random.normal(0, 1, num_hours)
        thd = np.clip(thd, 2.0, 12.0)
        
        # Power factor depends on reactive power compensation
        pf = 0.92 + 0.08 * np.random.normal(0, 1, num_hours)
        pf = np.clip(pf, 0.80, 1.00)
        
        return freq, voltage, thd, pf
    
    def generate_dataset(self, years=2, capacity_wind_mw=600, capacity_solar_mw=400):
        """
        Generate complete extended dataset
        
        Parameters:
        -----------
        years : int
            Number of years to generate (1-5 recommended)
        capacity_wind_mw : int
            Total wind farm capacity in MW
        capacity_solar_mw : int
            Total solar farm capacity in MW
        
        Returns:
        --------
        pd.DataFrame : Complete dataset with all parameters
        """
        
        num_days = years * 365
        num_hours = num_days * 24
        
        print(f"Generating {years}-year extended dataset ({num_hours:,} hourly records)...")
        
        # Generate renewable resources
        print("  - Generating wind data...")
        wind_speed, wind_power = self.generate_wind_data(num_days, capacity_wind_mw)
        
        print("  - Generating solar data...")
        solar_irradiance, solar_power = self.generate_solar_data(num_days, capacity_solar_mw)
        
        # Generate load
        print("  - Generating load demand...")
        load_demand = self.generate_load_data(num_days, base_load_mw=485)
        
        # Calculate totals
        total_renewable = wind_power + solar_power
        renewable_penetration = 100 * total_renewable / (total_renewable + load_demand + 50)  # +50 for losses
        
        # Generate grid dynamics
        print("  - Generating grid dynamics...")
        frequency, voltage, harmonics, power_factor = self.generate_grid_dynamics(
            num_hours, load_demand, total_renewable
        )
        
        # Create datetime index
        dates = [self.start_date + timedelta(hours=i) for i in range(num_hours)]
        
        # Create DataFrame
        df = pd.DataFrame({
            'Date': dates,
            'Wind_Speed_ms': wind_speed,
            'Wind_Power_MW': wind_power,
            'Solar_Irradiance_Wm2': solar_irradiance,
            'Solar_Power_MW': solar_power,
            'Total_Renewable_MW': total_renewable,
            'Load_Demand_MW': load_demand,
            'Renewable_Penetration_%': renewable_penetration,
            'Voltage_pu': voltage,
            'Frequency_Hz': frequency,
            'Harmonics_THD_%': harmonics,
            'Power_Factor': power_factor
        })
        
        print(f"✓ Dataset generated: {len(df):,} records")
        return df
    
    def generate_multiple_datasets(self, years_list=[1, 2, 3, 5]):
        """Generate multiple datasets of different sizes"""
        datasets = {}
        
        for years in years_list:
            print(f"\n{'='*60}")
            print(f"Generating {years}-year dataset")
            print(f"{'='*60}")
            
            df = self.generate_dataset(years=years)
            filename = f"extended_realtime_ieee39_{years}year_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = os.path.join(os.path.dirname(__file__), filename)
            
            # Save to CSV
            df.to_csv(filepath, index=False)
            print(f"✓ Saved: {filename}")
            
            # Calculate and print statistics
            self.print_statistics(df, years)
            
            datasets[f"{years}year"] = {
                'filepath': filepath,
                'records': len(df),
                'start_date': df['Date'].min(),
                'end_date': df['Date'].max(),
                'statistics': self.calculate_statistics(df)
            }
        
        return datasets
    
    def calculate_statistics(self, df):
        """Calculate dataset statistics"""
        stats = {
            'wind': {
                'min': float(df['Wind_Power_MW'].min()),
                'max': float(df['Wind_Power_MW'].max()),
                'mean': float(df['Wind_Power_MW'].mean()),
                'std': float(df['Wind_Power_MW'].std())
            },
            'solar': {
                'min': float(df['Solar_Power_MW'].min()),
                'max': float(df['Solar_Power_MW'].max()),
                'mean': float(df['Solar_Power_MW'].mean()),
                'std': float(df['Solar_Power_MW'].std())
            },
            'load': {
                'min': float(df['Load_Demand_MW'].min()),
                'max': float(df['Load_Demand_MW'].max()),
                'mean': float(df['Load_Demand_MW'].mean()),
                'std': float(df['Load_Demand_MW'].std())
            },
            'penetration': {
                'min': float(df['Renewable_Penetration_%'].min()),
                'max': float(df['Renewable_Penetration_%'].max()),
                'mean': float(df['Renewable_Penetration_%'].mean())
            },
            'frequency': {
                'min': float(df['Frequency_Hz'].min()),
                'max': float(df['Frequency_Hz'].max()),
                'mean': float(df['Frequency_Hz'].mean())
            },
            'voltage': {
                'min': float(df['Voltage_pu'].min()),
                'max': float(df['Voltage_pu'].max()),
                'mean': float(df['Voltage_pu'].mean())
            }
        }
        return stats
    
    def print_statistics(self, df, years):
        """Print dataset statistics"""
        print(f"\n📊 STATISTICS ({years}-year dataset)")
        print(f"{'─'*60}")
        
        print(f"\n🌬️  WIND POWER (MW):")
        print(f"  Min: {df['Wind_Power_MW'].min():.2f}")
        print(f"  Max: {df['Wind_Power_MW'].max():.2f}")
        print(f"  Mean: {df['Wind_Power_MW'].mean():.2f}")
        print(f"  Std: {df['Wind_Power_MW'].std():.2f}")
        
        print(f"\n☀️  SOLAR POWER (MW):")
        print(f"  Min: {df['Solar_Power_MW'].min():.2f}")
        print(f"  Max: {df['Solar_Power_MW'].max():.2f}")
        print(f"  Mean: {df['Solar_Power_MW'].mean():.2f}")
        print(f"  Std: {df['Solar_Power_MW'].std():.2f}")
        
        print(f"\n⚡ LOAD DEMAND (MW):")
        print(f"  Min: {df['Load_Demand_MW'].min():.2f}")
        print(f"  Max: {df['Load_Demand_MW'].max():.2f}")
        print(f"  Mean: {df['Load_Demand_MW'].mean():.2f}")
        print(f"  Std: {df['Load_Demand_MW'].std():.2f}")
        
        print(f"\n🌍 RENEWABLE PENETRATION (%):")
        print(f"  Min: {df['Renewable_Penetration_%'].min():.2f}%")
        print(f"  Max: {df['Renewable_Penetration_%'].max():.2f}%")
        print(f"  Mean: {df['Renewable_Penetration_%'].mean():.2f}%")
        
        print(f"\n📡 FREQUENCY (Hz):")
        print(f"  Min: {df['Frequency_Hz'].min():.4f}")
        print(f"  Max: {df['Frequency_Hz'].max():.4f}")
        print(f"  Mean: {df['Frequency_Hz'].mean():.4f}")
        
        print(f"\n⚙️  VOLTAGE (p.u.):")
        print(f"  Min: {df['Voltage_pu'].min():.4f}")
        print(f"  Max: {df['Voltage_pu'].max():.4f}")
        print(f"  Mean: {df['Voltage_pu'].mean():.4f}")
        
        print(f"\n🔤 HARMONICS (THD %):")
        print(f"  Min: {df['Harmonics_THD_%'].min():.2f}%")
        print(f"  Max: {df['Harmonics_THD_%'].max():.2f}%")
        print(f"  Mean: {df['Harmonics_THD_%'].mean():.2f}%")
        
        print(f"\n📊 Total Records: {len(df):,}")
        print(f"   Date Range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"   Duration: {(df['Date'].max() - df['Date'].min()).days} days")


def main():
    """Generate extended datasets of various sizes"""
    
    print("\n" + "="*60)
    print("EXTENDED REAL-TIME DATASET GENERATOR")
    print("Generating comprehensive datasets for FACTS device studies")
    print("="*60)
    
    generator = ExtendedDatasetGenerator()
    
    # Generate datasets: 1-year, 2-year, 3-year, 5-year
    datasets = generator.generate_multiple_datasets(years_list=[1, 2, 3, 5])
    
    # Save summary
    summary = {
        'generated_at': datetime.now().isoformat(),
        'datasets': datasets,
        'notes': [
            '1-year dataset: 8,760 records - suitable for annual analysis',
            '2-year dataset: 17,520 records - covers seasonal variations',
            '3-year dataset: 26,280 records - ideal for AI model training',
            '5-year dataset: 43,800 records - comprehensive long-term analysis',
            'All datasets include: wind, solar, load, frequency, voltage, harmonics',
            'Data is realistic with seasonal and daily patterns',
            'Suitable for FACTS device performance evaluation'
        ]
    }
    
    summary_file = f"extended_datasets_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    
    print(f"\n✓ Summary saved: {summary_file}")
    
    print("\n" + "="*60)
    print("✅ EXTENDED DATASETS GENERATION COMPLETE")
    print("="*60)
    print("\nGenerated files:")
    for key, dataset_info in datasets.items():
        print(f"  • {key}: {dataset_info['records']:,} records")
        print(f"    Path: {dataset_info['filepath']}")
    
    print("\n📝 USAGE RECOMMENDATIONS:")
    print("  • 1-year: Quick testing, single seasonal cycle")
    print("  • 2-year: Better seasonal coverage, trend analysis")
    print("  • 3-year: AI training, comprehensive patterns")
    print("  • 5-year: Long-term reliability, rare event capture")
    
    return datasets


if __name__ == "__main__":
    main()
