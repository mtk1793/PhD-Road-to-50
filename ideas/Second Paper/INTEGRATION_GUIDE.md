# Integration Guide: Replacing Synthetic Data with Real-Time Data
# Step-by-step instructions to modify python_implementation.py

## Option 1: Minimal Change (Recommended for Testing)

Replace this section in `python_implementation.py`:

### BEFORE (Current - Synthetic Data):
```python
# In main() or wherever you create DataGenerator
class DataGenerator:
    """Generate synthetic renewable energy and grid data"""
    
    def __init__(self, duration_hours=8760, time_step=1):  # 1 year, hourly data
        # ... synthetic generation code ...
    
    # ... methods like generate_wind_data(), generate_solar_data(), etc. ...

# Usage in your code:
data_gen = DataGenerator(duration_hours=8760)
data = data_gen.generate_complete_dataset()
```

### AFTER (New - Real-Time Data):
```python
# Import the real-time data integrator
from integrate_realtime_data import RealDataIntegrator

# Usage in your code:
integrator = RealDataIntegrator()
data = integrator.load_latest_realtime_dataset()

# Optionally validate and prepare:
if data is not None:
    integrator.validate_data()
    data = integrator.get_dataset_for_simulation()
else:
    print("Warning: Could not load real-time data. Using fallback...")
    data_gen = DataGenerator(duration_hours=8760)
    data = data_gen.generate_complete_dataset()
```

---

## Option 2: Flexible Approach (Recommended for Production)

### Add this function at the top of python_implementation.py:

```python
import os
from integrate_realtime_data import RealDataIntegrator

def load_data_source(use_realtime=True, synthetic_duration=8760):
    """
    Load data from real-time source or fallback to synthetic
    
    Args:
        use_realtime: Whether to try loading real-time data first
        synthetic_duration: Hours of synthetic data if fallback is needed
    
    Returns:
        DataFrame with complete dataset
    """
    
    if use_realtime:
        try:
            print("Attempting to load real-time data...")
            integrator = RealDataIntegrator()
            data = integrator.load_latest_realtime_dataset()
            
            if data is not None:
                integrator.validate_data()
                data = integrator.get_dataset_for_simulation()
                print(f"✓ Successfully loaded real-time data ({len(data)} records)")
                return data
        except Exception as e:
            print(f"⚠ Warning: Could not load real-time data: {e}")
    
    # Fallback to synthetic data
    print("Falling back to synthetic data generation...")
    data_gen = DataGenerator(duration_hours=synthetic_duration)
    data = data_gen.generate_complete_dataset()
    print(f"✓ Generated synthetic data ({len(data)} records)")
    return data


# Then in your main() or wherever you create data:
if __name__ == "__main__":
    # Load data (tries real-time first, falls back to synthetic)
    data = load_data_source(use_realtime=True)
    
    # Continue with your FACTS device simulations
    # ... rest of your code ...
```

---

## Option 3: Configuration File Approach (Best for Reproducibility)

### Create `config.json`:
```json
{
    "data_source": "realtime",
    "data_options": {
        "realtime": {
            "enabled": true,
            "fallback_to_synthetic": true,
            "validate_data": true
        },
        "synthetic": {
            "duration_hours": 8760,
            "time_step": 1
        }
    },
    "simulation": {
        "facts_devices": ["STATCOM", "SVC", "UPFC"],
        "output_format": "json"
    }
}
```

### Use configuration in python_implementation.py:
```python
import json
from integrate_realtime_data import RealDataIntegrator

def load_config(config_file="config.json"):
    """Load configuration from JSON"""
    with open(config_file, 'r') as f:
        return json.load(f)

def load_data_from_config(config):
    """Load data based on configuration"""
    
    config_data = config.get("data_options", {})
    
    if config.get("data_source") == "realtime":
        try:
            integrator = RealDataIntegrator()
            data = integrator.load_latest_realtime_dataset()
            
            if data is not None and config_data.get("realtime", {}).get("validate_data"):
                integrator.validate_data()
                data = integrator.get_dataset_for_simulation()
            
            if data is not None:
                return data
        except Exception as e:
            if config_data.get("realtime", {}).get("fallback_to_synthetic"):
                print(f"Falling back to synthetic: {e}")
            else:
                raise
    
    # Use synthetic data
    synthetic_opts = config_data.get("synthetic", {})
    data_gen = DataGenerator(
        duration_hours=synthetic_opts.get("duration_hours", 8760),
        time_step=synthetic_opts.get("time_step", 1)
    )
    return data_gen.generate_complete_dataset()


# In your main():
if __name__ == "__main__":
    config = load_config()
    data = load_data_from_config(config)
    # ... continue with simulations ...
```

