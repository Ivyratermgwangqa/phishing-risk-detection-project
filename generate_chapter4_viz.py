#!/usr/bin/env python3
"""
Generate all visualizations for Chapter 4 (Implementation) and Chapter 5 (Results)
Author: Generated for phishing-risk-detection-project
"""

import json
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create output directory
output_dir = Path('reports/chapter4')
output_dir.mkdir(exist_ok=True, parents=True)
(output_dir / 'figures').mkdir(exist_ok=True)
(output_dir / 'tables').mkdir(exist_ok=True)

print("=" * 70)
print("CHAPTER 4 & 5 VISUALIZATION GENERATOR")
print("=" * 70)

# ============================================================================
# LOAD ALL DATA
# ============================================================================
print("\n📂 Loading data...")

try:
    with open('models/training_metrics.json') as f:
        metrics = json.load(f)
    print("  ✓ Training metrics loaded")
except FileNotFoundError:
    print("  ✗ models/training_metrics.json not found!")
    metrics = None

try:
    with open('reports/cv_scores.json') as f:
        cv_data = json.load(f)
    print("  ✓ CV scores loaded")
except FileNotFoundError:
    print("  ✗ reports/cv_scores.json not found!")
    cv_data = None

try:
    with open('models/feature_names.json') as f:
        feature_names = json.load(f)
    print("  ✓ Feature names loaded")
except FileNotFoundError:
    print("  ✗ models/feature_names.json not found!")
    feature_names = None

# ============================================================================
# FIGURE 5.1: ROC CURVE
# ============================================================================
print("\n📊 Generating Figure 5.1: ROC Curve...")

