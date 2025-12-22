#!/usr/bin/env python3
"""
Batch analysis script for multiple participants

This script processes all JSON files in a directory and generates
individual analysis reports for each participant.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from analyze_experiment_data import ExperimentAnalyzer


def analyze_single_participant(data_file: Path, output_base: Path):
    """Analyze a single participant's data"""
    print(f"\n{'='*80}")
    print(f"📊 Analyzing: {data_file.name}")
    print(f"{'='*80}")
    
    # Load data
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading {data_file.name}: {e}")
        return None
    
    # Create analyzer
    analyzer = ExperimentAnalyzer(data)
    analyzer.parse_data()
    
    # Create output directory
    participant_id = data_file.stem
    output_dir = output_base / participant_id
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate report
    report = analyzer.generate_summary_report()
    report_path = output_dir / 'analysis_report.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"💾 Report saved to {report_path}")
    
    # Generate plots
    try:
        analyzer.plot_timeline(output_dir / 'timeline.png')
        analyzer.plot_engagement_heatmap(output_dir / 'engagement_heatmap.png')
        analyzer.plot_operation_distribution(output_dir / 'operations.png')
    except Exception as e:
        print(f"⚠️  Error generating plots: {e}")
    
    # Export data
    analyzer.export_to_csv(output_dir / 'processed_data.csv')
    analyzer.export_to_json(output_dir / 'analysis_results.json')
    
    # Return summary metrics
    return {
        'participant_id': participant_id,
        'success_metrics': analyzer.calculate_success_metrics(),
        'time_metrics': analyzer.calculate_time_metrics(),
        'abandonment': analyzer.detect_abandonment_point(),
    }


def generate_comparative_report(all_metrics: list, output_path: Path):
    """Generate a comparative report across all participants"""
    if not all_metrics:
        return
    
    print(f"\n{'='*80}")
    print("📊 Generating Comparative Report")
    print(f"{'='*80}")
    
    # Create DataFrame
    rows = []
    for metrics in all_metrics:
        row = {
            'Participant': metrics['participant_id'],
            'Success Rate': metrics['success_metrics']['success_rate'],
            'Total Points': metrics['success_metrics']['total_points'],
            'Total Time (s)': metrics['time_metrics']['total_time_sec'],
            'Mean Time (s)': metrics['time_metrics']['mean_engaged_time_sec'],
            'Abandonment Point': metrics['abandonment'].get('abandonment_point', 'None'),
        }
        rows.append(row)
    
    df = pd.DataFrame(rows)
    
    # Generate report
    report = []
    report.append("="*80)
    report.append("COMPARATIVE ANALYSIS - ALL PARTICIPANTS")
    report.append("="*80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Total Participants: {len(all_metrics)}")
    report.append("")
    
    report.append("📊 SUMMARY TABLE")
    report.append("-"*80)
    report.append(df.to_string(index=False))
    report.append("")
    
    report.append("📈 AGGREGATE STATISTICS")
    report.append("-"*80)
    report.append(f"Mean Success Rate:     {df['Success Rate'].mean():.1%}")
    report.append(f"Median Success Rate:   {df['Success Rate'].median():.1%}")
    report.append(f"Mean Total Time:       {df['Total Time (s)'].mean():.1f}s")
    report.append(f"Mean Points:           {df['Total Points'].mean():.1f}")
    report.append("")
    
    # Abandonment analysis
    abandoned_count = df[df['Abandonment Point'] != 'None'].shape[0]
    report.append("🚨 ABANDONMENT ANALYSIS")
    report.append("-"*80)
    report.append(f"Participants Who Abandoned:  {abandoned_count}/{len(all_metrics)} ({abandoned_count/len(all_metrics):.1%})")
    if abandoned_count > 0:
        abandon_df = df[df['Abandonment Point'] != 'None']
        report.append(f"Average Abandonment Point:   {abandon_df['Abandonment Point'].astype(float).mean():.1f}")
    report.append("")
    
    report.append("="*80)
    
    # Save report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"💾 Comparative report saved to {output_path}")
    
    # Save CSV
    csv_path = output_path.parent / 'comparative_data.csv'
    df.to_csv(csv_path, index=False)
    print(f"💾 Comparative data saved to {csv_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch analyze multiple participant data files')
    parser.add_argument('input_dir', type=str, help='Directory containing JSON data files')
    parser.add_argument('--output', '-o', type=str, default='batch_analysis_results',
                       help='Output directory for analysis results')
    parser.add_argument('--pattern', '-p', type=str, default='*.json',
                       help='File pattern to match (default: *.json)')
    
    args = parser.parse_args()
    
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output)
    
    if not input_dir.exists():
        print(f"❌ Input directory does not exist: {input_dir}")
        return
    
    # Find all matching files
    data_files = list(input_dir.glob(args.pattern))
    
    if not data_files:
        print(f"❌ No files found matching pattern: {args.pattern}")
        return
    
    print(f"📂 Found {len(data_files)} files to analyze")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Analyze each participant
    all_metrics = []
    for data_file in data_files:
        metrics = analyze_single_participant(data_file, output_dir)
        if metrics:
            all_metrics.append(metrics)
    
    # Generate comparative report
    if all_metrics:
        comparative_path = output_dir / 'comparative_report.txt'
        generate_comparative_report(all_metrics, comparative_path)
    
    print(f"\n{'='*80}")
    print(f"✅ Batch analysis complete!")
    print(f"📁 Results saved to: {output_dir.absolute()}")
    print(f"{'='*80}")


if __name__ == '__main__':
    main()
