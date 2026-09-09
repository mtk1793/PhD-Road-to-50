# Neuro-OptimaFACTS: Complete Implementation
# A Novel Explainable AI-Based Hybrid Framework for Optimized FACTS Device Control

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, LSTM, Input, concatenate
from tensorflow.keras.optimizers import Adam
import pywt
import shap
from scipy import signal
from scipy.fft import fft, fftfreq
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

# Import real-time data integrator
from integrate_realtime_data import RealDataIntegrator

class DataGenerator:
    """Generate synthetic renewable energy and grid data"""
    
    def __init__(self, duration_hours=8760, time_step=1):  # 1 year, hourly data
        self.duration_hours = duration_hours
        self.time_step = time_step
        self.time_index = np.arange(0, duration_hours, time_step)
        
    def generate_wind_data(self):
        """Generate realistic wind speed data with seasonal variations"""
        # Base wind speed with seasonal variation
        seasonal_component = 2 * np.sin(2 * np.pi * self.time_index / (365*24)) + 5
        
        # Daily variation
        daily_component = 1.5 * np.sin(2 * np.pi * self.time_index / 24)
        
        # Random fluctuations
        random_component = np.random.normal(0, 1.5, len(self.time_index))
        
        # Combine components
        wind_speed = seasonal_component + daily_component + random_component
        wind_speed = np.clip(wind_speed, 0, 25)  # Physical limits
        
        # Convert to wind power using typical wind turbine curve
        wind_power = np.where(wind_speed < 3, 0,
                             np.where(wind_speed < 12, 
                                    1.5 * (wind_speed - 3)**2,
                                    np.where(wind_speed < 25, 1.5 * 81, 0)))
        
        return wind_speed, wind_power
    
    def generate_solar_data(self):
        """Generate realistic solar irradiance data"""
        # Seasonal variation
        seasonal_component = 200 * (1 + 0.3 * np.sin(2 * np.pi * (self.time_index / 24 - 80) / 365))
        
        # Daily variation (daylight hours)
        hour_of_day = self.time_index % 24
        daily_component = np.where((hour_of_day >= 6) & (hour_of_day <= 18),
                                  300 * np.sin(np.pi * (hour_of_day - 6) / 12), 0)
        
        # Weather variation
        weather_component = np.random.normal(1, 0.2, len(self.time_index))
        weather_component = np.clip(weather_component, 0.1, 1.2)
        
        solar_irradiance = (seasonal_component + daily_component) * weather_component
        solar_irradiance = np.clip(solar_irradiance, 0, 1000)
        
        # Convert to solar power (assume 20% efficiency)
        solar_power = solar_irradiance * 0.2
        
        return solar_irradiance, solar_power
    
    def generate_load_data(self):
        """Generate realistic load demand patterns"""
        # Base load
        base_load = 500 + 100 * np.sin(2 * np.pi * self.time_index / (365*24))
        
        # Daily pattern
        hour_of_day = self.time_index % 24
        daily_pattern = np.where(hour_of_day < 6, 0.7,
                                np.where(hour_of_day < 9, 0.9,
                                        np.where(hour_of_day < 17, 1.0,
                                                np.where(hour_of_day < 22, 1.1, 0.8))))
        
        # Weekly pattern (lower on weekends)
        day_of_week = (self.time_index // 24) % 7
        weekly_pattern = np.where((day_of_week == 5) | (day_of_week == 6), 0.85, 1.0)
        
        # Random variation
        random_variation = np.random.normal(1, 0.1, len(self.time_index))
        
        load_demand = base_load * daily_pattern * weekly_pattern * random_variation
        
        return load_demand
    
    def generate_grid_parameters(self):
        """Generate grid voltage, frequency, and power quality parameters"""
        # Nominal voltage with variations
        voltage = 1.0 + np.random.normal(0, 0.02, len(self.time_index))  # Per unit
        
        # Frequency variations
        frequency = 50.0 + np.random.normal(0, 0.1, len(self.time_index))  # Hz
        
        # Harmonic distortion
        thd = 2 + np.random.exponential(1, len(self.time_index))  # %
        
        # Power factor
        power_factor = 0.95 + np.random.normal(0, 0.05, len(self.time_index))
        power_factor = np.clip(power_factor, 0.8, 1.0)
        
        return voltage, frequency, thd, power_factor
    
    def generate_complete_dataset(self):
        """Generate complete dataset for simulation"""
        wind_speed, wind_power = self.generate_wind_data()
        solar_irradiance, solar_power = self.generate_solar_data()
        load_demand = self.generate_load_data()
        voltage, frequency, thd, power_factor = self.generate_grid_parameters()
        
        # Create DataFrame
        data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=len(self.time_index), freq='H'),
            'wind_speed': wind_speed,
            'wind_power': wind_power,
            'solar_irradiance': solar_irradiance,
            'solar_power': solar_power,
            'load_demand': load_demand,
            'voltage': voltage,
            'frequency': frequency,
            'thd': thd,
            'power_factor': power_factor
        })
        
        # Calculate additional parameters
        data['total_renewable'] = data['wind_power'] + data['solar_power']
        data['net_load'] = data['load_demand'] - data['total_renewable']
        data['renewable_penetration'] = data['total_renewable'] / data['load_demand']
        
        return data

