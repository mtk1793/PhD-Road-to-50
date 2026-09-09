#!/usr/bin/env python3
"""
Integration Script: Real-Time Data with FACTS Device Simulations
Replaces synthetic data generation with real-time data for IEEE 39-Bus System
"""

import pandas as pd
import numpy as np
import glob
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealDataIntegrator:
    """Integrate real-time data with FACTS device simulations"""
    
    def __init__(self, data_folder='.'):
        """Initialize integrator"""
        self.data_folder = data_folder
        self.data = None
        self.data_source = None
        
    def load_latest_realtime_dataset(self):
        """Load the most recent real-time dataset"""
        logger.info("Loading latest real-time dataset...")
        
        # Find all complete datasets
        complete_files = glob.glob(os.path.join(self.data_folder, 'realtime_ieee39_complete_*.csv'))
        
        if not complete_files:
            logger.warning("No real-time datasets found. Falling back to synthetic data.")
            return None
        
        # Get most recent file
        latest_file = max(complete_files, key=os.path.getctime)
        logger.info(f"Loading dataset: {os.path.basename(latest_file)}")
        
        try:
            data = pd.read_csv(latest_file)
            data['Date'] = pd.to_datetime(data['Date'])
            self.data = data
            self.data_source = latest_file
            logger.info(f"Successfully loaded {len(data)} records from real-time data")
            return data
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return None
    
    def load_custom_dataset(self, filename):
        """Load a specific dataset"""
        logger.info(f"Loading custom dataset: {filename}")
        
        try:
            data = pd.read_csv(filename)
            data['Date'] = pd.to_datetime(data['Date'])
            self.data = data
            self.data_source = filename
            logger.info(f"Successfully loaded {len(data)} records")
            return data
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return None
    
    def validate_data(self):
        """Validate data quality"""
        logger.info("Validating data...")
        
        if self.data is None:
            logger.error("No data to validate")
            return False
        
        issues = []
        
        # Check for missing values
        missing = self.data.isnull().sum()
        if missing.sum() > 0:
            issues.append(f"Missing values detected:\n{missing[missing > 0]}")
        
        # Check for negative values in non-negative columns
        non_negative_cols = ['Wind_Speed_ms', 'Wind_Power_MW', 'Solar_Irradiance_Wm2', 
                            'Solar_Power_MW', 'Load_Demand_MW']
        for col in non_negative_cols:
            if col in self.data.columns:
                negatives = (self.data[col] < 0).sum()
                if negatives > 0:
                    issues.append(f"Negative values in {col}: {negatives} records")
        
        # Check for unrealistic frequency values
        if 'Frequency_Hz' in self.data.columns:
            freq_out = ((self.data['Frequency_Hz'] < 59.0) | (self.data['Frequency_Hz'] > 61.0)).sum()
            if freq_out > 0:
                issues.append(f"Unrealistic frequencies: {freq_out} records outside [59-61] Hz")
        
        # Check for unrealistic voltage values
        if 'Voltage_pu' in self.data.columns:
            volt_out = ((self.data['Voltage_pu'] < 0.9) | (self.data['Voltage_pu'] > 1.1)).sum()
            if volt_out > 0:
                issues.append(f"Unrealistic voltages: {volt_out} records outside [0.9-1.1] p.u.")
        
        if issues:
            logger.warning("Data validation issues found:")
            for issue in issues:
                logger.warning(f"  - {issue}")
            return False
        else:
            logger.info("✓ Data validation passed")
            return True
    
    def get_dataset_for_simulation(self):
        """Get cleaned and formatted data for simulation"""
        logger.info("Preparing data for simulation...")
        
        if self.data is None:
            logger.error("No data loaded")
            return None
        
        # Create working copy
        data = self.data.copy()
        
        # Forward fill any missing values
        data = data.fillna(method='ffill').fillna(method='bfill')
        
        # Ensure datetime index
        data['timestamp'] = data['Date']
        
        # Calculate additional parameters if not present
        if 'total_renewable' not in data.columns:
            data['total_renewable'] = (data.get('Wind_Power_MW', 0) + 
                                      data.get('Solar_Power_MW', 0))
        
        if 'net_load' not in data.columns:
            data['net_load'] = (data.get('Load_Demand_MW', 0) - 
                               data.get('total_renewable', 0))
        
        if 'renewable_penetration' not in data.columns:
            data['renewable_penetration'] = np.where(
                data.get('Load_Demand_MW', 1) > 0,
                data.get('total_renewable', 0) / data.get('Load_Demand_MW', 1),
                0
            )
        
        logger.info("Data preparation complete")
        return data
    
    def get_statistics(self):
        """Get comprehensive statistics"""
        logger.info("Calculating statistics...")
        
        if self.data is None:
            logger.error("No data loaded")
            return None
        
        data = self.data
        stats = {
            'data_points': len(data),
            'date_range': {
                'start': data['Date'].min().strftime('%Y-%m-%d %H:%M:%S'),
                'end': data['Date'].max().strftime('%Y-%m-%d %H:%M:%S'),
                'duration_hours': (data['Date'].max() - data['Date'].min()).total_seconds() / 3600
            },
            'wind': {
                'min': float(data.get('Wind_Speed_ms', [0]).min()),
                'max': float(data.get('Wind_Speed_ms', [0]).max()),
                'mean': float(data.get('Wind_Speed_ms', [0]).mean()),
                'std': float(data.get('Wind_Speed_ms', [0]).std()),
                'power_min': float(data.get('Wind_Power_MW', [0]).min()),
                'power_max': float(data.get('Wind_Power_MW', [0]).max()),
                'power_mean': float(data.get('Wind_Power_MW', [0]).mean())
            },
            'solar': {
                'irradiance_min': float(data.get('Solar_Irradiance_Wm2', [0]).min()),
                'irradiance_max': float(data.get('Solar_Irradiance_Wm2', [0]).max()),
                'irradiance_mean': float(data.get('Solar_Irradiance_Wm2', [0]).mean()),
                'power_min': float(data.get('Solar_Power_MW', [0]).min()),
                'power_max': float(data.get('Solar_Power_MW', [0]).max()),
                'power_mean': float(data.get('Solar_Power_MW', [0]).mean())
            },
            'load': {
                'min': float(data.get('Load_Demand_MW', [0]).min()),
                'max': float(data.get('Load_Demand_MW', [0]).max()),
                'mean': float(data.get('Load_Demand_MW', [0]).mean()),
                'std': float(data.get('Load_Demand_MW', [0]).std())
            },
            'grid': {
                'frequency_min': float(data.get('Frequency_Hz', [60]).min()),
                'frequency_max': float(data.get('Frequency_Hz', [60]).max()),
                'frequency_mean': float(data.get('Frequency_Hz', [60]).mean()),
                'voltage_min': float(data.get('Voltage_pu', [1.0]).min()),
                'voltage_max': float(data.get('Voltage_pu', [1.0]).max()),
                'voltage_mean': float(data.get('Voltage_pu', [1.0]).mean()),
                'harmonics_min': float(data.get('Harmonics_THD_%', [0]).min()),
                'harmonics_max': float(data.get('Harmonics_THD_%', [0]).max()),
                'harmonics_mean': float(data.get('Harmonics_THD_%', [0]).mean())
            },
            'renewable': {
                'penetration_min': float(data.get('Renewable_Penetration_%', [0]).min()),
                'penetration_max': float(data.get('Renewable_Penetration_%', [0]).max()),
                'penetration_mean': float(data.get('Renewable_Penetration_%', [0]).mean())
            }
        }
        
        return stats
    
    def export_for_simulation(self, output_filename=None):
        """Export data in format suitable for FACTS simulations"""
        
        if self.data is None:
            logger.error("No data to export")
            return None
        
        if output_filename is None:
            output_filename = f"ready_for_simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Prepare data
        export_data = self.get_dataset_for_simulation()
        
        # Save
        export_data.to_csv(output_filename, index=False)
        logger.info(f"Data exported to: {output_filename}")
        
        return output_filename
    
    def print_summary(self):
        """Print comprehensive summary"""
        
        if self.data is None:
            logger.error("No data loaded")
            return
        
        stats = self.get_statistics()
        
        print("\n" + "=" * 80)
        print("REAL-TIME DATA SUMMARY FOR IEEE 39-BUS SYSTEM")
        print("=" * 80 + "\n")
        
        print(f"Data Source: {os.path.basename(self.data_source)}")
        print(f"Total Records: {stats['data_points']}")
        print(f"Date Range: {stats['date_range']['start']} to {stats['date_range']['end']}")
        print(f"Duration: {stats['date_range']['duration_hours']:.1f} hours\n")
        
        print("WIND RESOURCES")
        print("-" * 80)
        print(f"  Wind Speed: {stats['wind']['min']:.2f} - {stats['wind']['max']:.2f} m/s "
              f"(avg: {stats['wind']['mean']:.2f} m/s)")
        print(f"  Wind Power: {stats['wind']['power_min']:.2f} - {stats['wind']['power_max']:.2f} MW "
              f"(avg: {stats['wind']['power_mean']:.2f} MW)\n")
        
        print("SOLAR RESOURCES")
        print("-" * 80)
        print(f"  Solar Irradiance: {stats['solar']['irradiance_min']:.2f} - "
              f"{stats['solar']['irradiance_max']:.2f} W/m² "
              f"(avg: {stats['solar']['irradiance_mean']:.2f} W/m²)")
        print(f"  Solar Power: {stats['solar']['power_min']:.2f} - {stats['solar']['power_max']:.2f} MW "
              f"(avg: {stats['solar']['power_mean']:.2f} MW)\n")
        
        print("LOAD DEMAND")
        print("-" * 80)
        print(f"  Peak Load: {stats['load']['max']:.2f} MW")
        print(f"  Minimum Load: {stats['load']['min']:.2f} MW")
        print(f"  Average Load: {stats['load']['mean']:.2f} MW")
        print(f"  Load Std Dev: {stats['load']['std']:.2f} MW\n")
        
        print("GRID PARAMETERS")
        print("-" * 80)
        print(f"  Frequency: {stats['grid']['frequency_min']:.2f} - "
              f"{stats['grid']['frequency_max']:.2f} Hz "
              f"(avg: {stats['grid']['frequency_mean']:.2f} Hz)")
        print(f"  Voltage: {stats['grid']['voltage_min']:.3f} - {stats['grid']['voltage_max']:.3f} p.u. "
              f"(avg: {stats['grid']['voltage_mean']:.3f} p.u.)")
        print(f"  Harmonics (THD): {stats['grid']['harmonics_min']:.2f}% - "
              f"{stats['grid']['harmonics_max']:.2f}% "
              f"(avg: {stats['grid']['harmonics_mean']:.2f}%)\n")
        
        print("RENEWABLE INTEGRATION")
        print("-" * 80)
        print(f"  Renewable Penetration: {stats['renewable']['penetration_min']:.2f}% - "
              f"{stats['renewable']['penetration_max']:.2f}% "
              f"(avg: {stats['renewable']['penetration_mean']:.2f}%)\n")
        
        print("=" * 80 + "\n")


