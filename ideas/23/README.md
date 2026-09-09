# Neural Network and ANFIS Load Frequency Control Simulation

This repository contains a comprehensive Python simulation of Neural Network and Adaptive Neuro-Fuzzy Inference System (ANFIS) controllers for load frequency control in hybrid renewable energy systems.

## Overview

The simulation implements a two-area interconnected power system with:
- High renewable energy penetration (wind and solar)
- Energy storage systems (BESS and SMES)  
- Conventional thermal generation
- Load disturbances and renewable fluctuations

## Files Description

1. `anfis_load_frequency_control_simulation.py` - Complete simulation script
2. `anfis_load_frequency_control_comprehensive.png` - Comprehensive visualization results
3. `simulation_results_summary.txt` - Detailed performance analysis
4. `performance_comparison_table.csv` - Quantitative comparison metrics
5. `detailed_simulation_data.csv` - Complete simulation time-series data

## Key Features

### Neural Network Predictor
- Predicts renewable power output using meteorological parameters
- Feed-forward architecture with tanh/sigmoid activations
- Inputs: Wind speed, solar irradiance, temperature, humidity, pressure, time of day

### ANFIS Controller
- 2 inputs: Frequency deviation (Δf) and its derivative (dΔf/dt)
- 7 trapezoidal membership functions per input
- 49 fuzzy rules total
- Takagi-Sugeno inference method

### System Parameters (from research paper)
- Nominal frequency: 50 Hz
- Inertia constants: H1=5s, H2=4s
- Damping coefficients: D1=0.8, D2=0.7 pu/Hz
- Tie-line coefficient: 0.2 pu/Hz
- BESS: K=1.0, T=0.1s
- SMES: K=1.0, T=0.05s

## Performance Results

ANFIS controller achieved significant improvements over conventional PI control:
- 39.71% reduction in overshoot
- 100% elimination of undershoot
- 45.28% reduction in frequency standard deviation
- 25.32% reduction in ISE (Integral Square Error)

## Running the Simulation

```python
python anfis_load_frequency_control_simulation.py
```

## Requirements

- numpy
- matplotlib  
- pandas
- scipy

## Research Reference

Based on: "Neural Network and Adaptive Neuro-Fuzzy Control for Load Frequency in Hybrid Renewable Energy Systems"

## Applications

- Islanded microgrids
- Weak interconnected power systems
- Remote hybrid power systems
- High renewable penetration grids
