#!/usr/bin/env python3
"""
Quick demo of analysis capabilities

Run this to see what the analysis script can do with sample data.
"""

import json
import sys
from pathlib import Path

# Sample data matching the structure provided by the user
SAMPLE_DATA = [
    {"metadata": {"randomized": False, "totalTasks": 3, "pointsPerTask": 1}},
    {
        "trial": 1,
        "testName": "Pattern-01",
        "success": True,
        "submitted": True,
        "timeSpent": 24489,
        "stepsCount": 5,
        "pointsEarned": 1,
        "totalPointsAfter": 1,
        "buttonClickActions": [
            {"buttonType": "binary", "operation": "add", "timestamp": 1766353671517},
            {"buttonType": "primitive", "operation": "line_vertical", "timestamp": 1766353672330}
        ],
        "operations": ["add(•, •)", "reflect_vertical(1)", "add(2, 1)", "reflect_diag(3)", "add(3, 4)"],
        "previewActions": [
            {"action": "confirm", "operationType": "add", "timestamp": 1766353675217}
        ],
        "favoriteActions": [
            {"action": "add", "favoriteId": "fav_001", "timestamp": 1766353687814}
        ],
        "undoActions": [
            {"type": "reset", "stepsCleared": 5, "timestamp": 1766353691162}
        ],
        "startedAt": 1766353664670
    },
    {
        "trial": 2,
        "testName": "Pattern-02",
        "success": True,
        "submitted": True,
        "timeSpent": 4298,
        "stepsCount": 1,
        "pointsEarned": 1,
        "totalPointsAfter": 2,
        "buttonClickActions": [
            {"buttonType": "binary", "operation": "add", "timestamp": 1766353692968}
        ],
        "operations": ["add(•, •)"],
        "previewActions": [
            {"action": "confirm", "operationType": "add", "timestamp": 1766353694746}
        ],
        "favoriteActions": [
            {"action": "use", "favoriteId": "fav_001", "timestamp": 1766353694030}
        ],
        "undoActions": [
            {"type": "reset", "stepsCleared": 1, "timestamp": 1766353697465}
        ],
        "startedAt": 1766353691163
    },
    {
        "trial": 3,
        "testName": "Pattern-03",
        "success": False,
        "submitted": True,
        "timeSpent": 6677,
        "stepsCount": 1,
        "pointsEarned": 0,
        "totalPointsAfter": 2,
        "buttonClickActions": [
            {"buttonType": "transform", "operation": "invert", "timestamp": 1766353701131}
        ],
        "operations": ["invert(•)"],
        "previewActions": [
            {"action": "confirm", "operationType": "invert", "timestamp": 1766353703438}
        ],
        "favoriteActions": [
            {"action": "use", "favoriteId": "fav_001", "timestamp": 1766353701847}
        ],
        "undoActions": [
            {"type": "reset", "stepsCleared": 1, "timestamp": 1766353706147}
        ],
        "startedAt": 1766353697468
    }
]


def main():
    print("="*80)
    print("🎯 Pattern Experiment Analysis - Quick Demo")
    print("="*80)
    print()
    
    # Save sample data
    sample_file = Path('sample_data.json')
    with open(sample_file, 'w', encoding='utf-8') as f:
        json.dump(SAMPLE_DATA, f, indent=2, ensure_ascii=False)
    
    print(f"📝 Created sample data file: {sample_file}")
    print()
    
    # Import analyzer
    try:
        from analyze_experiment_data import ExperimentAnalyzer
    except ImportError:
        print("❌ Could not import analyzer. Make sure you're in the analysis directory.")
        return
    
    # Create analyzer
    print("🔧 Initializing analyzer...")
    analyzer = ExperimentAnalyzer(SAMPLE_DATA)
    analyzer.parse_data()
    print()
    
    # Generate report
    print("📊 Generating analysis report...")
    print()
    report = analyzer.generate_summary_report()
    print(report)
    print()
    
    # Show DataFrame
    print("="*80)
    print("📋 PROCESSED DATA (first few rows)")
    print("="*80)
    print(analyzer.df[['trial', 'pattern_name', 'success', 'time_spent_sec', 'steps_count', 'engagement']].to_string())
    print()
    
    # Try to generate plots
    try:
        import matplotlib.pyplot as plt
        print("📊 Generating visualizations...")
        
        output_dir = Path('demo_output')
        output_dir.mkdir(exist_ok=True)
        
        analyzer.plot_timeline(output_dir / 'timeline.png')
        analyzer.plot_engagement_heatmap(output_dir / 'engagement.png')
        analyzer.plot_operation_distribution(output_dir / 'operations.png')
        
        print(f"✅ Plots saved to {output_dir}/")
        print()
    except Exception as e:
        print(f"⚠️  Could not generate plots: {e}")
        print()
    
    # Export data
    print("💾 Exporting results...")
    output_dir = Path('demo_output')
    output_dir.mkdir(exist_ok=True)
    
    analyzer.export_to_csv(output_dir / 'processed_data.csv')
    analyzer.export_to_json(output_dir / 'analysis_results.json')
    
    with open(output_dir / 'report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ All outputs saved to {output_dir}/")
    print()
    
    # Usage examples
    print("="*80)
    print("📚 NEXT STEPS")
    print("="*80)
    print()
    print("To analyze your own data:")
    print("  python analyze_experiment_data.py --input your_data.json --plots")
    print()
    print("To analyze from database:")
    print("  python analyze_experiment_data.py --database --participant P001 --plots")
    print()
    print("For batch analysis:")
    print("  python batch_analyze.py participant_data/ --output batch_results/")
    print()
    print("="*80)


if __name__ == '__main__':
    main()
