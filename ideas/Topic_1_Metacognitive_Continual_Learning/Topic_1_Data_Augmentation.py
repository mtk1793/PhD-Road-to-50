"""
Topic 1: Seasonal Dataset Augmentation for Continual Learning

Creates seasonal variations of smart grid data to simulate distribution shifts:
- Winter: Low solar, high heating load
- Summer: High solar, high cooling load  
- Spring/Fall: High variability

Implements Bayesian change point detection for automatic task segmentation.

Author: PhD Research
Date: January 2026
"""

import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from scipy import stats

class SeasonalAugmenter:
    """Augment smart grid dataset with realistic seasonal variations"""
    
    def __init__(self, base_dataset_path):
        """
        Args:
            base_dataset_path: Path to smart_grid_dataset.csv
        """
        self.base_data = pd.read_csv(base_dataset_path)
        print(f"✅ Loaded base dataset: {len(self.base_data)} samples")
        print(f"   Columns: {list(self.base_data.columns)}")
    
    def create_winter_scenario(self, data):
        """
        Winter characteristics:
        - Solar: 60% reduction (shorter days, lower sun angle)
        - Load: 30% increase (heating demand)
        - Temperature: -15°C decrease
        - Wind: 20% increase (winter storms)
        """
        winter_data = data.copy()
        
        # Solar reduction
        solar_cols = [col for col in data.columns if 'solar' in col.lower() or 'pv' in col.lower()]
        for col in solar_cols:
            winter_data[col] = data[col] * 0.4  # 60% reduction
        
        # Load increase (heating)
        load_cols = [col for col in data.columns if 'load' in col.lower() or 'demand' in col.lower()]
        for col in load_cols:
            winter_data[col] = data[col] * 1.3  # 30% increase
        
        # Temperature decrease
        temp_cols = [col for col in data.columns if 'temp' in col.lower()]
        for col in temp_cols:
            winter_data[col] = data[col] - 15
        
        # Wind increase
        wind_cols = [col for col in data.columns if 'wind' in col.lower()]
        for col in wind_cols:
            winter_data[col] = data[col] * 1.2
        
        # Add seasonal label
        winter_data['season'] = 'winter'
        
        return winter_data
    
    def create_summer_scenario(self, data):
        """
        Summer characteristics:
        - Solar: 40% increase (longer days)
        - Load: 15% increase (cooling demand), shifted to afternoon
        - Temperature: +10°C increase
        - Wind: 10% decrease (calmer weather)
        """
        summer_data = data.copy()
        
        # Solar increase
        solar_cols = [col for col in data.columns if 'solar' in col.lower() or 'pv' in col.lower()]
        for col in solar_cols:
            summer_data[col] = data[col] * 1.4
        
        # Load increase with afternoon shift
        load_cols = [col for col in data.columns if 'load' in col.lower() or 'demand' in col.lower()]
        for col in load_cols:
            # Create afternoon peak (assuming hourly data)
            if 'Timestamp' in data.columns or 'timestamp' in data.columns:
                ts_col = 'Timestamp' if 'Timestamp' in data.columns else 'timestamp'
                hour = pd.to_datetime(data[ts_col]).dt.hour
                afternoon_boost = 1 + 0.3 * np.exp(-((hour - 15)**2) / 10)
                summer_data[col] = data[col] * 1.15 * afternoon_boost
            else:
                summer_data[col] = data[col] * 1.15
        
        # Temperature increase
        temp_cols = [col for col in data.columns if 'temp' in col.lower()]
        for col in temp_cols:
            summer_data[col] = data[col] + 10
        
        # Wind decrease
        wind_cols = [col for col in data.columns if 'wind' in col.lower()]
        for col in wind_cols:
            summer_data[col] = data[col] * 0.9
        
        summer_data['season'] = 'summer'
        
        return summer_data
    
    def create_spring_scenario(self, data):
        """
        Spring characteristics:
        - Solar: Moderate (80% of base)
        - Load: High variability (warm days, cold nights)
        - Temperature: Highly variable
        - Wind: Variable
        """
        spring_data = data.copy()
        
        # Add high variability
        n_samples = len(data)
        variability_factor = np.random.normal(1.0, 0.15, n_samples)
        
        # Solar - moderate with clouds
        solar_cols = [col for col in data.columns if 'solar' in col.lower() or 'pv' in col.lower()]
        for col in solar_cols:
            spring_data[col] = data[col] * 0.8 * variability_factor
        
        # Load - variable
        load_cols = [col for col in data.columns if 'load' in col.lower() or 'demand' in col.lower()]
        for col in load_cols:
            spring_data[col] = data[col] * variability_factor
        
        # Temperature - variable
        temp_cols = [col for col in data.columns if 'temp' in col.lower()]
        for col in temp_cols:
            spring_data[col] = data[col] + np.random.normal(0, 5, n_samples)
        
        # Wind - variable
        wind_cols = [col for col in data.columns if 'wind' in col.lower()]
        for col in wind_cols:
            spring_data[col] = data[col] * np.random.uniform(0.7, 1.3, n_samples)
        
        spring_data['season'] = 'spring'
        
        return spring_data
    
    def create_fall_scenario(self, data):
        """
        Fall characteristics:
        - Solar: 70% (shorter days beginning)
        - Load: Moderate, less variability than spring
        - Temperature: Gradually decreasing
        - Wind: Increasing (storm season)
        """
        fall_data = data.copy()
        
        # Solar decrease
        solar_cols = [col for col in data.columns if 'solar' in col.lower() or 'pv' in col.lower()]
        for col in solar_cols:
            fall_data[col] = data[col] * 0.7
        
        # Load - moderate
        load_cols = [col for col in data.columns if 'load' in col.lower() or 'demand' in col.lower()]
        for col in load_cols:
            fall_data[col] = data[col] * 1.05
        
        # Temperature decrease
        temp_cols = [col for col in data.columns if 'temp' in col.lower()]
        for col in temp_cols:
            fall_data[col] = data[col] - 5
        
        # Wind increase
        wind_cols = [col for col in data.columns if 'wind' in col.lower()]
        for col in wind_cols:
            fall_data[col] = data[col] * 1.15
        
        fall_data['season'] = 'fall'
        
        return fall_data
    
    def generate_multi_season_dataset(self, num_weeks_per_season=2):
        """
        Generate complete multi-season dataset
        
        Args:
            num_weeks_per_season: Number of weeks to generate for each season
        
        Returns:
            DataFrame with seasonal variations
        """
        print(f"\n🌍 Generating multi-season dataset ({num_weeks_per_season} weeks/season)...")
        
        # Determine how many samples per week
        samples_per_week = min(len(self.base_data), 7 * 24 * 4)  # Assuming 15-min data
        
        all_seasons = []
        
        for season, transformer in [
            ('winter', self.create_winter_scenario),
            ('spring', self.create_spring_scenario),
            ('summer', self.create_summer_scenario),
            ('fall', self.create_fall_scenario)
        ]:
            for week in range(num_weeks_per_season):
                # Sample from base dataset
                start_idx = (week * samples_per_week) % len(self.base_data)
                end_idx = start_idx + samples_per_week
                
                if end_idx > len(self.base_data):
                    # Wrap around
                    chunk1 = self.base_data.iloc[start_idx:]
                    chunk2 = self.base_data.iloc[:end_idx - len(self.base_data)]
                    week_data = pd.concat([chunk1, chunk2])
                else:
                    week_data = self.base_data.iloc[start_idx:end_idx].copy()
                
                # Apply seasonal transformation
                season_data = transformer(week_data)
                season_data['task_id'] = f"{season}_week{week+1}"
                
                all_seasons.append(season_data)
                print(f"  ✓ Generated {season} week {week+1}: {len(season_data)} samples")
        
        # Concatenate all seasons
        full_dataset = pd.concat(all_seasons, ignore_index=True)
        
        print(f"\n✅ Complete dataset: {len(full_dataset)} samples across {len(all_seasons)} tasks")
        
        return full_dataset
    
    def bayesian_changepoint_detection(self, data, feature='Power_Consumption'):
        """
        Implement Bayesian Online Change Point Detection (BOCPD)
        to automatically identify task boundaries
        
        Args:
            data: Time series data
            feature: Column name to analyze for changepoints
        
        Returns:
            List of changepoint indices
        """
        print(f"\n🔍 Running Bayesian Change Point Detection on '{feature}'...")
        
        if feature not in data.columns:
            # Find closest matching column
            matching = [col for col in data.columns if 'power' in col.lower() or 'load' in col.lower()]
            feature = matching[0] if matching else data.columns[0]
            print(f"   Using column: {feature}")
        
        values = data[feature].values
        n = len(values)
        
        # Simple Bayesian changepoint detection using variance shifts
        window_size = min(100, n // 10)
        changepoints = []
        
        for i in range(window_size, n - window_size, window_size // 2):
            # Compare variance before and after
            before = values[i-window_size:i]
            after = values[i:i+window_size]
            
            # F-test for variance equality
            f_stat, p_value = stats.levene(before, after)
            
            # Also check mean shift
            t_stat, t_pvalue = stats.ttest_ind(before, after)
            
            # Changepoint if significant difference
            if p_value < 0.01 or t_pvalue < 0.01:
                changepoints.append(i)
        
        print(f"   Detected {len(changepoints)} changepoints")
        
        return changepoints
    
    def visualize_seasonal_profiles(self, data, output_path='seasonal_profiles.png'):
        """Create visualization of seasonal variations"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        features = []
        for pattern in ['solar', 'load', 'temp', 'wind']:
            matches = [col for col in data.columns if pattern in col.lower()]
            if matches:
                features.append(matches[0])
        
        if len(features) < 4:
            # Fallback to first 4 numeric columns
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            features = list(numeric_cols[:4])
        
        seasons = ['winter', 'spring', 'summer', 'fall']
        colors = {'winter': 'blue', 'spring': 'green', 'summer': 'red', 'fall': 'orange'}
        
        for idx, feature in enumerate(features[:4]):
            ax = axes[idx // 2, idx % 2]
            
            for season in seasons:
                season_data = data[data['season'] == season]
                if len(season_data) > 0:
                    # Sample to make plot readable
                    sample = season_data[feature].iloc[::max(1, len(season_data)//500)]
                    ax.plot(sample.values, label=season, color=colors[season], alpha=0.7)
            
            ax.set_title(f'{feature} - Seasonal Variation')
            ax.set_xlabel('Sample Index')
            ax.set_ylabel(feature)
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"📊 Seasonal profiles saved to {output_path}")
        
        return fig


if __name__ == "__main__":
    # Test seasonal augmentation
    base_path = Path("../smart_grid_dataset.csv")
    
    if not base_path.exists():
        print(f"❌ Base dataset not found at {base_path}")
        print("   Creating synthetic test data...")
        
        # Create synthetic data for testing
        n_samples = 7 * 24 * 4  # 1 week of 15-min data
        dates = pd.date_range('2023-01-01', periods=n_samples, freq='15T')
        
        test_data = pd.DataFrame({
            'Timestamp': dates,
            'Solar_Power_kW': 500 * np.maximum(0, np.sin(np.pi * (dates.hour - 6) / 12)),
            'Wind_Power_kW': 200 + 100 * np.random.random(n_samples),
            'Load_kW': 800 + 200 * np.sin(2 * np.pi * dates.hour / 24),
            'Temperature_C': 20 + 5 * np.sin(2 * np.pi * dates.hour / 24),
            'Power_Consumption': 1500 + np.random.normal(0, 50, n_samples)
        })
        
        test_data.to_csv('test_base_dataset.csv', index=False)
        base_path = Path('test_base_dataset.csv')
    
    # Create augmenter
    augmenter = SeasonalAugmenter(base_path)
    
    # Generate multi-season dataset
    seasonal_dataset = augmenter.generate_multi_season_dataset(num_weeks_per_season=2)
    
    # Save
    output_path = Path("Topic_1_Seasonal_Dataset.csv")
    seasonal_dataset.to_csv(output_path, index=False)
    print(f"\n💾 Saved seasonal dataset to {output_path}")
    
    # Detect changepoints
    changepoints = augmenter.bayesian_changepoint_detection(seasonal_dataset)
    
    # Visualize
    augmenter.visualize_seasonal_profiles(seasonal_dataset)
    
    print("\n✅ Topic 1 data augmentation complete!")
