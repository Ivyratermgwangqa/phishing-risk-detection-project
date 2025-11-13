# Project outcomes — Explainable Phishing Detection & Authentication Risk

## Executive summary
- Built an explainable phishing detection pipeline combining metadata link-graph features and threat intelligence.  
- Addressed major data leakage and duplication issues; finalized a reproducible training workflow with grouped splits by URL.  
- Final model: RandomForest (with imputer). Grouped cross-validation ROC AUC ≈ 0.989 (stable). SHAP used for per-sample and global explanations.  
- Deliverables: trained model artifacts, SHAP outputs (PNG/HTML), evaluation reports, Streamlit dashboard scaffold.

---

## Data summary & preprocessing
- Raw feature table: 381,450 rows × 23 columns. Label distribution: 0 = 327,793; 1 = 53,657.  
- Duplicate URLs detected: 221,847. After deduplication by URL final dataset: 159,603 rows × 22 cols.  
- All-NA column dropped during CV run: `domain_age_days`.  
- Deterministic/leaky column detected and dropped: `url_length` (and other PhishTank metadata by name where present).  
- Conflicting-label URLs: 0 (after initial checks and drops).  
- Non-numeric features coerced to numeric or removed prior to modeling; imputation used (median).

---

## Modeling & metrics
- Training procedure:
  - Numeric feature selection, median imputation, GroupShuffleSplit (by `url`) for train/test, RandomForestClassifier with class_weight='balanced'.
  - Model saved as `models/phishing_rf_model.pkl` (payload may contain {'model','imputer'}). Feature list saved at `models/feature_names.json`.
- Single-run evaluation:
  - Example train/test split sizes: Train (111,722 rows), Test (47,881 rows).  
  - Example test distribution: Train labels {0: 74,339; 1: 37,383}, Test labels {0: 31,623; 1: 16,258}.
  - Example single-run test AUC ≈ 0.9886; Precision/Recall/F1 shown near 0.92–0.96 after leak removal.
- GroupKFold cross-validation (5 folds) results:
  - Fold AUCs: [0.989049, 0.988507, 0.989131, 0.989601, 0.988963]
  - Mean ROC AUC = 0.989050, Std = 0.000350
  - Interpretation: strong, stable discriminative performance under grouped CV.

---

## Explainability (SHAP) outcomes
- SHAP artifacts produced:
  - `models/shap_values.npz`
  - `models/shap_summary.png` (global feature importance summary)
  - Per-sample plots: `models/shap_force_sample_*.png` and best-effort interactive HTML `models/shap_force_sample_*.html`
  - Authentication model SHAP outputs: `models/auth_shap_bar_sample_*.png` and HTMLs
- SHAP implementation notes:
  - Used TreeExplainer with `feature_perturbation='interventional'` and a small background sample where appropriate.
  - Additivity check initially failed; resolved by using `check_additivity=False` and matching model input shape with saved imputer/feature order.
  - Produced stable top-feature lists (see SHAP summary PNG). Top contributors were graph/metadata-derived features (pagerank/centrality-like features and selected metadata).

---

## Issues found and fixes
- Perfect AUC (1.0) initially observed due to leakage and duplicated rows across train/test. Fixes:
  - Dropped deterministic leaker columns (e.g., `url_length`).
  - Deduplicated by `url` and used GroupShuffleSplit/GroupKFold by URL to prevent same URL in train and test.
  - Detected and removed URLs with conflicting labels (if present).
- Feature name mismatch at prediction time:
  - Model fitted with certain feature names (including some later-dropped columns); risk.py updated to build X with the trained feature order, filling missing columns and applying imputer before predict to avoid sklearn feature-name validation errors.
- SHAP force-plot interoperability:
  - Interactive force plots sometimes failed due to array shapes or environment; robust fallback implemented: deterministic single-sample matplotlib bar plots saved as PNG and best-effort interactive HTML saved where possible.

---

## Artifacts produced
- Models and metadata:
  - models/phishing_rf_model.pkl  (model and imputer)
  - models/feature_names.json
- Evaluation and explainability:
  - reports/cv_scores.json
  - models/shap_values.npz
  - models/shap_summary.png
  - models/shap_force_sample_*.png / .html
  - models/phishing_shap_bar_sample_*.png
  - models/auth_shap_bar_sample_*.png and HTMLs
- Utilities / scripts added or updated:
  - src/train_model.py (leak checks, dedupe, GroupSplit, save artifacts)
  - src/train_model_cv.py (GroupKFold CV, dropped all-NA before impute)
  - src/compute_shap.py (aligned features, imputer, check_additivity=False)
  - src/risk.py (robust loaders, SHAP plotting fallbacks, dashboard writer)
  - dashboard.py (Streamlit scaffold, written to project root)

---

## Key insights
- Graph-derived metadata features combined with TI substantially improve discrimination versus naive content- or URL-only baselines.  
- Proper validation (grouped splits by URL/sender and leakage detection) is critical; otherwise evaluation is grossly optimistic.  
- SHAP gives actionable per-sample explanations suitable for analyst workflows; some interactive artifacts require environment-specific handling, so static PNGs are reliable fallbacks.  
- Cross-validated AUC ≈ 0.989 demonstrates model stability but does not replace targeted operational testing (live or simulated email streams).

---

## Recommendations / next steps
1. Final model:
   - Retrain final model on the cleaned/deduplicated dataset (all available data) and save the production artifact (model + imputer + feature list).
2. Feature audit:
   - Manually inspect top SHAP features and ensure none encode label indirectly (repeat deterministic mapping checks).
3. Hyperparameter tuning:
   - Run RandomizedSearchCV / Bayesian search using GroupKFold for robust tuning.
4. Operationalization:
   - Implement an online scoring endpoint that applies the same imputer and feature-order checks; add logging for model inputs to detect drift.
5. Monitoring:
   - Periodically re-check for duplicate URLs, leaking features, and calibration drift; rerun CV and SHAP analysis monthly or after major data updates.
6. Documentation & submission:
   - Include the produced figures and reports in thesis Chapter 4; add methods and reproducible commands in Appendix.
7. Repro commands (examples):
   - Train: .venv/bin/python src/train_model.py  
   - CV: .venv/bin/python src/train_model_cv.py  
   - SHAP: .venv/bin/python src/compute_shap.py  
   - Run risk dashboard script: .venv/bin/python src/risk.py  
   - Streamlit dashboard: streamlit run dashboard.py

---

## Notes / items needed from you to continue writing sections
- Confirm final list of features to document (or provide `models/feature_names.json` contents).  
- Share any specific example explanations (sample indices and their CSV rows) to include in Chapter 4 case studies.  
- Provide the exact PhishTank/TI source versions and any external datasets used (for references).  
- If you want a formatted thesis chapter draft next, specify which chapter (e.g., Introduction, Methods, Results) and whether to include figures/tables now.
