#!/usr/bin/env python3
"""
Generate all visualizations for Chapters 1-3 (Introduction, Literature Review, Methodology)
Includes architectural diagrams, flowcharts, and conceptual visualizations
Author: Generated for phishing-risk-detection-project
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
import numpy as np
from pathlib import Path

# Set style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['font.size'] = 10

# Create output directories
output_dir = Path('reports/chapters1-3')
output_dir.mkdir(exist_ok=True, parents=True)
(output_dir / 'chapter1').mkdir(exist_ok=True)
(output_dir / 'chapter2').mkdir(exist_ok=True)
(output_dir / 'chapter3').mkdir(exist_ok=True)

print("=" * 80)
print("CHAPTERS 1-3 VISUALIZATION GENERATOR")
print("=" * 80)

# ============================================================================
# FIGURE 1.1: Explainable Phishing Detection Framework Architecture
# ============================================================================
print("\n📊 Generating Figure 1.1: Framework Architecture...")

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Title
ax.text(5, 9.5, 'Explainable Phishing Detection Framework', 
        ha='center', va='top', fontsize=16, fontweight='bold')

# Layer 5: Output & Reporting (Top)
layer5 = FancyBboxPatch((1, 8), 8, 0.8, boxstyle="round,pad=0.05", 
                         edgecolor='#2ecc71', facecolor='#d5f4e6', linewidth=2)
ax.add_patch(layer5)
ax.text(5, 8.4, 'Layer 5: Output & Reporting', ha='center', va='center', 
        fontsize=11, fontweight='bold', color='#27ae60')
ax.text(5, 8.05, 'Dashboard • Risk Scores • SHAP Explanations', 
        ha='center', va='center', fontsize=8, style='italic')

# Arrow
ax.arrow(5, 7.95, 0, -0.3, head_width=0.15, head_length=0.1, fc='gray', ec='gray')

# Layer 4: ML Model (Prediction)
layer4 = FancyBboxPatch((1, 6.5), 8, 1.2, boxstyle="round,pad=0.05",
                         edgecolor='#3498db', facecolor='#d6eaf8', linewidth=2)
ax.add_patch(layer4)
ax.text(5, 7.35, 'Layer 4: Machine Learning Model', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#2874a6')
ax.text(5, 7.0, 'Random Forest Classifier', ha='center', va='center', fontsize=9)
ax.text(5, 6.7, 'Phishing Detection • Authentication Risk Assessment', 
        ha='center', va='center', fontsize=8, style='italic')

# Arrow
ax.arrow(5, 6.45, 0, -0.3, head_width=0.15, head_length=0.1, fc='gray', ec='gray')

# Layer 3: Feature Engineering
layer3 = FancyBboxPatch((1, 4.8), 8, 1.4, boxstyle="round,pad=0.05",
                         edgecolor='#e74c3c', facecolor='#fadbd8', linewidth=2)
ax.add_patch(layer3)
ax.text(5, 5.9, 'Layer 3: Feature Engineering', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#c0392b')

# Three feature boxes within layer 3
box_width = 2.3
boxes = [
    (1.5, 5.1, 'URL Features', '• Domain\n• Structure\n• Length'),
    (3.9, 5.1, 'Graph Features', '• PageRank\n• Betweenness\n• Centrality'),
    (6.3, 5.1, 'Threat Intel', '• VirusTotal\n• Malicious\n• Suspicious')
]
for x, y, title, content in boxes:
    box = FancyBboxPatch((x, y), box_width, 0.6, boxstyle="round,pad=0.03",
                          edgecolor='#c0392b', facecolor='white', linewidth=1)
    ax.add_patch(box)
    ax.text(x + box_width/2, y + 0.45, title, ha='center', va='center',
            fontsize=8, fontweight='bold')
    ax.text(x + box_width/2, y + 0.15, content, ha='center', va='center',
            fontsize=6)

# Arrow
ax.arrow(5, 4.75, 0, -0.3, head_width=0.15, head_length=0.1, fc='gray', ec='gray')

# Layer 2: Data Processing
layer2 = FancyBboxPatch((1, 3.3), 8, 1.2, boxstyle="round,pad=0.05",
                         edgecolor='#f39c12', facecolor='#fdebd0', linewidth=2)
ax.add_patch(layer2)
ax.text(5, 4.15, 'Layer 2: Data Processing & Enrichment', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#d68910')
ax.text(5, 3.8, 'Deduplication • Leakage Removal • Feature Extraction', 
        ha='center', va='center', fontsize=9)
ax.text(5, 3.5, 'Graph Construction • VirusTotal API Integration', 
        ha='center', va='center', fontsize=8, style='italic')

# Arrow
ax.arrow(5, 3.25, 0, -0.3, head_width=0.15, head_length=0.1, fc='gray', ec='gray')

# Layer 1: Data Input
layer1 = FancyBboxPatch((1, 1.8), 8, 1.2, boxstyle="round,pad=0.05",
                         edgecolor='#9b59b6', facecolor='#ebdef0', linewidth=2)
ax.add_patch(layer1)
ax.text(5, 2.65, 'Layer 1: Data Input', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#7d3c98')
ax.text(5, 2.3, 'URLs • Email Headers • Logs', ha='center', va='center', fontsize=9)
ax.text(5, 2.0, 'Raw Dataset (381,450 records) → Processed (159,603 unique URLs)', 
        ha='center', va='center', fontsize=8, style='italic')

# Bottom annotation
ax.text(5, 1.3, 'Framework enables explainable predictions with SHAP integration at Layer 5',
        ha='center', va='center', fontsize=9, style='italic', color='#34495e',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#ecf0f1', alpha=0.7))

# Add legend for layers
legend_elements = [
    mpatches.Patch(facecolor='#d5f4e6', edgecolor='#2ecc71', label='Output Layer'),
    mpatches.Patch(facecolor='#d6eaf8', edgecolor='#3498db', label='ML Layer'),
    mpatches.Patch(facecolor='#fadbd8', edgecolor='#e74c3c', label='Feature Layer'),
    mpatches.Patch(facecolor='#fdebd0', edgecolor='#f39c12', label='Processing Layer'),
    mpatches.Patch(facecolor='#ebdef0', edgecolor='#9b59b6', label='Input Layer')
]
ax.legend(handles=legend_elements, loc='lower left', fontsize=8, framealpha=0.9)

plt.tight_layout()
output_path = output_dir / 'chapter1' / 'fig1_1_framework_architecture.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: {output_path}")

# ============================================================================
# FIGURE 2.1: Overview of ML Approaches in Phishing Detection
# ============================================================================
print("\n📊 Generating Figure 2.1: ML Approaches Overview...")

fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Title
ax.text(5, 9.5, 'Machine Learning Approaches in Phishing Detection', 
        ha='center', va='top', fontsize=15, fontweight='bold')

# Main categories
categories = [
    {
        'name': 'Traditional ML',
        'x': 2, 'y': 7,
        'methods': ['Random Forest', 'SVM', 'Decision Trees', 'Naive Bayes'],
        'color': '#3498db'
    },
    {
        'name': 'Deep Learning',
        'x': 5, 'y': 7,
        'methods': ['CNN', 'RNN/LSTM', 'Transformers', 'Autoencoders'],
        'color': '#e74c3c'
    },
    {
        'name': 'Ensemble Methods',
        'x': 8, 'y': 7,
        'methods': ['Boosting', 'Bagging', 'Stacking', 'Voting'],
        'color': '#2ecc71'
    }
]

for cat in categories:
    # Main box
    box = FancyBboxPatch((cat['x']-0.8, cat['y']-0.3), 1.6, 0.5,
                          boxstyle="round,pad=0.05",
                          edgecolor=cat['color'], facecolor=cat['color'],
                          linewidth=2, alpha=0.7)
    ax.add_patch(box)
    ax.text(cat['x'], cat['y'], cat['name'], ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')
    
    # Methods boxes
    for i, method in enumerate(cat['methods']):
        y_pos = cat['y'] - 1.0 - i*0.6
        method_box = FancyBboxPatch((cat['x']-0.7, y_pos-0.2), 1.4, 0.35,
                                     boxstyle="round,pad=0.03",
                                     edgecolor=cat['color'], facecolor='white',
                                     linewidth=1.5)
        ax.add_patch(method_box)
        ax.text(cat['x'], y_pos, method, ha='center', va='center', fontsize=9)

# Our approach highlight
our_approach = FancyBboxPatch((1, 1.5), 8, 1,
                               boxstyle="round,pad=0.1",
                               edgecolor='#f39c12', facecolor='#fef5e7',
                               linewidth=3, linestyle='--')
ax.add_patch(our_approach)
ax.text(5, 2.2, 'Our Approach: Random Forest + SHAP Explainability', 
        ha='center', va='center', fontsize=12, fontweight='bold', color='#d68910')
ax.text(5, 1.85, 'Combines accuracy of ensemble methods with interpretability through SHAP', 
        ha='center', va='center', fontsize=9, style='italic', color='#7d6608')

# Add arrows pointing to our approach
for cat in categories:
    if cat['name'] in ['Traditional ML', 'Ensemble Methods']:
        ax.annotate('', xy=(5, 2.5), xytext=(cat['x'], 3.5),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='#95a5a6'))

# Bottom legend
ax.text(5, 0.8, 'Literature shows Random Forest provides optimal balance between accuracy and interpretability',
        ha='center', va='center', fontsize=9, style='italic',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#ecf0f1', alpha=0.8))

plt.tight_layout()
output_path = output_dir / 'chapter2' / 'fig2_1_ml_approaches_overview.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: {output_path}")

# ============================================================================
# FIGURE 3.1: Complete Framework Architecture with Five Layers
# ============================================================================
print("\n📊 Generating Figure 3.1: Five Layer Architecture...")

fig, ax = plt.subplots(figsize=(16, 11))
ax.set_xlim(0, 12)
ax.set_ylim(0, 11)
ax.axis('off')

ax.text(6, 10.5, 'Complete Framework Architecture - Five Layers', 
        ha='center', va='top', fontsize=16, fontweight='bold')

layers_detail = [
    {
        'y': 8.8, 'height': 1.3, 'name': 'Layer 5: Output & Reporting',
        'color': '#2ecc71', 'bg': '#d5f4e6',
        'components': [
            ('Interactive Dashboard', 'Streamlit-based UI'),
            ('Risk Scores', '0-100 scale'),
            ('SHAP Visualizations', 'Force/Bar/Summary plots'),
            ('Alerts & Reports', 'CSV/JSON export')
        ]
    },
    {
        'y': 7.0, 'height': 1.5, 'name': 'Layer 4: Machine Learning Models',
        'color': '#3498db', 'bg': '#d6eaf8',
        'components': [
            ('Phishing Classifier', 'Random Forest (100 trees)'),
            ('Auth Risk Model', 'Risk scoring'),
            ('SHAP Integration', 'TreeExplainer'),
            ('Model Persistence', 'Pickle serialization')
        ]
    },
    {
        'y': 5.0, 'height': 1.7, 'name': 'Layer 3: Feature Engineering',
        'color': '#e74c3c', 'bg': '#fadbd8',
        'components': [
            ('URL Features (7)', 'Domain, path, length'),
            ('Graph Features (6)', 'PageRank, centrality'),
            ('VirusTotal (3)', 'Malicious, suspicious'),
            ('Network Features (1)', 'IP analysis'),
            ('Domain Analysis (2)', 'WHOIS, registration')
        ]
    },
    {
        'y': 3.0, 'height': 1.7, 'name': 'Layer 2: Data Processing',
        'color': '#f39c12', 'bg': '#fdebd0',
        'components': [
            ('Deduplication', '221,847 duplicates removed'),
            ('Leakage Prevention', 'Target leakage check'),
            ('Graph Construction', 'NetworkX graph'),
            ('VT API Integration', 'Batch enrichment'),
            ('Feature Extraction', 'URL parsing')
        ]
    },
    {
        'y': 1.0, 'height': 1.7, 'name': 'Layer 1: Data Input',
        'color': '#9b59b6', 'bg': '#ebdef0',
        'components': [
            ('Raw Dataset', '381,450 URLs'),
            ('CSV Format', 'url, label columns'),
            ('Enron Emails', 'Authentication logs'),
            ('Data Validation', 'Schema check'),
            ('Initial Cleanup', 'Missing values')
        ]
    }
]

for layer in layers_detail:
    # Main layer box
    main_box = FancyBboxPatch((0.5, layer['y']), 11, layer['height'],
                               boxstyle="round,pad=0.05",
                               edgecolor=layer['color'], facecolor=layer['bg'],
                               linewidth=2.5)
    ax.add_patch(main_box)
    
    # Layer name
    ax.text(6, layer['y'] + layer['height'] - 0.25, layer['name'],
            ha='center', va='center', fontsize=12, fontweight='bold',
            color=layer['color'])
    
    # Components
    num_components = len(layer['components'])
    comp_width = 10.5 / num_components
    for i, (comp_name, comp_desc) in enumerate(layer['components']):
        x_pos = 1.0 + i * comp_width + comp_width/2
        y_pos = layer['y'] + layer['height']/2 - 0.2
        
        # Component box
        comp_box = FancyBboxPatch((1.0 + i*comp_width + 0.1, y_pos - 0.3),
                                   comp_width - 0.2, 0.6,
                                   boxstyle="round,pad=0.03",
                                   edgecolor=layer['color'], facecolor='white',
                                   linewidth=1.2)
        ax.add_patch(comp_box)
        
        ax.text(x_pos, y_pos + 0.15, comp_name, ha='center', va='center',
                fontsize=7, fontweight='bold')
        ax.text(x_pos, y_pos - 0.1, comp_desc, ha='center', va='center',
                fontsize=6, style='italic')
    
    # Arrow to next layer (except for layer 1)
    if layer['y'] > 1.5:
        ax.arrow(6, layer['y'] - 0.05, 0, -0.2, head_width=0.2, head_length=0.1,
                 fc='#34495e', ec='#34495e', linewidth=2)

plt.tight_layout()
output_path = output_dir / 'chapter3' / 'fig3_1_complete_five_layer_architecture.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: {output_path}")

# ============================================================================
# FIGURE 3.2: Data Flow Diagram
# ============================================================================
print("\n📊 Generating Figure 3.2: Data Flow Diagram...")

fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

ax.text(5, 9.5, 'Data Flow: From Input to Output', 
        ha='center', va='top', fontsize=15, fontweight='bold')

# Flow stages
flow = [
    {'name': 'Raw Data\n381,450 URLs', 'y': 8, 'color': '#9b59b6'},
    {'name': 'Deduplication\n159,603 unique', 'y': 6.5, 'color': '#3498db'},
    {'name': 'Feature Extraction\n19 features', 'y': 5, 'color': '#e74c3c'},
    {'name': 'Train/Test Split\n80/20', 'y': 3.5, 'color': '#f39c12'},
    {'name': 'Model Training\nRandom Forest', 'y': 2, 'color': '#2ecc71'},
    {'name': 'Predictions +\nSHAP Values', 'y': 0.5, 'color': '#1abc9c'}
]

for i, stage in enumerate(flow):
    # Stage box
    box = FancyBboxPatch((3.5, stage['y']-0.35), 3, 0.7,
                          boxstyle="round,pad=0.05",
                          edgecolor=stage['color'], facecolor=stage['color'],
                          linewidth=2, alpha=0.7)
    ax.add_patch(box)
    ax.text(5, stage['y'], stage['name'], ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')
    
    # Arrow to next stage
    if i < len(flow) - 1:
        ax.arrow(5, stage['y'] - 0.4, 0, -0.7, head_width=0.2, head_length=0.15,
                 fc='#34495e', ec='#34495e', linewidth=2)

# Side annotations
annotations = [
    {'y': 7.25, 'text': 'CSV file with url and label columns', 'side': 'right'},
    {'y': 5.75, 'text': 'Remove 221,847 duplicate URLs', 'side': 'left'},
    {'y': 4.25, 'text': 'URL + Graph + VirusTotal features', 'side': 'right'},
    {'y': 2.75, 'text': 'GroupKFold cross-validation', 'side': 'left'},
    {'y': 1.25, 'text': '100 decision trees, max_depth=20', 'side': 'right'}
]

for annot in annotations:
    x_pos = 7.2 if annot['side'] == 'right' else 2.8
    align = 'left' if annot['side'] == 'right' else 'right'
    
    ax.text(x_pos, annot['y'], annot['text'], ha=align, va='center',
            fontsize=8, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#ecf0f1', alpha=0.8))
    
    # Connection line
    line_x = [5, x_pos - 0.1] if annot['side'] == 'right' else [x_pos + 0.1, 5]
    ax.plot(line_x, [annot['y'], annot['y']], 'k--', alpha=0.3, linewidth=1)

plt.tight_layout()
output_path = output_dir / 'chapter3' / 'fig3_2_data_flow_diagram.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: {output_path}")

# ============================================================================
# FIGURE 3.3: Feature Extraction Pipeline
# ============================================================================
print("\n📊 Generating Figure 3.3: Feature Extraction Pipeline...")

fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')

ax.text(7, 7.5, 'Feature Extraction Pipeline', 
        ha='center', va='top', fontsize=15, fontweight='bold')

# Input URL
url_box = FancyBboxPatch((5.5, 6.2), 3, 0.6,
                          boxstyle="round,pad=0.05",
                          edgecolor='#34495e', facecolor='#ecf0f1',
                          linewidth=2)
ax.add_patch(url_box)
ax.text(7, 6.5, 'Input: URL String', ha='center', va='center',
        fontsize=11, fontweight='bold')

# Arrow down
ax.arrow(7, 6.15, 0, -0.3, head_width=0.2, head_length=0.1,
         fc='#34495e', ec='#34495e', linewidth=2)

# Three parallel extraction processes
processes = [
    {
        'x': 1, 'name': 'URL Analysis',
        'features': ['domain_length', 'path_length', 'num_subdomains', 
                     'has_ip', 'num_dots', 'num_hyphens', 'url_length'],
        'color': '#3498db'
    },
    {
        'x': 5.5, 'name': 'Graph Analysis',
        'features': ['pagerank', 'in_degree', 'out_degree',
                     'betweenness', 'closeness', 'clustering'],
        'color': '#e74c3c'
    },
    {
        'x': 10, 'name': 'Threat Intel',
        'features': ['vt_malicious', 'vt_suspicious', 'vt_harmless'],
        'color': '#2ecc71'
    }
]

for proc in processes:
    # Process box
    proc_box = FancyBboxPatch((proc['x'], 4.8), 3, 0.6,
                               boxstyle="round,pad=0.05",
                               edgecolor=proc['color'], facecolor=proc['color'],
                               linewidth=2, alpha=0.7)
    ax.add_patch(proc_box)
    ax.text(proc['x'] + 1.5, 5.1, proc['name'], ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')
    
    # Features list
    y_start = 4.3
    for i, feat in enumerate(proc['features']):
        feat_box = FancyBboxPatch((proc['x'] + 0.2, y_start - i*0.4), 2.6, 0.3,
                                   boxstyle="round,pad=0.02",
                                   edgecolor=proc['color'], facecolor='white',
                                   linewidth=1)
        ax.add_patch(feat_box)
        ax.text(proc['x'] + 1.5, y_start - i*0.4 + 0.15, feat,
                ha='center', va='center', fontsize=7)
    
    # Arrow from URL to process
    ax.annotate('', xy=(proc['x'] + 1.5, 5.4), xytext=(7, 5.8),
               arrowprops=dict(arrowstyle='->', lw=1.5, color='#95a5a6'))

# Merge box at bottom
merge_box = FancyBboxPatch((4.5, 0.5), 5, 0.8,
                            boxstyle="round,pad=0.05",
                            edgecolor='#f39c12', facecolor='#fef5e7',
                            linewidth=2.5)
ax.add_patch(merge_box)
ax.text(7, 1.1, 'Feature Vector Concatenation', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#d68910')
ax.text(7, 0.7, '19 features combined → Input to Random Forest', ha='center', va='center',
        fontsize=9, style='italic')

# Arrows to merge
for proc in processes:
    bottom_y = y_start - len(proc['features'])*0.4 + 0.3
    ax.annotate('', xy=(7, 1.3), xytext=(proc['x'] + 1.5, bottom_y),
               arrowprops=dict(arrowstyle='->', lw=1.5, color='#95a5a6'))

plt.tight_layout()
output_path = output_dir / 'chapter3' / 'fig3_3_feature_extraction_pipeline.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: {output_path}")

# ============================================================================
# FIGURE 3.4: URL Feature Extraction Process
# ============================================================================
print("\n📊 Generating Figure 3.4: URL Feature Extraction...")

fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis('off')

ax.text(6, 6.5, 'URL Feature Extraction Process', 
        ha='center', va='top', fontsize=14, fontweight='bold')

# Example URL
url_example = 'https://secure.login-verify.account-update.com/auth/login.php'
url_box = FancyBboxPatch((1, 5.5), 10, 0.6,
                          boxstyle="round,pad=0.05",
                          edgecolor='#e74c3c', facecolor='#fadbd8',
                          linewidth=2)
ax.add_patch(url_box)
ax.text(6, 5.8, f'Example: {url_example}', ha='center', va='center',
        fontsize=8, fontfamily='monospace')

# Features extracted
features_data = [
    ('domain_length', '38', 'Length of domain name'),
    ('url_length', '69', 'Total URL length'),
    ('num_subdomains', '4', 'Count of subdomains'),
    ('num_dots', '5', 'Dots in URL'),
    ('num_hyphens', '3', 'Hyphens (suspicious)'),
    ('has_ip', '0', 'IP address present'),
    ('path_length', '15', 'Length of path')
]

y_pos = 4.5
for i, (feat, value, desc) in enumerate(features_data):
    if i < 4:
        x = 1.5
        y = y_pos - (i * 0.7)
    else:
        x = 7
        y = y_pos - ((i-4) * 0.7)
    
    # Feature box
    feat_box = FancyBboxPatch((x, y), 3.5, 0.5,
                               boxstyle="round,pad=0.03",
                               edgecolor='#3498db', facecolor='#d6eaf8',
                               linewidth=1.5)
    ax.add_patch(feat_box)
    
    ax.text(x + 0.2, y + 0.25, feat, ha='left', va='center',
            fontsize=9, fontweight='bold')
    ax.text(x + 2.5, y + 0.25, value, ha='center', va='center',
            fontsize=10, fontweight='bold', color='#e74c3c',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white'))
    ax.text(x + 1.75, y + 0.05, desc, ha='center', va='center',
            fontsize=7, style='italic')

# Analysis note
note_box = FancyBboxPatch((2, 0.5), 8, 0.8,
                           boxstyle="round,pad=0.05",
                           edgecolor='#f39c12', facecolor='#fef9e7',
                           linewidth=2)
ax.add_patch(note_box)
ax.text(6, 1.0, 'Suspicious Indicators:', ha='center', va='center',
        fontsize=10, fontweight='bold', color='#d68910')
ax.text(6, 0.65, 'Long domain (38 chars) • Multiple subdomains (4) • Hyphens (3) → High phishing probability',
        ha='center', va='center', fontsize=8, style='italic')

plt.tight_layout()
output_path = output_dir / 'chapter3' / 'fig3_4_url_feature_extraction.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: {output_path}")

# ============================================================================
# FIGURE 3.5: Graph-Based Feature Analysis
# ============================================================================
print("\n📊 Generating Figure 3.5: Graph-Based Features...")

fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

ax.text(5, 9.5, 'Graph-Based Feature Analysis', 
        ha='center', va='top', fontsize=14, fontweight='bold')

# Simple graph visualization
# Nodes
nodes = [
    {'x': 5, 'y': 7, 'label': 'URL 1\n(Target)', 'color': '#e74c3c', 'size': 0.5},
    {'x': 3, 'y': 5.5, 'label': 'URL 2', 'color': '#3498db', 'size': 0.3},
    {'x': 7, 'y': 5.5, 'label': 'URL 3', 'color': '#3498db', 'size': 0.3},
    {'x': 2, 'y': 4, 'label': 'URL 4', 'color': '#95a5a6', 'size': 0.25},
    {'x': 8, 'y': 4, 'label': 'URL 5', 'color': '#95a5a6', 'size': 0.25},
]

# Edges
edges = [
    (0, 1), (0, 2), (1, 3), (2, 4), (1, 2)
]

# Draw edges
for src, dst in edges:
    ax.plot([nodes[src]['x'], nodes[dst]['x']], 
            [nodes[src]['y'], nodes[dst]['y']],
            'k-', alpha=0.3, linewidth=2)

# Draw nodes
for node in nodes:
    circle = Circle((node['x'], node['y']), node['size'],
                    facecolor=node['color'], edgecolor='black',
                    linewidth=2, alpha=0.7)
    ax.add_patch(circle)
    ax.text(node['x'], node['y'], node['label'], ha='center', va='center',
            fontsize=7, fontweight='bold', color='white')

# Graph features calculated
features = [
    ('PageRank', '0.247', 'Importance in network'),
    ('In-Degree', '0', 'Incoming connections'),
    ('Out-Degree', '2', 'Outgoing connections'),
    ('Betweenness', '0.333', 'Bridge centrality'),
    ('Closeness', '0.571', 'Avg distance to others'),
    ('Clustering', '0.0', 'Local connectivity')
]

y_start = 2.5
for i, (feat, value, desc) in enumerate(features):
    row = i // 3
    col = i % 3
    x = 1 + col * 3
    y = y_start - row * 0.8
    
    feat_box = FancyBboxPatch((x, y), 2.5, 0.6,
                               boxstyle="round,pad=0.03",
                               edgecolor='#2ecc71', facecolor='#d5f4e6',
                               linewidth=1.5)
    ax.add_patch(feat_box)
    
    ax.text(x + 0.15, y + 0.4, feat, ha='left', va='center',
            fontsize=8, fontweight='bold')
    ax.text(x + 1.9, y + 0.4, value, ha='center', va='center',
            fontsize=9, fontweight='bold', color='#e74c3c')
    ax.text(x + 1.25, y + 0.15, desc, ha='center', va='center',
            fontsize=6, style='italic')

plt.tight_layout()
output_path = output_dir / 'chapter3' / 'fig3_5_graph_feature_analysis.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: {output_path}")

# ============================================================================
# FIGURE 3.6: VirusTotal Intelligence Integration
# ============================================================================
print("\n📊 Generating Figure 3.6: VirusTotal Integration...")

fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

ax.text(5, 9.5, 'VirusTotal Intelligence Integration', 
        ha='center', va='top', fontsize=14, fontweight='bold')

# Process flow
# Step 1: URL input
step1 = FancyBboxPatch((3, 7.5), 4, 0.8,
                        boxstyle="round,pad=0.05",
                        edgecolor='#9b59b6', facecolor='#ebdef0',
                        linewidth=2)
ax.add_patch(step1)
ax.text(5, 7.9, 'Step 1: Extract URL', ha='center', va='center',
        fontsize=10, fontweight='bold')

ax.arrow(5, 7.45, 0, -0.4, head_width=0.2, head_length=0.1,
         fc='#34495e', ec='#34495e', linewidth=2)

# Step 2: VT API call
step2 = FancyBboxPatch((3, 6.0), 4, 0.8,
                        boxstyle="round,pad=0.05",
                        edgecolor='#3498db', facecolor='#d6eaf8',
                        linewidth=2)
ax.add_patch(step2)
ax.text(5, 6.4, 'Step 2: Query VirusTotal API', ha='center', va='center',
        fontsize=10, fontweight='bold')
ax.text(5, 6.15, 'POST /urls (batch mode)', ha='center', va='center',
        fontsize=8, style='italic', fontfamily='monospace')

ax.arrow(5, 5.95, 0, -0.4, head_width=0.2, head_length=0.1,
         fc='#34495e', ec='#34495e', linewidth=2)

# Step 3: Parse response
step3 = FancyBboxPatch((3, 4.5), 4, 0.8,
                        boxstyle="round,pad=0.05",
                        edgecolor='#e74c3c', facecolor='#fadbd8',
                        linewidth=2)
ax.add_patch(step3)
ax.text(5, 4.9, 'Step 3: Parse JSON Response', ha='center', va='center',
        fontsize=10, fontweight='bold')
ax.text(5, 4.65, 'Extract malicious/suspicious/harmless counts', ha='center', va='center',
        fontsize=8, style='italic')

ax.arrow(5, 4.45, 0, -0.4, head_width=0.2, head_length=0.1,
         fc='#34495e', ec='#34495e', linewidth=2)

# Step 4: Feature creation
step4 = FancyBboxPatch((3, 3.0), 4, 0.8,
                        boxstyle="round,pad=0.05",
                        edgecolor='#2ecc71', facecolor='#d5f4e6',
                        linewidth=2)
ax.add_patch(step4)
ax.text(5, 3.4, 'Step 4: Create Features', ha='center', va='center',
        fontsize=10, fontweight='bold')
ax.text(5, 3.15, 'vt_malicious, vt_suspicious, vt_harmless', ha='center', va='center',
        fontsize=8, style='italic', fontfamily='monospace')

# Example output
example = FancyBboxPatch((1.5, 1.2), 7, 1.5,
                          boxstyle="round,pad=0.05",
                          edgecolor='#f39c12', facecolor='#fef5e7',
                          linewidth=2)
ax.add_patch(example)
ax.text(5, 2.45, 'Example VirusTotal Response:', ha='center', va='center',
        fontsize=10, fontweight='bold', color='#d68910')

# Feature boxes
vt_features = [
    ('vt_malicious', '42', '#e74c3c'),
    ('vt_suspicious', '7', '#f39c12'),
    ('vt_harmless', '3', '#2ecc71')
]

x_start = 2.2
for i, (feat, val, color) in enumerate(vt_features):
    x = x_start + i * 2.2
    feat_box = FancyBboxPatch((x, 1.5), 1.8, 0.6,
                               boxstyle="round,pad=0.03",
                               edgecolor=color, facecolor='white',
                               linewidth=2)
    ax.add_patch(feat_box)
    ax.text(x + 0.9, 1.95, feat, ha='center', va='center',
            fontsize=8, fontweight='bold')
    ax.text(x + 0.9, 1.65, val, ha='center', va='center',
            fontsize=12, fontweight='bold', color=color)

ax.text(5, 0.8, 'High malicious count (42) → Strong phishing indicator',
        ha='center', va='center', fontsize=9, style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#ecf0f1', alpha=0.8))

plt.tight_layout()
output_path = output_dir / 'chapter3' / 'fig3_6_virustotal_integration.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: {output_path}")

# ============================================================================
# FIGURE 3.7: Random Forest Classifier Architecture
# ============================================================================
print("\n📊 Generating Figure 3.7: Random Forest Architecture...")

fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis('off')

ax.text(7, 8.5, 'Random Forest Classifier Architecture', 
        ha='center', va='top', fontsize=15, fontweight='bold')

# Input features
input_box = FancyBboxPatch((5, 7.0), 4, 0.8,
                            boxstyle="round,pad=0.05",
                            edgecolor='#9b59b6', facecolor='#ebdef0',
                            linewidth=2)
ax.add_patch(input_box)
ax.text(7, 7.5, 'Feature Vector (19 features)', ha='center', va='center',
        fontsize=11, fontweight='bold')
ax.text(7, 7.15, 'URL + Graph + VirusTotal features', ha='center', va='center',
        fontsize=8, style='italic')

# Trees
tree_positions = [1.5, 4, 6.5, 9, 11.5]
for i, x in enumerate(tree_positions):
    # Arrow from input
    ax.annotate('', xy=(x + 0.8, 6.2), xytext=(7, 6.9),
               arrowprops=dict(arrowstyle='->', lw=1.5, color='#95a5a6'))
    
    # Tree box
    tree_box = FancyBboxPatch((x, 4.5), 1.6, 1.5,
                               boxstyle="round,pad=0.05",
                               edgecolor='#2ecc71', facecolor='#d5f4e6',
                               linewidth=2)
    ax.add_patch(tree_box)
    
    # Tree structure (simplified)
    ax.plot([x + 0.8, x + 0.5], [5.7, 5.3], 'k-', linewidth=1.5)
    ax.plot([x + 0.8, x + 1.1], [5.7, 5.3], 'k-', linewidth=1.5)
    ax.plot([x + 0.5, x + 0.3], [5.3, 4.9], 'k-', linewidth=1)
    ax.plot([x + 0.5, x + 0.7], [5.3, 4.9], 'k-', linewidth=1)
    ax.plot([x + 1.1, x + 0.9], [5.3, 4.9], 'k-', linewidth=1)
    ax.plot([x + 1.1, x + 1.3], [5.3, 4.9], 'k-', linewidth=1)
    
    ax.text(x + 0.8, 5.9, f'Tree {i+1}', ha='center', va='center',
            fontsize=8, fontweight='bold')
    
    # Arrow to voting
    ax.annotate('', xy=(7, 3.5), xytext=(x + 0.8, 4.4),
               arrowprops=dict(arrowstyle='->', lw=1.5, color='#95a5a6'))

if len(tree_positions) < 100:
    ax.text(13, 5.5, '...', ha='center', va='center', fontsize=20, fontweight='bold')
    ax.text(13, 5.0, '(100 trees\ntotal)', ha='center', va='center',
            fontsize=7, style='italic')

# Voting mechanism
vote_box = FancyBboxPatch((5, 2.5), 4, 0.8,
                           boxstyle="round,pad=0.05",
                           edgecolor='#3498db', facecolor='#d6eaf8',
                           linewidth=2)
ax.add_patch(vote_box)
ax.text(7, 2.9, 'Majority Voting', ha='center', va='center',
        fontsize=11, fontweight='bold')
ax.text(7, 2.6, 'Aggregate predictions from all trees', ha='center', va='center',
        fontsize=8, style='italic')

ax.arrow(7, 2.45, 0, -0.35, head_width=0.25, head_length=0.12,
         fc='#34495e', ec='#34495e', linewidth=2)

# Output
output_box = FancyBboxPatch((5, 1.0), 4, 0.8,
                             boxstyle="round,pad=0.05",
                             edgecolor='#e74c3c', facecolor='#fadbd8',
                             linewidth=2)
ax.add_patch(output_box)
ax.text(7, 1.5, 'Final Prediction', ha='center', va='center',
        fontsize=11, fontweight='bold')
ax.text(7, 1.15, 'Phishing (1) or Benign (0) + Probability', ha='center', va='center',
        fontsize=8, style='italic')

# Parameters annotation
params_text = 'Model Parameters:\n• n_estimators=100\n• max_depth=20\n• min_samples_split=5\n• class_weight=balanced'
ax.text(0.5, 3.5, params_text, ha='left', va='top',
        fontsize=8, bbox=dict(boxstyle='round,pad=0.4', facecolor='#fef5e7',
                              edgecolor='#f39c12', linewidth=1.5))

plt.tight_layout()
output_path = output_dir / 'chapter3' / 'fig3_7_random_forest_architecture.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: {output_path}")

# ============================================================================
# FIGURE 3.8: Authentication Risk Model Components
# ============================================================================
print("\n📊 Generating Figure 3.8: Auth Risk Model...")

fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis('off')

ax.text(6, 7.5, 'Authentication Risk Model Components', 
        ha='center', va='top', fontsize=14, fontweight='bold')

# Input data
input_data = FancyBboxPatch((4, 6.2), 4, 0.8,
                             boxstyle="round,pad=0.05",
                             edgecolor='#9b59b6', facecolor='#ebdef0',
                             linewidth=2)
ax.add_patch(input_data)
ax.text(6, 6.7, 'Authentication Logs (Enron Dataset)', ha='center', va='center',
        fontsize=10, fontweight='bold')
ax.text(6, 6.4, 'User login events, timestamps, locations', ha='center', va='center',
        fontsize=8, style='italic')

ax.arrow(6, 6.15, 0, -0.3, head_width=0.2, head_length=0.1,
         fc='#34495e', ec='#34495e', linewidth=2)

# Feature extraction
features = [
    ('Login Time', 'Hour of day', '#3498db'),
    ('Location', 'IP/Geo data', '#e74c3c'),
    ('Device', 'User agent', '#2ecc71'),
    ('Frequency', 'Login rate', '#f39c12')
]

y_pos = 5.0
for i, (feat, desc, color) in enumerate(features):
    col = i % 2
    row = i // 2
    x = 2 + col * 4.5
    y = y_pos - row * 1.0
    
    feat_box = FancyBboxPatch((x, y), 3.5, 0.6,
                               boxstyle="round,pad=0.03",
                               edgecolor=color, facecolor='white',
                               linewidth=1.5)
    ax.add_patch(feat_box)
    ax.text(x + 0.2, y + 0.3, feat, ha='left', va='center',
            fontsize=9, fontweight='bold', color=color)
    ax.text(x + 1.75, y + 0.15, desc, ha='center', va='center',
            fontsize=7, style='italic')
    
    # Arrow from input
    ax.annotate('', xy=(x + 1.75, y + 0.6), xytext=(6, 6.1),
               arrowprops=dict(arrowstyle='->', lw=1, color='#bdc3c7', alpha=0.5))

# Risk scoring
risk_box = FancyBboxPatch((3.5, 2.0), 5, 1.0,
                           boxstyle="round,pad=0.05",
                           edgecolor='#e74c3c', facecolor='#fadbd8',
                           linewidth=2)
ax.add_patch(risk_box)
ax.text(6, 2.7, 'Risk Score Calculation', ha='center', va='center',
        fontsize=11, fontweight='bold')
ax.text(6, 2.4, 'Weighted combination of anomaly indicators', ha='center', va='center',
        fontsize=8, style='italic')
ax.text(6, 2.15, 'Output: Risk score 0-100', ha='center', va='center',
        fontsize=9, fontweight='bold', color='#c0392b')

# Arrows to risk
for i in range(4):
    col = i % 2
    row = i // 2
    x = 2 + col * 4.5 + 1.75
    y = y_pos - row * 1.0
    ax.annotate('', xy=(6, 3.0), xytext=(x, y - 0.05),
               arrowprops=dict(arrowstyle='->', lw=1.5, color='#95a5a6'))

# Decision thresholds
threshold_box = FancyBboxPatch((2, 0.5), 8, 1.0,
                                boxstyle="round,pad=0.05",
                                edgecolor='#f39c12', facecolor='#fef5e7',
                                linewidth=2)
ax.add_patch(threshold_box)
ax.text(6, 1.25, 'Risk Thresholds:', ha='center', va='center',
        fontsize=10, fontweight='bold', color='#d68910')

thresholds = [
    ('Low (0-30)', '#2ecc71'),
    ('Medium (31-70)', '#f39c12'),
    ('High (71-100)', '#e74c3c')
]

x_start = 2.8
for i, (level, color) in enumerate(thresholds):
    x = x_start + i * 2.5
    ax.text(x, 0.75, level, ha='left', va='center',
            fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=color, 
                     alpha=0.3, edgecolor=color, linewidth=1.5))

plt.tight_layout()
output_path = output_dir / 'chapter3' / 'fig3_8_auth_risk_model.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: {output_path}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("✅ GENERATION COMPLETE!")
print("=" * 80)
print(f"\n📁 All outputs saved to: {output_dir}/")
print("\nGenerated Figures:")
print("\n  Chapter 1 (Introduction):")
print("    • fig1_1_framework_architecture.png")
print("\n  Chapter 2 (Literature Review):")
print("    • fig2_1_ml_approaches_overview.png")
print("\n  Chapter 3 (Methodology):")
print("    • fig3_1_complete_five_layer_architecture.png")
print("    • fig3_2_data_flow_diagram.png")
print("    • fig3_3_feature_extraction_pipeline.png")
print("    • fig3_4_url_feature_extraction.png")
print("    • fig3_5_graph_feature_analysis.png")
print("    • fig3_6_virustotal_integration.png")
print("    • fig3_7_random_forest_architecture.png")
print("    • fig3_8_auth_risk_model.png")
print("\n💡 Next steps:")
print("    • View the generated images in reports/chapters1-3/")
print("    • Use these figures in your research report")
print("    • Run generate_chapter4_viz.py for Chapter 4 & 5 figures")
print("=" * 80)
