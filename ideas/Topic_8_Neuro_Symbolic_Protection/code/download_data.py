"""
Topic 8: Neuro-Symbolic Protection Coordination - Dataset Downloader
Dataset: IEEE 33-Bus Radial Distribution System Fault Data
Source: Hypothetical Repository (e.g., Protection Systems Data Bank)
"""

import os
import numpy as np

OUTPUT_DIR = "../data/raw"

def download_and_extract():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Simulating download of 'IEEE33_Faults.zip'...")
    
    # Simulate: 50,000 Fault Cases for Protection
    # Input: Current Waveforms (Samples), Output: Trip Decision (Binary)
    
    n_cases = 50000
    n_samples = 128 # 1 cycle at high sampling
    n_relays = 33
    
    # Inputs: Current Magnitude (Simple representation)
    # Normal current is ~1.0 pu, Fault current is > 5.0 pu
    X = np.random.normal(1.0, 0.1, (n_cases, n_samples, n_relays))
    
    # Inject faults
    Y = np.zeros((n_cases, n_relays)) 
    
    for i in range(n_cases):
        if np.random.rand() > 0.5: # 50% Fault Prob
            fault_loc = np.random.randint(0, n_relays)
            # Downstream relays see fault current
            X[i, :, :fault_loc+1] += np.random.uniform(5.0, 20.0) 
            # Correct relay to trip is 'fault_loc'
            Y[i, fault_loc] = 1
            
    np.save(os.path.join(OUTPUT_DIR, "current_waveforms.npy"), X)
    np.save(os.path.join(OUTPUT_DIR, "protection_targets.npy"), Y)
    
    print(f"Dataset extracted to {OUTPUT_DIR}")
    print(f" - Waveforms: {X.shape}")
    print(f" - Targets: {Y.shape}")

if __name__ == "__main__":
    download_and_extract()
