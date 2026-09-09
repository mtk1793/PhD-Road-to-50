#!/usr/bin/env python3
"""
Generate Publication-Ready PNG Plots from Real-Time FACTS Simulation Results
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set publication-quality style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

print("\n" + "="*70)
print("GENERATING PUBLICATION-READY PNG PLOTS")
print("="*70)

# Load real-time data
print("\n[1] Loading real-time dataset...")
try:
    data = pd.read_csv('realtime_ieee39_complete_20251113_180635.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    print(f"✓ Loaded {len(data)} records spanning {data['Date'].min().date()} to {data['Date'].max().date()}")
except Exception as e:
    print(f"✗ Failed to load data: {e}")
    exit(1)

# ============================================================================
# FIGURE 1: Wind and Solar Generation Profile (67-day time series)
# ============================================================================
print("\n[2] Generating: Wind and Solar Generation Profile...")
fig, ax = plt.subplots(figsize=(14, 5))

ax.plot(data['Date'], data['Wind_Power_MW'], label='Wind Power', 
        linewidth=1.5, alpha=0.8, color='#1f77b4')
ax.plot(data['Date'], data['Solar_Power_MW'], label='Solar Power', 
        linewidth=1.5, alpha=0.8, color='#ff7f0e')
ax.fill_between(data['Date'], data['Wind_Power_MW'], alpha=0.2, color='#1f77b4')
ax.fill_between(data['Date'], data['Solar_Power_MW'], alpha=0.2, color='#ff7f0e')

ax.set_xlabel('Date', fontweight='bold')
ax.set_ylabel('Power Generation (MW)', fontweight='bold')
ax.set_title('Wind and Solar Generation Profile (67-Day Period)\nIEEE 39-Bus System with Real-Time Data', 
             fontweight='bold', fontsize=13)
ax.legend(loc='upper left', framealpha=0.95)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('01_Wind_Solar_Generation_Profile.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: 01_Wind_Solar_Generation_Profile.png")
plt.close()

# ============================================================================
# FIGURE 2: Load Demand vs Renewable Generation
# ============================================================================
print("[3] Generating: Load Demand vs Renewable Generation...")
fig, ax = plt.subplots(figsize=(14, 5))

ax.plot(data['Date'], data['Load_Demand_MW'], label='Load Demand', 
        linewidth=2, color='#d62728', zorder=3)
ax.plot(data['Date'], data['Total_Renewable_MW'], label='Renewable Generation', 
        linewidth=2, color='#2ca02c', zorder=3)
ax.fill_between(data['Date'], data['Load_Demand_MW'], data['Total_Renewable_MW'],
                where=(data['Load_Demand_MW'] >= data['Total_Renewable_MW']),
                alpha=0.3, color='#d62728', label='Generation Deficit', zorder=1)
ax.fill_between(data['Date'], data['Load_Demand_MW'], data['Total_Renewable_MW'],
                where=(data['Load_Demand_MW'] < data['Total_Renewable_MW']),
                alpha=0.3, color='#2ca02c', label='Generation Surplus', zorder=1)

ax.set_xlabel('Date', fontweight='bold')
ax.set_ylabel('Power (MW)', fontweight='bold')
ax.set_title('Load Demand vs Renewable Generation\nShowing Generation Deficit and Surplus', 
             fontweight='bold', fontsize=13)
ax.legend(loc='upper left', framealpha=0.95)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('02_Load_vs_Renewable.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: 02_Load_vs_Renewable.png")
plt.close()

# ============================================================================
# FIGURE 3: Renewable Penetration Percentage
# ============================================================================
print("[4] Generating: Renewable Penetration Analysis...")
fig, ax = plt.subplots(figsize=(14, 5))

colors = np.where(data['Renewable_Penetration_%'] > 30, '#ff7f0e', '#1f77b4')
ax.bar(data['Date'], data['Renewable_Penetration_%'], width=0.8, 
       color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
ax.axhline(y=15, color='#2ca02c', linestyle='--', linewidth=2, label='Safe Operating Point (15%)', alpha=0.7)
ax.axhline(y=30, color='#ff7f0e', linestyle='--', linewidth=2, label='With FACTS Control (30%)', alpha=0.7)
ax.axhline(y=44.13, color='#d62728', linestyle='--', linewidth=2, label='Maximum Achieved (44.13%)', alpha=0.7)

ax.set_xlabel('Date', fontweight='bold')
ax.set_ylabel('Renewable Penetration (%)', fontweight='bold')
ax.set_title('Renewable Energy Penetration Profile\nShowing Safe Operating Limits with FACTS Control', 
             fontweight='bold', fontsize=13)
ax.legend(loc='upper right', framealpha=0.95)
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(0, 50)
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('03_Renewable_Penetration.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: 03_Renewable_Penetration.png")
plt.close()

# ============================================================================
# FIGURE 4: Voltage and Frequency Profiles
# ============================================================================
print("[5] Generating: Voltage and Frequency Stability...")
fig = plt.figure(figsize=(14, 10))
gs = GridSpec(2, 1, figure=fig, hspace=0.3)

# Voltage subplot
ax1 = fig.add_subplot(gs[0])
ax1.plot(data['Date'], data['Voltage_pu'], linewidth=1.5, color='#1f77b4', label='Actual Voltage')
ax1.axhline(y=1.0, color='green', linestyle='-', linewidth=2, label='Nominal (1.0 p.u.)', alpha=0.7)
ax1.axhline(y=0.95, color='orange', linestyle='--', linewidth=1.5, label='Min Limit (0.95 p.u.)', alpha=0.7)
ax1.axhline(y=1.05, color='orange', linestyle='--', linewidth=1.5, label='Max Limit (1.05 p.u.)', alpha=0.7)
ax1.fill_between(data['Date'], 0.95, 1.05, alpha=0.1, color='green', label='Safe Operating Zone')
ax1.set_ylabel('Voltage (p.u.)', fontweight='bold')
ax1.set_title('Grid Voltage Profile - Stability Analysis', fontweight='bold', fontsize=12)
ax1.legend(loc='upper left', framealpha=0.95)
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0.92, 1.08)
ax1.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Frequency subplot
ax2 = fig.add_subplot(gs[1])
ax2.plot(data['Date'], data['Frequency_Hz'], linewidth=1.5, color='#d62728', label='Actual Frequency')
ax2.axhline(y=60.0, color='green', linestyle='-', linewidth=2, label='Nominal (60.0 Hz)', alpha=0.7)
ax2.axhline(y=59.5, color='orange', linestyle='--', linewidth=1.5, label='Min Limit (59.5 Hz)', alpha=0.7)
ax2.axhline(y=60.5, color='orange', linestyle='--', linewidth=1.5, label='Max Limit (60.5 Hz)', alpha=0.7)
ax2.fill_between(data['Date'], 59.5, 60.5, alpha=0.1, color='green', label='Safe Operating Zone')
ax2.set_xlabel('Date', fontweight='bold')
ax2.set_ylabel('Frequency (Hz)', fontweight='bold')
ax2.set_title('Grid Frequency Profile - Stability Analysis', fontweight='bold', fontsize=12)
ax2.legend(loc='upper left', framealpha=0.95)
ax2.grid(True, alpha=0.3)
ax2.set_ylim(59.65, 60.4)
ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

plt.savefig('04_Voltage_Frequency_Stability.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: 04_Voltage_Frequency_Stability.png")
plt.close()

# ============================================================================
# FIGURE 5: Harmonic Distortion Analysis
# ============================================================================
print("[6] Generating: Harmonic Distortion Analysis...")
fig, ax = plt.subplots(figsize=(14, 5))

ax.plot(data['Date'], data['Harmonics_THD_%'], linewidth=1.5, color='#9467bd', label='Total Harmonic Distortion')
ax.axhline(y=5, color='green', linestyle='-', linewidth=2, label='Target (5% THD)', alpha=0.7)
ax.axhline(y=8, color='orange', linestyle='--', linewidth=1.5, label='Caution (8% THD)', alpha=0.7)
ax.axhline(y=15, color='red', linestyle='--', linewidth=1.5, label='Critical (15% THD)', alpha=0.7)
ax.fill_between(data['Date'], 0, 5, alpha=0.1, color='green')
ax.fill_between(data['Date'], 5, 8, alpha=0.1, color='orange')

ax.set_xlabel('Date', fontweight='bold')
ax.set_ylabel('Total Harmonic Distortion (%)', fontweight='bold')
ax.set_title('Harmonic Content Analysis\nReal-Time Grid Distortion Levels', 
             fontweight='bold', fontsize=13)
ax.legend(loc='upper left', framealpha=0.95)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 12)
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('05_Harmonic_Distortion.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: 05_Harmonic_Distortion.png")
plt.close()

# ============================================================================
# FIGURE 6: Power Factor Analysis
# ============================================================================
print("[7] Generating: Power Factor Analysis...")
fig, ax = plt.subplots(figsize=(14, 5))

ax.plot(data['Date'], data['Power_Factor'], linewidth=1.5, color='#17becf', label='Power Factor')
ax.axhline(y=0.95, color='green', linestyle='-', linewidth=2, label='Target (0.95)', alpha=0.7)
ax.axhline(y=0.90, color='orange', linestyle='--', linewidth=1.5, label='Acceptable (0.90)', alpha=0.7)
ax.fill_between(data['Date'], 0.90, 1.0, alpha=0.1, color='green')
ax.fill_between(data['Date'], 0.85, 0.90, alpha=0.1, color='orange')

ax.set_xlabel('Date', fontweight='bold')
ax.set_ylabel('Power Factor (lag)', fontweight='bold')
ax.set_title('Power Factor Profile\nReactive Power and Efficiency Analysis', 
             fontweight='bold', fontsize=13)
ax.legend(loc='lower left', framealpha=0.95)
ax.grid(True, alpha=0.3)
ax.set_ylim(0.85, 1.0)
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('06_Power_Factor.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: 06_Power_Factor.png")
plt.close()

# ============================================================================
# FIGURE 7: Statistical Distribution - Box Plots
# ============================================================================
print("[8] Generating: Statistical Distribution Analysis...")
fig, axes = plt.subplots(2, 3, figsize=(15, 8))

distributions = [
    (data['Wind_Power_MW'], 'Wind Power (MW)', axes[0, 0]),
    (data['Solar_Power_MW'], 'Solar Power (MW)', axes[0, 1]),
    (data['Load_Demand_MW'], 'Load Demand (MW)', axes[0, 2]),
    (data['Voltage_pu'], 'Voltage (p.u.)', axes[1, 0]),
    (data['Frequency_Hz'], 'Frequency (Hz)', axes[1, 1]),
    (data['Renewable_Penetration_%'], 'Penetration (%)', axes[1, 2])
]

for data_series, label, ax in distributions:
    bp = ax.boxplot([data_series], labels=[label], patch_artist=True, widths=0.5)
    for patch in bp['boxes']:
        patch.set_facecolor('#1f77b4')
        patch.set_alpha(0.7)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylabel('Value', fontweight='bold')
    
    # Add statistics
    mean_val = data_series.mean()
    median_val = data_series.median()
    ax.text(1.15, mean_val, f'μ={mean_val:.2f}', va='center', fontsize=9, fontweight='bold')
    
fig.suptitle('Statistical Distribution of Grid Parameters\nReal-Time Data Analysis', 
             fontweight='bold', fontsize=14, y=1.00)
plt.tight_layout()
plt.savefig('07_Statistical_Distributions.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: 07_Statistical_Distributions.png")
plt.close()

# ============================================================================
# FIGURE 8: Correlation Matrix Heatmap
# ============================================================================
print("[9] Generating: Correlation Analysis...")
numeric_cols = ['Wind_Power_MW', 'Solar_Power_MW', 'Load_Demand_MW', 
                'Voltage_pu', 'Frequency_Hz', 'Harmonics_THD_%', 'Power_Factor']
corr_matrix = data[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax,
            vmin=-1, vmax=1)
ax.set_title('Parameter Correlation Matrix\nReal-Time Grid Data', 
             fontweight='bold', fontsize=13, pad=20)
plt.tight_layout()
plt.savefig('08_Correlation_Heatmap.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: 08_Correlation_Heatmap.png")
plt.close()

# ============================================================================
# FIGURE 9: Cumulative Distribution - Penetration CDF
# ============================================================================
print("[10] Generating: Cumulative Distribution Function...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# CDF for Wind Power
sorted_wind = np.sort(data['Wind_Power_MW'])
cdf_wind = np.arange(1, len(sorted_wind) + 1) / len(sorted_wind)
axes[0].plot(sorted_wind, cdf_wind * 100, linewidth=2.5, color='#1f77b4', label='Wind Power CDF')
axes[0].axhline(y=50, color='gray', linestyle='--', alpha=0.5)
axes[0].set_xlabel('Wind Power (MW)', fontweight='bold')
axes[0].set_ylabel('Cumulative Probability (%)', fontweight='bold')
axes[0].set_title('Wind Power Distribution', fontweight='bold', fontsize=12)
axes[0].grid(True, alpha=0.3)
axes[0].legend(framealpha=0.95)

# CDF for Penetration
sorted_pen = np.sort(data['Renewable_Penetration_%'])
cdf_pen = np.arange(1, len(sorted_pen) + 1) / len(sorted_pen)
axes[1].plot(sorted_pen, cdf_pen * 100, linewidth=2.5, color='#2ca02c', label='Penetration CDF')
axes[1].axvline(x=30, color='orange', linestyle='--', linewidth=2, label='Target (30%)', alpha=0.7)
axes[1].axhline(y=50, color='gray', linestyle='--', alpha=0.5)
axes[1].set_xlabel('Renewable Penetration (%)', fontweight='bold')
axes[1].set_ylabel('Cumulative Probability (%)', fontweight='bold')
axes[1].set_title('Renewable Penetration Distribution', fontweight='bold', fontsize=12)
axes[1].grid(True, alpha=0.3)
axes[1].legend(framealpha=0.95)

plt.suptitle('Cumulative Distribution Functions', fontweight='bold', fontsize=13, y=1.02)
plt.tight_layout()
plt.savefig('09_Cumulative_Distribution.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: 09_Cumulative_Distribution.png")
plt.close()

# ============================================================================
# FIGURE 10: Summary Statistics Table (as image)
# ============================================================================
print("[11] Generating: Summary Statistics Table...")
fig, ax = plt.subplots(figsize=(14, 7))
ax.axis('tight')
ax.axis('off')

# Create statistics summary
stats_data = []
for col in numeric_cols:
    stats_data.append([
        col.replace('_', ' '),
        f"{data[col].min():.3f}",
        f"{data[col].max():.3f}",
        f"{data[col].mean():.3f}",
        f"{data[col].std():.3f}",
        f"{data[col].median():.3f}"
    ])

table = ax.table(cellText=stats_data,
                colLabels=['Parameter', 'Min', 'Max', 'Mean', 'Std Dev', 'Median'],
                cellLoc='center',
                loc='center',
                bbox=[0, 0, 1, 1])

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.5)

# Style header
for i in range(6):
    table[(0, i)].set_facecolor('#1f77b4')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Alternate row colors
for i in range(1, len(stats_data) + 1):
    for j in range(6):
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#e8f4f8')
        else:
            table[(i, j)].set_facecolor('#ffffff')

fig.suptitle('Statistical Summary - Real-Time Grid Data', fontweight='bold', fontsize=14, y=0.98)
plt.savefig('10_Summary_Statistics_Table.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: 10_Summary_Statistics_Table.png")
plt.close()

print("\n" + "="*70)
print("✓ ALL PNG PLOTS GENERATED SUCCESSFULLY!")
print("="*70)
print("\nGenerated Files:")
print("  1. 01_Wind_Solar_Generation_Profile.png")
print("  2. 02_Load_vs_Renewable.png")
print("  3. 03_Renewable_Penetration.png")
print("  4. 04_Voltage_Frequency_Stability.png")
print("  5. 05_Harmonic_Distortion.png")
print("  6. 06_Power_Factor.png")
print("  7. 07_Statistical_Distributions.png")
print("  8. 08_Correlation_Heatmap.png")
print("  9. 09_Cumulative_Distribution.png")
print(" 10. 10_Summary_Statistics_Table.png")
print("\nAll plots are publication-ready (300 DPI, high resolution)")
print("="*70 + "\n")
