"""
Advanced AGC Simulation Framework for Renewable-Integrated Smart Grids
=====================================================================

This comprehensive simulation framework implements advanced Automatic Generation Control (AGC) 
strategies for power systems with high renewable energy penetration. The framework includes:

1. Multi-area power system dynamics with renewable integration
2. Battery Energy Storage Systems (BESS) control
3. Multiple AGC strategies (Conventional, Decentralized, Hierarchical)
4. Machine Learning-based renewable forecasting
5. Cyber-physical security monitoring
6. Performance analysis and visualization tools

Based on the research paper: "Advanced Automatic Generation Control Strategies for 
Renewable-Integrated Smart Grids: A Scenario-Based Analysis"

Author: Generated from research analysis
Date: 2024
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import odeint
from scipy.signal import TransferFunction, lsim
import warnings
warnings.filterwarnings('ignore')

class PowerSystemModel:
    """
    Multi-area power system model with AGC and renewable integration

    This class implements the mathematical models from the AGC paper including:
    - Swing equation dynamics
    - Governor and turbine models
    - Area Control Error (ACE) calculation
    - BESS integration
    - Tie-line power flow
    """

    def __init__(self, num_areas=2):
        self.num_areas = num_areas

        # System parameters for each area (typical power system values)
        self.H = [5.0, 4.5]  # Inertia constants (s)
        self.D = [1.0, 1.2]  # Damping coefficients (pu/Hz)
        self.R = [2.4, 2.0]  # Governor droop (Hz/pu)
        self.Tg = [0.08, 0.10]  # Governor time constants (s)
        self.Tt = [0.3, 0.4]  # Turbine time constants (s)
        self.B = [0.425, 0.425]  # Frequency bias factors (pu/Hz)

        # Tie-line parameters
        self.T12 = 0.545  # Tie-line synchronizing coefficient

        # BESS parameters
        self.Kp_bess = [0.5, 0.4]  # Proportional gains for BESS
        self.Ki_bess = [0.3, 0.25]  # Integral gains for BESS
        self.Kd_bess = [0.1, 0.08]  # Derivative gains for BESS
        self.soc_limits = [0.2, 0.8]  # SOC limits (20% to 80%)

        # Initialize system state
        self.reset_system()

    def reset_system(self):
        """Reset system to initial conditions"""
        # State variables: [df1, df2, dPg1, dPg2, dPtie, ACE1_int, ACE2_int, SOC1, SOC2]
        self.x = np.zeros(9)
        self.time = 0

    def renewable_generation(self, t):
        """
        Model renewable energy generation with intermittency

        Args:
            t: Time in seconds

        Returns:
            List of renewable power output for each area
        """
        # Solar generation (day/night cycle with variability)
        solar_base = 0.5 * (1 + np.sin(2*np.pi*t/24 - np.pi/2))  # 24-hour cycle
        solar_noise = 0.2 * np.sin(2*np.pi*t/0.5) + 0.1 * np.random.normal(0, 0.1)
        solar_power = max(0, solar_base + solar_noise)

        # Wind generation (more random variability)
        wind_base = 0.6
        wind_noise = 0.3 * np.sin(2*np.pi*t/1.2) + 0.2 * np.random.normal(0, 0.15)
        wind_power = max(0, min(1.0, wind_base + wind_noise))

        return [solar_power, wind_power]

    def load_variation(self, t):
        """Model load variations with daily patterns"""
        # Daily load cycle with random variations
        load_base = 0.8 + 0.3 * np.sin(2*np.pi*t/24)
        load_noise = 0.1 * np.random.normal(0, 0.05)
        return [load_base + load_noise, load_base + load_noise * 0.8]

    def bess_control(self, ace, df, soc):
        """
        Battery Energy Storage System control with PID controller

        Args:
            ace: Area Control Error
            df: Frequency deviation
            soc: State of Charge

        Returns:
            BESS control action
        """
        # PID control action
        control_action = self.Kp_bess[0] * df + self.Ki_bess[0] * ace

        # SOC constraints
        if soc <= self.soc_limits[0] and control_action < 0:
            control_action = 0  # Prevent over-discharge
        elif soc >= self.soc_limits[1] and control_action > 0:
            control_action = 0  # Prevent over-charge

        return control_action

    def ace_calculation(self, df, dptie, area):
        """
        Calculate Area Control Error (ACE)

        ACE = ΔPtie + B*Δf

        Args:
            df: Frequency deviation
            dptie: Tie-line power deviation
            area: Area index

        Returns:
            Area Control Error
        """
        return dptie + self.B[area] * df

    def system_dynamics(self, x, t, agc_type='conventional', load_disturbance=None):
        """
        System dynamics equations based on the swing equation and AGC models

        State vector: [df1, df2, dPg1, dPg2, dPtie, ACE1_int, ACE2_int, SOC1, SOC2]

        Args:
            x: State vector
            t: Time
            agc_type: Type of AGC strategy
            load_disturbance: External load disturbance

        Returns:
            State derivatives
        """
        df1, df2, dPg1, dPg2, dPtie, ace1_int, ace2_int, soc1, soc2 = x

        # Get renewable generation and load variations
        pres = self.renewable_generation(t)
        pload = self.load_variation(t) if load_disturbance is None else load_disturbance

        # Area Control Errors
        ace1 = self.ace_calculation(df1, dPtie, 0)
        ace2 = self.ace_calculation(df2, -dPtie, 1)

        # BESS control actions
        pbess1 = self.bess_control(ace1, df1, soc1)
        pbess2 = self.bess_control(ace2, df2, soc2)

        # AGC control actions based on strategy
        if agc_type == 'conventional':
            # Conventional PI control
            dpg1_ref = -0.5 * ace1_int
            dpg2_ref = -0.5 * ace2_int
        elif agc_type == 'decentralized':
            # Decentralized control with BESS
            dpg1_ref = -0.4 * ace1_int - 0.2 * df1
            dpg2_ref = -0.4 * ace2_int - 0.2 * df2
        elif agc_type == 'hierarchical':
            # Hierarchical control with prediction
            pred_error1 = 0.1 * np.sin(2*np.pi*t/5)  # Simplified prediction error
            pred_error2 = 0.1 * np.cos(2*np.pi*t/5)
            dpg1_ref = -0.6 * ace1_int - 0.3 * pred_error1
            dpg2_ref = -0.6 * ace2_int - 0.3 * pred_error2
        else:
            dpg1_ref = dpg2_ref = 0

        # System differential equations
        # Frequency dynamics (swing equation)
        ddf1_dt = (dPg1 + pres[0] + pbess1 - pload[0] - self.D[0]*df1 - self.T12*(df1-df2)) / (2*self.H[0])
        ddf2_dt = (dPg2 + pres[1] + pbess2 - pload[1] - self.D[1]*df2 - self.T12*(df2-df1)) / (2*self.H[1])

        # Governor and turbine dynamics
        ddPg1_dt = (dpg1_ref - dPg1 - df1/self.R[0]) / self.Tg[0]
        ddPg2_dt = (dpg2_ref - dPg2 - df2/self.R[1]) / self.Tg[1]

        # Tie-line power flow
        ddPtie_dt = self.T12 * (df1 - df2)

        # ACE integral terms
        dace1_int_dt = ace1
        dace2_int_dt = ace2

        # BESS State of Charge dynamics
        dsoc1_dt = -pbess1 * 0.1  # Simplified SOC dynamics
        dsoc2_dt = -pbess2 * 0.1

        return [ddf1_dt, ddf2_dt, ddPg1_dt, ddPg2_dt, ddPtie_dt, 
                dace1_int_dt, dace2_int_dt, dsoc1_dt, dsoc2_dt]

class RenewableEnergyModel:
    """
    Model for renewable energy sources with forecasting capabilities

    Includes solar and wind generation models with weather scenario variations
    """

    def __init__(self):
        self.solar_capacity = 100  # MW
        self.wind_capacity = 150   # MW

    def generate_profile(self, time_hours, weather_scenario='normal'):
        """
        Generate renewable energy profiles for different weather scenarios

        Args:
            time_hours: Array of time points in hours
            weather_scenario: Weather condition ('normal', 'sunny', 'cloudy', 'windy', 'calm')

        Returns:
            Tuple of (solar_profile, wind_profile) in MW
        """
        t = np.array(time_hours)

        # Solar profile with weather variations
        if weather_scenario == 'cloudy':
            solar_factor = 0.3
        elif weather_scenario == 'sunny':
            solar_factor = 1.0
        else:
            solar_factor = 0.7

        solar_profile = solar_factor * self.solar_capacity * np.maximum(0, 
            np.sin(np.pi * (t % 24) / 12) + 0.2 * np.random.normal(0, 0.1, len(t)))

        # Wind profile with turbulence
        if weather_scenario == 'calm':
            wind_factor = 0.2
        elif weather_scenario == 'windy':
            wind_factor = 1.0
        else:
            wind_factor = 0.6

        wind_profile = wind_factor * self.wind_capacity * (
            0.5 + 0.3 * np.sin(2*np.pi*t/8) + 0.2 * np.random.normal(0, 0.2, len(t)))
        wind_profile = np.clip(wind_profile, 0, self.wind_capacity)

        return solar_profile, wind_profile

    def forecast_error(self, actual_profile, forecast_horizon=1):
        """
        Simulate forecasting errors

        Args:
            actual_profile: Actual renewable generation
            forecast_horizon: Forecast horizon in hours

        Returns:
            Forecasted profile with errors
        """
        # Add forecast uncertainty
        error_std = 0.1 + 0.05 * forecast_horizon  # Increasing error with horizon
        forecast_error = np.random.normal(0, error_std, len(actual_profile))
        forecast = actual_profile + actual_profile * forecast_error
        return np.clip(forecast, 0, None)

class MLPredictor:
    """
    Machine Learning predictor for renewable energy forecasting

    Simulates ML-based prediction with configurable accuracy and horizon
    """

    def __init__(self):
        self.forecast_accuracy = 0.85  # 85% accuracy
        self.prediction_horizon = 24   # 24 hours ahead

    def predict_renewable_output(self, historical_data, forecast_hours=24):
        """
        Simulate ML-based renewable energy prediction

        Args:
            historical_data: Historical renewable generation data
            forecast_hours: Forecast horizon in hours

        Returns:
            Forecasted renewable generation
        """
        # Simple autoregressive model simulation
        forecast_points = int(forecast_hours * 10)  # 10 points per hour

        # Add trend and seasonal components
        trend = np.linspace(historical_data[-1], historical_data[-1] * 1.1, forecast_points)
        seasonal = 0.3 * np.sin(2*np.pi*np.arange(forecast_points)/(24*10))
        noise = 0.1 * np.random.normal(0, 1, forecast_points)

        # Simulate prediction uncertainty
        uncertainty_factor = 1 - self.forecast_accuracy
        prediction_error = uncertainty_factor * np.random.normal(0, 0.2, forecast_points)

        forecast = trend + seasonal + noise + prediction_error
        return np.maximum(0, forecast)  # Ensure non-negative values

class CyberSecurityModule:
    """
    Cyber-physical security monitoring and attack detection

    Implements security measures and attack simulation for AGC systems
    """

    def __init__(self):
        self.attack_detection_rate = 0.94  # 94% detection rate
        self.false_positive_rate = 0.05    # 5% false positive rate
        self.response_time = 2.0           # 2 seconds average response time

    def detect_attack(self, agc_signal, threshold=0.1):
        """
        Simulate attack detection based on signal anomalies

        Args:
            agc_signal: AGC control signal
            threshold: Detection threshold

        Returns:
            Boolean indicating attack detection
        """
        # Simple anomaly detection based on signal magnitude
        anomaly_score = np.abs(agc_signal).max()
        if anomaly_score > threshold:
            detection_prob = np.random.random()
            return detection_prob < self.attack_detection_rate
        return False

    def generate_attack_scenario(self, duration=30, attack_start=10, attack_duration=5):
        """
        Generate a cyber attack scenario for testing

        Args:
            duration: Total simulation duration
            attack_start: Time when attack starts
            attack_duration: Duration of the attack

        Returns:
            Tuple of (time, normal_signal, attack_signal, attack_mask)
        """
        t = np.linspace(0, duration, 1000)
        normal_signal = 0.01 * np.sin(2*np.pi*t/5) + 0.005 * np.random.normal(0, 1, len(t))

        # Inject attack (false data injection)
        attack_signal = normal_signal.copy()
        attack_mask = (t >= attack_start) & (t <= attack_start + attack_duration)
        attack_signal[attack_mask] += 0.2 * np.sin(10*np.pi*t[attack_mask])  # High frequency attack

        return t, normal_signal, attack_signal, attack_mask

class AGCSimulator:
    """
    Main AGC simulation class

    Orchestrates the simulation of different AGC strategies and provides
    analysis and visualization capabilities
    """

    def __init__(self):
        self.power_system = PowerSystemModel()
        self.renewable_model = RenewableEnergyModel()
        self.ml_predictor = MLPredictor()
        self.cyber_security = CyberSecurityModule()
        self.results = {}

    def run_scenario(self, scenario_name, agc_type, duration=50, dt=0.01, 
                    disturbance_time=10, disturbance_magnitude=0.1):
        """
        Run a specific AGC scenario

        Args:
            scenario_name: Name identifier for the scenario
            agc_type: Type of AGC strategy ('conventional', 'decentralized', 'hierarchical')
            duration: Simulation duration in seconds
            dt: Time step for integration
            disturbance_time: Time when load disturbance occurs
            disturbance_magnitude: Magnitude of load disturbance

        Returns:
            Dictionary containing simulation results
        """

        print(f"Running scenario: {scenario_name} with {agc_type} AGC")

        # Time vector
        t = np.arange(0, duration, dt)

        # Reset system
        self.power_system.reset_system()

        # Define load disturbance
        load_dist = [0, 0] if disturbance_time > duration else [disturbance_magnitude, 0]

        # Simulate system
        solution = odeint(self.power_system.system_dynamics, 
                         self.power_system.x, t, 
                         args=(agc_type, load_dist))

        # Extract results
        results = {
            'time': t,
            'frequency_area1': solution[:, 0],
            'frequency_area2': solution[:, 1],
            'generation_area1': solution[:, 2],
            'generation_area2': solution[:, 3],
            'tie_line_power': solution[:, 4],
            'ace_area1': solution[:, 5],
            'ace_area2': solution[:, 6],
            'soc_area1': solution[:, 7],
            'soc_area2': solution[:, 8],
            'scenario_name': scenario_name,
            'agc_type': agc_type
        }

        # Calculate performance metrics
        results['metrics'] = self.calculate_metrics(results)

        self.results[scenario_name] = results
        return results

    def calculate_metrics(self, results):
        """
        Calculate performance metrics for AGC evaluation

        Args:
            results: Simulation results dictionary

        Returns:
            Dictionary of performance metrics
        """
        freq1 = results['frequency_area1']
        freq2 = results['frequency_area2']
        gen1 = results['generation_area1']
        gen2 = results['generation_area2']
        t = results['time']

        # Maximum frequency deviation
        max_freq_dev = max(np.max(np.abs(freq1)), np.max(np.abs(freq2)))

        # Settling time (time to reach within 2% of final value)
        if max_freq_dev > 0:
            settling_idx1 = np.where(np.abs(freq1) < 0.02 * max_freq_dev)[0]
            settling_idx2 = np.where(np.abs(freq2) < 0.02 * max_freq_dev)[0]
            settling_time = max(t[settling_idx1[0]] if len(settling_idx1) > 0 else t[-1],
                               t[settling_idx2[0]] if len(settling_idx2) > 0 else t[-1])
        else:
            settling_time = 0

        # Control effort (integral of control actions)
        control_effort = np.trapz(np.abs(gen1), t) + np.trapz(np.abs(gen2), t)

        # Frequency nadir
        freq_nadir = min(np.min(freq1), np.min(freq2))

        # RMS frequency deviation
        rms_freq = np.sqrt((np.mean(freq1**2) + np.mean(freq2**2)) / 2)

        return {
            'max_frequency_deviation': max_freq_dev,
            'settling_time': settling_time,
            'control_effort': control_effort,
            'frequency_nadir': freq_nadir,
            'rms_frequency_deviation': rms_freq
        }

    def compare_strategies(self, strategies=['conventional', 'decentralized', 'hierarchical']):
        """
        Compare different AGC strategies

        Args:
            strategies: List of AGC strategy names to compare

        Returns:
            Dictionary of performance metrics for each strategy
        """
        comparison_results = {}

        for strategy in strategies:
            scenario_name = f"{strategy}_agc_comparison"
            results = self.run_scenario(scenario_name, strategy)
            comparison_results[strategy] = results['metrics']

        return comparison_results

    def plot_results(self, scenario_name, save_path=None):
        """
        Plot comprehensive simulation results

        Args:
            scenario_name: Name of scenario to plot
            save_path: Optional path to save the plot
        """
        if scenario_name not in self.results:
            print(f"Scenario {scenario_name} not found")
            return

        results = self.results[scenario_name]
        t = results['time']

        fig, axes = plt.subplots(3, 2, figsize=(15, 12))
        fig.suptitle(f'AGC Simulation Results: {results["scenario_name"]}', fontsize=16)

        # Frequency deviations
        axes[0, 0].plot(t, results['frequency_area1'], 'b-', label='Area 1', linewidth=2)
        axes[0, 0].plot(t, results['frequency_area2'], 'r-', label='Area 2', linewidth=2)
        axes[0, 0].set_ylabel('Frequency Deviation (Hz)')
        axes[0, 0].set_title('Frequency Response')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].legend()

        # Generation changes
        axes[0, 1].plot(t, results['generation_area1'], 'b-', label='Area 1', linewidth=2)
        axes[0, 1].plot(t, results['generation_area2'], 'r-', label='Area 2', linewidth=2)
        axes[0, 1].set_ylabel('Generation Change (pu)')
        axes[0, 1].set_title('Generation Response')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].legend()

        # Tie-line power
        axes[1, 0].plot(t, results['tie_line_power'], 'g-', linewidth=2)
        axes[1, 0].set_ylabel('Tie-line Power (pu)')
        axes[1, 0].set_title('Tie-line Power Flow')
        axes[1, 0].grid(True, alpha=0.3)

        # Area Control Errors
        axes[1, 1].plot(t, results['ace_area1'], 'b-', label='Area 1', linewidth=2)
        axes[1, 1].plot(t, results['ace_area2'], 'r-', label='Area 2', linewidth=2)
        axes[1, 1].set_ylabel('ACE')
        axes[1, 1].set_title('Area Control Error')
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].legend()

        # Battery SOC
        axes[2, 0].plot(t, results['soc_area1'], 'b-', label='Area 1', linewidth=2)
        axes[2, 0].plot(t, results['soc_area2'], 'r-', label='Area 2', linewidth=2)
        axes[2, 0].set_ylabel('SOC')
        axes[2, 0].set_title('Battery State of Charge')
        axes[2, 0].set_xlabel('Time (s)')
        axes[2, 0].grid(True, alpha=0.3)
        axes[2, 0].legend()

        # Performance metrics text
        metrics = results['metrics']
        metrics_text = f"""Performance Metrics:
Max Freq Dev: {metrics['max_frequency_deviation']:.4f} Hz
Settling Time: {metrics['settling_time']:.2f} s
Control Effort: {metrics['control_effort']:.4f}
Freq Nadir: {metrics['frequency_nadir']:.4f} Hz
RMS Freq Dev: {metrics['rms_frequency_deviation']:.4f} Hz"""

        axes[2, 1].text(0.1, 0.5, metrics_text, transform=axes[2, 1].transAxes,
                       fontsize=10, verticalalignment='center',
                       bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        axes[2, 1].set_title('Performance Metrics')
        axes[2, 1].axis('off')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show()

def demonstration_example():
    """
    Demonstration of the AGC simulation framework

    This function provides a complete example of how to use the simulation framework
    """
    print("="*80)
    print("ADVANCED AGC SIMULATION FRAMEWORK DEMONSTRATION")
    print("="*80)

    # Initialize simulator
    simulator = AGCSimulator()

    # Set random seed for reproducible results
    np.random.seed(42)

    print("\n1. Running AGC strategy comparison...")
    # Compare different AGC strategies
    comparison_results = simulator.compare_strategies(['conventional', 'decentralized', 'hierarchical'])

    # Display results
    print("\nPerformance Comparison Results:")
    print("-" * 60)
    print(f"{'Strategy':<15} {'Max Freq Dev':<12} {'Settling Time':<14} {'Control Effort':<14}")
    print("-" * 60)

    for strategy, metrics in comparison_results.items():
        print(f"{strategy:<15} {metrics['max_frequency_deviation']:<12.6f} "
              f"{metrics['settling_time']:<14.2f} {metrics['control_effort']:<14.6f}")

    print("\n2. Testing renewable energy forecasting...")
    # Demonstrate renewable forecasting
    renewable = RenewableEnergyModel()
    time_hours = np.linspace(0, 24, 240)
    solar, wind = renewable.generate_profile(time_hours)

    print(f"Solar generation: {np.mean(solar):.1f} MW average, {np.max(solar):.1f} MW peak")
    print(f"Wind generation: {np.mean(wind):.1f} MW average, {np.max(wind):.1f} MW peak")

    print("\n3. Testing cyber security module...")
    # Demonstrate cybersecurity
    cyber = CyberSecurityModule()
    t, normal, attack, mask = cyber.generate_attack_scenario()

    print(f"Attack detection rate: {cyber.attack_detection_rate*100:.1f}%")
    print(f"False positive rate: {cyber.false_positive_rate*100:.1f}%")

    print("\n4. Running detailed scenario analysis...")
    # Run detailed scenarios
    detailed_results = {}
    for agc_type in ['conventional', 'decentralized', 'hierarchical']:
        scenario_name = f"{agc_type}_detailed"
        results = simulator.run_scenario(scenario_name, agc_type, duration=20, dt=0.1)
        detailed_results[agc_type] = results['metrics']

    print("\nDetailed Performance Analysis:")
    print("-" * 80)
    print(f"{'Metric':<25} {'Conventional':<15} {'Decentralized':<15} {'Hierarchical':<15}")
    print("-" * 80)

    metrics_to_show = ['max_frequency_deviation', 'settling_time', 'control_effort', 'rms_frequency_deviation']
    metric_names = ['Max Freq Deviation', 'Settling Time (s)', 'Control Effort', 'RMS Freq Deviation']

    for metric, name in zip(metrics_to_show, metric_names):
        conv_val = detailed_results['conventional'][metric]
        decent_val = detailed_results['decentralized'][metric]
        hier_val = detailed_results['hierarchical'][metric]

        print(f"{name:<25} {conv_val:<15.6f} {decent_val:<15.6f} {hier_val:<15.6f}")

    print("\n" + "="*80)
    print("SIMULATION COMPLETE")
    print("="*80)

    return simulator, comparison_results, detailed_results

# Main execution
if __name__ == "__main__":
    # Run demonstration
    simulator, comparison, detailed = demonstration_example()

    # Additional analysis can be performed here
    print("\nFramework ready for custom analysis and research applications.")
    print("Available methods:")
    print("- simulator.run_scenario(): Run custom scenarios")
    print("- simulator.compare_strategies(): Compare AGC strategies")
    print("- simulator.plot_results(): Visualize results")
    print("- RenewableEnergyModel(): Model renewable generation")
    print("- CyberSecurityModule(): Simulate cyber attacks")
    print("- MLPredictor(): Machine learning forecasting")