def main():
    """Main execution"""
    
    print("\n" + "=" * 80)
    print("REAL-TIME DATA INTEGRATION FOR FACTS DEVICE SIMULATIONS")
    print("IEEE 39-Bus Power System with Renewable Integration")
    print("=" * 80 + "\n")
    
    # Initialize integrator
    integrator = RealDataIntegrator()
    
    # Load latest dataset
    data = integrator.load_latest_realtime_dataset()
    
    if data is None:
        print("ERROR: Could not load real-time data")
        return
    
    # Validate data
    integrator.validate_data()
    
    # Print summary
    integrator.print_summary()
    
    # Export for simulation
    export_file = integrator.export_for_simulation()
    print(f"✓ Data ready for simulation: {export_file}\n")
    
    # Print integration instructions
    print("=" * 80)
    print("NEXT STEPS: Integration with FACTS Simulation")
    print("=" * 80 + "\n")
    print("1. MODIFY python_implementation.py:")
    print("   Replace:")
    print("     data_gen = DataGenerator(duration_hours=8760)")
    print("     data = data_gen.generate_complete_dataset()")
    print("   With:")
    print("     integrator = RealDataIntegrator()")
    print("     data = integrator.load_latest_realtime_dataset()")
    print()
    print("2. RUN FACTS DEVICE SIMULATIONS:")
    print("   python python_implementation.py")
    print()
    print("3. RESULTS WILL BE:")
    print("   • STATCOM_performance.json - STATCOM device performance")
    print("   • SVC_performance.json - SVC device performance")
    print("   • UPFC_performance.json - UPFC device performance")
    print("   • Model comparisons with real-world data")
    print()
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
