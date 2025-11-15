# Chapter 4: Data Source Guide for Visualizations and Demonstrations

This guide maps each figure and table in Chapter 4 to its data source location, showing you exactly where to get the data for creating visualizations and demonstrations.

---

## Quick Reference: Key Data Locations

### Primary Data Sources
- **Raw Dataset**: `/data/raw/dataset_full.csv` (381,450 records)
- **Processed Features**: `/data/processed/url_features_vt.csv` (159,603 deduplicated records)
- **Graph Features**: `/data/processed/phishing_graph_features_vt.csv`
- **Training Metrics**: `/models/training_metrics.json`
- **CV Scores**: `/reports/cv_scores.json`
- **Model Artifacts**: `/models/phishing_rf_model.pkl`
- **SHAP Values**: `/models/shap_values.npz`
- **SHAP Visualizations**: `/models/phishing_shap_*.png`

### Notebooks (Analysis & Generation)
- **Data Exploration**: `notebooks/01-data-exploration.ipynb`
- **Feature Engineering**: `notebooks/02-feature-engineering.ipynb`
- **Graph Visualizations**: `notebooks/03-graph-visuals.ipynb`
- **Model Training**: `notebooks/04-model-training.ipynb`
- **Auth Risk Model**: `notebooks/05-auth-risk-model.ipynb`

### Source Code (Pipeline Scripts)
- **Feature Extraction**: `src/extract_features.py`
- **Graph Features**: `src/compute_graph_features.py`
- **VirusTotal Integration**: `src/enrich_virustotal.py`
- **Model Training**: `src/train_model.py`
- **SHAP Computation**: `src/compute_shap.py`
- **Model Evaluation**: `src/evaluate_models.py`

---

## Chapter 4: Implementation - Detailed Data Sources

### Section 4.1: Model Development

#### **Figure 4.1: Training and Validation Workflow**
**What to show**: The complete pipeline from raw data to trained model

**Data Sources**:
- Pipeline structure: See `src/train_model.py` (lines showing data loading, preprocessing, training)
- Workflow steps: `notebooks/04-model-training.ipynb` (sequential cells)
- Training configuration: `models/training_metrics.json` → `"train_test_split"` section

**How to create**:
```python
# Extract from training_metrics.json
import json
with open('models/training_metrics.json') as f:
    metrics = json.load(f)
    
# Show:
# 1. Initial data shape: metrics['data_stats']['initial_shape']
# 2. Train/test split: metrics['train_test_split']
# 3. Label distribution: metrics['train_test_split']['train_label_dist']
```

**Key Information**:
- Initial dataset: 159,603 samples, 26 features
- After leakage removal: 159,603 samples, 19 features
- Train/Test split: 70/30 (111,722 / 47,881)
- GroupKFold validation: 5 folds

---

#### **Figure 4.2: Data Preprocessing Pipeline**
**What to show**: Steps from raw data to ML-ready features

**Data Sources**:
- Raw data stats: `models/training_metrics.json` → `"data_stats"`
- Preprocessing steps: `src/train_model.py` (preprocessing section)
- Feature engineering: `notebooks/02-feature-engineering.ipynb`

**Pipeline Steps to Visualize**:
1. **Data Loading**: `data/raw/dataset_full.csv` (381,450 records)
2. **Deduplication**: Removed 221,847 duplicates → 159,603 unique URLs
3. **Feature Engineering**: 
   - URL features: `src/extract_features.py`
   - Graph features: `src/compute_graph_features.py`
   - VT enrichment: `src/enrich_virustotal.py`
4. **Leakage Removal**: Dropped `url_length` (see `models/training_metrics.json` → `"dropped_leakage_cols"`)
5. **Final Features**: 19 features (see `models/feature_names.json`)

**Code to Extract**:
```python
# Get feature names
import json
with open('models/feature_names.json') as f:
    features = json.load(f)
print(f"Final features ({len(features)}): {features}")
```

---

### Section 4.2: Explainability Integration

