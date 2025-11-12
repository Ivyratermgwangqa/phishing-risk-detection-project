import os
import sys
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import json
from urllib.parse import urlparse
import tldextract

from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import StandardScaler, LabelEncoder

warnings.filterwarnings('ignore')
plt.style.use('default')
sns.set_palette("husl")

# === Paths to models and data from your notebooks ===
# Support both running from root and from src directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
MODEL_DIR = os.path.join(BASE_DIR, 'models')

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
        # Only use the features the model was trained on
        features = ['distance_km', 'login_hour', 'new_device']
        if X is None:
            X = self.auth_logs[features]
        else:
            X = X[features]
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
        features = ['distance_km', 'login_hour', 'new_device']
        if X is None:
            X = self.auth_logs[features]
        else:
            X = X[features]
        explainer = shap.TreeExplainer(self.auth_model)
        shap_values = explainer.shap_values(X)
        sv = shap_values[1] if isinstance(shap_values, list) and len(shap_values) > 1 else shap_values[0]
        shap.summary_plot(sv, X, show=True)
        shap.force_plot(explainer.expected_value[1] if hasattr(explainer.expected_value, '__len__') else explainer.expected_value, 
                        sv[idx], X.iloc[idx], matplotlib=True)
        plt.show()

    def extract_url_features(self, url):
        """Extract basic features from a URL for prediction."""
        parsed = urlparse(url)
        ext = tldextract.extract(url)
        
        features = {
            'url_length': len(url),
            'domain_length': len(parsed.netloc),
            'path_length': len(parsed.path),
            'has_ip': 1 if parsed.netloc.replace('.', '').replace(':', '').isdigit() else 0,
            'has_at': 1 if '@' in url else 0,
            'num_dots': url.count('.'),
            'num_hyphens': url.count('-'),
            'num_underscores': url.count('_'),
            'num_slashes': url.count('/'),
            'num_questionmarks': url.count('?'),
            'num_equals': url.count('='),
            'num_ampersands': url.count('&'),
            'is_https': 1 if parsed.scheme == 'https' else 0,
            'tld': ext.suffix,
            'subdomain_count': len(ext.subdomain.split('.')) if ext.subdomain else 0,
        }
        return features

    def get_threat_intel(self, url, sender_email=None):
        """
        Get threat intelligence for a URL and sender.
        Returns a dictionary with threat intelligence details.
        
        Note: This is a simplified implementation. For production use,
        integrate with actual threat intelligence APIs like VirusTotal.
        """
        threat_intel = {
            'url': url,
            'sender': sender_email,
            'malicious': False,
            'suspicious': False,
            'detection_engines': 0,
            'source': 'local_analysis'
        }
        
        # Simple heuristics for demonstration
        parsed = urlparse(url)
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top']
        suspicious_keywords = ['login', 'secure', 'account', 'verify', 'update', 'confirm']
        
        # Check for suspicious TLD
        for tld in suspicious_tlds:
            if url.lower().endswith(tld):
                threat_intel['suspicious'] = True
                threat_intel['detection_engines'] += 1
                break
        
        # Check for suspicious keywords
        url_lower = url.lower()
        for keyword in suspicious_keywords:
            if keyword in url_lower:
                threat_intel['suspicious'] = True
                threat_intel['detection_engines'] += 1
                break
        
        # Check sender domain reputation (simplified)
        if sender_email and sender_email.count('@') == 1:
            sender_domain = sender_email.split('@')[1]
            # In production, check against known malicious domains
            if sender_domain != parsed.netloc:
                threat_intel['suspicious'] = True
                threat_intel['detection_engines'] += 1
        
        return threat_intel

    def predict_single(self, input_data, return_shap=False):
        """
        Predict phishing risk for a single URL with threat intelligence.
        
        Args:
            input_data: dict with 'url' and optionally 'sender' keys
            return_shap: bool, whether to return SHAP values
            
        Returns:
            dict with prediction, probability, threat intelligence, and optionally SHAP values
        """
        url = input_data.get('url', '')
        sender = input_data.get('sender', '')
        
        # Extract features
        url_features = self.extract_url_features(url)
        
        # Get threat intelligence
        threat_intel = self.get_threat_intel(url, sender)
        
        # Get reference features from training data
        feature_cols = [col for col in self.phish_features.columns 
                       if col not in ['label', 'url', 'sender_domain', 'domain']]
        
        # Create feature vector with defaults
        X_dict = {col: 0 for col in feature_cols}
        
        # Update with extracted features where names match
        for key, value in url_features.items():
            if key in X_dict:
                X_dict[key] = value
        
        # Convert to DataFrame
        X = pd.DataFrame([X_dict])
        
        # Make prediction
        pred = self.phish_model.predict(X)[0]
        prob = self.phish_model.predict_proba(X)[0, 1] if hasattr(self.phish_model, 'predict_proba') else pred
        
        result = {
            'url': url,
            'sender': sender,
            'prediction': int(pred),
            'probability': float(prob),
            'threat_intelligence': threat_intel
        }
        
        # Add SHAP values if requested
        if return_shap:
            import shap
            explainer = shap.TreeExplainer(self.phish_model)
            shap_values = explainer.shap_values(X)
            sv = shap_values[1] if isinstance(shap_values, list) and len(shap_values) > 1 else shap_values[0]
            
            # Get top contributing features
            feature_importance = list(zip(feature_cols, sv[0]))
            feature_importance.sort(key=lambda x: abs(x[1]), reverse=True)
            
            result['shap_values'] = {
                'top_contributors': [
                    {'feature': feat, 'value': float(val)} 
                    for feat, val in feature_importance[:10]
                ]
            }
        
        return result

# === Example usage ===

if __name__ == "__main__":
    print("=== Explainable Phishing Detection Framework ===")
    
    # Check if SINGLE_PREDICT mode is enabled
    single_predict_mode = os.environ.get('SINGLE_PREDICT', '0') == '1'
    
    if single_predict_mode:
        print("Running in SINGLE_PREDICT mode...")
        print("Initializing framework...")
        framework = PhishingDetectionFramework()
        
        print("\n" + "="*60)
        print("Single URL Prediction with Threat Intelligence")
        print("="*60)
        
        # Get user input
        url = input("\nEnter URL to analyze: ").strip()
        sender = input("Enter sender email (optional): ").strip()
        
        # Perform prediction
        print("\nAnalyzing...")
        input_data = {'url': url, 'sender': sender if sender else None}
        result = framework.predict_single(input_data, return_shap=True)
        
        # Display results
        print("\n" + "="*60)
        print("PREDICTION RESULTS")
        print("="*60)
        print(f"URL: {result['url']}")
        if result['sender']:
            print(f"Sender: {result['sender']}")
        print(f"\nPredicted Label: {result['prediction']} {'(Phishing)' if result['prediction'] == 1 else '(Legitimate)'}")
        print(f"Probability: {result['probability']:.4f}")
        
        print("\n" + "-"*60)
        print("THREAT INTELLIGENCE")
        print("-"*60)
        ti = result['threat_intelligence']
        print(f"Malicious: {ti['malicious']}")
        print(f"Suspicious: {ti['suspicious']}")
        print(f"Detection Engines: {ti['detection_engines']}")
        print(f"Source: {ti['source']}")
        
        if 'shap_values' in result:
            print("\n" + "-"*60)
            print("TOP CONTRIBUTING FEATURES (SHAP)")
            print("-"*60)
            for contrib in result['shap_values']['top_contributors'][:5]:
                print(f"  {contrib['feature']}: {contrib['value']:.4f}")
        
        print("\n" + "="*60)
    else:
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