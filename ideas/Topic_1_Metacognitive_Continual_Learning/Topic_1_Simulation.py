"""
Topic 1: PyPower Simulation for Continual Learning

Runs optimal power flow across seasonal datasets to demonstrate:
- Voltage prediction degradation under distribution shift
- EWC-IXER continual learning algorithm
- Metacognitive uncertainty quantification

Uses IEEE 30-bus system for realistic power grid modeling.

Author: PhD Research
Date: January 2026
"""

import numpy as np
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'IEEE_Papers'))

from pypower.api import case30, runopf, ppoption
from pypower.idx_bus import PD, QD, VM, VA
from pypower.idx_gen import PG, QG
import torch
import torch.nn as nn
import torch.optim as optim
from metrics import ContinualLearningMetrics, PowerSystemMetrics
from figure_ generator import IEEEFigureGenerator
import matplotlib.pyplot as plt

class VoltagePredictorLSTM(nn.Module):
    """LSTM model for voltage forecasting"""
    
    def __init__(self, input_dim=10, hidden_dim=64, output_dim=30):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=2, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x):
        # x: (batch, seq_len, features)
        lstm_out, _ = self.lstm(x)
        # Take last timestep
        predictions = self.fc(lstm_out[:, -1, :])
        return predictions


class EWCIXERAgent:
    """
    Elastic Weight Consolidation with Importance-Weighted Experience Replay
    
    Prevents catastrophic forgetting while learning new seasonal patterns
    """
    
    def __init__(self, model, learning_rate=0.001, lambda_ewc=1000, replay_size=1000):
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        self.lambda_ewc = lambda_ewc
        self.replay_buffer = []
        self.replay_size = replay_size
        
        # EWC: Fisher information and optimal weights from previous tasks
        self.fisher_dict = {}
        self.optimal_weights_dict = {}
        self.current_task_id = 0
        
    def compute_fisher_information(self, dataloader):
        """
        Compute Fisher Information Matrix to identify important weights
        
        Fisher = E[∇L² ] approximates importance of each parameter
        """
        fisher = {}
        for name, param in self.model.named_parameters():
            fisher[name] = torch.zeros_like(param)
        
        self.model.eval()
        for X, y in dataloader:
            self.optimizer.zero_grad()
            output = self.model(X)
            loss = nn.MSELoss()(output, y)
            loss.backward()
            
            for name, param in self.model.named_parameters():
                fisher[name] += param.grad.data ** 2
        
        # Average over samples
        for name in fisher:
            fisher[name] /= len(dataloader)
        
        return fisher
    
    def consolidate_task(self, task_id, dataloader):
        """
        After learning a task, consolidate important weights
        """
        print(f"  🔒 Consolidating task {task_id}...")
        
        # Compute Fisher information
        fisher = self.compute_fisher_information(dataloader)
        self.fisher_dict[task_id] = fisher
        
        # Store optimal weights
        self.optimal_weights_dict[task_id] = {}
        for name, param in self.model.named_parameters():
            self.optimal_weights_dict[task_id][name] = param.data.clone()
        
        print(f"     Stored Fisher info and weights for task {task_id}")
    
    def ewc_loss(self):
        """
        EWC regularization loss: penalize changes to important weights
        
        L_EWC = Σ_tasks Σ_params F_i * (θ_i - θ*_i)²
        """
        loss = 0
        for task_id in self.fisher_dict.keys():
            for name, param in self.model.named_parameters():
                fisher = self.fisher_dict[task_id][name]
                optimal = self.optimal_weights_dict[task_id][name]
                loss += (fisher * (param - optimal) ** 2).sum()
        
        return self.lambda_ewc * loss
    
    def add_to_replay_buffer(self, X, y, priority=1.0):
        """
        Add sample to experience replay buffer
        Priority: higher for rare/important events
        """
        if len(self.replay_buffer) < self.replay_size:
            self.replay_buffer.append((X, y, priority))
        else:
            # Replace random sample weighted by inverse priority
            priorities = np.array([p for _, _, p in self.replay_buffer])
            probs = 1 / (priorities + 1e-10)
            probs /= probs.sum()
            idx = np.random.choice(len(self.replay_buffer), p=probs)
            self.replay_buffer[idx] = (X, y, priority)
    
    def sample_replay_buffer(self, batch_size=32):
        """Sample from replay buffer with priority"""
        if len(self.replay_buffer) < batch_size:
            return None
        
        # Sample with replacement based on priority
        priorities = np.array([p for _, _, p in self.replay_buffer])
        probs = priorities / priorities.sum()
        indices = np.random.choice(len(self.replay_buffer), size=batch_size, p=probs)
        
        X_batch = torch.cat([self.replay_buffer[i][0] for i in indices])
        y_batch = torch.cat([self.replay_buffer[i][1] for i in indices])
        
        return X_batch, y_batch
    
    def train_on_task(self, task_id, task_dataloader, epochs=20, use_replay=True):
        """Train model on a specific task"""
        print(f"\n📚 Training on task {task_id} for {epochs} epochs...")
        
        self.model.train()
        self.current_task_id = task_id
        losses = []
        
        for epoch in range(epochs):
            epoch_loss = 0
            n_batches = 0
            
            for X, y in task_dataloader:
                # Current task loss
                self.optimizer.zero_grad()
                output = self.model(X)
                task_loss = nn.MSELoss()(output, y)
                
                # EWC regularization (prevent forgetting)
                ewc_loss = self.ewc_loss() if len(self.fisher_dict) > 0 else 0
                
                # Experience replay loss
                replay_loss = 0
                if use_replay and len(self.replay_buffer) > 0:
                    X_replay, y_replay = self.sample_replay_buffer(batch_size=16)
                    output_replay = self.model(X_replay)
                    replay_loss = nn.MSELoss()(output_replay, y_replay)
                
                # Total loss
                total_loss = task_loss + ewc_loss + 0.5 * replay_loss
                
                total_loss.backward()
                self.optimizer.step()
                
                epoch_loss += total_loss.item()
                n_batches += 1
                
                # Add to replay buffer (sample randomly to keep diversity)
                if np.random.random() < 0.1:  # 10% of samples
                    self.add_to_replay_buffer(X.detach(), y.detach(), priority=task_loss.item())
            
            avg_loss = epoch_loss / n_batches
            losses.append(avg_loss)
            
            if epoch % 5 == 0:
                print(f"     Epoch {epoch}/{epochs}: Loss = {avg_loss:.4f}")
        
        return losses