#### **Figure 4.3: SHAP Value Calculation Process**
**What to show**: How SHAP values are computed for model predictions

**Data Sources**:
- SHAP computation code: `src/compute_shap.py`
- Pre-computed SHAP values: `models/shap_values.npz`
- Sample explanations: `notebooks/04-model-training.ipynb` (SHAP section)

**How to Access**:
```python
import numpy as np
import shap

# Load SHAP values
shap_data = np.load('models/shap_values.npz')
shap_values = shap_data['shap_values']
base_value = shap_data['expected_value']

# Load model and test data from training_metrics
# Then create SHAP explainer
explainer = shap.TreeExplainer(model)
```

**Key Concepts to Illustrate**:
1. Base value (expected model output): ~0.336
2. Feature contributions (positive/negative SHAP values)
3. Final prediction = base_value + sum(SHAP values)

---

#### **Figure 4.4: Feature Attribution Methodology**
**What to show**: How features contribute to individual predictions

**Data Sources**:
- SHAP force plots: `models/phishing_shap_force_sample_*.html`
- SHAP bar plots: `models/phishing_shap_bar_sample_*.png`
- Annotation CSVs: `models/phishing_shap_sample_*_annot.csv`

**Available Examples**:
- **Phishing samples** (5 examples):
  - `phishing_shap_bar_sample_0_idx_2.png`
  - `phishing_shap_bar_sample_1_idx_27.png`
  - `phishing_shap_bar_sample_2_idx_27629.png`
  - `phishing_shap_bar_sample_3_idx_45463.png`
  - `phishing_shap_bar_sample_4_idx_18.png`

**How to Use**:
```python
# Load annotation data
import pandas as pd
annot = pd.read_csv('models/phishing_shap_sample_0_idx_2_annot.csv')
# Shows: feature_name, feature_value, shap_value, contribution_direction
```

---

## Chapter 5: Results and Analysis - Data Sources

### Section 5.1: Model Performance

#### **Figure 5.1: ROC Curve for Phishing Classifier**
**Data Source**: `models/training_metrics.json` → `"roc_curve"` section

**Metrics**:
- AUC: 0.9888
- FPR values: `metrics['roc_curve']['fpr']`
- TPR values: `metrics['roc_curve']['tpr']`

**How to Create**:
```python
import json
import matplotlib.pyplot as plt
from sklearn.metrics import auc

with open('models/training_metrics.json') as f:
    metrics = json.load(f)

fpr = metrics['roc_curve']['fpr']
tpr = metrics['roc_curve']['tpr']
roc_auc = metrics['model_performance']['auc']

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve - Phishing Detection Model')
plt.legend()
plt.savefig('reports/roc_curve.png', dpi=300, bbox_inches='tight')
```

---

#### **Figure 5.2: Authentication Risk Model ROC Curve**
**Data Source**: `models/auth_risk_holdout_roc.png` (already generated)

**Location**: `/models/auth_risk_holdout_roc.png`

**Associated Notebook**: `notebooks/05-auth-risk-model.ipynb`

---

#### **Figure 5.3: Confusion Matrix for Test Set**
**Data Source**: Calculate from test predictions

**How to Generate**:
```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import pickle

# Load model and test data
with open('models/phishing_rf_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Need test data from training pipeline or notebook
# y_test and X_test from split in training_metrics.json

y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, 
                               display_labels=['Benign', 'Phishing'])
disp.plot()
plt.savefig('reports/confusion_matrix.png', dpi=300, bbox_inches='tight')
```

**Expected Results** (from metrics):
- Precision: 0.9236 → Few false positives
- Recall: 0.9632 → Catches 96% of phishing

---

#### **Figure 5.4: Precision-Recall Curve**
**Data Source**: Generate from model predictions

**Alternative**: Use `notebooks/04-model-training.ipynb` to regenerate

---

### Section 5.2: SHAP Explanations

#### **Figure 5.5: SHAP Summary Plot**
**Data Source**: `models/phishing_shap_summary.png` (already generated!)

**Location**: `/models/phishing_shap_summary.png`