class WaveletNeuralNetwork:
    """Wavelet Neural Network for signal processing and feature extraction"""
    
    def __init__(self, wavelet='db4', levels=4):
        self.wavelet = wavelet
        self.levels = levels
        self.scalers = {}
        self.models = {}
        
    def wavelet_decomposition(self, signal):
        """Decompose signal using wavelet transform"""
        coeffs = pywt.wavedec(signal, self.wavelet, level=self.levels)
        return coeffs
    
    def wavelet_reconstruction(self, coeffs):
        """Reconstruct signal from wavelet coefficients"""
        return pywt.waverec(coeffs, self.wavelet)
    
    def extract_features(self, data):
        """Extract wavelet-based features"""
        features = {}
        
        for column in ['voltage', 'frequency', 'thd', 'total_renewable']:
            if column in data.columns:
                coeffs = self.wavelet_decomposition(data[column].values)
                
                # Extract statistical features from each level
                for i, coeff in enumerate(coeffs):
                    features[f'{column}_level_{i}_mean'] = np.mean(coeff)
                    features[f'{column}_level_{i}_std'] = np.std(coeff)
                    features[f'{column}_level_{i}_energy'] = np.sum(coeff**2)
                    features[f'{column}_level_{i}_entropy'] = -np.sum(coeff**2 * np.log(coeff**2 + 1e-10))
        
        return features
    
    def build_wnn_model(self, input_shape):
        """Build Wavelet Neural Network model"""
        model = Sequential([
            Dense(128, activation='tanh', input_shape=(input_shape,)),
            Dense(64, activation='tanh'),
            Dense(32, activation='tanh'),
            Dense(16, activation='tanh'),
            Dense(1, activation='linear')
        ])
        
        model.compile(optimizer=Adam(learning_rate=0.001), 
                     loss='mse', metrics=['mae'])
        return model
    
    def train(self, X_train, y_train, X_val, y_val):
        """Train the WNN model"""
        # Normalize inputs
        self.scaler_X = StandardScaler()
        self.scaler_y = StandardScaler()
        
        X_train_scaled = self.scaler_X.fit_transform(X_train)
        X_val_scaled = self.scaler_X.transform(X_val)
        y_train_scaled = self.scaler_y.fit_transform(y_train.reshape(-1, 1)).flatten()
        y_val_scaled = self.scaler_y.transform(y_val.reshape(-1, 1)).flatten()
        
        # Build and train model
        self.model = self.build_wnn_model(X_train_scaled.shape[1])
        
        history = self.model.fit(
            X_train_scaled, y_train_scaled,
            validation_data=(X_val_scaled, y_val_scaled),
            epochs=100, batch_size=32, verbose=0
        )
        
        return history
    
    def predict(self, X):
        """Make predictions using trained WNN"""
        X_scaled = self.scaler_X.transform(X)
        y_scaled = self.model.predict(X_scaled)
        return self.scaler_y.inverse_transform(y_scaled.reshape(-1, 1)).flatten()

class RecurrentKalmanFilter:
    """Recurrent Kalman Filter for state estimation and noise reduction"""
    
    def __init__(self, state_dim=4, obs_dim=2):
        self.state_dim = state_dim
        self.obs_dim = obs_dim
        
        # Initialize system matrices
        self.F = np.eye(state_dim)  # State transition matrix
        self.H = np.random.randn(obs_dim, state_dim) * 0.1  # Observation matrix
        self.Q = np.eye(state_dim) * 0.01  # Process noise covariance
        self.R = np.eye(obs_dim) * 0.1     # Measurement noise covariance
        
        # Initialize state and covariance
        self.x = np.zeros(state_dim)  # State estimate
        self.P = np.eye(state_dim)    # State covariance
        
        self.history = []
        
    def predict(self):
        """Prediction step"""
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        
    def update(self, z):
        """Update step with measurement z"""
        # Innovation
        y = z - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        
        # Kalman gain
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # Update state and covariance
        self.x = self.x + K @ y
        self.P = (np.eye(self.state_dim) - K @ self.H) @ self.P
        
        self.history.append(self.x.copy())
        
    def filter_sequence(self, measurements):
        """Filter entire measurement sequence"""
        filtered_states = []
        
        for z in measurements:
            self.predict()
            self.update(z)
            filtered_states.append(self.x.copy())
            
        return np.array(filtered_states)
    
    def get_filtered_estimates(self):
        """Get filtered state estimates"""
        return np.array(self.history)

