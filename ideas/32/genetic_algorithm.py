# Genetic Algorithm Module
# Metaheuristic optimization for network reconfiguration fine-tuning

import numpy as np
import random

class GeneticAlgorithm:
    """Genetic Algorithm for network reconfiguration optimization"""

    def __init__(self, network, population_size=50, num_generations=100):
        self.network = network
        self.population_size = population_size
        self.num_generations = num_generations
        self.crossover_rate = 0.8
        self.mutation_rate = 0.1
        self.elite_size = 5

        # Get switchable lines
        self.switchable_lines = [line for line, data in network.switches.items() 
                                if data['controllable']]
        self.chromosome_length = len(self.switchable_lines)

        self.best_fitness_history = []
        self.avg_fitness_history = []

    def create_individual(self):
        """Create a random individual (chromosome)"""
        # Ensure radiality constraint: exactly n-1 lines closed
        num_buses = len(self.network.buses)
        num_closed = num_buses - 1

        chromosome = [0] * self.chromosome_length

        # Randomly select lines to close
        indices = random.sample(range(self.chromosome_length), 
                               min(num_closed, self.chromosome_length))
        for idx in indices:
            chromosome[idx] = 1

        return chromosome

    def evaluate_fitness(self, chromosome):
        """Evaluate fitness of a chromosome"""
        # Apply chromosome to network
        switch_actions = chromosome
        success, _ = self.network.apply_switching_action(switch_actions)

        if not success:
            return -1000  # Heavy penalty for invalid configuration

        # Calculate fitness based on power flow results
        pf_results = self.network.three_phase_power_flow()

        # Multi-objective fitness
        loss_fitness = -pf_results['power_losses'] * 100
        voltage_fitness = -pf_results['voltage_deviation'] * 50

        # Penalty for voltage violations
        voltage_penalty = 0
        if pf_results['min_voltage'] < 0.95:
            voltage_penalty -= 1000 * (0.95 - pf_results['min_voltage'])
        if pf_results['max_voltage'] > 1.05:
            voltage_penalty -= 1000 * (pf_results['max_voltage'] - 1.05)

        fitness = loss_fitness + voltage_fitness + voltage_penalty
        return fitness

    # Complete implementation of all methods...