**Shows**: Global feature importance across all predictions

---

#### **Figure 5.6-5.7: SHAP Bar Plots (Phishing vs Benign)**
**Data Sources**:

**High-Risk (Phishing) Examples**:
- `models/phishing_shap_bar_sample_0_idx_2.png`
- `models/phishing_shap_bar_sample_1_idx_27.png`
- `models/phishing_shap_bar_sample_2_idx_27629.png`
- `models/phishing_shap_bar_sample_3_idx_45463.png`
- `models/phishing_shap_bar_sample_4_idx_18.png`

**How to Select**:
- Pick 1-2 high-risk samples (e.g., sample_0 and sample_3)
- Pick 1-2 low-risk samples (need to generate from benign predictions)

---

#### **Figure 5.8: SHAP Force Plot**
**Data Sources**:
- `models/phishing_shap_force_sample_0_idx_2.html` (interactive)
- `models/phishing_shap_force_sample_1_idx_27.html`
- `models/phishing_shap_force_sample_2_idx_27629.html`
- `models/phishing_shap_force_sample_3_idx_45463.html`
- `models/phishing_shap_force_sample_4_idx_18.html`

**Note**: These are HTML files - open in browser or screenshot for report

---

#### **Figure 5.10: Authentication Risk SHAP**
**Data Sources**:
- `models/auth_shap_bar_sample_0_idx_120.png`
- `models/auth_shap_bar_sample_1_idx_121.png`
- `models/auth_shap_bar_sample_2_idx_119.png`
- `models/auth_shap_bar_sample_3_idx_9.png`
- `models/auth_shap_bar_sample_4_idx_112.png`

**Associated Model**: `models/auth_risk_model_holdout.pkl`

---

### Section 5.3: Feature Importance Analysis

#### **Figure 5.11: Global Feature Importance Rankings**
**Data Source**: Extract from Random Forest model

**How to Generate**:
```python
import pickle
import pandas as pd
import matplotlib.pyplot as plt

# Load model
with open('models/phishing_rf_model.pkl', 'rb') as f:
    pipeline = pickle.load(f)

# Get Random Forest from pipeline
rf_model = pipeline.named_steps['classifier']
feature_names = json.load(open('models/feature_names.json'))

# Get feature importances
importances = rf_model.feature_importances_
feature_imp = pd.DataFrame({
    'feature': feature_names,
    'importance': importances
}).sort_values('importance', ascending=False)

# Plot
plt.figure(figsize=(10, 6))
plt.barh(feature_imp['feature'], feature_imp['importance'])
plt.xlabel('Feature Importance')
plt.title('Global Feature Importance - Random Forest')
plt.tight_layout()
plt.savefig('reports/feature_importance.png', dpi=300, bbox_inches='tight')
```

---

#### **Figure 5.12: VirusTotal Score Impact**
**Data Sources**:
- Feature data: `data/processed/url_features_vt.csv`
- VT columns: `vt_malicious_votes`, `vt_suspicious_votes`, `vt_threat_score`

**Analysis Code**:
```python
import pandas as pd

# Load processed data
df = pd.read_csv('data/processed/url_features_vt.csv')

# Analyze VT score distribution by label
vt_impact = df.groupby('label')['vt_threat_score'].value_counts()

# Correlation analysis
correlations = df[['vt_malicious_votes', 'vt_suspicious_votes', 
                    'vt_threat_score', 'label']].corr()['label']
```

**Key Stats** (from your tables):
- VT malicious correlation: 0.0631
- VT suspicious correlation: 0.0396
- VT threat score correlation: 0.0835

---

#### **Figure 5.13: Graph Features Contribution**
**Data Source**: SHAP values for graph features

**Graph Features** (6 total):
- `domain_degree_agg`
- `sender_degree_agg`
- `domain_degree_weighted`
- `domain_clustering_agg`
- `domain_betweenness_approx`
- `sender_betweenness_approx`

