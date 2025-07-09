# evaluate_models.py
# Generate evaluation reports and plots
import joblib
import pandas as pd
from sklearn.metrics import roc_curve, auc, precision_recall_fscore_support
import matplotlib.pyplot as plt


def evaluate_phishing(model_path: str, feature_csv: str):
    clf = joblib.load(model_path)
    df = pd.read_csv(feature_csv)
    X = df.drop(columns=['label'])
    y = df['label']
    prob = clf.predict_proba(X)[:,1]
    fpr, tpr, _ = roc_curve(y, prob)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr)
    plt.title(f"Phishing ROC AUC = {roc_auc:.2f}")
    plt.show()

# utils.py
# Shared helper functions
import re
import urllib.parse
import tldextract


def extract_urls(text: str) -> list:
    """Extract all URLs from a text string"""
    regex = r'https?://[^\s]+'  # simple pattern
    return re.findall(regex, text)


def parse_domain_age(domain: str) -> int:
    """Stub for domain age calculation"""
    # Implement as needed
    return 0