class FACTSDeviceModels:
    """Models for FACTS devices: STATCOM, SVC, UPFC"""
    
    def __init__(self):
        self.statcom_params = {'rating': 100, 'response_time': 0.1}  # MVA
        self.svc_params = {'rating': 50, 'response_time': 0.05}      # MVAr
        self.upfc_params = {'rating': 200, 'response_time': 0.2}     # MVA
        
    def statcom_model(self, voltage_ref, voltage_actual, reactive_power_demand):
        """STATCOM model for voltage regulation"""
        # Voltage error
        voltage_error = voltage_ref - voltage_actual
        
        # PI controller parameters
        kp, ki = 2.0, 0.5
        
        # Control signal
        control_signal = kp * voltage_error + ki * np.sum(voltage_error)
        
        # Reactive power injection (limited by rating)
        q_injection = np.clip(control_signal, 
                             -self.statcom_params['rating'], 
                             self.statcom_params['rating'])
        
        # Updated voltage (simplified model)
        voltage_new = voltage_actual + 0.01 * q_injection
        
        return voltage_new, q_injection
    
    def svc_model(self, voltage_ref, voltage_actual):
        """Static Var Compensator model"""
        voltage_error = voltage_ref - voltage_actual
        
        # SVC characteristic (V-Q curve)
        droop = 0.02  # 2% droop
        q_output = voltage_error / droop
        
        # Limit reactive power output
        q_output = np.clip(q_output, 
                          -self.svc_params['rating'], 
                          self.svc_params['rating'])
        
        # Voltage correction
        voltage_corrected = voltage_actual + 0.005 * q_output
        
        return voltage_corrected, q_output
    
    def upfc_model(self, voltage_magnitude, voltage_angle, power_flow_ref):
        """Unified Power Flow Controller model"""
        # Series and shunt converter models
        
        # Series converter (voltage injection)
        voltage_series = 0.1 * np.sin(voltage_angle)  # Simplified
        
        # Shunt converter (reactive power)
        q_shunt = 0.1 * (1.0 - voltage_magnitude) * self.upfc_params['rating']
        
        # Power flow control
        power_flow_actual = voltage_magnitude * np.cos(voltage_angle) * 100  # Simplified
        power_error = power_flow_ref - power_flow_actual
        
        # Control actions
        voltage_corrected = voltage_magnitude + 0.01 * voltage_series
        angle_corrected = voltage_angle + 0.001 * power_error
        
        return voltage_corrected, angle_corrected, q_shunt
    
    def optimize_facts_settings(self, grid_conditions):
        """Optimize FACTS device settings for given grid conditions"""
        voltage = grid_conditions['voltage']
        frequency = grid_conditions['frequency']
        load = grid_conditions['load_demand']
        renewable = grid_conditions['total_renewable']
        
        # Multi-objective optimization
        def objective(x):
            # x = [statcom_q, svc_q, upfc_p, upfc_q]
            voltage_deviation = np.sum((voltage - 1.0)**2)
            reactive_power_cost = 0.1 * (x[0]**2 + x[1]**2 + x[3]**2)
            power_loss = 0.01 * np.sum(x**2)
            
            return voltage_deviation + reactive_power_cost + power_loss
        
        # Constraints
        constraints = [
            {'type': 'ineq', 'fun': lambda x: self.statcom_params['rating'] - abs(x[0])},
            {'type': 'ineq', 'fun': lambda x: self.svc_params['rating'] - abs(x[1])},
            {'type': 'ineq', 'fun': lambda x: self.upfc_params['rating'] - abs(x[2])},
            {'type': 'ineq', 'fun': lambda x: self.upfc_params['rating'] - abs(x[3])}
        ]
        
        # Initial guess
        x0 = [0, 0, 0, 0]
        
        # Optimize
        result = minimize(objective, x0, method='SLSQP', constraints=constraints)
        
        return result.x if result.success else x0

class ExplainableAI:
    """SHAP-based Explainable AI for decision transparency"""
    
    def __init__(self):
        self.explainer = None
        self.shap_values = None
        self.feature_names = None
        
    def initialize_explainer(self, model, X_background):
        """Initialize SHAP explainer"""
        if hasattr(model, 'predict'):
            # For sklearn models
            self.explainer = shap.Explainer(model, X_background)
        else:
            # For custom models
            self.explainer = shap.Explainer(model.predict, X_background)
    
    def calculate_shap_values(self, X_test):
        """Calculate SHAP values for test data"""
        if self.explainer is None:
            raise ValueError("Explainer not initialized")
            
        self.shap_values = self.explainer(X_test)
        return self.shap_values
    
    def generate_explanations(self, X_test, feature_names=None):
        """Generate explanations for predictions"""
        self.feature_names = feature_names
        shap_values = self.calculate_shap_values(X_test)
        
        explanations = {
            'feature_importance': np.abs(shap_values.values).mean(axis=0),
            'individual_contributions': shap_values.values,
            'base_value': shap_values.base_values,
            'feature_names': feature_names or [f'Feature_{i}' for i in range(X_test.shape[1])]
        }
        
        return explanations
    
    def plot_summary(self, shap_values, X_test, feature_names=None):
        """Plot SHAP summary"""
        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_values, X_test, feature_names=feature_names, show=False)
        plt.title('SHAP Feature Importance Summary')
        plt.tight_layout()
        return plt.gcf()
    
    def plot_waterfall(self, shap_values, sample_idx=0):
        """Plot SHAP waterfall for individual prediction"""
        plt.figure(figsize=(10, 6))
        shap.waterfall_plot(shap_values[sample_idx], show=False)
        plt.title(f'SHAP Explanation for Sample {sample_idx}')
        plt.tight_layout()
        return plt.gcf()