**How to Analyze**:
```python
# Load SHAP values
shap_data = np.load('models/shap_values.npz')
shap_values = shap_data['shap_values']

# Get indices of graph features
graph_features = ['domain_degree_agg', 'sender_degree_agg', 
                  'domain_degree_weighted', 'domain_clustering_agg', 
                  'domain_betweenness_approx', 'sender_betweenness_approx']

# Calculate mean absolute SHAP values for graph features
feature_names = json.load(open('models/feature_names.json'))
graph_indices = [feature_names.index(f) for f in graph_features]
graph_shap = np.abs(shap_values[:, graph_indices]).mean(axis=0)
```

---

### Section 5.4: Comparative Analysis

#### **Figure 5.16: Cross-Validation Scores Distribution**
**Data Source**: `reports/cv_scores.json`

**Available Data**:
```json
{
  "scores": [0.9890, 0.9885, 0.9891, 0.9896, 0.9890],
  "mean": 0.9891,
  "std": 0.0003
}
```

**How to Visualize**:
```python
import json
import matplotlib.pyplot as plt

with open('reports/cv_scores.json') as f:
    cv_data = json.load(f)

scores = cv_data['scores']
folds = list(range(1, len(scores) + 1))

plt.figure(figsize=(8, 5))
plt.bar(folds, scores, alpha=0.7, color='steelblue')
plt.axhline(cv_data['mean'], color='red', linestyle='--', 
            label=f"Mean = {cv_data['mean']:.4f}")
plt.xlabel('Fold Number')
plt.ylabel('AUC-ROC Score')
plt.title('Cross-Validation Performance (5-Fold GroupKFold)')
plt.ylim([0.988, 0.990])
plt.legend()
plt.savefig('reports/cv_scores_distribution.png', dpi=300, bbox_inches='tight')
```

---

## Tables - Data Sources

### **Table 1: Model Performance Metrics**
**Data Source**: `models/training_metrics.json` → `"model_performance"`

```python
metrics = {
    'AUC-ROC': 0.9888,
    'Precision': 0.9236,
    'Recall': 0.9632,
    'F1 Score': 0.9430
}
```

---

### **Table 2: Cross-Validation Performance**
**Data Source**: `reports/cv_scores.json`

Already formatted in `list_of_tables.md`

---

### **Table 3: VirusTotal Feature Columns**
**Data Source**: Documentation + `data/processed/url_features_vt.csv` column names

**Verify**:
```python
df = pd.read_csv('data/processed/url_features_vt.csv')
vt_cols = [col for col in df.columns if col.startswith('vt_')]
print(vt_cols)
# ['vt_malicious_votes', 'vt_suspicious_votes', 'vt_threat_score']
```

---

### **Table 4: Dataset Statistics**
**Data Source**: `models/training_metrics.json` → `"data_stats"`

```python
stats = {
    'Total records (raw)': 381450,  # Original dataset
    'Duplicate URLs detected': 221847,  # Calculated
    'Final records (deduplicated)': 159603,
    'Final features': 19,
    'Benign samples': 105962,
    'Phishing samples': 53641,
    'Class ratio': 33.6%
}
```

---

### **Table 5: VirusTotal Threat Distribution**
**Data Source**: Analyze `data/processed/url_features_vt.csv`

```python
df = pd.read_csv('data/processed/url_features_vt.csv')

# Count threat classifications
vt_dist = df['vt_threat_score'].value_counts()
benign = (df['vt_threat_score'] == 0).sum()
suspicious = (df['vt_threat_score'] == 1).sum()
malicious = (df['vt_threat_score'] == 2).sum()
```

---

### **Table 6: Feature Categories**
**Data Source**: `models/feature_names.json` + categorization

```python
feature_categories = {
    'URL Structure': ['has_at', 'has_ip', 'num_dots', 'num_hyphens', 
                      'num_qm', 'num_underscores', 'path_length'],
    'Domain Analysis': ['sender_domain_mismatch', 'subdomain_count'],
    'Graph Features': ['domain_degree_agg', 'sender_degree_agg', 
                       'domain_degree_weighted', 'domain_clustering_agg', 
                       'domain_betweenness_approx', 'sender_betweenness_approx'],
    'Network Features': ['url_degree_simple'],
    'Threat Intelligence': ['vt_malicious_votes', 'vt_suspicious_votes', 
                            'vt_threat_score']
}
```

