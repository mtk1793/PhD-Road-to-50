# Hybrid AGC Framework Simulation

This repository contains a comprehensive Python simulation of a Hybrid Automatic Generation Control (AGC) framework for integrated wind-solar energy systems.

## Features

- **Multi-area Power System**: 3-area interconnected system with conventional and renewable generation
- **Ensemble ML Forecasting**: RBFNN for wind power + SVM for solar power prediction
- **Enhanced ACO Optimization**: Metaheuristic optimization for PID parameter tuning
- **Virtual Inertia Control**: Compensation for low-inertia renewable systems
- **Comprehensive Testing**: Multiple disturbance scenarios and performance metrics

## Key Results

The hybrid framework demonstrates significant improvements over conventional AGC:

- **31.8%** reduction in maximum frequency deviation (step load)
- **30.4%** improvement for wind power fluctuations
- **22.3%** improvement for solar cloud coverage
- **29.1%** reduction in ITAE performance index
- **16.0%** reduction in control effort

## Files

- `hybrid_agc_complete_simulation.py`: Complete simulation code
- `hybrid_agc_main_results.png`: Main performance comparison plots
- `hybrid_agc_scenarios.png`: Multi-scenario evaluation results
- `hybrid_agc_ml_forecasting.png`: ML forecasting demonstration
- `hybrid_agc_aco_optimization.png`: Optimization convergence plots
- `simulation_report.txt`: Comprehensive results summary

## Usage

```python
python hybrid_agc_complete_simulation.py
```

## Requirements

- numpy
- matplotlib  
- scipy
- scikit-learn

## Citation

If you use this code in your research, please cite:
"Hybrid AGC Framework for Integrated Wind-Solar Energy Systems Using Ensemble Neural-SVM Architecture with Metaheuristic PID Optimization"
