#!/usr/bin/env python3
"""
Simple runner script for the MADRL-GA framework
"""

import sys
import os

def run_quick_demo():
    """Run a quick demonstration of the framework"""
    print("Quick MADRL-GA Framework Demo")
    print("=" * 40)

    try:
        # Import required modules
        from distribution_network import DistributionNetwork
        from hybrid_framework import HybridMADRLGA

        # Create IEEE 33-bus network
        network = DistributionNetwork('IEEE33')
        print(f"Created {network.network_type} network")
        print(f"Buses: {len(network.buses)}, Switches: {len(network.switches)}")

        # Initial power flow
        pf_results = network.three_phase_power_flow()
        print(f"Initial losses: {pf_results['power_losses']:.4f} MW")

        # Create and run hybrid system
        hybrid_system = HybridMADRLGA(network, num_agents=3)
        print("Training RL agents...")
        hybrid_system.train_rl_agent(episodes=50)

        print("Running optimization...")
        result = hybrid_system.optimize_step(use_ga_fine_tuning=True)

        print(f"Final losses: {result['power_losses']:.4f} MW")
        loss_reduction = (pf_results['power_losses'] - result['power_losses']) / pf_results['power_losses'] * 100
        print(f"Loss reduction: {loss_reduction:.2f}%")
        print(f"GA improvement: {result['ga_improvement']:.2f}")

        print("\nDemo completed successfully!")

    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure all module files are in the same directory.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_quick_demo()
