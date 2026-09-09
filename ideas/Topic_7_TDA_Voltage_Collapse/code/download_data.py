"""
Topic 7: Topological Data Analysis (TDA) for Voltage Collapse - Dataset Downloader
Dataset: IEEE 118-Bus Voltage Stability / Continuation Power Flow Data
Source: Hypothetical Repository (e.g., Simulated CAScade Data)
"""

import os
import numpy as np

OUTPUT_DIR = "../data/raw"

def download_and_extract():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Simulating download of 'IEEE118_VoltageCollapse_Traj.zip'...")
    
    # Simulate Data: 5000 snapshots along P-V curves
    # Shape: [N_Samples, N_Buses]
    # N_Samples = 5000, N_Buses = 118
    # We simulate a "nose curve" where voltage drops as index increases
    
    n_samples = 5000
    n_buses = 118
    
    # Create smooth degradation
    t = np.linspace(0, 1, n_samples)
    base_voltage = np.ones((n_samples, n_buses))
    
    # Introduce collapse at random buses
    collapse_profile = 1.0 - 0.5 * t**2 # Quadratic drop to 0.5 pu
    
    # Apply to random subset of buses (Zone 2)
    zone2_buses = np.random.choice(n_buses, 30, replace=False)
    for b in zone2_buses:
        base_voltage[:, b] = collapse_profile + np.random.normal(0, 0.01, n_samples)
        
    np.save(os.path.join(OUTPUT_DIR, "voltage_magnitudes.npy"), base_voltage)
    
    # Adjacency Matrix (Placeholder for topology)
    adj = np.random.randint(0, 2, (n_buses, n_buses))
    np.save(os.path.join(OUTPUT_DIR, "adjacency.npy"), adj)
    
    print(f"Dataset extracted to {OUTPUT_DIR}")
    print(f" - Voltage Snapshots: {base_voltage.shape}")

if __name__ == "__main__":
    download_and_extract()
