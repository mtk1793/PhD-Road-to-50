# Demonstration and Example Usage
# Complete example of using the MADRL-GA framework for distribution network reconfiguration

import numpy as np
import matplotlib.pyplot as plt
from distribution_network import DistributionNetwork
from madrl_system import MultiAgentDQN
from genetic_algorithm import GeneticAlgorithm
from hybrid_framework import HybridMADRLGA, MADRLFramework
from visualization_tools import MADRLVisualizer, export_results_to_csv, generate_detailed_report

def run_basic_example():
    """Run a basic example with IEEE 33-bus system"""
    print("="*60)
    print("BASIC EXAMPLE: IEEE 33-BUS SYSTEM")
    print("="*60)

    # Create network
    network = DistributionNetwork('IEEE33')
    print(f"Created {network.network_type} network with {len(network.buses)} buses and {len(network.switches)} switches")

    # Initial power flow
    initial_pf = network.three_phase_power_flow()
    print(f"Initial power losses: {initial_pf['power_losses']:.4f} MW")
    print(f"Initial min voltage: {initial_pf['min_voltage']:.4f} p.u.")

    # Create hybrid system
    hybrid_system = HybridMADRLGA(network, num_agents=5)

    # Train RL agents
    print("\nTraining MADRL agents...")
    training_history = hybrid_system.train_rl_agent(episodes=100)

    # Run optimization
    print("\nRunning hybrid optimization...")
    results = hybrid_system.run_optimization(num_steps=3, use_ga_fine_tuning=True)

    # Generate report
    report = hybrid_system.generate_report()
    print("\n" + report)

    return hybrid_system, results

def run_comprehensive_evaluation():
    """Run comprehensive evaluation on both test systems"""
    print("="*60)
    print("COMPREHENSIVE EVALUATION: IEEE 33-BUS AND 123-BUS")
    print("="*60)

    # Create framework
    framework = MADRLFramework()

    # Run evaluation
    results = framework.run_comprehensive_evaluation()

    # Create visualizations
    visualizer = MADRLVisualizer(framework)

    # Generate performance dashboard
    print("\nGenerating performance dashboard...")
    visualizer.generate_performance_dashboard()

    # Export results
    export_results_to_csv(framework, 'madrl_ga_results.csv')
    generate_detailed_report(framework, 'madrl_ga_detailed_report.txt')

    return framework, results

def demonstrate_individual_components():
    """Demonstrate individual components of the framework"""
    print("="*60)
    print("COMPONENT DEMONSTRATION")
    print("="*60)

    # 1. Distribution Network
    print("\n1. DISTRIBUTION NETWORK COMPONENT")
    print("-" * 40)
    network = DistributionNetwork('IEEE33')

    # Show initial state
    pf_results = network.three_phase_power_flow()
    print(f"Network type: {network.network_type}")
    print(f"Buses: {len(network.buses)}")
    print(f"Lines: {len(network.lines)}")
    print(f"Switches: {len(network.switches)}")
    print(f"Power losses: {pf_results['power_losses']:.4f} MW")
    print(f"Voltage range: {pf_results['min_voltage']:.4f} - {pf_results['max_voltage']:.4f} p.u.")

    # 2. MADRL System
    print("\n2. MULTI-AGENT DQN COMPONENT")
    print("-" * 40)
    madrl_system = MultiAgentDQN(network, num_agents=3)
    print(f"Number of agents: {madrl_system.num_agents}")
    print(f"State size: {len(network.get_state_vector())}")
    print(f"Action size per agent: 2")

    # Train for a few episodes
    print("Training for 50 episodes...")
    for episode in range(50):
        reward, loss = madrl_system.train_episode()
        if episode % 10 == 0:
            print(f"Episode {episode}: Reward = {reward:.2f}, Loss = {loss:.4f}")

    # 3. Genetic Algorithm
    print("\n3. GENETIC ALGORITHM COMPONENT")
    print("-" * 40)
    ga_system = GeneticAlgorithm(network, population_size=20, num_generations=30)
    print(f"Population size: {ga_system.population_size}")
    print(f"Chromosome length: {ga_system.chromosome_length}")
    print(f"Crossover rate: {ga_system.crossover_rate}")
    print(f"Mutation rate: {ga_system.mutation_rate}")

    # Run optimization
    print("Running GA optimization...")
    best_solution, best_fitness = ga_system.optimize()
    print(f"Best fitness achieved: {best_fitness:.2f}")

    # 4. Hybrid System
    print("\n4. HYBRID MADRL-GA COMPONENT")
    print("-" * 40)
    hybrid_system = HybridMADRLGA(network, num_agents=3)

    # Single optimization step
    result = hybrid_system.optimize_step(use_ga_fine_tuning=True)
    print(f"RL fitness: {result['rl_fitness']:.2f}")
    print(f"GA improvement: {result['ga_improvement']:.2f}")
    print(f"Final power losses: {result['power_losses']:.4f} MW")
    print(f"Execution time: {result['execution_time']:.2f} seconds")

