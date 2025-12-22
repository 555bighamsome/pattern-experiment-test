#!/usr/bin/env python3
"""
Pattern Language Experiment Data Analysis Script

This script analyzes experimental data from the pattern construction task,
including success rates, time metrics, cognitive strategies, and behavioral patterns.

Usage:
    python analyze_experiment_data.py --input data.json
    python analyze_experiment_data.py --input data.json --output report.html
    python analyze_experiment_data.py --database --participant P001
"""

import json
import argparse
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Tuple
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass, asdict
import warnings

warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']  # 支持中文


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class TrialMetrics:
    """Metrics for a single trial"""
    trial_number: int
    pattern_name: str
    success: bool
    time_spent: float  # milliseconds
    steps_count: int
    points_earned: int
    button_clicks: int
    preview_confirmations: int
    undo_resets: int
    favorite_actions: int
    operations_used: List[str]
    
    # Advanced metrics
    time_per_step: float
    efficiency_score: float  # success / (time * steps)
    engagement_level: str  # 'high', 'medium', 'low', 'abandoned'


@dataclass
class ParticipantSummary:
    """Overall summary for a participant"""
    participant_id: str
    condition: str
    total_tasks: int
    completed_tasks: int
    successful_tasks: int
    success_rate: float
    total_time: float  # seconds
    average_time_per_task: float
    total_steps: int
    total_points: int
    abandonment_point: int  # Which task they gave up
    
    # Behavioral patterns
    favorite_used_count: int
    most_used_operation: str
    learning_efficiency: float  # improvement over time


# ============================================================================
# Core Analysis Functions
# ============================================================================

