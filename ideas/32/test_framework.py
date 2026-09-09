# Test and Validation Script
# Automated testing for the MADRL-GA framework components

import unittest
import numpy as np
import time
import sys
import os

# Add the current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from distribution_network import DistributionNetwork
    from madrl_system import MultiAgentDQN, DQNAgent
    from genetic_algorithm import GeneticAlgorithm
    from hybrid_framework import HybridMADRLGA, MADRLFramework
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required modules are available")
    sys.exit(1)

class TestDistributionNetwork(unittest.TestCase):
    """Test cases for Distribution Network component"""

    def setUp(self):
        self.network_33 = DistributionNetwork('IEEE33')
        self.network_123 = DistributionNetwork('IEEE123')

    def test_network_initialization(self):
        """Test network initialization"""
        # IEEE 33-bus
        self.assertEqual(len(self.network_33.buses), 33)
        self.assertEqual(self.network_33.network_type, 'IEEE33')
        self.assertTrue(len(self.network_33.switches) > 0)

        # IEEE 123-bus
        self.assertEqual(len(self.network_123.buses), 123)
        self.assertEqual(self.network_123.network_type, 'IEEE123')

    def test_power_flow(self):
        """Test power flow calculation"""
        pf_results = self.network_33.three_phase_power_flow()

        self.assertIn('power_losses', pf_results)
        self.assertIn('voltages', pf_results)
        self.assertIn('min_voltage', pf_results)
        self.assertIn('max_voltage', pf_results)

        # Check reasonable values
        self.assertGreater(pf_results['power_losses'], 0)
        self.assertGreater(pf_results['min_voltage'], 0.8)
        self.assertLess(pf_results['max_voltage'], 1.2)

    def test_state_vector(self):
        """Test state vector generation"""
        state = self.network_33.get_state_vector()
        self.assertIsInstance(state, np.ndarray)
        self.assertGreater(len(state), 0)

    def test_radiality_check(self):
        """Test radiality constraint checking"""
        # Initial configuration should be radial
        self.assertTrue(self.network_33.is_radial())

    def test_switching_actions(self):
        """Test switching action application"""
        # Get current switch states
        initial_switches = len([s for s in self.network_33.switches.values() if s['status'] == 1])

        # Try a simple switch action
        switch_actions = [1] * len(self.network_33.switches)
        success, message = self.network_33.apply_switching_action(switch_actions)

        # Result may be success or failure depending on radiality
        self.assertIsInstance(success, bool)
        self.assertIsInstance(message, str)

class TestMADRLSystem(unittest.TestCase):
    """Test cases for MADRL system"""

    def setUp(self):
        self.network = DistributionNetwork('IEEE33')
        self.madrl = MultiAgentDQN(self.network, num_agents=3)

    def test_agent_initialization(self):
        """Test agent initialization"""
        self.assertEqual(self.madrl.num_agents, 3)
        self.assertEqual(len(self.madrl.agents), 3)

        # Test individual agent
        agent = self.madrl.agents[0]
        self.assertIsInstance(agent, DQNAgent)
        self.assertEqual(agent.action_size, 2)

    def test_joint_action(self):
        """Test joint action generation"""
        state = self.network.get_state_vector()
        joint_action = self.madrl.get_joint_action(state)

        self.assertEqual(len(joint_action), self.madrl.num_agents)
        self.assertTrue(all(isinstance(a, (int, np.integer)) for a in joint_action))

    def test_training_episode(self):
        """Test single training episode"""
        reward, loss = self.madrl.train_episode()

        self.assertIsInstance(reward, (int, float))
        self.assertIsInstance(loss, (int, float, type(None)))

    def test_reward_calculation(self):
        """Test reward calculation"""
        pf_results = self.network.three_phase_power_flow()
        reward = self.madrl._calculate_reward(pf_results)

        self.assertIsInstance(reward, (int, float))

class TestGeneticAlgorithm(unittest.TestCase):
    """Test cases for Genetic Algorithm"""

    def setUp(self):
        self.network = DistributionNetwork('IEEE33')
        self.ga = GeneticAlgorithm(self.network, population_size=10, num_generations=5)

    def test_ga_initialization(self):
        """Test GA initialization"""
        self.assertEqual(self.ga.population_size, 10)
        self.assertEqual(self.ga.num_generations, 5)
        self.assertGreater(self.ga.chromosome_length, 0)

    def test_individual_creation(self):
        """Test individual creation"""
        individual = self.ga.create_individual()

        self.assertEqual(len(individual), self.ga.chromosome_length)
        self.assertTrue(all(x in [0, 1] for x in individual))

    def test_population_creation(self):
        """Test population creation"""
        population = self.ga.create_population()

        self.assertEqual(len(population), self.ga.population_size)
        self.assertTrue(all(len(ind) == self.ga.chromosome_length for ind in population))

    def test_fitness_evaluation(self):
        """Test fitness evaluation"""
        individual = self.ga.create_individual()
        fitness = self.ga.evaluate_fitness(individual)

        self.assertIsInstance(fitness, (int, float))

    def test_genetic_operators(self):
        """Test genetic operators"""
        parent1 = self.ga.create_individual()
        parent2 = self.ga.create_individual()

        # Test crossover
        child1, child2 = self.ga.crossover(parent1, parent2)
        self.assertEqual(len(child1), self.ga.chromosome_length)
        self.assertEqual(len(child2), self.ga.chromosome_length)

        # Test mutation
        mutated = self.ga.mutate(parent1)
        self.assertEqual(len(mutated), self.ga.chromosome_length)

    def test_chromosome_repair(self):
        """Test chromosome repair functionality"""
        # Create invalid chromosome (all zeros)
        invalid_chromosome = [0] * self.ga.chromosome_length
        repaired = self.ga.repair_chromosome(invalid_chromosome)

        # Should have appropriate number of 1s for radiality
        num_ones = sum(repaired)
        expected_ones = len(self.network.buses) - 1
        self.assertLessEqual(abs(num_ones - expected_ones), 2)  # Allow some tolerance

