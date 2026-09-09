# Hybrid MADRL-GA Framework
# Complete framework for distribution network reconfiguration using
# Multi-Agent Deep Reinforcement Learning with Genetic Algorithm fine-tuning

import numpy as np
import time
from distribution_network import DistributionNetwork
from madrl_system import MultiAgentDQN
from genetic_algorithm import GeneticAlgorithm

class HybridMADRLGA:
    """Hybrid Multi-Agent Deep Reinforcement Learning with Genetic Algorithm Fine-tuning"""

    def __init__(self, network, num_agents=5):
        self.network = network
        self.madrl = MultiAgentDQN(network, num_agents)
        self.ga = GeneticAlgorithm(network, population_size=30, num_generations=50)

        self.performance_history = {
            'episodes': [],
            'rl_rewards': [],
            'ga_improvements': [],
            'total_improvements': [],
            'power_losses': [],
            'voltage_deviations': [],
            'execution_times': []
        }

    def train_rl_agent(self, episodes=500):
        """Train the MADRL agents"""
        print("Training MADRL agents...")
        training_history = self.madrl.train(episodes)
        return training_history

    def optimize_step(self, use_ga_fine_tuning=True):
        """Single optimization step using hybrid approach"""
        start_time = time.time()

        # Get RL solution
        state = self.network.get_state_vector()
        joint_action = self.madrl.get_joint_action(state)

        # Convert to chromosome format for GA
        rl_solution = [0] * len(self.ga.switchable_lines)
        for i, action in enumerate(joint_action[:len(rl_solution)]):
            rl_solution[i] = action

        # Apply RL solution and evaluate
        success, _ = self.network.apply_switching_action(rl_solution)
        if success:
            pf_results = self.network.three_phase_power_flow()
            rl_fitness = self.ga.evaluate_fitness(rl_solution)
        else:
            rl_fitness = -1000
            pf_results = {'power_losses': float('inf'), 'voltage_deviation': float('inf')}

        ga_improvement = 0
        final_solution = rl_solution

        if use_ga_fine_tuning and success:
            # Fine-tune with GA
            best_ga_solution, best_ga_fitness = self.ga.optimize(initial_solution=rl_solution)
            ga_improvement = best_ga_fitness - rl_fitness

            if ga_improvement > 0:
                final_solution = best_ga_solution
                self.network.apply_switching_action(final_solution)
                pf_results = self.network.three_phase_power_flow()

        execution_time = time.time() - start_time

        return {
            'rl_solution': rl_solution,
            'final_solution': final_solution,
            'rl_fitness': rl_fitness,
            'ga_improvement': ga_improvement,
            'power_losses': pf_results['power_losses'],
            'voltage_deviation': pf_results['voltage_deviation'],
            'execution_time': execution_time
        }

    # Additional methods for optimization and reporting...

class MADRLFramework:
    """Main framework for training and evaluating MADRL system"""

    def __init__(self):
        self.networks = {}
        self.hybrid_systems = {}
        self.results = {}

    def create_network(self, network_type='IEEE33'):
        """Create and store a network"""
        network = DistributionNetwork(network_type)
        self.networks[network_type] = network
        return network

    def create_hybrid_system(self, network_type='IEEE33', num_agents=5):
        """Create hybrid MADRL-GA system"""
        if network_type not in self.networks:
            self.create_network(network_type)

        network = self.networks[network_type]
        hybrid_system = HybridMADRLGA(network, num_agents)
        self.hybrid_systems[network_type] = hybrid_system
        return hybrid_system

    # Additional methods for comprehensive evaluation...