---

## Detailed Step-by-Step Integration

### Step 1: Add Import at Top of File
```python
# Add this import with your other imports
from integrate_realtime_data import RealDataIntegrator
```

### Step 2: Modify DataGenerator Section
```python
# Find this section (around line 21-23):
class DataGenerator:
    """Generate synthetic renewable energy and grid data"""
    
    def __init__(self, duration_hours=8760, time_step=1):

# Add this function BEFORE the DataGenerator class:
def get_data_source(prefer_realtime=True):
    """Get data from real-time or synthetic source"""
    
    if prefer_realtime:
        integrator = RealDataIntegrator()
        data = integrator.load_latest_realtime_dataset()
        if data is not None:
            print("✓ Using real-time data")
            return data
    
    print("✓ Using synthetic data")
    gen = DataGenerator(duration_hours=8760)
    return gen.generate_complete_dataset()
```

### Step 3: Modify Data Loading
```python
# Find where you create the data (look for):
# data = data_gen.generate_complete_dataset()

# Replace with:
data = get_data_source(prefer_realtime=True)
```

### Step 4: Test Integration
```bash
python python_implementation.py
```

Expected output:
```
✓ Using real-time data
✓ Successfully loaded 1609 records from real-time data
✓ Data validation passed
[FACTS device simulations proceed with real-time data...]
```

---

## Advanced: Comparing Results

### Add Analysis Function:
```python
def compare_simulations(synthetic_results, realtime_results):
    """Compare FACTS device performance between synthetic and real-time data"""
    
    comparison = {
        'STATCOM': {
            'synthetic_r2': synthetic_results.get('STATCOM', {}).get('r2_score'),
            'realtime_r2': realtime_results.get('STATCOM', {}).get('r2_score'),
            'improvement': None  # Will calculate
        },
        'SVC': {
            'synthetic_r2': synthetic_results.get('SVC', {}).get('r2_score'),
            'realtime_r2': realtime_results.get('SVC', {}).get('r2_score'),
            'improvement': None
        },
        'UPFC': {
            'synthetic_r2': synthetic_results.get('UPFC', {}).get('r2_score'),
            'realtime_r2': realtime_results.get('UPFC', {}).get('r2_score'),
            'improvement': None
        }
    }
    
    # Calculate improvements
    for device in comparison:
        synth = comparison[device]['synthetic_r2']
        real = comparison[device]['realtime_r2']
        if synth is not None and real is not None:
            comparison[device]['improvement'] = real - synth
    
    return comparison

# Usage:
if __name__ == "__main__":
    # Run with synthetic data
    synthetic_data = DataGenerator().generate_complete_dataset()
    synthetic_results = run_facts_simulations(synthetic_data)
    
    # Run with real-time data
    realtime_data = get_data_source(prefer_realtime=True)
    realtime_results = run_facts_simulations(realtime_data)
    
    # Compare
    comparison = compare_simulations(synthetic_results, realtime_results)
    print(json.dumps(comparison, indent=2))
```

---

## Verification Checklist

Before running full simulations, verify:

- [ ] `integrate_realtime_data.py` is in the same directory
- [ ] Real-time CSV files exist (from `quickstart_realtime_data.py`)
- [ ] Import statement works: `from integrate_realtime_data import RealDataIntegrator`
- [ ] Data loads without errors: `integrator.load_latest_realtime_dataset()`
- [ ] Data has correct columns (Wind_Speed_ms, Solar_Irradiance_Wm2, Load_Demand_MW, etc.)
- [ ] Data shape is as expected (1,609 rows for Jan 1 - Mar 9, 2023)
- [ ] Validation passes: `integrator.validate_data()`

