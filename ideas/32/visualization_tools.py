# Visualization and Analysis Tools
# Comprehensive visualization suite for MADRL-GA optimization results

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Rectangle
import networkx as nx

class MADRLVisualizer:
    """Visualization tools for MADRL-GA optimization results"""

    def __init__(self, framework):
        self.framework = framework
        plt.style.use('seaborn-v0_8')

    def plot_training_convergence(self, network_type='IEEE33', save_path=None):
        """Plot training convergence curves"""
        if network_type not in self.framework.results:
            print(f"No results available for {network_type}")
            return

        training_history = self.framework.results[network_type]['training_history']

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        # Rewards
        ax1.plot(training_history['episodes'], training_history['rewards'], 'b-', alpha=0.7)
        ax1.set_title('Training Rewards')
        ax1.set_xlabel('Episode')
        ax1.set_ylabel('Reward')
        ax1.grid(True)

        # Losses
        ax2.plot(training_history['episodes'], training_history['losses'], 'r-', alpha=0.7)
        ax2.set_title('Training Losses')
        ax2.set_xlabel('Episode')
        ax2.set_ylabel('Loss')
        ax2.grid(True)

        # Epsilon decay
        ax3.plot(training_history['episodes'], training_history['epsilon'], 'g-', alpha=0.7)
        ax3.set_title('Exploration Rate (Epsilon)')
        ax3.set_xlabel('Episode')
        ax3.set_ylabel('Epsilon')
        ax3.grid(True)

        # Moving average of rewards
        window = 50
        if len(training_history['rewards']) > window:
            moving_avg = pd.Series(training_history['rewards']).rolling(window).mean()
            ax4.plot(training_history['episodes'], training_history['rewards'], 'b-', alpha=0.3, label='Raw')
            ax4.plot(training_history['episodes'], moving_avg, 'b-', linewidth=2, label=f'{window}-episode MA')
            ax4.set_title('Reward Moving Average')
            ax4.set_xlabel('Episode')
            ax4.set_ylabel('Reward')
            ax4.legend()
            ax4.grid(True)

        plt.suptitle(f'{network_type} Training Convergence', fontsize=16)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

    def plot_optimization_performance(self, network_type='IEEE33', save_path=None):
        """Plot optimization performance metrics"""
        if network_type not in self.framework.results:
            print(f"No results available for {network_type}")
            return

        hybrid_system = self.framework.results[network_type]['hybrid_system']
        history = hybrid_system.performance_history

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        # RL vs GA improvements
        x = range(len(history['rl_rewards']))
        ax1.bar(x, history['rl_rewards'], alpha=0.7, label='RL Fitness', color='blue')
        ax1.bar(x, history['ga_improvements'], bottom=history['rl_rewards'], 
                alpha=0.7, label='GA Improvement', color='orange')
        ax1.set_title('RL vs GA Contributions')
        ax1.set_xlabel('Optimization Step')
        ax1.set_ylabel('Fitness')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Power losses
        ax2.plot(x, history['power_losses'], 'r-o', linewidth=2, markersize=4)
        ax2.set_title('Power Losses')
        ax2.set_xlabel('Optimization Step')
        ax2.set_ylabel('Power Losses (MW)')
        ax2.grid(True)

        # Voltage deviations
        ax3.plot(x, history['voltage_deviations'], 'g-o', linewidth=2, markersize=4)
        ax3.set_title('Voltage Deviations')
        ax3.set_xlabel('Optimization Step')
        ax3.set_ylabel('Voltage Deviation (p.u.)')
        ax3.grid(True)

        # Execution times
        ax4.bar(x, history['execution_times'], alpha=0.7, color='purple')
        ax4.set_title('Execution Times')
        ax4.set_xlabel('Optimization Step')
        ax4.set_ylabel('Time (seconds)')
        ax4.grid(True, alpha=0.3)

        plt.suptitle(f'{network_type} Optimization Performance', fontsize=16)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

    def plot_network_topology(self, network_type='IEEE33', save_path=None):
        """Plot network topology with switch status"""
        if network_type not in self.framework.networks:
            print(f"No network available for {network_type}")
            return

        network = self.framework.networks[network_type]

        # Create graph
        G = nx.Graph()

        # Add nodes
        for bus_id in network.buses:
            G.add_node(bus_id)

        # Add edges based on current switch status
        closed_lines = []
        open_lines = []

        for line, data in network.lines.items():
            if data['status'] == 1:
                G.add_edge(line[0], line[1])
                closed_lines.append(line)
            else:
                open_lines.append(line)

        # Create layout
        if network_type == 'IEEE33':
            # Custom layout for IEEE 33-bus for better visualization
            pos = nx.spring_layout(G, k=3, iterations=50)
        else:
            pos = nx.spring_layout(G, k=2, iterations=30)

        plt.figure(figsize=(12, 8))

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=300, alpha=0.8)

        # Draw closed lines (thick, solid)
        nx.draw_networkx_edges(G, pos, edgelist=closed_lines, 
                              edge_color='blue', width=2, alpha=0.8)

        # Draw open lines (thin, dashed) - need to add them manually
        for line in open_lines:
            x1, y1 = pos[line[0]]
            x2, y2 = pos[line[1]]
            plt.plot([x1, x2], [y1, y2], 'r--', alpha=0.5, linewidth=1)

        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=8)

        plt.title(f'{network_type} Network Topology\nBlue: Closed Switches, Red Dashed: Open Switches')
        plt.axis('off')

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

    def plot_comparison_analysis(self, save_path=None):
        """Plot comparison between IEEE33 and IEEE123 systems"""
        if len(self.framework.results) < 2:
            print("Need results from both IEEE33 and IEEE123 systems for comparison")
            return

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        systems = list(self.framework.results.keys())
        colors = ['blue', 'red']

        # Training performance comparison
        for i, system in enumerate(systems):
            history = self.framework.results[system]['training_history']
            ax1.plot(history['episodes'], history['rewards'], 
                    color=colors[i], alpha=0.7, label=system)
        ax1.set_title('Training Rewards Comparison')
        ax1.set_xlabel('Episode')
        ax1.set_ylabel('Reward')
        ax1.legend()
        ax1.grid(True)

        # Final power losses comparison
        final_losses = []
        for system in systems:
            hybrid_system = self.framework.results[system]['hybrid_system']
            final_losses.append(hybrid_system.performance_history['power_losses'][-1])

        ax2.bar(systems, final_losses, color=colors, alpha=0.7)
        ax2.set_title('Final Power Losses')
        ax2.set_ylabel('Power Losses (MW)')
        ax2.grid(True, alpha=0.3)

        # Execution time comparison
        avg_times = []
        for system in systems:
            hybrid_system = self.framework.results[system]['hybrid_system']
            avg_times.append(np.mean(hybrid_system.performance_history['execution_times']))

        ax3.bar(systems, avg_times, color=colors, alpha=0.7)
        ax3.set_title('Average Execution Time')
        ax3.set_ylabel('Time (seconds)')
        ax3.grid(True, alpha=0.3)

        # GA improvement contribution
        ga_contributions = []
        for system in systems:
            hybrid_system = self.framework.results[system]['hybrid_system']
            ga_contributions.append(np.mean(hybrid_system.performance_history['ga_improvements']))

        ax4.bar(systems, ga_contributions, color=colors, alpha=0.7)
        ax4.set_title('Average GA Improvement')
        ax4.set_ylabel('Fitness Improvement')
        ax4.grid(True, alpha=0.3)

        plt.suptitle('IEEE33 vs IEEE123 System Comparison', fontsize=16)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

    def generate_performance_dashboard(self, save_path=None):
        """Generate comprehensive performance dashboard"""
        fig = plt.figure(figsize=(20, 12))

        # Create grid layout
        gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)

        for i, network_type in enumerate(['IEEE33', 'IEEE123']):
            if network_type not in self.framework.results:
                continue

            hybrid_system = self.framework.results[network_type]['hybrid_system']
            history = hybrid_system.performance_history
            training_history = self.framework.results[network_type]['training_history']

            # Training convergence
            ax1 = fig.add_subplot(gs[0, i*2:i*2+2])
            ax1.plot(training_history['episodes'], training_history['rewards'], alpha=0.7)
            ax1.set_title(f'{network_type} Training Convergence')
            ax1.set_ylabel('Reward')
            ax1.grid(True)

            # Power losses
            ax2 = fig.add_subplot(gs[1, i*2])
            x = range(len(history['power_losses']))
            ax2.plot(x, history['power_losses'], 'r-o', markersize=3)
            ax2.set_title(f'{network_type} Power Losses')
            ax2.set_ylabel('Losses (MW)')
            ax2.grid(True)

            # Voltage deviations
            ax3 = fig.add_subplot(gs[1, i*2+1])
            ax3.plot(x, history['voltage_deviations'], 'g-o', markersize=3)
            ax3.set_title(f'{network_type} Voltage Deviations')
            ax3.set_ylabel('Deviation (p.u.)')
            ax3.grid(True)

        # Comparison metrics
        if len(self.framework.results) >= 2:
            systems = list(self.framework.results.keys())

            # Loss reduction comparison
            ax4 = fig.add_subplot(gs[2, 0])
            loss_reductions = []
            for system in systems:
                hybrid_system = self.framework.results[system]['hybrid_system']
                history = hybrid_system.performance_history
                initial = history['power_losses'][0]
                final = history['power_losses'][-1]
                reduction = (initial - final) / initial * 100
                loss_reductions.append(reduction)

            ax4.bar(systems, loss_reductions, color=['blue', 'red'], alpha=0.7)
            ax4.set_title('Loss Reduction (%)')
            ax4.set_ylabel('Reduction (%)')
            ax4.grid(True, alpha=0.3)

            # Average execution time
            ax5 = fig.add_subplot(gs[2, 1])
            avg_times = []
            for system in systems:
                hybrid_system = self.framework.results[system]['hybrid_system']
                avg_times.append(np.mean(hybrid_system.performance_history['execution_times']))

            ax5.bar(systems, avg_times, color=['blue', 'red'], alpha=0.7)
            ax5.set_title('Avg Execution Time')
            ax5.set_ylabel('Time (s)')
            ax5.grid(True, alpha=0.3)

            # GA contribution
            ax6 = fig.add_subplot(gs[2, 2])
            ga_contributions = []
            for system in systems:
                hybrid_system = self.framework.results[system]['hybrid_system']
                ga_contributions.append(np.mean(hybrid_system.performance_history['ga_improvements']))

            ax6.bar(systems, ga_contributions, color=['blue', 'red'], alpha=0.7)
            ax6.set_title('GA Contribution')
            ax6.set_ylabel('Avg Improvement')
            ax6.grid(True, alpha=0.3)

            # Summary statistics
            ax7 = fig.add_subplot(gs[2, 3])
            ax7.axis('off')
            summary_text = "PERFORMANCE SUMMARY\n\n"
            for system in systems:
                hybrid_system = self.framework.results[system]['hybrid_system']
                history = hybrid_system.performance_history

                loss_reduction = ((history['power_losses'][0] - history['power_losses'][-1]) / 
                                history['power_losses'][0] * 100)
                avg_time = np.mean(history['execution_times'])
                avg_ga = np.mean(history['ga_improvements'])

                summary_text += f"{system}:\n"
                summary_text += f"  Loss Reduction: {loss_reduction:.1f}%\n"
                summary_text += f"  Avg Time: {avg_time:.2f}s\n"
                summary_text += f"  GA Benefit: {avg_ga:.1f}\n\n"

            ax7.text(0.1, 0.9, summary_text, transform=ax7.transAxes, 
                    fontsize=10, verticalalignment='top', fontfamily='monospace')

        plt.suptitle('MADRL-GA Optimization Dashboard', fontsize=18, y=0.98)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

