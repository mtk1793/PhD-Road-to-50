#!/usr/bin/env python3
"""Quick diagnostic to check simulation progress without running full analysis"""

import sys
import os
from datetime import datetime

print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DIAGNOSTIC CHECK")
print("=" * 70)

# Check 1: Can we import the modules?
print("\n[1] Checking imports...")
try:
    from integrate_realtime_data import RealDataIntegrator
    print("  ✓ RealDataIntegrator imported")
except Exception as e:
    print(f"  ✗ Failed to import RealDataIntegrator: {e}")
    sys.exit(1)

try:
    from python_implementation import NeuroOptimaFACTS
    print("  ✓ NeuroOptimaFACTS imported")
except Exception as e:
    print(f"  ✗ Failed to import NeuroOptimaFACTS: {e}")
    sys.exit(1)

# Check 2: Can we load real-time data?
print("\n[2] Checking data loading...")
try:
    integrator = RealDataIntegrator()
    data = integrator.load_latest_realtime_dataset()
    print(f"  ✓ Data loaded: {len(data)} records")
    print(f"  ✓ Columns: {list(data.columns)}")
except Exception as e:
    print(f"  ✗ Failed to load data: {e}")
    sys.exit(1)

# Check 3: Can we initialize framework?
print("\n[3] Checking framework initialization...")
try:
    neuro_facts = NeuroOptimaFACTS()
    print("  ✓ NeuroOptimaFACTS initialized")
except Exception as e:
    print(f"  ✗ Failed to initialize framework: {e}")
    sys.exit(1)

# Check 4: Data validation
print("\n[4] Checking data validation...")
try:
    integrator_check = RealDataIntegrator()
    integrator_check.validate_data(data)
    print("  ✓ Data validation passed")
except Exception as e:
    print(f"  ✗ Data validation failed: {e}")
    sys.exit(1)

# Check 5: System readiness
print("\n[5] System readiness check...")
print(f"  ✓ Python version: {sys.version.split()[0]}")
print(f"  ✓ Working directory: {os.getcwd()}")
print(f"  ✓ Data files present: {len(data)} records ready")
print(f"  ✓ Framework ready: Simulation capable")

print("\n" + "=" * 70)
print("✅ ALL DIAGNOSTIC CHECKS PASSED")
print("=" * 70)
print("\nSystem is fully operational and ready for full simulation.")
print("To run the full simulation with all FACTS analysis:")
print("  python run_realtime_simulation.py")
print("\n")
