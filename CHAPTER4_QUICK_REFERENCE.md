# Chapter 4: Quick Reference - Where to Get What

## 🎯 Quick Answer: Your Data is Already There!

Most of your visualizations are **already generated** in the `models/` directory!

---

## ✅ ALREADY AVAILABLE (Just Copy & Use)

### SHAP Visualizations (Chapter 5, Section 5.2)
📍 **Location**: `models/`

```
models/
├── phishing_shap_summary.png          ← Figure 5.5 (Global feature importance)
├── phishing_shap_bar_sample_0_idx_2.png      ← Figure 5.6 (Phishing example)
├── phishing_shap_bar_sample_1_idx_27.png     ← Figure 5.7 (Another example)
├── phishing_shap_bar_sample_2_idx_27629.png
├── phishing_shap_bar_sample_3_idx_45463.png
├── phishing_shap_bar_sample_4_idx_18.png
├── phishing_shap_force_sample_0_idx_2.html   ← Figure 5.8 (Force plots)
├── phishing_shap_force_sample_1_idx_27.html
├── phishing_shap_force_sample_2_idx_27629.html
├── phishing_shap_force_sample_3_idx_45463.html
└── phishing_shap_force_sample_4_idx_18.html
```

### Authentication Risk Visualizations
📍 **Location**: `models/`

```
models/
├── auth_risk_holdout_roc.png          ← Figure 5.2 (Auth Risk ROC curve)
├── auth_shap_bar_sample_0_idx_120.png ← Figure 5.10 (Auth SHAP)
├── auth_shap_bar_sample_1_idx_121.png
├── auth_shap_bar_sample_2_idx_119.png
├── auth_shap_bar_sample_3_idx_9.png
└── auth_shap_bar_sample_4_idx_112.png
```

---

## 📊 GENERATE WITH ONE COMMAND

Run this script to create all remaining visualizations:

```bash
python generate_chapter4_viz.py
```

**This creates**:
- ✅ Figure 5.1: ROC Curve
- ✅ Figure 5.15: Performance Comparison
- ✅ Figure 5.16: CV Scores Distribution
- ✅ Figure 4.1: Train/Test Split
- ✅ Figure 4.2: Preprocessing Stats
- ✅ Feature Categories Pie Chart
- ✅ Tables 1, 2, 4 (CSV format)

**Output location**: `reports/chapter4/`

---

## 📋 TABLES - Data Sources

### Table 1: Model Performance Metrics
📍 **Source**: `models/training_metrics.json` → `model_performance`

```json
{
  "auc": 0.9888,
  "precision": 0.9236,
  "recall": 0.9632,
  "f1": 0.9430
}
```

### Table 2: Cross-Validation Performance
📍 **Source**: `reports/cv_scores.json`

```json
{
  "scores": [0.9890, 0.9885, 0.9891, 0.9896, 0.9890],
  "mean": 0.9891,
  "std": 0.0003
}
```

### Table 4: Dataset Statistics
📍 **Source**: `models/training_metrics.json` → `data_stats`

- Total records (raw): 381,450
- Deduplicated records: 159,603
- Final features: 19
- Benign samples: 105,962
- Phishing samples: 53,641

### Table 5: VirusTotal Threat Distribution
📍 **Source**: `data/processed/url_features_vt.csv`

**To calculate**:
```python
import pandas as pd
df = pd.read_csv('data/processed/url_features_vt.csv')
df['vt_threat_score'].value_counts()
```

### Table 6: Feature Categories
📍 **Source**: `models/feature_names.json` + manual categorization

**19 Features**:
- URL Structure (7): `has_at`, `has_ip`, `num_dots`, `num_hyphens`, `num_qm`, `num_underscores`, `path_length`
- Domain Analysis (2): `sender_domain_mismatch`, `subdomain_count`
- Graph Features (6): `domain_degree_agg`, `sender_degree_agg`, `domain_degree_weighted`, `domain_clustering_agg`, `domain_betweenness_approx`, `sender_betweenness_approx`
- Network Features (1): `url_degree_simple`
- Threat Intelligence (3): `vt_malicious_votes`, `vt_suspicious_votes`, `vt_threat_score`

