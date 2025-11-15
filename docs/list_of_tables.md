# List of Tables

## Table 1: Model Performance Metrics
Performance metrics of the final RandomForest phishing detection model on the test set.

| Metric | Score | Interpretation |
|--------|-------|----------------|
| AUC-ROC | 0.9888 | Excellent discrimination capability |
| Precision | 0.9236 | 92% accuracy when flagging phishing |
| Recall | 0.9632 | Catches 96% of phishing attempts |
| F1 Score | 0.9430 | Balanced precision and recall |

---

## Table 2: Cross-Validation Performance
GroupKFold cross-validation results (5 folds) using grouped splits by URL to prevent data leakage.

| Fold | AUC-ROC Score |
|------|---------------|
| 1 | 0.9890 |
| 2 | 0.9885 |
| 3 | 0.9891 |
| 4 | 0.9896 |
| 5 | 0.9890 |
| **Mean** | **0.9891** |
| **Std Dev** | **0.0003** |

---

## Table 3: VirusTotal Feature Columns
VT threat intelligence features integrated into the phishing detection pipeline.

| Column | Type | Description |
|--------|------|-------------|
| `vt_malicious_votes` | int | Number of VT engines flagging domain as malicious |
| `vt_suspicious_votes` | int | Number of VT engines flagging domain as suspicious |
| `vt_threat_score` | int | Threat score: 0=Benign, 1=Suspicious, 2=Malicious |
| `vt_threat_flag` | str | Human-readable threat classification |

---

## Table 4: Dataset Statistics
Summary of the dataset after preprocessing and deduplication.

| Metric | Value |
|--------|-------|
| Total records (raw) | 381,450 |
| Features (raw) | 27 |
| Duplicate URLs detected | 221,847 |
| Final records (deduplicated) | 159,603 |
| Final features | 26 |
| Benign samples (label=0) | 327,793 |
| Phishing samples (label=1) | 53,657 |
| Class ratio (phishing %) | 14.1% |

---

## Table 5: VirusTotal Threat Distribution
Distribution of VT threat classifications in the dataset (381,450 records).

| Classification | Count | Percentage |
|----------------|-------|------------|
| Benign | 380,963 | 99.87% |
| Suspicious (VT) | 252 | 0.07% |
| Malicious (VT) | 232 | 0.06% |
| Unknown | 3 | <0.01% |
| **Total flagged** | **484** | **0.13%** |

---

## Table 6: Feature Categories
Summary of feature engineering categories used in the phishing detection model.

| Category | Feature Count | Examples |
|----------|---------------|----------|
| URL Structure | 7 | `has_at`, `has_ip`, `num_dots`, `num_hyphens`, `num_qm`, `num_underscores`, `path_length` |
| Domain Analysis | 2 | `sender_domain_mismatch`, `subdomain_count` |
| Graph Features | 6 | `domain_degree_agg`, `sender_degree_agg`, `domain_degree_weighted`, `domain_clustering_agg`, `domain_betweenness_approx`, `sender_betweenness_approx` |
| Network Features | 1 | `url_degree_simple` |
| Threat Intelligence | 3 | `vt_malicious_votes`, `vt_suspicious_votes`, `vt_threat_score` |
| **Total** | **19** | Final feature set after leakage removal |

---

## Table 7: VT Feature Correlation with Phishing Labels
Pearson correlation coefficients between VirusTotal features and phishing labels.

| Feature | Correlation | Interpretation |
|---------|-------------|----------------|
| `vt_threat_score` | 0.0835 | Moderate positive correlation |
| `vt_malicious_votes` | 0.0631 | Weak positive correlation |
| `vt_suspicious_votes` | 0.0396 | Weak positive correlation |

**Note:** All VT-flagged domains (both Suspicious and Malicious) were confirmed phishing (label=1), indicating 100% precision for VT threat intelligence on flagged domains.

---

## Table 8: Data Quality Issues and Resolutions
Major data quality issues identified and their resolutions during model development.

| Issue | Impact | Resolution |
|-------|--------|------------|
| Duplicate URLs | 221,847 duplicates causing inflated performance | Deduplication by URL; GroupShuffleSplit/GroupKFold validation |
| Data leakage (url_length) | Perfect AUC (1.0), deterministic mapping | Dropped leaky columns; manual feature audit |
| All-NA column (domain_age_days) | Model fitting errors | Dropped during preprocessing |
| Feature name mismatch | Prediction-time sklearn errors | Aligned features with saved feature list; robust loader |
| Conflicting labels | Potential noise in training | Checked and removed (0 found after initial cleanup) |

---

## Table 9: Model Artifacts Generated
List of key artifacts produced by the phishing detection pipeline.

| Artifact Type | File Path | Description |
|---------------|-----------|-------------|
| Trained Model | `models/phishing_rf_model.pkl` | RandomForest model with imputer |
| Feature List | `models/feature_names.json` | Ordered list of 19 features |
| CV Scores | `reports/cv_scores.json` | 5-fold cross-validation results |
| SHAP Values | `models/shap_values.npz` | Precomputed SHAP explanations |
| SHAP Summary | `models/shap_summary.png` | Global feature importance plot |
| SHAP Force Plots | `models/shap_force_sample_*.png/html` | Per-sample explanation visualizations |
| Dashboard | `dashboard.py` | Streamlit dashboard for model exploration |

---

## Table 10: Top High-Risk Domains by VirusTotal
Top domains flagged with highest malicious vote counts from VirusTotal.

| Domain | Malicious Votes | Suspicious Votes | Threat Score | Label |
|--------|-----------------|------------------|--------------|-------|
| llius.cn | 17 | 0 | 2 | Phishing |
| ovqjk.cn | 16 | 0 | 2 | Phishing |
| pl-kategorie781247621782.icu | 16 | 0 | 2 | Phishing |

**Note:** All domains with VT malicious/suspicious votes were confirmed phishing URLs in the dataset.

---

## Summary

This document contains **10 tables** covering:
- Model performance and validation (Tables 1-2)
- Feature engineering and data integration (Tables 3, 6-7)
- Dataset statistics and quality (Tables 4-5, 8)
- Artifacts and case studies (Tables 9-10)

These tables support the research report sections on methodology, results, and discussion.
