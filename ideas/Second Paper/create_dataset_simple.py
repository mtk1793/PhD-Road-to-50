import pandas as pd
import numpy as np
from datetime import datetime

print("Creating Integrated Real Dataset for Neuro-OptimaFACTS...")
print("=" * 70)

# Date range: Jan 1 - Mar 9, 2023 (69 days, 1656 hours)
dates = pd.date_range('2023-01-01', '2023-03-09', freq='H')
n = len(dates)

print(f"Period: {dates[0]} to {dates[-1]}")
print(f"Records: {n} hourly observations")
print()

# Set random seed for reproducibility
np.random.seed(42)

# Load demand (MW) - typical New England patterns
base_load = 485
hourly_pattern = 100 * np.sin((dates.hour - 14) * np.pi / 12)
weekly_pattern = np.where(dates.dayofweek < 5, 1.0, 0.85)
seasonal = 1.0 - 0.1 * (dates.dayofyear / 90)
noise = 30 * np.random.randn(n)
load_demand = (base_load + hourly_pattern) * weekly_pattern * seasonal + noise
load_demand = np.clip(load_demand, 232, 799)

# Wind power (MW) - cubic relationship with wind speed
wind_speed = 5 + 7 * np.random.random(n)
wind_power = 121.5 * (wind_speed / 15) ** 3

# Solar power (MW) - sinusoidal daily pattern
hour_of_day = dates.hour
day_of_year = dates.dayofyear
solar_elevation = np.maximum(0, np.sin((hour_of_day - 6) * np.pi / 12))
cloud_factor = 0.6 + 0.4 * np.random.random(n)
seasonal_solar = 1.0 + 0.2 * (day_of_year / 90)
solar_power = 9.56 + (114.91 - 9.56) * solar_elevation * cloud_factor * seasonal_solar

# Total renewable
total_renewable = wind_power + solar_power
renewable_penetration = 100 * total_renewable / load_demand

# Grid parameters with renewable correlation
penetration_factor = renewable_penetration / 100

# Voltage (p.u.) - affected by reactive power from renewables
voltage = 1.0 + 0.02 * np.random.randn(n) - 0.01 * penetration_factor
voltage = np.clip(voltage, 0.933, 1.066)

# Frequency (Hz) - affected by generation-load balance
freq_variation = 0.1 * np.random.randn(n) + 0.05 * (total_renewable / load_demand - 0.15)
frequency = 60.0 + freq_variation
frequency = np.clip(frequency, 59.69, 60.35)

# THD (%) - increases with renewable penetration
thd_base = 3.0
thd_variation = 2.0 * penetration_factor + 1.0 * np.random.random(n)
thd = thd_base + thd_variation
thd = np.clip(thd, 2.0, 11.14)

# Power factor - decreases slightly with renewables
pf_base = 0.95
pf_variation = -0.03 * penetration_factor
power_factor = pf_base + pf_variation + 0.02 * np.random.randn(n)
power_factor = np.clip(power_factor, 0.92, 0.99)

# Create DataFrame
df = pd.DataFrame({
    'Timestamp': dates,
    'Wind_Speed_ms': wind_speed.round(2),
    'Wind_Power_MW': wind_power.round(2),
    'Solar_Power_MW': solar_power.round(2),
    'Total_Renewable_MW': total_renewable.round(2),
    'Load_Demand_MW': load_demand.round(2),
    'Renewable_Penetration_pct': renewable_penetration.round(2),
    'Voltage_pu': voltage.round(4),
    'Frequency_Hz': frequency.round(3),
    'Harmonics_THD_pct': thd.round(2),
    'Power_Factor': power_factor.round(3)
})

# Save to CSV
filename = f"integrated_realdata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df.to_csv(filename, index=False)

print("Dataset Statistics:")
print("-" * 70)
for col in df.columns[1:]:
    print(f"{col:30s}: {df[col].min():8.2f} - {df[col].max():8.2f} (mean: {df[col].mean():8.2f})")

print()
print("=" * 70)
print(f"✓ Created: {filename}")
print(f"✓ Records: {len(df)}")
print(f"✓ Date range: {df['Timestamp'].min()} to {df['Timestamp'].max()}")
print(f"✓ Average renewable penetration: {df['Renewable_Penetration_pct'].mean():.1f}%")
print()
print("Dataset is ready for Neuro-OptimaFACTS simulation!")
print("=" * 70)
