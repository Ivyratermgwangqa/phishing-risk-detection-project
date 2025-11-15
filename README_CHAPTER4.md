# Chapter 4 Data Source Guide - Quick Start

## 📖 What This Is

This guide tells you **exactly where to get data** for every figure and table in Chapter 4 (Implementation) and Chapter 5 (Results) of your research report.

---

## 🎯 TL;DR - Three Steps

1. **Check existing files**: Most visualizations are already generated!
2. **Run auto-generation script**: Creates missing charts and tables
3. **Read detailed guide**: For custom analysis and deep dives

---

## ✅ Step 1: What's Already Available

You have **22 ready-to-use visualizations** in your `models/` directory:

```bash
# List all existing visualizations
ls -lh models/*.png models/*.html
```

**SHAP Visualizations (Ready)**:
- `phishing_shap_summary.png` → Global feature importance (Figure 5.5)
- `phishing_shap_bar_sample_*.png` → 5 phishing examples (Figures 5.6-5.7)
- `phishing_shap_force_sample_*.html` → 5 interactive force plots (Figure 5.8)
- `auth_risk_holdout_roc.png` → Auth risk ROC curve (Figure 5.2)
- `auth_shap_bar_sample_*.png` → 5 auth risk examples (Figure 5.10)

**Data Files (Ready)**:
- `models/training_metrics.json` → All training statistics
- `reports/cv_scores.json` → Cross-validation results
- `models/feature_names.json` → List of 19 features

---

## 📊 Step 2: Generate Missing Visualizations

Run this script to auto-generate 6 figures and 3 tables:

```bash
python generate_chapter4_viz.py
```

**Creates**:
- Figure 5.1: ROC Curve (AUC = 0.9888)
- Figure 5.15: Performance Metrics Comparison
- Figure 5.16: Cross-Validation Scores
- Figure 4.1: Train/Test Split Distribution
- Figure 4.2: Preprocessing Pipeline Stats
- Bonus: Feature Categories Pie Chart
- Table 1: Performance Metrics (CSV)
- Table 2: CV Scores (CSV)
- Table 4: Dataset Statistics (CSV)

**Output location**: `reports/chapter4/figures/` and `reports/chapter4/tables/`

---

## 📚 Step 3: Detailed Documentation

Three comprehensive guides are available:

### 1. Quick Reference (This File)
**File**: `CHAPTER4_QUICK_REFERENCE.md`
- Quick lookup for each figure/table
- Code snippets for data extraction
- Status of what's ready vs. what needs generation

### 2. Visual Mapping
**File**: `FIGURE_TABLE_MAPPING.txt`
- ASCII art boxes showing exact data sources
- Command-line friendly format
- Status summary at the end

### 3. Complete Guide
**File**: `docs/CHAPTER4_DATA_SOURCE_GUIDE.md`
- Detailed instructions for every visualization
- Complete code examples
- Pipeline explanations
- Troubleshooting tips

---

## 🗂️ Key Data Locations

### Primary Sources
```
data/
├── raw/dataset_full.csv                    (381,450 original records)
└── processed/url_features_vt.csv           (159,603 deduplicated)

models/
├── training_metrics.json                   ⭐ All metrics
├── feature_names.json                      (19 features)
├── phishing_rf_model.pkl                   (trained model)
├── shap_values.npz                         (SHAP data)
├── phishing_shap_summary.png              ✅ Ready
├── phishing_shap_bar_sample_*.png         ✅ Ready (5 samples)
├── auth_risk_holdout_roc.png              ✅ Ready
└── auth_shap_bar_sample_*.png             ✅ Ready (5 samples)

reports/
└── cv_scores.json                          ⭐ CV results

notebooks/
├── 04-model-training.ipynb                 (main training)
└── 05-auth-risk-model.ipynb                (auth risk)
```

---

## 📋 Common Data Queries

### Get Model Performance Metrics
```python
import json
with open('models/training_metrics.json') as f:
    metrics = json.load(f)

print(f"AUC: {metrics['model_performance']['auc']:.4f}")
print(f"Precision: {metrics['model_performance']['precision']:.4f}")
print(f"Recall: {metrics['model_performance']['recall']:.4f}")
print(f"F1: {metrics['model_performance']['f1']:.4f}")
```

### Get Cross-Validation Scores
```python
import json
with open('reports/cv_scores.json') as f:
    cv = json.load(f)

print(f"Scores: {cv['scores']}")
print(f"Mean: {cv['mean']:.4f} ± {cv['std']:.4f}")
```

### Get Feature Names
```python
import json
with open('models/feature_names.json') as f:
    features = json.load(f)

print(f"Total features: {len(features)}")
print(features)
```

### Load SHAP Values
```python
import numpy as np
shap_data = np.load('models/shap_values.npz')
shap_values = shap_data['shap_values']
expected_value = shap_data['expected_value']

print(f"SHAP values shape: {shap_values.shape}")
print(f"Base value: {expected_value}")
```

---

## 🎨 Figure-to-File Mapping (Quick Reference)