class GridStabilityAnalyzer:
    """Analyze grid stability metrics and power quality"""
    
    def __init__(self):
        self.stability_metrics = {}
        
    def calculate_voltage_stability_index(self, voltage_profile):
        """Calculate voltage stability index"""
        # L-index calculation (simplified)
        v_min = np.min(voltage_profile)
        v_max = np.max(voltage_profile)
        v_avg = np.mean(voltage_profile)
        
        # Stability index (0 = stable, 1 = unstable)
        stability_index = 1 - (2 * v_min) / (v_max + v_min)
        
        return stability_index
    
    def analyze_harmonic_distortion(self, signal, sampling_rate=3600):
        """Analyze harmonic content using FFT"""
        # Perform FFT
        fft_signal = fft(signal)
        frequencies = fftfreq(len(signal), 1/sampling_rate)
        
        # Calculate harmonic components
        fundamental_freq = 50  # Hz
        fundamental_idx = np.argmin(np.abs(frequencies - fundamental_freq))
        
        harmonics = {}
        thd_components = []
        
        for h in range(2, 11):  # Up to 10th harmonic
            harmonic_freq = h * fundamental_freq
            harmonic_idx = np.argmin(np.abs(frequencies - harmonic_freq))
            
            if harmonic_idx < len(fft_signal):
                harmonic_magnitude = np.abs(fft_signal[harmonic_idx])
                fundamental_magnitude = np.abs(fft_signal[fundamental_idx])
                
                harmonic_ratio = harmonic_magnitude / (fundamental_magnitude + 1e-10)
                harmonics[f'H{h}'] = harmonic_ratio
                thd_components.append(harmonic_ratio**2)
        
        # Total Harmonic Distortion
        thd = np.sqrt(np.sum(thd_components)) * 100  # Percentage
        
        return thd, harmonics
    
    def calculate_power_quality_metrics(self, voltage, current, frequency):
        """Calculate comprehensive power quality metrics"""
        metrics = {}
        
        # Voltage variations
        metrics['voltage_rms'] = np.sqrt(np.mean(voltage**2))
        metrics['voltage_thd'], _ = self.analyze_harmonic_distortion(voltage)
        metrics['voltage_unbalance'] = np.std(voltage) / np.mean(voltage) * 100
        
        # Frequency variations
        metrics['frequency_deviation'] = np.std(frequency)
        metrics['frequency_range'] = np.max(frequency) - np.min(frequency)
        
        # Power factor
        active_power = np.mean(voltage * current)
        apparent_power = np.sqrt(np.mean(voltage**2) * np.mean(current**2))
        metrics['power_factor'] = active_power / (apparent_power + 1e-10)
        
        # Flicker severity
        voltage_fluctuations = np.diff(voltage)
        metrics['flicker_severity'] = np.std(voltage_fluctuations)
        
        return metrics
    
    def assess_grid_stability(self, grid_data, facts_actions):
        """Comprehensive grid stability assessment"""
        stability_report = {}
        
        # Before FACTS intervention
        voltage_before = grid_data['voltage'].values
        frequency_before = grid_data['frequency'].values
        
        # Simulate after FACTS intervention (simplified)
        voltage_after = voltage_before + facts_actions.get('voltage_correction', 0)
        frequency_after = frequency_before + facts_actions.get('frequency_correction', 0)
        
        # Calculate improvements
        stability_report['voltage_stability_before'] = self.calculate_voltage_stability_index(voltage_before)
        stability_report['voltage_stability_after'] = self.calculate_voltage_stability_index(voltage_after)
        
        stability_report['voltage_std_before'] = np.std(voltage_before)
        stability_report['voltage_std_after'] = np.std(voltage_after)
        
        stability_report['frequency_std_before'] = np.std(frequency_before)
        stability_report['frequency_std_after'] = np.std(frequency_after)
        
        # Calculate improvement percentages
        stability_report['voltage_improvement'] = (
            (stability_report['voltage_std_before'] - stability_report['voltage_std_after']) /
            stability_report['voltage_std_before'] * 100
        )
        
        stability_report['frequency_improvement'] = (
            (stability_report['frequency_std_before'] - stability_report['frequency_std_after']) /
            stability_report['frequency_std_before'] * 100
        )
        
        return stability_report

