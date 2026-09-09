"""
Topic 10: DeepONet Operator Learning - Dataset Downloader
Dataset: IEEE 118-Bus & 300-Bus Function Space Data (Loads -> Voltages)
Source: Hypothetical Repository (e.g., SciML-Power-Data)
"""

import os
import numpy as np

OUTPUT_DIR = "../data/raw"

def download_and_extract():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Simulating download of 'IEEE118_OperatorData.zip'...")
    
    # Simulate: 50,000 Samples of (Input Function, Output Function)
    # Input u(x): Active/Reactive Power Injection at all buses
    # Output G(u)(x): Voltage Magnitude/Angle at all buses
    
    n_samples = 50000
    n_buses = 118
    
    # Random Gaussian Random Fields (GRF) for Loads (Smooth variations)
    # Shape: [N, Buses, 2] (P, Q)
    U_loads = np.random.normal(0.5, 0.2, (n_samples, n_buses, 2))
    
    # Output Voltages (Solutions to AC-OPF)
    # Shape: [N, Buses, 2] (Vm, Va)
    V_sol = np.random.normal(1.0, 0.05, (n_samples, n_buses, 2))
    
    # Sensor Locations (Coordinates of buses for Trunk Net)
    # Normalized coordinates [0, 1]
    coords = np.random.rand(n_buses, 2) 
    
    np.save(os.path.join(OUTPUT_DIR, "load_functions_u.npy"), U_loads)
    np.save(os.path.join(OUTPUT_DIR, "voltage_functions_v.npy"), V_sol)
    np.save(os.path.join(OUTPUT_DIR, "bus_coordinates.npy"), coords)
    
    print(f"Dataset extracted to {OUTPUT_DIR}")
    print(f" - Load Functions: {U_loads.shape}")
    print(f" - Voltage Solutions: {V_sol.shape}")

if __name__ == "__main__":
    download_and_extract()