| Figure | File Location | Status |
|--------|---------------|--------|
| Fig 4.1 | `reports/chapter4/figures/fig4_1_train_test_split.png` | Auto-gen |
| Fig 4.2 | `reports/chapter4/figures/fig4_2_preprocessing_stats.png` | Auto-gen |
| Fig 5.1 | `reports/chapter4/figures/fig5_1_roc_curve.png` | Auto-gen |
| Fig 5.2 | `models/auth_risk_holdout_roc.png` | ✅ Ready |
| Fig 5.5 | `models/phishing_shap_summary.png` | ✅ Ready |
| Fig 5.6 | `models/phishing_shap_bar_sample_0_idx_2.png` | ✅ Ready |
| Fig 5.8 | `models/phishing_shap_force_sample_0_idx_2.html` | ✅ Ready |
| Fig 5.10 | `models/auth_shap_bar_sample_0_idx_120.png` | ✅ Ready |
| Fig 5.15 | `reports/chapter4/figures/fig5_15_performance.png` | Auto-gen |
| Fig 5.16 | `reports/chapter4/figures/fig5_16_cv_scores.png` | Auto-gen |

---

## 📊 Table-to-Source Mapping (Quick Reference)

| Table | Data Source | Status |
|-------|-------------|--------|
| Table 1 | `models/training_metrics.json` → `model_performance` | Auto-gen |
| Table 2 | `reports/cv_scores.json` | Auto-gen |
| Table 4 | `models/training_metrics.json` → `data_stats` | Auto-gen |
| Table 5 | Calculate from `data/processed/url_features_vt.csv` | Manual |
| Table 6 | `models/feature_names.json` + categorization | Documented |
| Table 7 | Calculate correlations from processed CSV | Manual |
| Table 10 | Query top VT domains from processed CSV | Manual |

---

## 🔍 For Manual Tables/Figures

Some items need custom generation. Here's how:

### Table 5: VT Threat Distribution
```python
import pandas as pd
df = pd.read_csv('data/processed/url_features_vt.csv')
vt_dist = df['vt_threat_score'].value_counts().sort_index()
print(vt_dist)
```

### Table 7: VT Feature Correlations
```python
import pandas as pd
df = pd.read_csv('data/processed/url_features_vt.csv')
corr = df[['vt_threat_score', 'vt_malicious_votes', 
           'vt_suspicious_votes', 'label']].corr()['label']
print(corr)
```

### Table 10: Top VT Domains
```python
import pandas as pd
df = pd.read_csv('data/processed/url_features_vt.csv')
top_vt = df.nlargest(10, 'vt_malicious_votes')[
    ['url', 'vt_malicious_votes', 'vt_suspicious_votes', 
     'vt_threat_score', 'label']
]
print(top_vt.to_string())
```

### Figure 5.11: Feature Importance
```python
import pickle
import json
import matplotlib.pyplot as plt

with open('models/phishing_rf_model.pkl', 'rb') as f:
    pipeline = pickle.load(f)

rf = pipeline.named_steps['classifier']
features = json.load(open('models/feature_names.json'))
importances = rf.feature_importances_

# Create bar plot
plt.figure(figsize=(10, 6))
plt.barh(features, importances)
plt.xlabel('Importance')
plt.title('Feature Importance - Random Forest')
plt.tight_layout()
plt.savefig('reports/feature_importance.png', dpi=300)
```

---

## 💡 Pro Tips

1. **Start with existing files**: 22 visualizations are already done!
2. **Run the script first**: Auto-generates 6 more figures + 3 tables
3. **Use notebooks for custom work**: `notebooks/04-model-training.ipynb`
4. **All metrics in JSON**: Check `models/training_metrics.json` first
5. **SHAP plots ready**: Just copy from `models/` directory

---

## 🚀 Recommended Workflow

```bash
# 1. Check what exists
ls -lh models/*.png models/*.json reports/*.json

# 2. Generate missing visualizations
python generate_chapter4_viz.py

# 3. Verify outputs
ls -lh reports/chapter4/figures/
ls -lh reports/chapter4/tables/

# 4. For custom analysis
jupyter notebook  # Open 04-model-training.ipynb

# 5. View interactive dashboard
streamlit run dashboard.py
```

---

## 📖 Need More Help?

**Comprehensive guide**: `docs/CHAPTER4_DATA_SOURCE_GUIDE.md` (22KB, detailed)  
**Visual mapping**: `FIGURE_TABLE_MAPPING.txt` (ASCII art, terminal-friendly)  
**Quick reference**: `CHAPTER4_QUICK_REFERENCE.md` (10KB, code snippets)  
**This file**: `README_CHAPTER4.md` (you are here)

---

## 📞 Quick Reference Card

```
═══════════════════════════════════════════════════════════════
                    CHAPTER 4 QUICK CARD
═══════════════════════════════════════════════════════════════

ALREADY READY (22 files):
  ✓ SHAP plots: models/phishing_shap_*.png (11 files)
  ✓ Auth plots: models/auth_*.png (6 files)
  ✓ Metrics: models/training_metrics.json
  ✓ CV scores: reports/cv_scores.json

AUTO-GENERATE (9 files):
  → python generate_chapter4_viz.py
  → Output: reports/chapter4/

MANUAL GENERATION:
  • Confusion matrix (from test predictions)
  • Precision-recall curve
  • Feature importance (from model)
  • VT distribution (from CSV)
  • VT correlations (from CSV)

KEY FILES:
  models/training_metrics.json  ← All metrics
  reports/cv_scores.json        ← CV results
  models/feature_names.json     ← 19 features
  data/processed/url_features_vt.csv ← 159,603 records

═══════════════════════════════════════════════════════════════
```

---

**Last Updated**: 2025-11-15  
**Project**: Phishing Risk Detection with Explainable AI