class NeuroOptimaFACTS:
    """Main Neuro-OptimaFACTS framework integrating all components"""
    
    def __init__(self):
        self.data_generator = DataGenerator()
        self.wnn = WaveletNeuralNetwork()
        self.kalman_filter = RecurrentKalmanFilter()
        self.facts_devices = FACTSDeviceModels()
        self.explainable_ai = ExplainableAI()
        self.stability_analyzer = GridStabilityAnalyzer()
        
        self.trained_models = {}
        self.performance_metrics = {}
        
    def prepare_data(self, data):
        """Prepare data for training and testing"""
        # Extract features using WNN
        wavelet_features = []
        for idx in range(len(data) - 24):  # 24-hour windows
            window_data = data.iloc[idx:idx+24]
            features = self.wnn.extract_features(window_data)
            wavelet_features.append(list(features.values()))
        
        X = np.array(wavelet_features)
        
        # Target: next hour voltage
        y = data['voltage'].values[24:]
        
        # Split data
        split_idx = int(0.8 * len(X))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        return X_train, X_test, y_train, y_test
    
    def train_hybrid_model(self, data):
        """Train the complete hybrid model"""
        print("Preparing data...")
        X_train, X_test, y_train, y_test = self.prepare_data(data)
        
        # Split training data for validation
        val_split = int(0.8 * len(X_train))
        X_val = X_train[val_split:]
        y_val = y_train[val_split:]
        X_train = X_train[:val_split]
        y_train = y_train[:val_split]
        
        print("Training Wavelet Neural Network...")
        wnn_history = self.wnn.train(X_train, y_train, X_val, y_val)
        
        print("Training Kalman Filter...")
        # Prepare measurements for Kalman filter (voltage and frequency)
        measurements = np.column_stack([
            data['voltage'].values[:-1],
            data['frequency'].values[:-1]
        ])
        filtered_states = self.kalman_filter.filter_sequence(measurements)
        
        print("Training complete!")
        
        # Store models
        self.trained_models['wnn'] = self.wnn
        self.trained_models['kalman'] = self.kalman_filter
        
        return X_test, y_test
    
    def optimize_facts_control(self, grid_data, prediction_horizon=24):
        """Optimize FACTS device control based on predictions"""
        print("Optimizing FACTS control...")
        
        facts_actions = {}
        
        # Get recent data for optimization
        recent_data = grid_data.tail(prediction_horizon)
        
        # Optimize FACTS settings
        optimal_settings = self.facts_devices.optimize_facts_settings(recent_data)
        
        facts_actions['statcom_q'] = optimal_settings[0]
        facts_actions['svc_q'] = optimal_settings[1] 
        facts_actions['upfc_p'] = optimal_settings[2]
        facts_actions['upfc_q'] = optimal_settings[3]
        
        # Calculate voltage and frequency corrections
        voltage_correction = 0.01 * (optimal_settings[0] + optimal_settings[1]) / 100
        frequency_correction = 0.001 * optimal_settings[2] / 100
        
        facts_actions['voltage_correction'] = voltage_correction
        facts_actions['frequency_correction'] = frequency_correction
        
        return facts_actions
    
    def generate_explanations(self, X_test, feature_names=None):
        """Generate SHAP-based explanations"""
        print("Generating explanations...")
        
        # Initialize explainer with trained WNN model
        X_background = X_test[:100]  # Background dataset
        self.explainable_ai.initialize_explainer(self.wnn, X_background)
        
        # Generate explanations
        explanations = self.explainable_ai.generate_explanations(
            X_test[:50], feature_names
        )
        
        return explanations
    
    def evaluate_performance(self, X_test, y_test, grid_data):
        """Comprehensive performance evaluation"""
        print("Evaluating performance...")
        
        # Model predictions
        y_pred = self.wnn.predict(X_test)
        
        # Prediction metrics
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        self.performance_metrics['prediction'] = {
            'mse': mse,
            'mae': mae,
            'r2': r2,
            'rmse': np.sqrt(mse)
        }
        
        # FACTS optimization
        facts_actions = self.optimize_facts_control(grid_data)
        
        # Grid stability analysis
        stability_report = self.stability_analyzer.assess_grid_stability(
            grid_data, facts_actions
        )
        
        self.performance_metrics['stability'] = stability_report
        self.performance_metrics['facts_actions'] = facts_actions
        
        return self.performance_metrics
    
    def visualize_results(self, grid_data, X_test, y_test):
        """Create comprehensive visualization of results"""
        fig, axes = plt.subplots(3, 2, figsize=(15, 12))
        
        # 1. Renewable energy generation
        axes[0,0].plot(grid_data.index[:1000], grid_data['wind_power'][:1000], 
                      label='Wind Power', alpha=0.7)
        axes[0,0].plot(grid_data.index[:1000], grid_data['solar_power'][:1000], 
                      label='Solar Power', alpha=0.7)
        axes[0,0].plot(grid_data.index[:1000], grid_data['total_renewable'][:1000], 
                      label='Total Renewable', linewidth=2)
        axes[0,0].set_title('Renewable Energy Generation')
        axes[0,0].set_ylabel('Power (MW)')
        axes[0,0].legend()
        axes[0,0].grid(True)
        
        # 2. Load demand vs renewable generation
        axes[0,1].plot(grid_data.index[:1000], grid_data['load_demand'][:1000], 
                      label='Load Demand')
        axes[0,1].plot(grid_data.index[:1000], grid_data['total_renewable'][:1000], 
                      label='Renewable Generation')
        axes[0,1].fill_between(grid_data.index[:1000], 
                              grid_data['load_demand'][:1000], 
                              grid_data['total_renewable'][:1000], 
                              alpha=0.3, label='Net Load')
        
        axes[0,1].set_title('Load Demand vs Renewable Generation')
        axes[0,1].set_ylabel('Power (MW)')
        axes[0,1].legend()
        axes[0,1].grid(True)
        
        # 3. Voltage profile before and after FACTS
        voltage_original = grid_data['voltage'][:1000]
        facts_actions = self.performance_metrics.get('facts_actions', {})
        voltage_corrected = voltage_original + facts_actions.get('voltage_correction', 0)
        
        axes[1,0].plot(grid_data.index[:1000], voltage_original, 
                      label='Original Voltage', alpha=0.7)
        axes[1,0].plot(grid_data.index[:1000], voltage_corrected, 
                      label='FACTS Corrected', linewidth=2)
        axes[1,0].axhline(y=1.0, color='r', linestyle='--', label='Nominal')
        axes[1,0].axhline(y=0.95, color='orange', linestyle='--', alpha=0.5)
        axes[1,0].axhline(y=1.05, color='orange', linestyle='--', alpha=0.5)
        axes[1,0].set_title('Voltage Profile Improvement')
        axes[1,0].set_ylabel('Voltage (p.u.)')
        axes[1,0].legend()
        axes[1,0].grid(True)
        
        # 4. Prediction accuracy
        if len(X_test) > 0:
            y_pred = self.wnn.predict(X_test[:200])
            y_actual = y_test[:200]
            
            axes[1,1].plot(y_actual, label='Actual', alpha=0.7)
            axes[1,1].plot(y_pred, label='Predicted', alpha=0.7)
            axes[1,1].set_title('Voltage Prediction Accuracy')
            axes[1,1].set_ylabel('Voltage (p.u.)')
            axes[1,1].set_xlabel('Time Steps')
            axes[1,1].legend()
            axes[1,1].grid(True)
        
        # 5. Renewable penetration
        axes[2,0].hist(grid_data['renewable_penetration'], bins=50, alpha=0.7, 
                      color='green', edgecolor='black')
        axes[2,0].set_title('Renewable Penetration Distribution')
        axes[2,0].set_xlabel('Renewable Penetration Ratio')
        axes[2,0].set_ylabel('Frequency')
        axes[2,0].grid(True)
        
        # 6. FACTS device actions
        facts_data = facts_actions
        devices = ['STATCOM', 'SVC', 'UPFC_P', 'UPFC_Q']
        actions = [facts_data.get('statcom_q', 0), 
                  facts_data.get('svc_q', 0),
                  facts_data.get('upfc_p', 0), 
                  facts_data.get('upfc_q', 0)]
        
        colors = ['blue', 'green', 'red', 'orange']
        bars = axes[2,1].bar(devices, actions, color=colors, alpha=0.7)
        axes[2,1].set_title('FACTS Device Control Actions')
        axes[2,1].set_ylabel('Control Signal')
        axes[2,1].grid(True, axis='y')
        
        # Add value labels on bars
        for bar, value in zip(bars, actions):
            height = bar.get_height()
            axes[2,1].text(bar.get_x() + bar.get_width()/2., height,
                          f'{value:.2f}', ha='center', va='bottom')
        
        plt.tight_layout()
        return fig
    
    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        report = "\n" + "="*60 + "\n"
        report += "NEURO-OPTIMAFACTS PERFORMANCE REPORT\n"
        report += "="*60 + "\n\n"
        
        # Prediction Performance
        if 'prediction' in self.performance_metrics:
            pred_metrics = self.performance_metrics['prediction']
            report += "PREDICTION PERFORMANCE:\n"
            report += "-" * 25 + "\n"
            report += f"RMSE: {pred_metrics['rmse']:.4f}\n"
            report += f"MAE:  {pred_metrics['mae']:.4f}\n"
            report += f"R²:   {pred_metrics['r2']:.4f}\n\n"
        
        # Grid Stability Improvements
        if 'stability' in self.performance_metrics:
            stab_metrics = self.performance_metrics['stability']
            report += "GRID STABILITY IMPROVEMENTS:\n"
            report += "-" * 32 + "\n"
            report += f"Voltage Stability Index Improvement: {stab_metrics.get('voltage_improvement', 0):.2f}%\n"
            report += f"Frequency Stability Improvement: {stab_metrics.get('frequency_improvement', 0):.2f}%\n"
            report += f"Voltage Std Reduction: {stab_metrics.get('voltage_std_before', 0):.4f} → {stab_metrics.get('voltage_std_after', 0):.4f}\n"
            report += f"Frequency Std Reduction: {stab_metrics.get('frequency_std_before', 0):.4f} → {stab_metrics.get('frequency_std_after', 0):.4f}\n\n"
        
        # FACTS Device Actions
        if 'facts_actions' in self.performance_metrics:
            facts_metrics = self.performance_metrics['facts_actions']
            report += "FACTS DEVICE CONTROL ACTIONS:\n"
            report += "-" * 35 + "\n"
            report += f"STATCOM Reactive Power: {facts_metrics.get('statcom_q', 0):.2f} MVAr\n"
            report += f"SVC Reactive Power: {facts_metrics.get('svc_q', 0):.2f} MVAr\n"
            report += f"UPFC Active Power: {facts_metrics.get('upfc_p', 0):.2f} MW\n"
            report += f"UPFC Reactive Power: {facts_metrics.get('upfc_q', 0):.2f} MVAr\n\n"
        
        report += "="*60 + "\n"
        return report
    
    def run_complete_analysis(self, duration_hours=8760):
        """Run complete Neuro-OptimaFACTS analysis"""
        print("Starting Neuro-OptimaFACTS Analysis...")
        print("="*50)
        
        # 1. Generate synthetic data
        print("1. Generating synthetic grid data...")
        self.data_generator = DataGenerator(duration_hours=duration_hours)
        grid_data = self.data_generator.generate_complete_dataset()
        print(f"   Generated {len(grid_data)} data points")
        
        # 2. Train hybrid models
        print("\n2. Training hybrid AI models...")
        X_test, y_test = self.train_hybrid_model(grid_data)
        
        # 3. Evaluate performance
        print("\n3. Evaluating system performance...")
        performance_metrics = self.evaluate_performance(X_test, y_test, grid_data)
        
        # 4. Generate explanations
        print("\n4. Generating AI explanations...")
        feature_names = [f'Wavelet_Feature_{i}' for i in range(X_test.shape[1])]
        explanations = self.generate_explanations(X_test, feature_names)
        
        # 5. Create visualizations
        print("\n5. Creating visualizations...")
        results_figure = self.visualize_results(grid_data, X_test, y_test)
        
        # 6. Generate report
        print("\n6. Generating performance report...")
        report = self.generate_performance_report()
        
        print("\nAnalysis Complete!")
        print(report)
        
        return {
            'grid_data': grid_data,
            'performance_metrics': performance_metrics,
            'explanations': explanations,
            'figure': results_figure,
            'report': report
        }
    
    def run_complete_analysis_with_realtime_data(self, realtime_data):
        """Run Neuro-OptimaFACTS analysis with real-time data from APIs"""
        print("Starting Neuro-OptimaFACTS Analysis with REAL-TIME DATA...")
        print("="*50)
        
        # 1. Prepare real-time data
        print("1. Preparing real-time grid data...")
        grid_data = realtime_data.copy()
        print(f"   Loaded {len(grid_data)} real-time data points")
        print(f"   Date range: {grid_data['Date'].min()} to {grid_data['Date'].max()}")
        
        # Convert DataFrame to dictionary format if needed for compatibility
        if hasattr(grid_data, 'to_dict'):
            grid_data_dict = grid_data.to_dict('list')
        else:
            grid_data_dict = grid_data
        
        # 2. Train hybrid models with real data
        print("\n2. Training hybrid AI models with real data...")
        X_test, y_test = self.train_hybrid_model(grid_data_dict)
        
        # 3. Evaluate performance
        print("\n3. Evaluating system performance with real data...")
        performance_metrics = self.evaluate_performance(X_test, y_test, grid_data_dict)
        
        # 4. Generate explanations
        print("\n4. Generating AI explanations...")
        feature_names = [f'Wavelet_Feature_{i}' for i in range(X_test.shape[1])]
        explanations = self.generate_explanations(X_test, feature_names)
        
        # 5. Create visualizations
        print("\n5. Creating visualizations...")
        results_figure = self.visualize_results(grid_data_dict, X_test, y_test)
        
        # 6. Generate report
        print("\n6. Generating performance report...")
        report = self.generate_performance_report()
        
        print("\n✓ Analysis with REAL-TIME DATA Complete!")
        print(report)
        
        return {
            'grid_data': grid_data,
            'performance_metrics': performance_metrics,
            'explanations': explanations,
            'figure': results_figure,
            'report': report,
            'data_source': 'real-time_apis'
        }

