
"""
Advanced Automatic Generation Control (AGC) Simulation for Renewable-Integrated Smart Grids
Comprehensive simulation suite based on IEEE research paper analysis

Author: Generated from Technical Analysis
Date: 2024
Purpose: Simulate and analyze advanced AGC strategies for renewable energy integration
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import odeint
from scipy.optimize import minimize
import control as ctrl
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings('ignore')

class PowerSystemModel:
    """
    Multi-area power system model with renewable integration
    """
    def __init__(self, num_areas=3, renewable_penetration=0.3):
        self.num_areas = num_areas
        self.renewable_penetration = renewable_penetration

        # System parameters (per unit)
        self.H = np.array([5.0, 4.5, 5.5])  # Inertia constants
        self.D = np.array([1.0, 1.2, 0.8])  # Damping coefficients
        self.R = np.array([2.4, 2.0, 2.8])  # Droop characteristics
        self.B = np.array([0.425, 0.385, 0.455])  # Bias factors

        # Tie-line parameters
        self.T12 = 0.2  # Synchronizing coefficient area 1-2
        self.T13 = 0.15  # Synchronizing coefficient area 1-3
        self.T23 = 0.18  # Synchronizing coefficient area 2-3

        # AGC parameters
        self.Ki = np.array([0.3, 0.25, 0.35])  # Integral gains
        self.Kp = np.array([0.8, 0.7, 0.9])   # Proportional gains
        self.Kd = np.array([0.1, 0.12, 0.08])  # Derivative gains

        # Renewable and BESS parameters
        self.P_renewable = np.zeros(num_areas)
        self.P_bess = np.zeros(num_areas)
        self.SoC = np.array([0.5, 0.5, 0.5])  # Battery State of Charge
        self.SoC_min = 0.2
        self.SoC_max = 0.9

        # Initialize state variables
        self.reset_states()

    def reset_states(self):
        """Reset all system states to initial conditions"""
        self.delta_f = np.zeros(self.num_areas)  # Frequency deviations
        self.delta_Pm = np.zeros(self.num_areas)  # Mechanical power changes
        self.delta_Ptie = np.zeros(self.num_areas)  # Tie-line power changes
        self.ACE = np.zeros(self.num_areas)  # Area Control Error
        self.ACE_integral = np.zeros(self.num_areas)  # Integral of ACE
        self.time = 0

    def calculate_renewable_power(self, t):
        """
        Simulate renewable power generation with intermittency
        """
        # Solar pattern (day-night cycle with clouds)
        solar_base = 0.5 * (1 + np.sin(2 * np.pi * t / 24 - np.pi/2))
        solar_noise = 0.2 * np.sin(2 * np.pi * t) * np.random.normal(0, 0.1)

        # Wind pattern (more random)
        wind_base = 0.3 + 0.4 * np.sin(2 * np.pi * t / 12)
        wind_noise = 0.3 * np.random.normal(0, 0.15)

        for i in range(self.num_areas):
            if i == 0:  # Area 1: Solar dominant
                self.P_renewable[i] = self.renewable_penetration * (0.7 * solar_base + 0.3 * wind_base + solar_noise)
            elif i == 1:  # Area 2: Wind dominant  
                self.P_renewable[i] = self.renewable_penetration * (0.3 * solar_base + 0.7 * wind_base + wind_noise)
            else:  # Area 3: Mixed
                self.P_renewable[i] = self.renewable_penetration * (0.5 * solar_base + 0.5 * wind_base + 0.5*(solar_noise + wind_noise))

        return self.P_renewable

    def calculate_load_demand(self, t):
        """
        Simulate load demand with daily patterns and demand response
        """
        # Base load pattern (daily cycle)
        base_load = 0.8 + 0.3 * np.sin(2 * np.pi * t / 24 - np.pi/3)

        # Random load variations
        load_noise = 0.1 * np.random.normal(0, 0.05)

        # Demand response (reduces load during high demand periods)
        dr_factor = 1.0
        if hasattr(self, 'demand_response_active') and self.demand_response_active:
            if np.any(np.abs(self.delta_f) > 0.1):  # Activate DR if frequency deviation > 0.1 Hz
                dr_factor = 0.95

        delta_PL = np.array([base_load + load_noise] * self.num_areas) * dr_factor
        return delta_PL

    def bess_control(self, dt=0.1):
        """
        Battery Energy Storage System control logic
        """
        for i in range(self.num_areas):
            # BESS response to frequency deviation
            if self.delta_f[i] < -0.05 and self.SoC[i] > self.SoC_min:  # Discharge
                P_bess_cmd = -min(0.2, (self.SoC[i] - self.SoC_min) * 2)
                self.SoC[i] += P_bess_cmd * dt / 3600  # Update SoC
                self.P_bess[i] = P_bess_cmd
            elif self.delta_f[i] > 0.05 and self.SoC[i] < self.SoC_max:  # Charge
                P_bess_cmd = min(0.2, (self.SoC_max - self.SoC[i]) * 2)
                self.SoC[i] += P_bess_cmd * dt / 3600  # Update SoC
                self.P_bess[i] = P_bess_cmd
            else:
                self.P_bess[i] = 0

        return self.P_bess

    def system_dynamics(self, states, t, delta_PL, agc_type='conventional'):
        """
        System dynamics for numerical integration
        """
        # Unpack states
        n_states = len(states) // self.num_areas
        delta_f = states[:self.num_areas]
        if n_states > 1:
            delta_Pm = states[self.num_areas:2*self.num_areas]
        else:
            delta_Pm = np.zeros(self.num_areas)
        if n_states > 2:
            ACE_integral = states[2*self.num_areas:3*self.num_areas]
        else:
            ACE_integral = np.zeros(self.num_areas)

        # Calculate renewable power and BESS response
        P_renewable = self.calculate_renewable_power(t)
        P_bess = self.bess_control()

        # Calculate tie-line power flows
        delta_Ptie = np.zeros(self.num_areas)
        delta_Ptie[0] = self.T12 * (delta_f[0] - delta_f[1]) + self.T13 * (delta_f[0] - delta_f[2])
        delta_Ptie[1] = self.T12 * (delta_f[1] - delta_f[0]) + self.T23 * (delta_f[1] - delta_f[2])
        delta_Ptie[2] = self.T13 * (delta_f[2] - delta_f[0]) + self.T23 * (delta_f[2] - delta_f[1])

        # Calculate Area Control Error
        ACE = delta_Ptie + self.B * delta_f

        # AGC control signal
        if agc_type == 'conventional':
            delta_Pm = -self.Ki * ACE_integral
        elif agc_type == 'pid':
            delta_Pm = -self.Kp * ACE - self.Ki * ACE_integral - self.Kd * np.gradient(ACE)
        elif agc_type == 'adaptive':
            # Adaptive gains based on system conditions
            adaptive_Ki = self.Ki * (1 + 0.5 * np.abs(delta_f))
            delta_Pm = -adaptive_Ki * ACE_integral

        # System dynamics (swing equation)
        d_delta_f_dt = (delta_Pm + P_renewable + P_bess - delta_PL - delta_Ptie - self.D * delta_f) / (2 * self.H)
        d_delta_Pm_dt = np.zeros(self.num_areas)  # Simplified for this model
        d_ACE_integral_dt = ACE

        # Combine derivatives
        if n_states == 1:
            return d_delta_f_dt
        elif n_states == 2:
            return np.concatenate([d_delta_f_dt, d_delta_Pm_dt])
        else:
            return np.concatenate([d_delta_f_dt, d_delta_Pm_dt, d_ACE_integral_dt])

class MLPredictor:
    """
    Machine Learning predictor for renewable energy forecasting
    """
    def __init__(self, predictor_type='random_forest'):
        self.predictor_type = predictor_type
        if predictor_type == 'random_forest':
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        elif predictor_type == 'neural_network':
            self.model = MLPRegressor(hidden_layer_sizes=(50, 30), max_iter=1000, random_state=42)
        self.is_trained = False

    def prepare_features(self, time_series, window_size=24):
        """
        Prepare features for ML prediction
        """
        X, y = [], []
        for i in range(window_size, len(time_series)):
            X.append(time_series[i-window_size:i])
            y.append(time_series[i])
        return np.array(X), np.array(y)

    def train(self, time_series):
        """
        Train the ML model
        """
        X, y = self.prepare_features(time_series)
        self.model.fit(X, y)
        self.is_trained = True

    def predict_next(self, recent_data, horizon=1):
        """
        Predict next values
        """
        if not self.is_trained:
            return np.zeros(horizon)

        predictions = []
        current_data = recent_data.copy()

        for _ in range(horizon):
            X_pred = current_data[-24:].reshape(1, -1)
            pred = self.model.predict(X_pred)[0]
            predictions.append(pred)
            current_data = np.append(current_data[1:], pred)

        return np.array(predictions)

class CyberSecurityModule:
    """
    Cyber-physical security module for AGC systems
    """
    def __init__(self):
        self.attack_detection_rate = 0.94
        self.false_positive_rate = 0.05
        self.attack_active = False
        self.attack_history = []

    def detect_attack(self, system_data):
        """
        Detect cyber attacks based on system anomalies
        """
        # Simple anomaly detection based on frequency deviation patterns
        anomaly_score = 0

        # Check for unusual frequency patterns
        if np.any(np.abs(system_data['delta_f']) > 0.5):
            anomaly_score += 0.3

        # Check for inconsistent control signals
        if np.any(np.abs(system_data['ACE']) > 0.2):
            anomaly_score += 0.2

        # Check for rapid changes
        if len(self.attack_history) > 1:
            freq_change_rate = np.abs(system_data['delta_f'] - self.attack_history[-1]['delta_f'])
            if np.any(freq_change_rate > 0.1):
                anomaly_score += 0.3

        # Detection decision
        detection_threshold = 0.4
        attack_detected = anomaly_score > detection_threshold and np.random.random() < self.attack_detection_rate

        self.attack_history.append(system_data.copy())
        if len(self.attack_history) > 100:
            self.attack_history.pop(0)

        return attack_detected, anomaly_score

    def simulate_attack(self, attack_type='data_injection'):
        """
        Simulate different types of cyber attacks
        """
        if attack_type == 'data_injection':
            # False data injection attack
            noise_factor = 0.1 * np.random.normal(0, 1, 3)
            return noise_factor
        elif attack_type == 'dos':
            # Denial of service - communication delay
            return 'communication_delay'
        elif attack_type == 'replay':
            # Replay attack - use old data
            return 'replay_attack'
        else:
            return np.zeros(3)

class AGCSimulator:
    """
    Main AGC simulation class
    """
    def __init__(self, num_areas=3, renewable_penetration=0.3):
        self.power_system = PowerSystemModel(num_areas, renewable_penetration)
        self.ml_predictor = MLPredictor('random_forest')
        self.security_module = CyberSecurityModule()
        self.simulation_results = {}

    def run_scenario(self, scenario_type='conventional', simulation_time=24, dt=0.1):
        """
        Run specific AGC scenario simulation
        """
        t_span = np.arange(0, simulation_time, dt)

        # Initialize results storage
        results = {
            'time': t_span,
            'delta_f': np.zeros((len(t_span), self.power_system.num_areas)),
            'ACE': np.zeros((len(t_span), self.power_system.num_areas)),
            'P_renewable': np.zeros((len(t_span), self.power_system.num_areas)),
            'P_bess': np.zeros((len(t_span), self.power_system.num_areas)),
            'SoC': np.zeros((len(t_span), self.power_system.num_areas)),
            'attack_detected': np.zeros(len(t_span)),
            'control_effort': np.zeros(len(t_span))
        }

        # Set scenario-specific parameters
        if scenario_type == 'decentralized_bess':
            self.power_system.renewable_penetration = 0.4
        elif scenario_type == 'hierarchical_ml':
            # Train ML predictor with synthetic data
            synthetic_data = np.random.normal(0.3, 0.1, 1000)
            self.ml_predictor.train(synthetic_data)
        elif scenario_type == 'ami_dr':
            self.power_system.demand_response_active = True
        elif scenario_type == 'wams_adaptive':
            # Enable adaptive control
            pass

        # Reset system states
        self.power_system.reset_states()

        # Simulation loop
        for i, t in enumerate(t_span):
            # Calculate load demand
            delta_PL = self.power_system.calculate_load_demand(t)

            # System dynamics integration
            if i == 0:
                # Initial conditions
                current_states = np.zeros(3 * self.power_system.num_areas)
            else:
                # Simple Euler integration for demonstration
                dt_step = dt
                derivs = self.power_system.system_dynamics(current_states, t, delta_PL, scenario_type)
                current_states += derivs * dt_step

            # Update system states
            self.power_system.delta_f = current_states[:self.power_system.num_areas]
            self.power_system.ACE_integral = current_states[2*self.power_system.num_areas:3*self.power_system.num_areas]

            # Calculate current ACE
            delta_Ptie = np.zeros(self.power_system.num_areas)
            delta_Ptie[0] = self.power_system.T12 * (self.power_system.delta_f[0] - self.power_system.delta_f[1]) + \
                           self.power_system.T13 * (self.power_system.delta_f[0] - self.power_system.delta_f[2])
            delta_Ptie[1] = self.power_system.T12 * (self.power_system.delta_f[1] - self.power_system.delta_f[0]) + \
                           self.power_system.T23 * (self.power_system.delta_f[1] - self.power_system.delta_f[2])
            delta_Ptie[2] = self.power_system.T13 * (self.power_system.delta_f[2] - self.power_system.delta_f[0]) + \
                           self.power_system.T23 * (self.power_system.delta_f[2] - self.power_system.delta_f[1])

            self.power_system.ACE = delta_Ptie + self.power_system.B * self.power_system.delta_f

            # Renewable power calculation
            P_renewable = self.power_system.calculate_renewable_power(t)

            # BESS control
            P_bess = self.power_system.bess_control(dt)

            # Security monitoring
            system_data = {
                'delta_f': self.power_system.delta_f,
                'ACE': self.power_system.ACE
            }
            attack_detected, _ = self.security_module.detect_attack(system_data)

            # Store results
            results['delta_f'][i] = self.power_system.delta_f
            results['ACE'][i] = self.power_system.ACE
            results['P_renewable'][i] = P_renewable
            results['P_bess'][i] = P_bess
            results['SoC'][i] = self.power_system.SoC
            results['attack_detected'][i] = attack_detected
            results['control_effort'][i] = np.sum(np.abs(self.power_system.ACE))

        # Calculate performance metrics
        performance_metrics = self.calculate_performance_metrics(results)
        results['performance_metrics'] = performance_metrics

        return results

    def calculate_performance_metrics(self, results):
        """
        Calculate key performance metrics
        """
        metrics = {}

        # Frequency deviation metrics
        max_freq_dev = np.max(np.abs(results['delta_f']))
        rms_freq_dev = np.sqrt(np.mean(results['delta_f']**2))

        # Settling time (time to reach within 1% of final value)
        settling_indices = []
        for area in range(self.power_system.num_areas):
            freq_area = results['delta_f'][:, area]
            final_value = freq_area[-1]
            settling_criterion = 0.01 * abs(final_value) if abs(final_value) > 0.01 else 0.01

            # Find last time the signal was outside the settling band
            outside_band = np.abs(freq_area - final_value) > settling_criterion
            if np.any(outside_band):
                settling_idx = np.where(outside_band)[0][-1]
                settling_indices.append(settling_idx)
            else:
                settling_indices.append(0)

        settling_time = np.mean([results['time'][idx] for idx in settling_indices])

        # Control effort
        total_control_effort = np.sum(results['control_effort'])

        # Attack detection rate
        attack_detection_rate = np.mean(results['attack_detected']) if np.any(results['attack_detected']) else 0

        metrics = {
            'max_frequency_deviation': max_freq_dev,
            'rms_frequency_deviation': rms_freq_dev,
            'settling_time': settling_time,
            'total_control_effort': total_control_effort,
            'attack_detection_rate': attack_detection_rate
        }

        return metrics

    def compare_scenarios(self, scenarios=['conventional', 'decentralized_bess', 'hierarchical_ml', 'ami_dr', 'wams_adaptive']):
        """
        Compare multiple AGC scenarios
        """
        comparison_results = {}

        for scenario in scenarios:
            print(f"Running {scenario} scenario...")
            results = self.run_scenario(scenario)
            comparison_results[scenario] = results

        return comparison_results

    def plot_results(self, results, scenario_name='AGC Simulation'):
        """
        Plot simulation results
        """
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle(f'{scenario_name} Results', fontsize=16, fontweight='bold')

        # Frequency deviations
        axes[0,0].plot(results['time'], results['delta_f'])
        axes[0,0].set_title('Frequency Deviations')
        axes[0,0].set_xlabel('Time (hours)')
        axes[0,0].set_ylabel('Δf (Hz)')
        axes[0,0].grid(True)
        axes[0,0].legend([f'Area {i+1}' for i in range(self.power_system.num_areas)])

        # Area Control Error
        axes[0,1].plot(results['time'], results['ACE'])
        axes[0,1].set_title('Area Control Error')
        axes[0,1].set_xlabel('Time (hours)')
        axes[0,1].set_ylabel('ACE')
        axes[0,1].grid(True)
        axes[0,1].legend([f'Area {i+1}' for i in range(self.power_system.num_areas)])

        # Renewable Power
        axes[0,2].plot(results['time'], results['P_renewable'])
        axes[0,2].set_title('Renewable Power Generation')
        axes[0,2].set_xlabel('Time (hours)')
        axes[0,2].set_ylabel('P_renewable (p.u.)')
        axes[0,2].grid(True)
        axes[0,2].legend([f'Area {i+1}' for i in range(self.power_system.num_areas)])

        # BESS Power
        axes[1,0].plot(results['time'], results['P_bess'])
        axes[1,0].set_title('BESS Power Output')
        axes[1,0].set_xlabel('Time (hours)')
        axes[1,0].set_ylabel('P_BESS (p.u.)')
        axes[1,0].grid(True)
        axes[1,0].legend([f'Area {i+1}' for i in range(self.power_system.num_areas)])

        # Battery State of Charge
        axes[1,1].plot(results['time'], results['SoC'] * 100)
        axes[1,1].set_title('Battery State of Charge')
        axes[1,1].set_xlabel('Time (hours)')
        axes[1,1].set_ylabel('SoC (%)')
        axes[1,1].grid(True)
        axes[1,1].legend([f'Area {i+1}' for i in range(self.power_system.num_areas)])

        # Control Effort and Security
        axes[1,2].plot(results['time'], results['control_effort'], 'b-', label='Control Effort')
        ax2 = axes[1,2].twinx()
        ax2.plot(results['time'], results['attack_detected'], 'r-', alpha=0.7, label='Attack Detected')
        axes[1,2].set_title('Control Effort & Security Status')
        axes[1,2].set_xlabel('Time (hours)')
        axes[1,2].set_ylabel('Control Effort', color='b')
        ax2.set_ylabel('Attack Detected', color='r')
        axes[1,2].grid(True)

        plt.tight_layout()
        plt.show()

        # Print performance metrics
        print(f"\n{scenario_name} Performance Metrics:")
        print("-" * 40)
        for key, value in results['performance_metrics'].items():
            print(f"{key.replace('_', ' ').title()}: {value:.4f}")

def main():
    """
    Main simulation function demonstrating all AGC scenarios
    """
    print("Advanced AGC Simulation for Renewable-Integrated Smart Grids")
    print("=" * 60)

    # Initialize simulator
    simulator = AGCSimulator(num_areas=3, renewable_penetration=0.3)

    # Run comparison of all scenarios
    scenarios = ['conventional', 'decentralized_bess', 'hierarchical_ml', 'ami_dr', 'wams_adaptive']
    comparison_results = simulator.compare_scenarios(scenarios)

    # Plot results for each scenario
    for scenario_name, results in comparison_results.items():
        simulator.plot_results(results, scenario_name.replace('_', ' ').title())

    # Create comparison summary
    print("\nScenario Comparison Summary:")
    print("=" * 50)

    comparison_df = pd.DataFrame()
    for scenario_name, results in comparison_results.items():
        metrics = results['performance_metrics']
        comparison_df[scenario_name] = pd.Series(metrics)

    print(comparison_df.round(4))

    # Calculate improvement percentages relative to conventional
    if 'conventional' in comparison_df.columns:
        improvement_df = pd.DataFrame()
        baseline = comparison_df['conventional']

        for col in comparison_df.columns:
            if col != 'conventional':
                improvement = ((baseline - comparison_df[col]) / baseline * 100)
                improvement_df[col] = improvement

        print("\nImprovement Percentages (vs Conventional AGC):")
        print("=" * 50)
        print(improvement_df.round(2))

    return comparison_results

if __name__ == "__main__":
    results = main()