def analyze_scalability():
    """Analyze scalability between different network sizes"""
    print("="*60)
    print("SCALABILITY ANALYSIS")
    print("="*60)

    results = {}

    for network_type in ['IEEE33', 'IEEE123']:
        print(f"\nAnalyzing {network_type} system...")

        # Create network
        network = DistributionNetwork(network_type)

        # Create hybrid system
        hybrid_system = HybridMADRLGA(network, num_agents=5)

        # Measure training time
        import time
        start_time = time.time()
        training_history = hybrid_system.train_rl_agent(episodes=50)
        training_time = time.time() - start_time

        # Measure optimization time
        start_time = time.time()
        opt_results = hybrid_system.run_optimization(num_steps=2, use_ga_fine_tuning=True)
        optimization_time = time.time() - start_time

        # Store results
        results[network_type] = {
            'buses': len(network.buses),
            'switches': len(network.switches),
            'state_size': len(network.get_state_vector()),
            'training_time': training_time,
            'optimization_time': optimization_time,
            'final_losses': hybrid_system.performance_history['power_losses'][-1],
            'avg_ga_improvement': np.mean(hybrid_system.performance_history['ga_improvements'])
        }

    # Display comparison
    print("\nSCALABILITY COMPARISON:")
    print("-" * 50)
    print(f"{'Metric':<20} {'IEEE33':<15} {'IEEE123':<15}")
    print("-" * 50)

    for metric in ['buses', 'switches', 'state_size']:
        print(f"{metric.capitalize():<20} {results['IEEE33'][metric]:<15} {results['IEEE123'][metric]:<15}")

    print("-" * 50)
    for metric in ['training_time', 'optimization_time']:
        print(f"{metric.replace('_', ' ').title():<20} {results['IEEE33'][metric]:<15.2f} {results['IEEE123'][metric]:<15.2f}")

    print("-" * 50)
    for metric in ['final_losses', 'avg_ga_improvement']:
        print(f"{metric.replace('_', ' ').title():<20} {results['IEEE33'][metric]:<15.4f} {results['IEEE123'][metric]:<15.4f}")

def parameter_sensitivity_analysis():
    """Analyze sensitivity to different parameters"""
    print("="*60)
    print("PARAMETER SENSITIVITY ANALYSIS")
    print("="*60)

    network = DistributionNetwork('IEEE33')
    base_losses = network.three_phase_power_flow()['power_losses']

    # Test different number of agents
    print("\nTesting different numbers of agents:")
    print("-" * 40)

    for num_agents in [3, 5, 7]:
        hybrid_system = HybridMADRLGA(network, num_agents=num_agents)
        hybrid_system.train_rl_agent(episodes=50)
        result = hybrid_system.optimize_step(use_ga_fine_tuning=True)

        loss_reduction = (base_losses - result['power_losses']) / base_losses * 100
        print(f"Agents: {num_agents}, Loss reduction: {loss_reduction:.2f}%, "
              f"Time: {result['execution_time']:.2f}s")

    # Test GA parameters
    print("\nTesting different GA parameters:")
    print("-" * 40)

    ga_configs = [
        {'population_size': 20, 'num_generations': 30},
        {'population_size': 30, 'num_generations': 50},
        {'population_size': 50, 'num_generations': 30}
    ]

    for config in ga_configs:
        hybrid_system = HybridMADRLGA(network, num_agents=5)
        hybrid_system.ga.population_size = config['population_size']
        hybrid_system.ga.num_generations = config['num_generations']

        hybrid_system.train_rl_agent(episodes=30)
        result = hybrid_system.optimize_step(use_ga_fine_tuning=True)

        print(f"Pop: {config['population_size']}, Gen: {config['num_generations']}, "
              f"GA improvement: {result['ga_improvement']:.2f}, "
              f"Time: {result['execution_time']:.2f}s")

def main():
    """Main demonstration function"""
    print("MADRL-GA FRAMEWORK DEMONSTRATION")
    print("=" * 60)
    print("This demonstration showcases the Adaptive Multi-Agent Deep")
    print("Reinforcement Learning Framework with Metaheuristic Fine-Tuning")
    print("for Real-Time Reconfiguration of Distribution Networks.")
    print("=" * 60)

    try:
        # Run basic example
        basic_results = run_basic_example()

        # Demonstrate components
        demonstrate_individual_components()

        # Analyze scalability
        analyze_scalability()

        # Parameter sensitivity
        parameter_sensitivity_analysis()

        print("\n" + "="*60)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nAll components have been tested and demonstrated.")
        print("Check the generated files for detailed results and reports.")

    except Exception as e:
        print(f"\nError during demonstration: {str(e)}")
        print("Please check the implementation and try again.")

if __name__ == "__main__":
    main()
