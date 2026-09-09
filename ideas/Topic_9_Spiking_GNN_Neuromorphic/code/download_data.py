"""
Topic 9: Event-Driven Spiking Graph Neural Networks - Dataset Downloader
Dataset: IEEE 123-Bus Feeder Event/Spiking Data
Source: Hypothetical Repository (e.g., Neuromorphic-Grid-Data)
"""

import os
import numpy as np

OUTPUT_DIR = "../data/raw"

def download_and_extract():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Simulating download of 'IEEE123_SpikingEvents.zip'...")
    
    # Simulate: Spiking Data (Address-Event Representation - AER)
    # Events: (Time, Bus_ID, Polarity)
    
    # Grid: 123 Buses. Time: 10 seconds.
    # Sparsity: Only 0.1% of time steps have events
    
    n_events = 20000
    max_time_ms = 10000 
    n_buses = 123
    
    # Randomly generate events
    timestamps = np.sort(np.random.randint(0, max_time_ms, n_events))
    bus_ids = np.random.randint(0, n_buses, n_events)
    polarities = np.random.choice([-1, 1], n_events)
    
    events = np.stack([timestamps, bus_ids, polarities], axis=1)
    
    np.save(os.path.join(OUTPUT_DIR, "events_aer.npy"), events)
    
    # Adjacency for Graph Construction
    adj = np.random.randint(0, 2, (n_buses, n_buses))
    np.save(os.path.join(OUTPUT_DIR, "adjacency.npy"), adj)
    
    print(f"Dataset extracted to {OUTPUT_DIR}")
    print(f" - Events (T, Node, Pol): {events.shape}")

if __name__ == "__main__":
    download_and_extract()