### Quick Test Script:
```python
# Save as test_integration.py
from integrate_realtime_data import RealDataIntegrator

integrator = RealDataIntegrator()
data = integrator.load_latest_realtime_dataset()

if data is not None:
    print(f"✓ Data loaded: {len(data)} records")
    print(f"✓ Columns: {list(data.columns)}")
    print(f"✓ Date range: {data['Date'].min()} to {data['Date'].max()}")
    
    is_valid = integrator.validate_data()
    if is_valid:
        print("✓ All validations passed!")
    else:
        print("✗ Validation failed")
else:
    print("✗ Could not load data")
```

Run it:
```bash
python test_integration.py
```

Expected output:
```
✓ Data loaded: 1609 records
✓ Columns: ['Date', 'Wind_Speed_ms', 'Wind_Power_MW', 'Solar_Irradiance_Wm2', 'Solar_Power_MW', ...]
✓ Date range: 2023-01-01 00:00:00 to 2023-03-09 00:00:00
✓ All validations passed!
```

---

## Troubleshooting Integration

### Issue 1: "ModuleNotFoundError: No module named 'integrate_realtime_data'"
**Solution**: 
- Ensure `integrate_realtime_data.py` is in the same directory
- Or add to path: `sys.path.insert(0, os.getcwd())`

### Issue 2: "No real-time datasets found"
**Solution**:
- Run `python quickstart_realtime_data.py` first to generate datasets
- Check files were created: `ls realtime_*.csv`

### Issue 3: "Attribute error: 'DataFrame' has no attribute 'method'"
**Solution**:
- Update pandas: `pip install --upgrade pandas`
- Use new syntax: `data.ffill()` instead of `data.fillna(method='ffill')`

### Issue 4: Data shape mismatch
**Solution**:
- Verify expected columns in `get_dataset_for_simulation()`
- Check if column names match your code expectations
- Use `data.columns` to inspect

---

## Performance Considerations

### Data Size
- Synthetic (1 year): 8,760 records
- Real-time (1 year period): 8,760 records
- Your loaded datasets: 1,609 records (Jan-Mar only)
- No performance penalty; data sizes are equivalent

### Memory Usage
- Full dataset: ~2-3 MB in memory
- Safe to load multiple datasets for comparison
- No issues on modern computers

### Processing Time
- Data loading: < 1 second
- Validation: < 0.5 seconds
- Preparation for simulation: < 1 second
- Total overhead: < 2 seconds per load

---

## Example: Complete Modified Section

Here's a complete example of how your code might look:

```python
# python_implementation.py (modified)

import numpy as np
import pandas as pd
# ... other imports ...
from integrate_realtime_data import RealDataIntegrator  # NEW

class DataGenerator:
    """Generate synthetic renewable energy and grid data"""
    # ... existing code unchanged ...

def get_data_source(prefer_realtime=True):
    """
    Load data from real-time source or synthetic generation
    
    Args:
        prefer_realtime: If True, try loading real-time data first
        
    Returns:
        DataFrame with simulation data
    """
    if prefer_realtime:
        try:
            integrator = RealDataIntegrator()
            data = integrator.load_latest_realtime_dataset()
            if data is not None:
                integrator.validate_data()
                data = integrator.get_dataset_for_simulation()
                print("Using real-time data for simulation")
                return data
        except Exception as e:
            print(f"Warning: Could not load real-time data: {e}")
    
    # Fallback to synthetic
    print("Using synthetic data for simulation")
    data_gen = DataGenerator(duration_hours=8760)
    return data_gen.generate_complete_dataset()

# Main execution
if __name__ == "__main__":
    # Load data (now supports both real-time and synthetic)
    data = get_data_source(prefer_realtime=True)  # NEW
    
    # ... rest of your FACTS device simulation code ...
    # The data structure is identical, so no other changes needed!
    
    # Example: Your existing code should work as-is
    # statcom = STATCOMController(data)
    # svc = SVCController(data)
    # upfc = UPFCController(data)
    # ... etc ...
```

---

## Final Notes

1. **Minimal Changes**: Only 3-4 lines need to change in your existing code
2. **Backward Compatible**: Existing code structure remains unchanged
3. **Automatic Fallback**: If real-time data unavailable, uses synthetic
4. **Data Compatible**: Same DataFrame format, all columns present
5. **Reproducible**: Timestamps included for exact date ranges

You're ready to integrate! 🚀
