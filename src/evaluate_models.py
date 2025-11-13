# evaluate_models.py
# Generate evaluation reports and plots
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc, precision_recall_fscore_support, roc_auc_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def evaluate_phishing(model_path: str, feature_csv: str, out_roc: str = "phishing_roc_curve.png"):
    payload = joblib.load(model_path)
    # payload may be dict with model and imputer
    if isinstance(payload, dict):
        clf = payload.get('model')
        imputer = payload.get('imputer')
    else:
        clf = payload
        imputer = None

    df = pd.read_csv(feature_csv)
    # drop non-feature columns
    drop_cols = ['label', 'url', 'sender', 'sender_domain', 'domain']
    X = df.drop(columns=[c for c in drop_cols if c in df.columns], errors='ignore')
    # keep numeric columns only
    X = X.select_dtypes(include=[np.number])
    y = df['label'].astype(int)

    if imputer is not None:
        X_proc = pd.DataFrame(imputer.transform(X), columns=X.columns)
    else:
        X_proc = X.fillna(X.median())

    if not hasattr(clf, "predict_proba"):
        raise SystemExit("Model does not support predict_proba required for ROC")

    prob = clf.predict_proba(X_proc)[:, 1]
    fpr, tpr, _ = roc_curve(y, prob)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(6, 6))
    plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.3f}")
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
    plt.legend(loc='lower right')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f"Phishing ROC AUC = {roc_auc:.3f}")
    plt.savefig(out_roc, bbox_inches='tight')
    print("ROC curve saved to", out_roc)

    # other metrics
    y_pred = (prob >= 0.5).astype(int)
    prec, recall, f1, _ = precision_recall_fscore_support(y, y_pred, average='binary', zero_division=0)
    try:
        auc_score = roc_auc_score(y, prob)
    except Exception:
        auc_score = roc_auc
    print(f"AUC: {auc_score:.4f}  Precision: {prec:.4f}  Recall: {recall:.4f}  F1: {f1:.4f}")

if __name__ == "__main__":
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_PATH = os.environ.get('MODEL_PATH') or os.path.join(PROJECT_ROOT, 'models', 'phishing_rf_model.pkl')
    FEATURES = os.environ.get('ALL_FEATURES') or os.path.join(PROJECT_ROOT, 'data', 'processed', 'phishing_graph_features.csv')
    evaluate_phishing(MODEL_PATH, FEATURES, out_roc=os.path.join(PROJECT_ROOT, 'reports', 'phishing_roc_curve.png'))