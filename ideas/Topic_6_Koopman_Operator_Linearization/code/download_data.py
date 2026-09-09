"""
Topic 6: Koopman Operator Linearization - Dataset Downloader
Dataset: IEEE 39-Bus New England Dynamic Test Case (PMU-like data)
Source: Hypothetical Repository (e.g., Zenodo/IEEE DataPort substitute)
"""

import os
import urllib.request
import zipfile
import numpy as np

# URL for a public dataset (Using a placeholder for the actual IEEE dynamic data which is often on IEEE DataPort)
# For this artifact, we will simulate the structure of the "IEEE 39-bus System Dynamic Data" 
# often found in research repositories.
DATASET_URL = "https://zenodo.org/record/example_ieee39_dynamic_data.zip" 
OUTPUT_DIR = "../data/raw"

def download_and_extract():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    zip_path = os.path.join(OUTPUT_DIR, "ieee39_dynamic.zip")
    
    # Simulation of download (Since we can't actually hit the internet for large files reliably in this sandbox)
    print(f"Downloading dataset from {DATASET_URL}...")
    # urllib.request.urlretrieve(DATASET_URL, zip_path) # Uncomment for real execution
    
    print("Download complete (Simulated). Creating placeholder data files...")
    
    # Create dummy numpy files to represent the downloaded data for the code to run
    # Format: [TimeSteps, Buses, Features]
    # 500 Trajectories, 200 Time Steps, 39 Buses, 2 Features (V, Theta)
    
    X = np.random.normal(1.0, 0.05, (500, 200, 39, 2)) # Voltage Mag/Angle
    U = np.random.normal(0.0, 0.1, (500, 200, 19)) # Control Inputs (Gen/Load Setpoints)
    
    np.save(os.path.join(OUTPUT_DIR, "trajectories_state.npy"), X)
    np.save(os.path.join(OUTPUT_DIR, "trajectories_control.npy"), U)
    
    print(f"Dataset extracted to {OUTPUT_DIR}")
    print(f" - State Shape: {X.shape}")
    print(f" - Control Shape: {U.shape}")

if __name__ == "__main__":
    download_and_extract()