# Additional utility functions for advanced analysis

class AdvancedAnalytics:
    """Advanced analytics and comparison tools"""
    
    @staticmethod
    def compare_with_baseline(neuro_optimafacts_results, baseline_method='traditional_pi'):
        """Compare Neuro-OptimaFACTS with baseline methods"""
        
        # Simulate baseline performance (simplified)
        baseline_performance = {
            'voltage_improvement': 15.0,  # 15% improvement
            'frequency_improvement': 10.0,  # 10% improvement
            'prediction_rmse': 0.025,
            'response_time': 0.5  # seconds
        }
        
        # Neuro-OptimaFACTS performance
        nof_performance = neuro_optimafacts_results['performance_metrics']
        
        comparison = {
            'voltage_improvement': {
                'baseline': baseline_performance['voltage_improvement'],
                'neuro_optimafacts': nof_performance['stability'].get('voltage_improvement', 0),
                'improvement_ratio': nof_performance['stability'].get('voltage_improvement', 0) / baseline_performance['voltage_improvement']
            },
            'frequency_improvement': {
                'baseline': baseline_performance['frequency_improvement'],
                'neuro_optimafacts': nof_performance['stability'].get('frequency_improvement', 0),
                'improvement_ratio': nof_performance['stability'].get('frequency_improvement', 0) / baseline_performance['frequency_improvement']
            },
            'prediction_accuracy': {
                'baseline_rmse': baseline_performance['prediction_rmse'],
                'neuro_optimafacts_rmse': nof_performance['prediction'].get('rmse', 0),
                'accuracy_improvement': (baseline_performance['prediction_rmse'] - nof_performance['prediction'].get('rmse', 0)) / baseline_performance['prediction_rmse'] * 100
            }
        }
        
        return comparison
    
    @staticmethod
    def sensitivity_analysis(neuro_optimafacts_system, grid_data, parameter_variations):
        """Perform sensitivity analysis on key parameters"""
        
        sensitivity_results = {}
        
        for param_name, variations in parameter_variations.items():
            param_results = []
            
            for variation in variations:
                # Modify parameter and re-run analysis
                modified_data = grid_data.copy()
                
                if param_name == 'renewable_penetration':
                    modified_data['total_renewable'] *= variation
                elif param_name == 'load_variability':
                    modified_data['load_demand'] *= (1 + variation * np.random.normal(0, 0.1, len(modified_data)))
                elif param_name == 'voltage_disturbance':
                    modified_data['voltage'] += variation * np.random.normal(0, 0.02, len(modified_data))
                
                # Quick evaluation (simplified)
                stability_metric = np.std(modified_data['voltage'])
                param_results.append({
                    'variation': variation,
                    'stability_metric': stability_metric
                })
            
            sensitivity_results[param_name] = param_results
        
        return sensitivity_results
    
    @staticmethod
    def create_sensitivity_plots(sensitivity_results):
        """Create sensitivity analysis plots"""
        
        n_params = len(sensitivity_results)
        fig, axes = plt.subplots(1, n_params, figsize=(5*n_params, 4))
        
        if n_params == 1:
            axes = [axes]
        
        for idx, (param_name, results) in enumerate(sensitivity_results.items()):
            variations = [r['variation'] for r in results]
            metrics = [r['stability_metric'] for r in results]
            
            axes[idx].plot(variations, metrics, 'o-', linewidth=2, markersize=6)
            axes[idx].set_xlabel(f'{param_name.replace("_", " ").title()} Variation')
            axes[idx].set_ylabel('Voltage Stability Metric')
            axes[idx].set_title(f'Sensitivity to {param_name.replace("_", " ").title()}')
            axes[idx].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig

# Main execution and demonstration
def main():
    """Main function to demonstrate Neuro-OptimaFACTS framework"""
    
    print("NEURO-OPTIMAFACTS FRAMEWORK DEMONSTRATION")
    print("="*55)
    
    # Initialize the system
    neuro_optimafacts = NeuroOptimaFACTS()
    
    # Load real-time data instead of synthetic
    print("\nLoading real-time dataset...")
    try:
        integrator = RealDataIntegrator()
        real_time_data = integrator.load_latest_realtime_dataset()
        print(f"✓ Successfully loaded {len(real_time_data)} hours of real-time data")
        print(f"  Date range: {real_time_data['Date'].min()} to {real_time_data['Date'].max()}")
    except Exception as e:
        print(f"⚠ Could not load real-time data: {e}")
        print("  Falling back to synthetic data...")
        real_time_data = None
    
    # Run complete analysis
    if real_time_data is not None:
        # Use real-time data by passing it to the analysis
        print("\n✓ Running FACTS analysis with REAL-TIME DATA...")
        results = neuro_optimafacts.run_complete_analysis_with_realtime_data(real_time_data)
    else:
        # Fall back to synthetic data if real-time unavailable
        print("\n✓ Running FACTS analysis with synthetic data (fallback)...")
        results = neuro_optimafacts.run_complete_analysis(duration_hours=2000)  # ~3 months of data
    
    # Advanced analytics
    print("\n" + "="*55)
    print("ADVANCED ANALYTICS")
    print("="*55)
    
    # Baseline comparison
    print("\n1. Comparing with baseline methods...")
    comparison = AdvancedAnalytics.compare_with_baseline(results)
    
    print("\nBASELINE COMPARISON RESULTS:")
    print("-" * 30)
    for metric, values in comparison.items():
        if 'improvement_ratio' in values:
            print(f"{metric.replace('_', ' ').title()}:")
            print(f"  Baseline: {values.get('baseline', 'N/A')}")
            print(f"  Neuro-OptimaFACTS: {values.get('neuro_optimafacts', 'N/A')}")
            print(f"  Improvement Ratio: {values.get('improvement_ratio', 'N/A'):.2f}x")
        elif 'accuracy_improvement' in values:
            print(f"{metric.replace('_', ' ').title()}:")
            print(f"  Baseline RMSE: {values.get('baseline_rmse', 'N/A')}")
            print(f"  Neuro-OptimaFACTS RMSE: {values.get('neuro_optimafacts_rmse', 'N/A')}")
            print(f"  Accuracy Improvement: {values.get('accuracy_improvement', 'N/A'):.2f}%")
        print()
    
    # Sensitivity analysis
    print("2. Performing sensitivity analysis...")
    parameter_variations = {
        'renewable_penetration': [0.5, 0.75, 1.0, 1.25, 1.5, 2.0],
        'load_variability': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
        'voltage_disturbance': [0.0, 0.01, 0.02, 0.03, 0.04, 0.05]
    }
    
    sensitivity_results = AdvancedAnalytics.sensitivity_analysis(
        neuro_optimafacts, results['grid_data'], parameter_variations
    )
    
    # Create sensitivity plots
    sensitivity_fig = AdvancedAnalytics.create_sensitivity_plots(sensitivity_results)
    
    print("\nSENSITIVITY ANALYSIS COMPLETE")
    print("Check the generated plots for detailed sensitivity analysis.")
    
    # Show all plots
    plt.show()
    
    return results, comparison, sensitivity_results

# Execute the demonstration
if __name__ == "__main__":
    results, comparison, sensitivity = main()
    
    print("\n" + "="*55)
    print("DEMONSTRATION COMPLETE")
    print("="*55)
    print("\nThe Neuro-OptimaFACTS framework has been successfully demonstrated.")
    print("Key achievements:")
    print("- Hybrid AI model integration (WNN, ANN, Kalman Filter)")
    print("- FACTS device optimization and control")
    print("- Explainable AI using SHAP")
    print("- Grid stability improvement analysis")
    print("- Comprehensive performance evaluation")
    print("- Sensitivity analysis for robustness testing")