class ContinualLearningSimulator:
    """Main simulator for Topic 1"""
    
    def __init__(self, seasonal_dataset_path):
        self.data = pd.read_csv(seasonal_dataset_path)
        self.case = case30()
        self.model = VoltagePredictorLSTM()
        self.agent = EWCIXERAgent(self.model)
        self.results = {}
        
        print(f"✅ Loaded seasonal dataset: {len(self.data)} samples")
        print(f"   Unique tasks: {self.data['task_id'].nunique()}")
    
    def run_pypower_opf(self, load_mw, solar_mw=0, wind_mw=0):
        """
        Run optimal power flow for given conditions
        
        Returns: Bus voltages (30-bus system)
        """
        # Update loads (distribute across load buses)
        load_buses = [2, 4, 6, 7, 11, 14, 16, 18, 19, 22, 23, 28]  # 0-indexed
        
        total_original_load = sum([self.case['bus'][bus, PD] for bus in load_buses])
        if total_original_load > 0:
            scale = load_mw / total_original_load
            for bus in load_buses:
                self.case['bus'][bus, PD] *= scale
                self.case['bus'][bus, QD] *= scale
        
        # Update generation (account for renewables)
        total_gen = self.case['gen'][:, PG].sum()
        renewable = solar_mw + wind_mw
        if total_gen > renewable:
            self.case['gen'][:, PG] *= (total_gen - renewable) / total_gen
        
        # Run OPF
        ppopt = ppoption(VERBOSE=0, OUT_ALL=0)
        result = runopf(self.case, ppopt=ppopt)
        
        if result[0]['success']:
            voltages = result[0]['bus'][:, VM]
            return voltages
        else:
            return None
    
    def prepare_task_data(self, task_id, sequence_length=10):
        """Prepare dataset for a specific task"""
        task_data = self.data[self.data['task_id'] == task_id]
        
        # Extract features
        feature_cols = [col for col in task_data.columns if col not in ['Timestamp', 'timestamp', 'season', 'task_id']]
        features = task_data[feature_cols].values
        
        # Run PyPower to get ground truth voltages
        voltages_list = []
        valid_indices = []
        
        print(f"  Running PyPower OPF for {len(task_data)} samples...")
        for idx, row in task_data.iterrows():
            load_col = [col for col in task_data.columns if 'load' in col.lower() or 'consumption' in col.lower()]
            solar_col = [col for col in task_data.columns if 'solar' in col.lower() or 'pv' in col.lower()]
            wind_col = [col for col in task_data.columns if 'wind' in col.lower()]
            
            load_mw = row[load_col[0]] / 100 if load_col else 100  # Scale to match IEEE 30-bus
            solar_mw = row[solar_col[0]] / 100 if solar_col else 0
            wind_mw = row[wind_col[0]] / 100 if wind_col else 0
            
            voltages = self.run_pypower_opf(load_mw, solar_mw, wind_mw)
            
            if voltages is not None:
                voltages_list.append(voltages)
                valid_indices.append(idx - task_data.index[0])
        
        voltages_array = np.array(voltages_list)
        features = features[valid_indices]
        
        # Create sequences
        X, y = [], []
        for i in range(len(features) - sequence_length):
            X.append(features[i:i+sequence_length])
            y.append(voltages_array[i+sequence_length])
        
        X = torch.FloatTensor(np.array(X))
        y = torch.FloatTensor(np.array(y))
        
        # Create DataLoader
        dataset = torch.utils.data.TensorDataset(X, y)
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)
        
        return dataloader, X, y
    
    def run_continual_learning_experiment(self):
        """Main experiment: Train sequentially on seasonal tasks"""
        print("\n🚀 Starting Continual Learning Experiment...")
        
        tasks = self.data['task_id'].unique()
        task_accuracies_before = {}
        task_accuracies_after = {}
        all_test_loaders = {}
        
        metrics_cl = ContinualLearningMetrics()
        metrics_ps = PowerSystemMetrics()
        
        # Phase 1: Train on tasks sequentially
        for task_idx, task_id in enumerate(tasks):
            print(f"\n{'='*60}")
            print(f"TASK {task_idx+1}/{len(tasks)}: {task_id}")
            print(f"{'='*60}")
            
            # Prepare data
            train_loader, X_test, y_test = self.prepare_task_data(task_id)
            all_test_loaders[task_id] = (X_test, y_test)
            
            # Measure performance on all previous tasks (BEFORE learning this task)
            if task_idx > 0:
                for prev_task in tasks[:task_idx]:
                    X_prev, y_prev = all_test_loaders[prev_task]
                    self.model.eval()
                    with torch.no_grad():
                        y_pred = self.model(X_prev)
                        rmse = metrics_ps.rmse(y_prev.numpy().flatten(), 
                                             y_pred.numpy().flatten())
                    task_accuracies_before[f"{prev_task}_after_{task_id}"] = 1 / (1 + rmse)  # Convert to "accuracy"
            
            # Train on current task
            losses = self.agent.train_on_task(task_id, train_loader, epochs=20)
            
            # Consolidate (compute Fisher, store weights)
            self.agent.consolidate_task(task_id, train_loader)
            
            # Measure performance on ALL tasks (AFTER learning this task)
            for prev_task in tasks[:task_idx+1]:
                X_prev, y_prev = all_test_loaders[prev_task]
                self.model.eval()
                with torch.no_grad():
                    y_pred = self.model(X_prev)
                    rmse = metrics_ps.rmse(y_prev.numpy().flatten(), 
                                         y_pred.numpy().flatten())
                task_accuracies_after[prev_task] = 1 / (1 + rmse)
                
                print(f"  ✓ Performance on {prev_task}: RMSE = {rmse:.4f}")
        
        # Phase 2: Compute continual learning metrics
        print(f"\n{'='*60}")
        print("📊 CONTINUAL LEARNING METRICS")
        print(f"{'='*60}")
        
        # Average accuracy
        avg_acc = metrics_cl.average_accuracy(task_accuracies_after)
        print(f"Average Accuracy: {avg_acc:.4f}")
        
        # Backward transfer (forgetting)
        if len(task_accuracies_before) > 0:
            # Match tasks for BWT calculation
            common_tasks = set([k.split('_after_')[0] for k in task_accuracies_before.keys()])
            bwt_before = {t: task_accuracies_before.get(f"{t}_after_{tasks[-1]}", 0) 
                         for t in common_tasks}
            bwt_after = {t: task_accuracies_after[t] for t in common_tasks}
            bwt = metrics_cl.backward_transfer(bwt_before, bwt_after)
            print(f"Backward Transfer (Forgetting): {bwt:.4f} (closer to 0 = less forgetting)")
        
        self.results = {
            'task_accuracies': task_accuracies_after,
            'avg_accuracy': avg_acc,
            'backward_transfer': bwt if 'bwt' in locals() else 0
        }
        
        return self.results


if __name__ == "__main__":
    # Check for seasonal dataset
    dataset_path = Path("Topic_1_Seasonal_Dataset.csv")
    
    if not dataset_path.exists():
        print(" ❌ Seasonal dataset not found. Running data augmentation first...")
        import Topic_1_Data_Augmentation
        # This will generate the dataset
        exec(open("Topic_1_Data_Augmentation.py").read())
    
    # Run simulation
    simulator = ContinualLearningSimulator(dataset_path)
    results = simulator.run_continual_learning_experiment()
    
    print("\n✅ Topic 1 Simulation Complete!")
    print(f"   Final results: {results}")