class ExperimentAnalyzer:
    """Main analyzer class for experiment data"""
    
    def __init__(self, data: List[Dict[str, Any]]):
        """
        Initialize analyzer with raw experiment data
        
        Args:
            data: List of trial dictionaries from JSON
        """
        self.raw_data = data
        self.metadata = data[0] if data and 'metadata' in data[0] else {}
        self.trials = data[1:] if len(data) > 1 else []
        self.df = None
        self.metrics = []
        
    def parse_data(self) -> pd.DataFrame:
        """Parse raw data into structured DataFrame"""
        print("📊 Parsing experiment data...")
        
        rows = []
        for trial in self.trials:
            if 'trial' not in trial:
                continue
                
            row = {
                'trial': trial.get('trial'),
                'pattern_name': trial.get('testName'),
                'success': trial.get('success'),
                'submitted': trial.get('submitted'),
                'time_spent_ms': trial.get('timeSpent', 0),
                'time_spent_sec': trial.get('timeSpent', 0) / 1000.0,
                'steps_count': trial.get('stepsCount', 0),
                'points_earned': trial.get('pointsEarned', 0),
                'total_points_after': trial.get('totalPointsAfter', 0),
                
                # Interaction counts
                'button_clicks': len(trial.get('buttonClickActions', [])),
                'preview_actions': len(trial.get('previewActions', [])),
                'workflow_actions': len(trial.get('workflowActions', [])),
                'favorite_actions': len(trial.get('favoriteActions', [])),
                'undo_actions': len(trial.get('undoActions', [])),
                
                # Operation details
                'operations': trial.get('operations', []),
                'num_operations': len(trial.get('operations', [])),
                
                # Timestamps
                'started_at': trial.get('startedAt'),
            }
            
            # Calculate derived metrics
            if row['steps_count'] > 0:
                row['time_per_step'] = row['time_spent_sec'] / row['steps_count']
            else:
                row['time_per_step'] = 0
                
            # Engagement level
            row['engagement'] = self._classify_engagement(
                row['time_spent_sec'], 
                row['steps_count'],
                row['button_clicks']
            )
            
            rows.append(row)
        
        self.df = pd.DataFrame(rows)
        print(f"✅ Parsed {len(self.df)} trials")
        return self.df
    
    def _classify_engagement(self, time: float, steps: int, clicks: int) -> str:
        """Classify engagement level based on activity"""
        if steps == 0 and time < 1:
            return 'abandoned'
        elif steps == 0 and time < 5:
            return 'low'
        elif steps >= 1 and time >= 5:
            return 'high'
        else:
            return 'medium'
    
    # ========================================================================
    # Analysis Methods
    # ========================================================================
    
    def calculate_success_metrics(self) -> Dict[str, Any]:
        """Calculate overall success metrics"""
        print("\n📈 Calculating success metrics...")
        
        total_trials = len(self.df)
        submitted_trials = self.df['submitted'].sum()
        successful_trials = self.df['success'].sum()
        
        metrics = {
            'total_trials': total_trials,
            'submitted_trials': int(submitted_trials),
            'successful_trials': int(successful_trials),
            'success_rate': successful_trials / submitted_trials if submitted_trials > 0 else 0,
            'completion_rate': submitted_trials / total_trials if total_trials > 0 else 0,
            'total_points': int(self.df['points_earned'].sum()),
            'max_possible_points': total_trials,
        }
        
        print(f"  Success Rate: {metrics['success_rate']:.1%}")
        print(f"  Completion Rate: {metrics['completion_rate']:.1%}")
        print(f"  Points: {metrics['total_points']}/{metrics['max_possible_points']}")
        
        return metrics
    
    def calculate_time_metrics(self) -> Dict[str, Any]:
        """Calculate time-related metrics"""
        print("\n⏱️  Calculating time metrics...")
        
        # Filter out extremely fast trials (likely skipped)
        engaged_trials = self.df[self.df['time_spent_sec'] >= 1.0]
        
        metrics = {
            'total_time_sec': self.df['time_spent_sec'].sum(),
            'mean_time_sec': self.df['time_spent_sec'].mean(),
            'median_time_sec': self.df['time_spent_sec'].median(),
            'std_time_sec': self.df['time_spent_sec'].std(),
            
            # Engaged trials only
            'mean_engaged_time_sec': engaged_trials['time_spent_sec'].mean() if len(engaged_trials) > 0 else 0,
            'median_engaged_time_sec': engaged_trials['time_spent_sec'].median() if len(engaged_trials) > 0 else 0,
            
            # Time per step
            'mean_time_per_step': self.df[self.df['time_per_step'] > 0]['time_per_step'].mean(),
        }
        
        print(f"  Total Time: {metrics['total_time_sec']:.1f}s")
        print(f"  Mean Time (engaged): {metrics['mean_engaged_time_sec']:.1f}s")
        print(f"  Mean Time per Step: {metrics['mean_time_per_step']:.2f}s")
        
        return metrics
    
    def detect_abandonment_point(self) -> Dict[str, Any]:
        """Detect when participant started abandoning tasks"""
        print("\n🚨 Detecting abandonment pattern...")
        
        # Look for sudden drop in engagement
        abandonment_point = None
        for i, row in self.df.iterrows():
            if row['engagement'] == 'abandoned' or (row['steps_count'] == 0 and row['time_spent_sec'] < 1):
                # Check if this is start of consistent abandonment
                if i + 2 < len(self.df):
                    next_two = self.df.iloc[i:i+3]
                    if (next_two['steps_count'] == 0).sum() >= 2:
                        abandonment_point = int(row['trial'])
                        break
        
        # Calculate pre and post abandonment metrics
        if abandonment_point:
            pre_abandon = self.df[self.df['trial'] < abandonment_point]
            post_abandon = self.df[self.df['trial'] >= abandonment_point]
            
            metrics = {
                'abandonment_point': abandonment_point,
                'trials_before_abandonment': len(pre_abandon),
                'trials_after_abandonment': len(post_abandon),
                'success_before': pre_abandon['success'].sum(),
                'success_after': post_abandon['success'].sum(),
                'avg_time_before': pre_abandon['time_spent_sec'].mean(),
                'avg_time_after': post_abandon['time_spent_sec'].mean(),
            }
        else:
            metrics = {
                'abandonment_point': None,
                'message': 'No clear abandonment pattern detected'
            }
        
        if abandonment_point:
            print(f"  ⚠️  Abandonment detected at Trial {abandonment_point}")
            print(f"  Before: {metrics['success_before']} successes, {metrics['avg_time_before']:.1f}s avg")
            print(f"  After: {metrics['success_after']} successes, {metrics['avg_time_after']:.1f}s avg")
        else:
            print(f"  ✅ No abandonment detected")
        
        return metrics
    
    def analyze_operations(self) -> Dict[str, Any]:
        """Analyze operation usage patterns"""
        print("\n🔧 Analyzing operation usage...")
        
        # Flatten all operations
        all_ops = []
        for ops in self.df['operations']:
            all_ops.extend(ops)
        
        # Count operation types
        op_counts = {}
        op_types = {'add': 0, 'subtract': 0, 'reflect': 0, 'rotate': 0, 'invert': 0, 'other': 0}
        
        for op in all_ops:
            # Count specific operation
            op_counts[op] = op_counts.get(op, 0) + 1
            
            # Categorize
            if 'add' in op.lower():
                op_types['add'] += 1
            elif 'subtract' in op.lower():
                op_types['subtract'] += 1
            elif 'reflect' in op.lower():
                op_types['reflect'] += 1
            elif 'rotate' in op.lower():
                op_types['rotate'] += 1
            elif 'invert' in op.lower():
                op_types['invert'] += 1
            else:
                op_types['other'] += 1
        
        most_used = max(op_counts.items(), key=lambda x: x[1]) if op_counts else (None, 0)
        
        metrics = {
            'total_operations': len(all_ops),
            'unique_operations': len(op_counts),
            'operation_counts': op_counts,
            'operation_types': op_types,
            'most_used_operation': most_used[0],
            'most_used_count': most_used[1],
        }
        
        print(f"  Total Operations: {metrics['total_operations']}")
        print(f"  Unique Operations: {metrics['unique_operations']}")
        print(f"  Most Used: {metrics['most_used_operation']} ({metrics['most_used_count']} times)")
        
        return metrics
    
    def analyze_learning_curve(self) -> Dict[str, Any]:
        """Analyze learning progression over trials"""
        print("\n📚 Analyzing learning curve...")
        
        # Only analyze trials with actual engagement
        engaged = self.df[self.df['engagement'].isin(['high', 'medium'])]
        
        if len(engaged) < 3:
            return {'message': 'Insufficient engaged trials for learning analysis'}
        
        # Split into phases
        first_third = engaged.iloc[:len(engaged)//3]
        last_third = engaged.iloc[-len(engaged)//3:]
        
        metrics = {
            'early_success_rate': first_third['success'].mean(),
            'late_success_rate': last_third['success'].mean(),
            'early_avg_time': first_third['time_spent_sec'].mean(),
            'late_avg_time': last_third['time_spent_sec'].mean(),
            'early_avg_steps': first_third['steps_count'].mean(),
            'late_avg_steps': last_third['steps_count'].mean(),
            
            # Learning indicators
            'time_improvement': (first_third['time_spent_sec'].mean() - last_third['time_spent_sec'].mean()),
            'efficiency_improvement': (last_third['success'].mean() - first_third['success'].mean()),
        }
        
        print(f"  Early Success Rate: {metrics['early_success_rate']:.1%}")
        print(f"  Late Success Rate: {metrics['late_success_rate']:.1%}")
        print(f"  Time Improvement: {metrics['time_improvement']:.1f}s")
        
        return metrics
    
    def analyze_favorites(self) -> Dict[str, Any]:
        """Analyze favorite pattern usage"""
        print("\n⭐ Analyzing favorite usage...")
        
        favorite_trials = self.df[self.df['favorite_actions'] > 0]
        
        total_fav_actions = self.df['favorite_actions'].sum()
        trials_using_favs = len(favorite_trials)
        
        # Analyze success rate when using favorites
        if len(favorite_trials) > 0:
            success_with_favs = favorite_trials['success'].mean()
        else:
            success_with_favs = 0
        
        metrics = {
            'total_favorite_actions': int(total_fav_actions),
            'trials_using_favorites': trials_using_favs,
            'success_rate_with_favorites': success_with_favs,
            'avg_time_with_favorites': favorite_trials['time_spent_sec'].mean() if len(favorite_trials) > 0 else 0,
        }
        
        print(f"  Total Favorite Actions: {metrics['total_favorite_actions']}")
        print(f"  Trials Using Favorites: {metrics['trials_using_favorites']}")
        print(f"  Success Rate with Favorites: {metrics['success_rate_with_favorites']:.1%}")
        
        return metrics
    
    # ========================================================================
    # Visualization Methods
    # ========================================================================
    
    def plot_timeline(self, save_path: str = None):
        """Plot task completion timeline"""
        fig, axes = plt.subplots(3, 1, figsize=(14, 10))
        
        # Plot 1: Success/Failure over trials
        colors = ['green' if s else 'red' if s is False else 'gray' for s in self.df['success']]
        axes[0].bar(self.df['trial'], self.df['steps_count'], color=colors, alpha=0.7)
        axes[0].set_xlabel('Trial Number')
        axes[0].set_ylabel('Steps Count')
        axes[0].set_title('Task Completion Timeline (Green=Success, Red=Fail, Gray=Null)')
        axes[0].grid(True, alpha=0.3)
        
        # Plot 2: Time spent per trial
        axes[1].plot(self.df['trial'], self.df['time_spent_sec'], marker='o', linestyle='-', color='blue')
        axes[1].set_xlabel('Trial Number')
        axes[1].set_ylabel('Time (seconds)')
        axes[1].set_title('Time Spent per Trial')
        axes[1].grid(True, alpha=0.3)
        
        # Plot 3: Cumulative points
        axes[2].plot(self.df['trial'], self.df['total_points_after'], marker='o', linestyle='-', color='purple')
        axes[2].set_xlabel('Trial Number')
        axes[2].set_ylabel('Cumulative Points')
        axes[2].set_title('Point Accumulation')
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"  💾 Saved timeline plot to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_engagement_heatmap(self, save_path: str = None):
        """Plot engagement heatmap"""
        fig, ax = plt.subplots(figsize=(14, 4))
        
        # Create engagement matrix
        engagement_map = {'abandoned': 0, 'low': 1, 'medium': 2, 'high': 3}
        engagement_values = self.df['engagement'].map(engagement_map)
        
        # Reshape for heatmap (1 row)
        matrix = engagement_values.values.reshape(1, -1)
        
        sns.heatmap(matrix, cmap='RdYlGn', cbar_kws={'label': 'Engagement'},
                    xticklabels=self.df['trial'], yticklabels=['Engagement'],
                    ax=ax, vmin=0, vmax=3)
        
        ax.set_title('Engagement Level Across Trials')
        ax.set_xlabel('Trial Number')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"  💾 Saved engagement heatmap to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_operation_distribution(self, save_path: str = None):
        """Plot distribution of operations used"""
        ops_data = self.analyze_operations()
        
        if not ops_data['operation_counts']:
            print("  ⚠️  No operations to plot")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Plot 1: Specific operations
        ops_sorted = dict(sorted(ops_data['operation_counts'].items(), key=lambda x: x[1], reverse=True))
        ax1.barh(list(ops_sorted.keys()), list(ops_sorted.values()), color='steelblue')
        ax1.set_xlabel('Count')
        ax1.set_title('Specific Operations Used')
        ax1.grid(True, alpha=0.3, axis='x')
        
        # Plot 2: Operation types
        ax2.pie(ops_data['operation_types'].values(), 
                labels=ops_data['operation_types'].keys(),
                autopct='%1.1f%%', startangle=90)
        ax2.set_title('Operation Types Distribution')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"  💾 Saved operation distribution to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    # ========================================================================
    # Report Generation
    # ========================================================================
    
    def generate_summary_report(self) -> str:
        """Generate a text summary report"""
        report = []
        report.append("=" * 80)
        report.append("PATTERN LANGUAGE EXPERIMENT - ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Basic info
        report.append(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"📊 Total Trials: {len(self.df)}")
        report.append("")
        
        # Success metrics
        success = self.calculate_success_metrics()
        report.append("🎯 SUCCESS METRICS")
        report.append("-" * 80)
        report.append(f"  Success Rate:     {success['success_rate']:.1%}")
        report.append(f"  Completion Rate:  {success['completion_rate']:.1%}")
        report.append(f"  Total Points:     {success['total_points']}/{success['max_possible_points']}")
        report.append("")
        
        # Time metrics
        time_m = self.calculate_time_metrics()
        report.append("⏱️  TIME METRICS")
        report.append("-" * 80)
        report.append(f"  Total Time:       {time_m['total_time_sec']:.1f}s ({time_m['total_time_sec']/60:.1f}min)")
        report.append(f"  Mean Time:        {time_m['mean_time_sec']:.1f}s")
        report.append(f"  Mean (Engaged):   {time_m['mean_engaged_time_sec']:.1f}s")
        report.append(f"  Time per Step:    {time_m['mean_time_per_step']:.2f}s")
        report.append("")
        
        # Abandonment
        abandon = self.detect_abandonment_point()
        report.append("🚨 ABANDONMENT ANALYSIS")
        report.append("-" * 80)
        if abandon.get('abandonment_point'):
            report.append(f"  Abandonment Point: Trial {abandon['abandonment_point']}")
            report.append(f"  Success Before:    {abandon['success_before']} trials")
            report.append(f"  Success After:     {abandon['success_after']} trials")
        else:
            report.append(f"  No clear abandonment pattern detected")
        report.append("")
        
        # Operations
        ops = self.analyze_operations()
        report.append("🔧 OPERATION ANALYSIS")
        report.append("-" * 80)
        report.append(f"  Total Operations:  {ops['total_operations']}")
        report.append(f"  Unique Operations: {ops['unique_operations']}")
        report.append(f"  Most Used:         {ops['most_used_operation']} ({ops['most_used_count']}x)")
        report.append("")
        
        # Favorites
        favs = self.analyze_favorites()
        report.append("⭐ FAVORITE USAGE")
        report.append("-" * 80)
        report.append(f"  Total Actions:     {favs['total_favorite_actions']}")
        report.append(f"  Trials Used:       {favs['trials_using_favorites']}")
        report.append(f"  Success Rate:      {favs['success_rate_with_favorites']:.1%}")
        report.append("")
        
        # Learning
        learning = self.analyze_learning_curve()
        if 'message' not in learning:
            report.append("📚 LEARNING CURVE")
            report.append("-" * 80)
            report.append(f"  Early Success:     {learning['early_success_rate']:.1%}")
            report.append(f"  Late Success:      {learning['late_success_rate']:.1%}")
            report.append(f"  Time Improvement:  {learning['time_improvement']:.1f}s")
            report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def export_to_csv(self, filepath: str):
        """Export processed data to CSV"""
        self.df.to_csv(filepath, index=False)
        print(f"📄 Exported data to {filepath}")
    
    def export_to_json(self, filepath: str):
        """Export analysis results to JSON"""
        results = {
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'total_trials': len(self.df),
            },
            'success_metrics': self.calculate_success_metrics(),
            'time_metrics': self.calculate_time_metrics(),
            'abandonment_analysis': self.detect_abandonment_point(),
            'operation_analysis': self.analyze_operations(),
            'favorite_analysis': self.analyze_favorites(),
            'learning_curve': self.analyze_learning_curve(),
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Exported analysis to {filepath}")


# ============================================================================
# Database Integration (Optional)
# ============================================================================

def load_from_database(participant_id: str = None) -> List[Dict]:
    """
    Load data from MySQL database
    
    Args:
        participant_id: Optional participant ID to filter
    
    Returns:
        List of trial dictionaries
    """
    try:
        import pymysql
        from db_config import DB_CONFIG
    except ImportError:
        print("❌ pymysql not installed. Run: pip install pymysql")
        return []
    
    print(f"🔌 Connecting to database...")
    
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    if participant_id:
        query = "SELECT * FROM experiment_data WHERE participant_id = %s"
        cursor.execute(query, (participant_id,))
    else:
        query = "SELECT * FROM experiment_data ORDER BY created_at DESC LIMIT 1"
        cursor.execute(query)
    
    row = cursor.fetchone()
    
    if not row:
        print("❌ No data found")
        return []
    
    # Parse JSON fields
    task_data = json.loads(row['task_data']) if row['task_data'] else []
    freeplay_data = json.loads(row['freeplay_data']) if row['freeplay_data'] else []
    
    conn.close()
    
    print(f"✅ Loaded data for participant: {row['participant_id']}")
    
    return task_data if task_data else freeplay_data


# ============================================================================
# Main Function
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='Analyze pattern experiment data')
    parser.add_argument('--input', '-i', type=str, help='Input JSON file path')
    parser.add_argument('--output', '-o', type=str, help='Output directory for reports')
    parser.add_argument('--database', '-d', action='store_true', help='Load from database')
    parser.add_argument('--participant', '-p', type=str, help='Participant ID (for database)')
    parser.add_argument('--plots', action='store_true', help='Generate plots')
    parser.add_argument('--csv', action='store_true', help='Export to CSV')
    parser.add_argument('--json', action='store_true', help='Export analysis to JSON')
    
    args = parser.parse_args()
    
    # Load data
    if args.database:
        data = load_from_database(args.participant)
    elif args.input:
        print(f"📂 Loading data from {args.input}...")
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        print("❌ Please provide --input or --database flag")
        return
    
    if not data:
        print("❌ No data to analyze")
        return
    
    # Initialize analyzer
    analyzer = ExperimentAnalyzer(data)
    analyzer.parse_data()
    
    # Generate report
    print("\n" + "=" * 80)
    report = analyzer.generate_summary_report()
    print(report)
    
    # Create output directory
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path('analysis_output')
        output_dir.mkdir(exist_ok=True)
    
    # Save text report
    report_path = output_dir / 'analysis_report.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n💾 Report saved to {report_path}")
    
    # Generate plots
    if args.plots:
        print("\n📊 Generating visualizations...")
        analyzer.plot_timeline(output_dir / 'timeline.png')
        analyzer.plot_engagement_heatmap(output_dir / 'engagement_heatmap.png')
        analyzer.plot_operation_distribution(output_dir / 'operations.png')
    
    # Export data
    if args.csv:
        analyzer.export_to_csv(output_dir / 'processed_data.csv')
    
    if args.json:
        analyzer.export_to_json(output_dir / 'analysis_results.json')
    
    print("\n✅ Analysis complete!")
    print(f"📁 Output directory: {output_dir.absolute()}")


if __name__ == '__main__':
    main()