### Table 7: VT Feature Correlation
📍 **Source**: Calculate from `data/processed/url_features_vt.csv`

```python
df = pd.read_csv('data/processed/url_features_vt.csv')
correlations = df[['vt_threat_score', 'vt_malicious_votes', 
                    'vt_suspicious_votes', 'label']].corr()['label']
```

**Expected values**:
- `vt_threat_score`: 0.0835
- `vt_malicious_votes`: 0.0631
- `vt_suspicious_votes`: 0.0396

### Table 10: Top High-Risk Domains
📍 **Source**: Query `data/processed/url_features_vt.csv`

```python
df = pd.read_csv('data/processed/url_features_vt.csv')
top_vt = df.nlargest(10, 'vt_malicious_votes')[
    ['url', 'vt_malicious_votes', 'vt_suspicious_votes', 
     'vt_threat_score', 'label']
]
```

---

## 🔍 DETAILED FIGURES - Where to Get Data

### Chapter 4: Implementation

#### Figure 4.1: Training and Validation Workflow
**Source**: `models/training_metrics.json`
```python
import json
with open('models/training_metrics.json') as f:
    m = json.load(f)

# Show workflow steps:
print(f"Train shape: {m['train_test_split']['train_shape']}")
print(f"Test shape: {m['train_test_split']['test_shape']}")
print(f"Features: {m['features']['feature_names']}")
```

#### Figure 4.2: Data Preprocessing Pipeline
**Sources**: 
- `models/training_metrics.json` → `data_stats`
- `src/train_model.py` (code walkthrough)

**Pipeline stages**:
1. Raw: 381,450 rows, 27 features
2. Deduplicated: 159,603 rows
3. After leakage removal: 19 features
4. Train/test split: 70/30

#### Figure 4.3: SHAP Value Calculation Process
**Source**: `src/compute_shap.py` + `models/shap_values.npz`

```python
import numpy as np
shap_data = np.load('models/shap_values.npz')
shap_values = shap_data['shap_values']
expected_value = shap_data['expected_value']
```

#### Figure 4.4: Feature Attribution Methodology
**Source**: `models/phishing_shap_sample_*_annot.csv`

```python
import pandas as pd
annot = pd.read_csv('models/phishing_shap_sample_0_idx_2_annot.csv')
# Shows feature contributions for a specific prediction
```

---

### Chapter 5: Results and Analysis

#### Figure 5.1: ROC Curve
**Source**: `models/training_metrics.json` → `roc_curve`
**Script**: `generate_chapter4_viz.py` (auto-generates)

#### Figure 5.2: Auth Risk ROC Curve
**Source**: `models/auth_risk_holdout_roc.png` ✅ **Already exists!**

#### Figure 5.3: Confusion Matrix
**Generate from**: Test predictions

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import pickle