if metrics and 'roc_curve' in metrics:
    fpr = metrics['roc_curve']['fpr']
    tpr = metrics['roc_curve']['tpr']
    roc_auc = metrics['model_performance']['auc']
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f'Phishing Classifier (AUC = {roc_auc:.4f})', 
             linewidth=2.5, color='#2ecc71')
    plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier', linewidth=1.5, alpha=0.7)
    plt.xlabel('False Positive Rate', fontsize=13, fontweight='bold')
    plt.ylabel('True Positive Rate', fontsize=13, fontweight='bold')
    plt.title('ROC Curve - Phishing Detection Model', fontsize=15, fontweight='bold', pad=15)
    plt.legend(fontsize=11, loc='lower right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_path = output_dir / 'figures' / 'fig5_1_roc_curve.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: {output_path}")
else:
    print("  ✗ Skipped (missing data)")

# ============================================================================
# FIGURE 5.15: MODEL PERFORMANCE COMPARISON
# ============================================================================
print("\n📊 Generating Figure 5.15: Performance Metrics Comparison...")

if metrics and 'model_performance' in metrics:
    perf = metrics['model_performance']
    metric_names = ['AUC-ROC', 'Precision', 'Recall', 'F1 Score']
    metric_values = [perf['auc'], perf['precision'], perf['recall'], perf['f1']]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
    bars = ax.bar(metric_names, metric_values, color=colors, alpha=0.8, 
                  edgecolor='black', linewidth=1.5)
    
    ax.set_ylabel('Score', fontsize=13, fontweight='bold')
    ax.set_title('Model Performance Across Metrics', fontsize=15, fontweight='bold', pad=15)
    ax.set_ylim([0.90, 1.0])
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, value in zip(bars, metric_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{value:.4f}', ha='center', va='bottom', 
                fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    output_path = output_dir / 'figures' / 'fig5_15_performance_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: {output_path}")
else:
    print("  ✗ Skipped (missing data)")

# ============================================================================
# FIGURE 5.16: CROSS-VALIDATION SCORES
# ============================================================================
print("\n📊 Generating Figure 5.16: CV Scores Distribution...")

if cv_data:
    scores = cv_data['scores']
    folds = list(range(1, len(scores) + 1))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(folds, scores, alpha=0.75, color='steelblue', 
                  edgecolor='navy', linewidth=1.5, width=0.6)
    
    # Add mean line
    mean_line = ax.axhline(cv_data['mean'], color='red', linestyle='--', 
                           linewidth=2.5,
                           label=f"Mean = {cv_data['mean']:.4f} ± {cv_data['std']:.4f}")
    
    ax.set_xlabel('Fold Number', fontsize=13, fontweight='bold')
    ax.set_ylabel('AUC-ROC Score', fontsize=13, fontweight='bold')
    ax.set_title('Cross-Validation Performance (5-Fold GroupKFold)', 
                 fontsize=15, fontweight='bold', pad=15)
    ax.set_ylim([0.9880, 0.9900])
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add score labels on bars
    for fold, score in zip(folds, scores):
        ax.text(fold, score + 0.00005, f'{score:.4f}', 
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    output_path = output_dir / 'figures' / 'fig5_16_cv_scores.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: {output_path}")
else:
    print("  ✗ Skipped (missing data)")

# ============================================================================
# FEATURE CATEGORIES PIE CHART
# ============================================================================
print("\n📊 Generating Feature Categories Distribution...")

if feature_names:
    categories = {
        'URL Structure': 7,
        'Domain Analysis': 2,
        'Graph Features': 6,
        'Network Features': 1,
        'Threat Intelligence': 3
    }
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = sns.color_palette("pastel", len(categories))
    wedges, texts, autotexts = ax.pie(categories.values(), labels=categories.keys(), 
                                        autopct='%1.1f%%', startangle=90, 
                                        colors=colors, textprops={'fontsize': 12})
    
    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    ax.set_title('Feature Categories Distribution\n(19 Total Features)', 
                 fontsize=15, fontweight='bold', pad=20)
    
    plt.tight_layout()
    output_path = output_dir / 'figures' / 'feature_categories_pie.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: {output_path}")
else:
    print("  ✗ Skipped (missing data)")

# ============================================================================
# TRAINING WORKFLOW DIAGRAM (Simple Bar Chart)
# ============================================================================
print("\n📊 Generating Figure 4.1: Training Workflow Stats...")

if metrics and 'train_test_split' in metrics:
    split_data = metrics['train_test_split']
    
    categories = ['Training Set', 'Test Set']
    benign_counts = [split_data['train_label_dist']['0'], 
                     split_data['test_label_dist']['0']]
    phishing_counts = [split_data['train_label_dist']['1'], 
                       split_data['test_label_dist']['1']]
    
    x = np.arange(len(categories))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, benign_counts, width, label='Benign (0)', 
                   color='#3498db', alpha=0.8, edgecolor='black')
    bars2 = ax.bar(x + width/2, phishing_counts, width, label='Phishing (1)', 
                   color='#e74c3c', alpha=0.8, edgecolor='black')
    
    ax.set_ylabel('Sample Count', fontsize=13, fontweight='bold')
    ax.set_title('Train/Test Split - Label Distribution', fontsize=15, 
                 fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add count labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    output_path = output_dir / 'figures' / 'fig4_1_train_test_split.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: {output_path}")
else:
    print("  ✗ Skipped (missing data)")

# ============================================================================
# DATA PREPROCESSING STATS
# ============================================================================
print("\n📊 Generating Figure 4.2: Data Preprocessing Stats...")

if metrics and 'data_stats' in metrics:
    stats = metrics['data_stats']
    
    stages = ['Initial\nDataset', 'After\nDeduplication', 'After Leakage\nRemoval', 'Final\nDataset']
    row_counts = [381450, 159603, 159603, 159603]  # From your data
    feature_counts = [27, 26, 19, 19]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Row counts
    bars1 = ax1.bar(stages, row_counts, color=['#95a5a6', '#3498db', '#2ecc71', '#27ae60'],
                    alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Number of Rows', fontsize=12, fontweight='bold')
    ax1.set_title('Dataset Size Through Pipeline', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.tick_params(axis='x', labelsize=10)
    
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}', ha='center', va='bottom', fontsize=9)
    
    # Feature counts
    bars2 = ax2.bar(stages, feature_counts, color=['#95a5a6', '#e67e22', '#e74c3c', '#c0392b'],
                    alpha=0.8, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Number of Features', fontsize=12, fontweight='bold')
    ax2.set_title('Feature Count Through Pipeline', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.tick_params(axis='x', labelsize=10)
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=10)
    
    plt.suptitle('Data Preprocessing Pipeline Statistics', fontsize=15, 
                 fontweight='bold', y=1.02)
    plt.tight_layout()
    output_path = output_dir / 'figures' / 'fig4_2_preprocessing_stats.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: {output_path}")
else:
    print("  ✗ Skipped (missing data)")

# ============================================================================
# GENERATE TABLES
# ============================================================================
print("\n📝 Generating tables...")

# Table 1: Performance Metrics
if metrics and 'model_performance' in metrics:
    perf = metrics['model_performance']
    table1 = pd.DataFrame({
        'Metric': ['AUC-ROC', 'Precision', 'Recall', 'F1 Score'],
        'Score': [perf['auc'], perf['precision'], perf['recall'], perf['f1']],
        'Interpretation': [
            'Excellent discrimination capability',
            '92% accuracy when flagging phishing',
            'Catches 96% of phishing attempts',
            'Balanced precision and recall'
        ]
    })
    output_path = output_dir / 'tables' / 'table1_performance_metrics.csv'
    table1.to_csv(output_path, index=False)
    print(f"  ✓ Saved: {output_path}")

# Table 2: CV Scores
if cv_data:
    cv_table = pd.DataFrame({
        'Fold': list(range(1, len(cv_data['scores']) + 1)),
        'AUC-ROC Score': cv_data['scores']
    })
    cv_table.loc[len(cv_table)] = ['Mean', cv_data['mean']]
    cv_table.loc[len(cv_table)] = ['Std Dev', cv_data['std']]
    
    output_path = output_dir / 'tables' / 'table2_cv_scores.csv'
    cv_table.to_csv(output_path, index=False)
    print(f"  ✓ Saved: {output_path}")

# Table 4: Dataset Stats
if metrics:
    stats_table = pd.DataFrame({
        'Metric': [
            'Total records (raw)',
            'Features (raw)',
            'Duplicate URLs detected',
            'Final records (deduplicated)',
            'Final features',
            'Benign samples (label=0)',
            'Phishing samples (label=1)',
            'Class ratio (phishing %)'
        ],
        'Value': [
            '381,450',
            '27',
            '221,847',
            '159,603',
            '19',
            f"{metrics['data_stats']['label_counts']['0']:,}",
            f"{metrics['data_stats']['label_counts']['1']:,}",
            f"{(metrics['data_stats']['label_counts']['1'] / 159603 * 100):.1f}%"
        ]
    })
    output_path = output_dir / 'tables' / 'table4_dataset_stats.csv'
    stats_table.to_csv(output_path, index=False)
    print(f"  ✓ Saved: {output_path}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("✅ GENERATION COMPLETE!")
print("=" * 70)
print(f"\n📁 All outputs saved to: {output_dir}/")
print("\nGenerated Files:")
print("  Figures:")
print("    • fig5_1_roc_curve.png")
print("    • fig5_15_performance_comparison.png")
print("    • fig5_16_cv_scores.png")
print("    • fig4_1_train_test_split.png")
print("    • fig4_2_preprocessing_stats.png")
print("    • feature_categories_pie.png")
print("\n  Tables:")
print("    • table1_performance_metrics.csv")
print("    • table2_cv_scores.csv")
print("    • table4_dataset_stats.csv")

print("\n📖 For complete guide, see: docs/CHAPTER4_DATA_SOURCE_GUIDE.md")
print("\n💡 To view existing SHAP plots, check: models/phishing_shap_*.png")
print("=" * 70)
