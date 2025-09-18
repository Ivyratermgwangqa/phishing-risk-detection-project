import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import StandardScaler, LabelEncoder

warnings.filterwarnings('ignore')
plt.style.use('default')
sns.set_palette("husl")

# === Paths to models and data from your notebooks ===
DATA_DIR = os.path.join('..', 'data', 'processed')
MODEL_DIR = os.path.join('..', 'models')

PHISH_FEATURES_CSV = os.path.join(DATA_DIR, 'phishing_graph_features.csv')
AUTH_LOGS_CSV = os.path.join(DATA_DIR, 'auth_logs.csv')
PHISH_MODEL_PATH = os.path.join(MODEL_DIR, 'phishing_rf_model.pkl')
AUTH_MODEL_PATH = os.path.join(MODEL_DIR, 'auth_risk_model.pkl')

class PhishingDetectionFramework:
    """
    Explainable Phishing Detection Framework with Authentication Risk Modeling
    """
    
    def __init__(self):
        print("Loading trained models and datasets...")
        # Load phishing detection model and features
        self.phish_model = joblib.load(PHISH_MODEL_PATH)
        self.phish_features = pd.read_csv(PHISH_FEATURES_CSV)
        # Load authentication risk model and logs (if available)
        if os.path.exists(AUTH_MODEL_PATH) and os.path.exists(AUTH_LOGS_CSV):
            self.auth_model = joblib.load(AUTH_MODEL_PATH)
            self.auth_logs = pd.read_csv(AUTH_LOGS_CSV)
        else:
            self.auth_model = None
            self.auth_logs = None

    def predict_phishing(self, X=None):
        """Predict phishing risk using the loaded model.
        If X is None, use the loaded feature table."""
        if X is None:
            X = self.phish_features.drop(columns=['label', 'url', 'sender_domain', 'domain'], errors='ignore')
        preds = self.phish_model.predict(X)
        probs = self.phish_model.predict_proba(X)[:, 1] if hasattr(self.phish_model, 'predict_proba') else preds
        return preds, probs

    def predict_auth_risk(self, X=None):
        """Predict authentication risk using the loaded model."""
        if self.auth_model is None or self.auth_logs is None:
            print("Auth model or logs not loaded.")
            return None, None
        if X is None:
            X = self.auth_logs.drop(columns=['label'], errors='ignore')
        preds = self.auth_model.predict(X)
        probs = self.auth_model.predict_proba(X)[:, 1] if hasattr(self.auth_model, 'predict_proba') else preds
        return preds, probs

    def explain_phishing(self, X=None, idx=0):
        """Show SHAP explanation for a phishing prediction."""
        import shap
        if X is None:
            X = self.phish_features.drop(columns=['label', 'url', 'sender_domain', 'domain'], errors='ignore')
        explainer = shap.TreeExplainer(self.phish_model)
        shap_values = explainer.shap_values(X)
        # Pick positive class if available
        sv = shap_values[1] if isinstance(shap_values, list) and len(shap_values) > 1 else shap_values[0]
        shap.summary_plot(sv, X, show=True)
        shap.force_plot(explainer.expected_value[1] if hasattr(explainer.expected_value, '__len__') else explainer.expected_value, 
                        sv[idx], X.iloc[idx], matplotlib=True)
        plt.show()

    def explain_auth(self, X=None, idx=0):
        """Show SHAP explanation for an auth risk prediction."""
        import shap
        if self.auth_model is None or self.auth_logs is None:
            print("Auth model or logs not loaded.")
            return
        if X is None:
            X = self.auth_logs.drop(columns=['label'], errors='ignore')
        explainer = shap.TreeExplainer(self.auth_model)
        shap_values = explainer.shap_values(X)
        sv = shap_values[1] if isinstance(shap_values, list) and len(shap_values) > 1 else shap_values[0]
        shap.summary_plot(sv, X, show=True)
        shap.force_plot(explainer.expected_value[1] if hasattr(explainer.expected_value, '__len__') else explainer.expected_value, 
                        sv[idx], X.iloc[idx], matplotlib=True)
        plt.show()

# === Example usage ===

if __name__ == "__main__":
    print("=== Explainable Phishing Detection Framework ===")
    print("Initializing framework...")

    framework = PhishingDetectionFramework()

    print("\nPhishing model predictions on loaded features:")
    preds, probs = framework.predict_phishing()
    print(pd.Series(preds).value_counts())
    print("Sample predicted probabilities:", probs[:5])

    if framework.auth_model is not None:
        print("\nAuth risk model predictions on loaded logs:")
        apreds, aprobs = framework.predict_auth_risk()
        print(pd.Series(apreds).value_counts())
        print("Sample auth risk probabilities:", aprobs[:5])

    # Show SHAP explanations for the first phishing sample
    print("\nGenerating SHAP explanation for phishing model (first sample)...")
    framework.explain_phishing(idx=0)

    # Show SHAP explanations for the first auth sample (if available)
    if framework.auth_model is not None:
        print("\nGenerating SHAP explanation for auth risk model (first sample)...")
        framework.explain_auth(idx=0)