with open('models/phishing_rf_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Need to load test data and make predictions
# Then: cm = confusion_matrix(y_test, y_pred)
```

#### Figure 5.5: SHAP Summary Plot
**Source**: `models/phishing_shap_summary.png` ✅ **Already exists!**

#### Figure 5.6-5.7: SHAP Bar Plots
**Source**: `models/phishing_shap_bar_sample_*.png` ✅ **Already exists!**

Pick best examples:
- High-risk phishing: `phishing_shap_bar_sample_0_idx_2.png`
- Another example: `phishing_shap_bar_sample_3_idx_45463.png`

#### Figure 5.8: SHAP Force Plot
**Source**: `models/phishing_shap_force_sample_*.html` ✅ **Already exists!**

Open in browser and screenshot, or use PNG version if available

#### Figure 5.10: Auth Risk SHAP
**Source**: `models/auth_shap_bar_sample_*.png` ✅ **Already exists!**

#### Figure 5.11: Global Feature Importance
**Generate from**: Model's feature importances

```python
import pickle
import json
with open('models/phishing_rf_model.pkl', 'rb') as f:
    pipeline = pickle.load(f)

rf = pipeline.named_steps['classifier']
importances = rf.feature_importances_
features = json.load(open('models/feature_names.json'))

# Create bar plot
```

#### Figure 5.15: Performance Comparison
**Source**: `models/training_metrics.json` → `model_performance`
**Script**: `generate_chapter4_viz.py` (auto-generates)

#### Figure 5.16: CV Scores Distribution
**Source**: `reports/cv_scores.json`
**Script**: `generate_chapter4_viz.py` (auto-generates)

---

## 🚀 Quick Start Workflow

### Step 1: Check what's already available
```bash
# View existing SHAP plots
ls -lh models/*.png

# View existing data files
ls -lh models/*.json
ls -lh reports/*.json
```

### Step 2: Generate missing visualizations
```bash
python generate_chapter4_viz.py
```

### Step 3: View outputs
```bash
# View generated figures
ls -lh reports/chapter4/figures/

# View generated tables
ls -lh reports/chapter4/tables/
```

### Step 4: For custom analysis, use notebooks
```bash
# Open Jupyter
jupyter notebook

# Navigate to:
# - notebooks/04-model-training.ipynb
# - notebooks/05-auth-risk-model.ipynb
```

---

## 📖 Data File Locations Summary

```
phishing-risk-detection-project/
│
├── data/
│   ├── raw/
│   │   └── dataset_full.csv (381,450 records - original)
│   └── processed/
│       ├── url_features_vt.csv (159,603 records - deduplicated)
│       └── phishing_graph_features_vt.csv (graph features)
│
├── models/
│   ├── training_metrics.json ⭐ (all training stats)
│   ├── feature_names.json (19 feature names)
│   ├── phishing_rf_model.pkl (trained model)
│   ├── shap_values.npz (SHAP explanations)
│   ├── phishing_shap_summary.png ✅ (ready to use)
│   ├── phishing_shap_bar_sample_*.png ✅ (ready to use)
│   ├── auth_risk_holdout_roc.png ✅ (ready to use)
│   └── auth_shap_bar_sample_*.png ✅ (ready to use)
│
├── reports/
│   ├── cv_scores.json ⭐ (cross-validation results)
│   └── chapter4/ (generated by script)
│       ├── figures/
│       └── tables/
│
├── notebooks/
│   ├── 01-data-exploration.ipynb
│   ├── 02-feature-engineering.ipynb
│   ├── 03-graph-visuals.ipynb
│   ├── 04-model-training.ipynb ⭐ (main training)
│   └── 05-auth-risk-model.ipynb
│
└── src/
    ├── train_model.py (training pipeline)
    ├── compute_shap.py (SHAP generation)
    ├── extract_features.py (feature engineering)
    └── evaluate_models.py (metrics calculation)
```

---

## 💡 Pro Tips

1. **Most visualizations exist**: Check `models/` first before generating
2. **Use the script**: `generate_chapter4_viz.py` creates what's missing
3. **For custom plots**: Modify notebooks in `notebooks/`
4. **All metrics in JSON**: `models/training_metrics.json` has everything
5. **SHAP plots ready**: Just copy PNG files from `models/`

---

## ❓ Common Questions

**Q: Where is the confusion matrix?**
A: Generate using test predictions from the model. Not pre-saved.

**Q: Where are precision-recall curves?**
A: Need to generate from `models/training_metrics.json` ROC data or re-run evaluation.

**Q: Can I regenerate everything?**
A: Yes! Run `notebooks/04-model-training.ipynb` from scratch.

**Q: Where's the raw data?**
A: `data/raw/dataset_full.csv` (381,450 records before deduplication)

**Q: Where's the final processed data?**
A: `data/processed/url_features_vt.csv` (159,603 deduplicated records)

---

## 📚 For More Details

See comprehensive guide: `docs/CHAPTER4_DATA_SOURCE_GUIDE.md`