---

### **Table 7: VT Feature Correlation**
**Data Source**: Calculate from `data/processed/url_features_vt.csv`

```python
df = pd.read_csv('data/processed/url_features_vt.csv')
correlations = df[['vt_threat_score', 'vt_malicious_votes', 
                    'vt_suspicious_votes', 'label']].corr()['label']
```

---

### **Table 10: Top High-Risk Domains**
**Data Source**: Query `data/processed/url_features_vt.csv`

```python
df = pd.read_csv('data/processed/url_features_vt.csv')

# Get top domains by VT malicious votes
top_vt = df.nlargest(10, 'vt_malicious_votes')[
    ['url', 'vt_malicious_votes', 'vt_suspicious_votes', 
     'vt_threat_score', 'label']
]
```

---

## Dashboard Visualizations (Chapter 6)

### **Figure 6.1-6.5: Dashboard Screenshots**
**Data Source**: Run the dashboard and capture screenshots

**How to Run**:
```bash
streamlit run dashboard.py
```

**Tabs to Screenshot**:
1. **Model Training Tab**: Shows performance metrics from `models/training_metrics.json`
2. **Phishing SHAP Tab**: Displays SHAP visualizations from `models/`
3. **Authentication Risk Tab**: Shows auth risk predictions
4. **Framework Tab**: Shows framework architecture diagram

---

## Quick Start: Generate All Chapter 4 Visualizations

### Step 1: Verify Data Availability
```bash
# Check key files exist
ls -lh models/training_metrics.json
ls -lh reports/cv_scores.json
ls -lh models/phishing_shap_summary.png
ls -lh data/processed/url_features_vt.csv
```

### Step 2: Create Visualization Script
```python
# create_chapter4_visualizations.py
import json
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Load all data
with open('models/training_metrics.json') as f:
    metrics = json.load(f)

with open('reports/cv_scores.json') as f:
    cv_data = json.load(f)

with open('models/feature_names.json') as f:
    feature_names = json.load(f)

# 1. ROC Curve (Figure 5.1)
fpr = metrics['roc_curve']['fpr']
tpr = metrics['roc_curve']['tpr']
roc_auc = metrics['model_performance']['auc']

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc:.4f})', linewidth=2)
plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
plt.xlabel('False Positive Rate', fontsize=12)
plt.ylabel('True Positive Rate', fontsize=12)
plt.title('ROC Curve - Phishing Detection Model', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.savefig('reports/figure5_1_roc_curve.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. CV Scores Distribution (Figure 5.16)
scores = cv_data['scores']
folds = list(range(1, len(scores) + 1))

plt.figure(figsize=(8, 5))
bars = plt.bar(folds, scores, alpha=0.7, color='steelblue', edgecolor='navy')
plt.axhline(cv_data['mean'], color='red', linestyle='--', linewidth=2,
            label=f"Mean = {cv_data['mean']:.4f} ± {cv_data['std']:.4f}")
plt.xlabel('Fold Number', fontsize=12)
plt.ylabel('AUC-ROC Score', fontsize=12)
plt.title('Cross-Validation Performance (5-Fold GroupKFold)', fontsize=14, fontweight='bold')
plt.ylim([0.988, 0.990])
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3, axis='y')
plt.savefig('reports/figure5_16_cv_scores.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Performance Metrics Comparison (Figure 5.15)
perf = metrics['model_performance']
metric_names = ['AUC-ROC', 'Precision', 'Recall', 'F1 Score']
metric_values = [perf['auc'], perf['precision'], perf['recall'], perf['f1']]

plt.figure(figsize=(10, 6))
bars = plt.bar(metric_names, metric_values, color=['#2ecc71', '#3498db', '#e74c3c', '#f39c12'],
               alpha=0.8, edgecolor='black')
plt.ylabel('Score', fontsize=12)
plt.title('Model Performance Across Metrics', fontsize=14, fontweight='bold')
plt.ylim([0.9, 1.0])
plt.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bar, value in zip(bars, metric_values):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{value:.4f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.savefig('reports/figure5_15_performance_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Feature Categories Summary (Figure based on Table 6)
categories = {
    'URL Structure': 7,
    'Domain Analysis': 2,
    'Graph Features': 6,
    'Network Features': 1,
    'Threat Intel (VT)': 3
}

plt.figure(figsize=(10, 6))
plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%',
        startangle=90, colors=sns.color_palette("pastel"))
plt.title('Feature Categories Distribution (19 Total Features)', 
          fontsize=14, fontweight='bold')
plt.savefig('reports/feature_categories_pie.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ All Chapter 4 visualizations generated successfully!")
print(f"  - ROC Curve: reports/figure5_1_roc_curve.png")
print(f"  - CV Scores: reports/figure5_16_cv_scores.png")
print(f"  - Performance Comparison: reports/figure5_15_performance_comparison.png")
print(f"  - Feature Categories: reports/feature_categories_pie.png")
```