# Additional utility functions
def export_results_to_csv(framework, filename):
    """Export results to CSV format"""
    all_data = []

    for network_type, results in framework.results.items():
        hybrid_system = results['hybrid_system']
        history = hybrid_system.performance_history

        for i in range(len(history['episodes'])):
            row = {
                'network_type': network_type,
                'step': i,
                'rl_reward': history['rl_rewards'][i],
                'ga_improvement': history['ga_improvements'][i],
                'total_improvement': history['total_improvements'][i],
                'power_losses': history['power_losses'][i],
                'voltage_deviation': history['voltage_deviations'][i],
                'execution_time': history['execution_times'][i]
            }
            all_data.append(row)

    df = pd.DataFrame(all_data)
    df.to_csv(filename, index=False)
    print(f"Results exported to {filename}")

def generate_detailed_report(framework, filename):
    """Generate detailed text report"""
    with open(filename, 'w') as f:
        f.write("COMPREHENSIVE MADRL-GA OPTIMIZATION REPORT\n")
        f.write("=" * 50 + "\n\n")

        for network_type, results in framework.results.items():
            f.write(f"\n{network_type} SYSTEM ANALYSIS\n")
            f.write("-" * 30 + "\n")

            hybrid_system = results['hybrid_system']
            report = hybrid_system.generate_report()
            f.write(report)
            f.write("\n")

    print(f"Detailed report saved to {filename}")