class TestHybridFramework(unittest.TestCase):
    """Test cases for Hybrid Framework"""

    def setUp(self):
        self.network = DistributionNetwork('IEEE33')
        self.hybrid = HybridMADRLGA(self.network, num_agents=3)

    def test_hybrid_initialization(self):
        """Test hybrid system initialization"""
        self.assertIsInstance(self.hybrid.madrl, MultiAgentDQN)
        self.assertIsInstance(self.hybrid.ga, GeneticAlgorithm)
        self.assertEqual(self.hybrid.madrl.num_agents, 3)

    def test_rl_solution_generation(self):
        """Test RL solution generation"""
        rl_solution = self.hybrid.get_rl_solution()

        self.assertIsInstance(rl_solution, list)
        self.assertEqual(len(rl_solution), len(self.hybrid.ga.switchable_lines))
        self.assertTrue(all(x in [0, 1] for x in rl_solution))

    def test_optimization_step(self):
        """Test single optimization step"""
        # Train for a few episodes first
        self.hybrid.train_rl_agent(episodes=5)

        result = self.hybrid.optimize_step(use_ga_fine_tuning=False)

        self.assertIn('rl_solution', result)
        self.assertIn('final_solution', result)
        self.assertIn('rl_fitness', result)
        self.assertIn('power_losses', result)
        self.assertIn('execution_time', result)

    def test_performance_tracking(self):
        """Test performance tracking"""
        # Train and run one step
        self.hybrid.train_rl_agent(episodes=3)
        self.hybrid.optimize_step(use_ga_fine_tuning=False)

        history = self.hybrid.performance_history
        self.assertGreater(len(history['episodes']), 0)
        self.assertGreater(len(history['power_losses']), 0)

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete framework"""

    def test_complete_workflow(self):
        """Test complete optimization workflow"""
        # Create framework
        framework = MADRLFramework()

        # Create network and hybrid system
        network = framework.create_network('IEEE33')
        hybrid_system = framework.create_hybrid_system('IEEE33', num_agents=3)

        # Quick training
        training_history = hybrid_system.train_rl_agent(episodes=5)
        self.assertIn('episodes', training_history)

        # Quick optimization
        results = hybrid_system.run_optimization(num_steps=1, use_ga_fine_tuning=False)
        self.assertEqual(len(results), 1)

        # Generate report
        report = hybrid_system.generate_report()
        self.assertIsInstance(report, str)
        self.assertIn('OPTIMIZATION REPORT', report)

    def test_scalability(self):
        """Test scalability across different network sizes"""
        for network_type in ['IEEE33', 'IEEE123']:
            network = DistributionNetwork(network_type)
            hybrid_system = HybridMADRLGA(network, num_agents=2)

            # Quick test
            hybrid_system.train_rl_agent(episodes=2)
            result = hybrid_system.optimize_step(use_ga_fine_tuning=False)

            self.assertIsInstance(result['power_losses'], (int, float))
            self.assertGreater(result['execution_time'], 0)

def run_performance_benchmark():
    """Run performance benchmark"""
    print("\nRunning Performance Benchmark...")
    print("=" * 50)

    results = {}

    for network_type in ['IEEE33', 'IEEE123']:
        print(f"\nTesting {network_type}...")

        # Create system
        network = DistributionNetwork(network_type)
        hybrid_system = HybridMADRLGA(network, num_agents=3)

        # Measure training time
        start_time = time.time()
        hybrid_system.train_rl_agent(episodes=10)
        training_time = time.time() - start_time

        # Measure optimization time
        start_time = time.time()
        result = hybrid_system.optimize_step(use_ga_fine_tuning=True)
        optimization_time = time.time() - start_time

        results[network_type] = {
            'buses': len(network.buses),
            'switches': len(network.switches),
            'training_time': training_time,
            'optimization_time': optimization_time,
            'power_losses': result['power_losses']
        }

        print(f"  Buses: {results[network_type]['buses']}")
        print(f"  Training time: {training_time:.2f}s")
        print(f"  Optimization time: {optimization_time:.2f}s")
        print(f"  Power losses: {result['power_losses']:.4f} MW")

    print("\nBenchmark Summary:")
    print("-" * 30)
    for system, data in results.items():
        print(f"{system}: {data['training_time']:.2f}s training, {data['optimization_time']:.2f}s optimization")

def main():
    """Main test function"""
    print("MADRL-GA Framework Test Suite")
    print("=" * 50)

    # Run unit tests
    print("Running unit tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)

    # Run performance benchmark
    run_performance_benchmark()

    print("\n" + "=" * 50)
    print("Testing completed!")

if __name__ == "__main__":
    main()
