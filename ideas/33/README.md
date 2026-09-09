# Advanced FACTS Control System Simulation

## Overview
This simulation framework demonstrates advanced control strategies for FACTS (Flexible AC Transmission System) devices in modern power systems using reinforcement learning techniques.

## Features
- **Multi-bus power system modeling**: IEEE 14-bus test system
- **Multiple FACTS devices**: SVC, STATCOM, SSSC, and UPFC models
- **Reinforcement Learning controller**: SAC-based coordination
- **Power flow analysis**: Complete system analysis capabilities
- **System stability assessment**: Voltage and stability metrics
- **Performance comparison**: RL vs conventional control methods

## Files Generated
1. `advanced_facts_control_simulation.py` - Complete standalone simulation
2. `facts_control_comprehensive_analysis.png` - Detailed visualization
3. `facts_devices_configuration.csv` - FACTS device specifications
4. `performance_comparison.csv` - Control method comparison
5. `voltage_analysis.csv` - Bus voltage analysis
6. `rl_training_data.csv` - Training progression data
7. `system_analysis_summary.md` - Comprehensive analysis report

## Requirements
```bash
pip install numpy matplotlib pandas scipy seaborn scikit-learn
```

## Usage
```bash
python advanced_facts_control_simulation.py
```

## Key Results
- RL-based coordinated control outperforms conventional PI control
- Multi-objective optimization balances losses, voltage stability, and costs
- Adaptive learning enables robust operation under varying conditions
- Economic benefits through reduced operational costs

## Technical Specifications
- **Power System**: IEEE 14-bus, 20-line system
- **FACTS Devices**: 4 devices with 180 MVA total rating
- **RL Algorithm**: Soft Actor-Critic (SAC) based coordination
- **State Space**: 40-dimensional system state vector
- **Action Space**: 5-dimensional control signal vector

## Applications
- Power system stability enhancement
- Voltage regulation and reactive power management
- Power flow control and optimization
- Grid integration of renewable energy sources
- Smart grid and microgrid applications

## Research Impact
This simulation framework provides a comprehensive platform for:
- Advanced power system control research
- FACTS device optimization studies
- Reinforcement learning applications in power systems
- Multi-objective power system optimization
- Real-time control strategy development

## Future Enhancements
- Integration with larger test systems (IEEE 57-bus, 118-bus)
- Advanced RL algorithms (PPO, DDPG, TD3)
- Real-time hardware-in-the-loop testing
- Uncertainty quantification and robust control
- Integration with renewable energy forecasting