### Step 3: Run Visualization Script
```bash
python create_chapter4_visualizations.py
```

---

## Summary Checklist for Chapter 4

### ✅ Already Generated (Ready to Use)
- [x] SHAP summary plot: `models/phishing_shap_summary.png`
- [x] SHAP bar plots (5 phishing samples): `models/phishing_shap_bar_sample_*.png`
- [x] SHAP force plots (5 samples): `models/phishing_shap_force_sample_*.html`
- [x] Auth risk ROC: `models/auth_risk_holdout_roc.png`
- [x] Auth SHAP examples: `models/auth_shap_bar_sample_*.png`
- [x] Training metrics: `models/training_metrics.json`
- [x] CV scores: `reports/cv_scores.json`

### 📊 Need to Generate
- [ ] ROC curve plot (use script above)
- [ ] Confusion matrix (need test predictions)
- [ ] Precision-recall curve
- [ ] Feature importance bar chart (use script above)
- [ ] CV scores distribution (use script above)
- [ ] Performance metrics comparison (use script above)

### 📝 Tables (Data Ready in JSON/CSV)
- [x] Table 1: Performance metrics → `models/training_metrics.json`
- [x] Table 2: CV scores → `reports/cv_scores.json`
- [x] Table 4: Dataset stats → `models/training_metrics.json`
- [ ] Table 5: VT distribution → Calculate from `data/processed/url_features_vt.csv`
- [ ] Table 7: VT correlations → Calculate from processed data
- [ ] Table 10: Top VT domains → Query processed data

---

## File Organization Recommendation

Create a `reports/chapter4/` directory structure:

```
reports/chapter4/
├── figures/
│   ├── implementation/
│   │   ├── fig4_1_training_workflow.png
│   │   └── fig4_2_preprocessing_pipeline.png
│   └── results/
│       ├── fig5_1_roc_curve.png
│       ├── fig5_2_auth_roc.png
│       ├── fig5_5_shap_summary.png
│       ├── fig5_6_shap_phishing_sample.png
│       └── fig5_16_cv_scores.png
├── tables/
│   ├── table1_performance_metrics.csv
│   ├── table2_cv_scores.csv
│   └── table4_dataset_stats.csv
└── data_extracts/
    ├── model_metrics.json
    ├── feature_importance.csv
    └── vt_analysis.csv
```

---

## Need Help?

**For data questions**: Check `models/training_metrics.json` first
**For visualizations**: Use existing `.png` files in `models/`
**For custom plots**: Run notebooks in `notebooks/` directory
**For pipeline understanding**: Read source code in `src/`

**Key Contact Points**:
- Training pipeline: `src/train_model.py`
- SHAP generation: `src/compute_shap.py`
- Dashboard: `dashboard.py`
- Notebooks: `notebooks/04-model-training.ipynb`
