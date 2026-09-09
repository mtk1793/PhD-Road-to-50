#!/usr/bin/env python3
"""
Quick script to run FACTS simulations with real-time data
"""

import sys
import json
from integrate_realtime_data import RealDataIntegrator
from python_implementation import NeuroOptimaFACTS, AdvancedAnalytics

def main():
    print("\n" + "="*70)
    print("NEURO-OPTIMAFACTS SIMULATION WITH REAL-TIME DATA")
    print("="*70)
    
    # Step 1: Load real-time data
    print("\n[STEP 1] Loading real-time dataset from APIs...")
    try:
        integrator = RealDataIntegrator()
        real_time_data = integrator.load_latest_realtime_dataset()
        print(f"✓ Successfully loaded {len(real_time_data)} hours of real-time data")
        print(f"  Date range: {real_time_data['Date'].min()} to {real_time_data['Date'].max()}")
        print(f"  Columns: {list(real_time_data.columns)}")
    except Exception as e:
        print(f"✗ Failed to load real-time data: {e}")
        sys.exit(1)
    
    # Step 2: Initialize FACTS framework
    print("\n[STEP 2] Initializing Neuro-OptimaFACTS framework...")
    try:
        neuro_optimafacts = NeuroOptimaFACTS()
        print("✓ Framework initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize framework: {e}")
        sys.exit(1)
    
    # Step 3: Run complete analysis with real-time data
    print("\n[STEP 3] Running FACTS analysis with real-time data...")
    print("-" * 70)
    try:
        results = neuro_optimafacts.run_complete_analysis_with_realtime_data(real_time_data)
        print("-" * 70)
        print("✓ FACTS analysis completed successfully")
    except Exception as e:
        print(f"✗ FACTS analysis failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Step 4: Advanced analytics
    print("\n[STEP 4] Performing advanced analytics...")
    try:
        # Baseline comparison
        print("  - Comparing with baseline methods...")
        comparison = AdvancedAnalytics.compare_with_baseline(results)
        
        print("\n  Baseline Comparison Results:")
        print("  " + "-" * 60)
        for metric, values in comparison.items():
            if 'improvement_ratio' in values:
                print(f"    {metric.replace('_', ' ').title()}:")
                print(f"      Baseline: {values.get('baseline', 'N/A'):.4f}")
                print(f"      Neuro-OptimaFACTS: {values.get('neuro_optimafacts', 'N/A'):.4f}")
                print(f"      Improvement Ratio: {values.get('improvement_ratio', 'N/A'):.2f}x")
            elif 'accuracy_improvement' in values:
                print(f"    {metric.replace('_', ' ').title()}:")
                print(f"      Baseline RMSE: {values.get('baseline_rmse', 'N/A'):.6f}")
                print(f"      Neuro-OptimaFACTS RMSE: {values.get('neuro_optimafacts_rmse', 'N/A'):.6f}")
                print(f"      Accuracy Improvement: {values.get('accuracy_improvement', 'N/A'):.2f}%")
        
        # Sensitivity analysis
        print("\n  - Performing sensitivity analysis...")
        parameter_variations = {
            'renewable_penetration': [0.5, 0.75, 1.0, 1.25, 1.5, 2.0],
            'load_variability': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            'voltage_disturbance': [0.0, 0.01, 0.02, 0.03, 0.04, 0.05]
        }
        
        sensitivity_results = AdvancedAnalytics.sensitivity_analysis(
            neuro_optimafacts, 
            results['grid_data'], 
            parameter_variations
        )
        print("  ✓ Sensitivity analysis completed")
        
    except Exception as e:
        print(f"✗ Advanced analytics failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 5: Save results to JSON files
    print("\n[STEP 5] Saving results to JSON files...")
    try:
        # Save comprehensive report
        with open('realtime_simulation_report.json', 'w') as f:
            report_data = {
                'title': 'Neuro-OptimaFACTS Real-Time Simulation Report',
                'data_source': 'Real-time APIs (NOAA, NREL, EIA, OpenWeatherMap, ISO-RTO)',
                'data_points': len(real_time_data),
                'date_range': {
                    'start': str(real_time_data['Date'].min()),
                    'end': str(real_time_data['Date'].max())
                },
                'performance_metrics': results.get('performance_metrics', {}),
                'comparison_with_baseline': comparison if 'comparison' in locals() else {},
                'data_statistics': {
                    'renewable_penetration': {
                        'min': float(real_time_data['Renewable_Penetration_%'].min()),
                        'max': float(real_time_data['Renewable_Penetration_%'].max()),
                        'mean': float(real_time_data['Renewable_Penetration_%'].mean())
                    },
                    'voltage': {
                        'min': float(real_time_data['Voltage_pu'].min()),
                        'max': float(real_time_data['Voltage_pu'].max()),
                        'mean': float(real_time_data['Voltage_pu'].mean())
                    },
                    'frequency': {
                        'min': float(real_time_data['Frequency_Hz'].min()),
                        'max': float(real_time_data['Frequency_Hz'].max()),
                        'mean': float(real_time_data['Frequency_Hz'].mean())
                    }
                }
            }
            json.dump(report_data, f, indent=2, default=str)
        print("✓ Saved realtime_simulation_report.json")
        
        # Save performance metrics
        with open('FACTS_realtime_performance.json', 'w') as f:
            json.dump(results.get('performance_metrics', {}), f, indent=2, default=str)
        print("✓ Saved FACTS_realtime_performance.json")
        
    except Exception as e:
        print(f"✗ Failed to save results: {e}")
    
    print("\n" + "="*70)
    print("SIMULATION COMPLETE!")
    print("="*70)
    print("\nGenerated files:")
    print("  - realtime_simulation_report.json")
    print("  - FACTS_realtime_performance.json")
    print("\n✓ All FACTS devices analyzed with real-time data validation")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
