import os
import json
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'phishing_rf_model.pkl')
FEATURES_PATH = os.path.join(PROJECT_ROOT, 'models', 'feature_names.json')
INPATH = os.environ.get('ALL_FEATURES') or os.path.join(PROJECT_ROOT, 'data', 'processed', 'phishing_graph_features.csv')
OUT_DIR = os.path.join(PROJECT_ROOT, 'models')
SHAP_VALUES_PATH = os.path.join(OUT_DIR, 'shap_values.npz')
SHAP_SUMMARY_PNG = os.path.join(OUT_DIR, 'shap_summary.png')

if not os.path.exists(MODEL_PATH):
    raise SystemExit("Model not found: " + MODEL_PATH)

data = pd.read_csv(INPATH)

with open(FEATURES_PATH, 'r') as f:
    features = json.load(f)

# Prepare X using saved feature list and the saved imputer so shapes match the model training
payload = joblib.load(MODEL_PATH)
clf = payload.get('model') if isinstance(payload, dict) else payload
imputer = payload.get('imputer') if isinstance(payload, dict) else None

# Ensure feature order and presence
# Keep only columns present both in features and dataframe, in the same order
features_present = [f for f in features if f in data.columns]
if not features_present:
    # fallback to numeric selection (shouldn't happen if features were saved correctly)
    X = data.select_dtypes(include=[np.number]).drop(columns=['label'], errors='ignore').fillna(0)
    features_present = X.columns.tolist()
else:
    X = data[features_present].copy()

# If imputer exists, transform with it to match training preprocessing
if imputer is not None:
    X_proc = pd.DataFrame(imputer.transform(X), columns=features_present, index=X.index)
else:
    X_proc = X.fillna(0)

# Sample rows for SHAP to limit memory/time
sample_n = min(2000, len(X_proc))
X_sample = X_proc.sample(n=sample_n, random_state=42)

try:
    import shap
except Exception:
    raise SystemExit("shap not installed. Install with: .venv/bin/pip install shap")

# Use TreeExplainer with interventional perturbation and disable strict additivity check if it fails
# This ensures the explainer uses the same feature space the model was trained on.
if hasattr(clf, 'estimators_'):
    explainer = shap.TreeExplainer(clf, feature_perturbation='interventional')
    # call with check_additivity=False to avoid hard failure if tiny numerical mismatch occurs
    shap_values = explainer.shap_values(X_sample, check_additivity=False)
    to_save = shap_values
else:
    explainer = shap.KernelExplainer(clf.predict_proba, shap.kmeans(X_proc, 10))
    shap_values = explainer.shap_values(X_sample)
    to_save = shap_values

# save shap arrays (may be large)
np.savez_compressed(SHAP_VALUES_PATH, *to_save)
# produce summary plot
plt.figure(figsize=(8, 6))
if isinstance(shap_values, list):
    vals = shap_values[1] if len(shap_values) > 1 else shap_values[0]
else:
    vals = shap_values
shap.summary_plot(vals, X_sample, show=False)
plt.tight_layout()
plt.savefig(SHAP_SUMMARY_PNG, bbox_inches='tight')
print("SHAP values saved to:", SHAP_VALUES_PATH)
print("SHAP summary plot saved to:", SHAP_SUMMARY_PNG)