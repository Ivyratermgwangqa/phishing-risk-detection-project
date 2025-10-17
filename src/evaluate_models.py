# evaluate_models.py
# Generate evaluation reports and plots
import joblib
import pandas as pd
from sklearn.metrics import roc_curve, auc, precision_recall_fscore_support
import matplotlib.pyplot as plt


def evaluate_phishing(model_path: str, feature_csv: str):
    clf = joblib.load(model_path)
    df = pd.read_csv(feature_csv)
    # Drop non-numeric/non-feature columns as in training
    X = df.drop(columns=['label', 'url', 'sender_domain', 'domain'], errors='ignore')
    y = df['label']
    prob = clf.predict_proba(X)[:,1]
    fpr, tpr, _ = roc_curve(y, prob)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr)
    plt.title(f"Phishing ROC AUC = {roc_auc:.2f}")
    plt.savefig("phishing_roc_curve.png", bbox_inches='tight')
    print("ROC curve saved to phishing_roc_curve.png")

if __name__ == "__main__":
    # Update these paths as needed for your project structure
    model_path = "../models/phishing_rf_model.pkl"
    feature_csv = "../data/processed/phishing_graph_features.csv"
    evaluate_phishing(model_path, feature_csv)

# utils.py
# Shared helper functions
import re
import urllib.parse
import tldextract


def extract_urls(text: str) -> list:
    """Extract all URLs from a text string"""
    regex = r'https?://[^\s]+'  # simple pattern
    raw = re.findall(regex, text)
    # normalize URLs and remove fragments
    return [normalize_url(u) for u in raw]


def parse_domain_age(domain: str) -> int:
    """Stub for domain age calculation"""
    # Basic domain parsing using tldextract to extract domain parts
    parts = tldextract.extract(domain)
    if not parts.domain:
        return 0
    # placeholder: use length of domain name as a deterministic proxy
    return len(parts.domain)


def normalize_url(url: str) -> str:
    """Normalize a URL: remove fragments, lowercase scheme+host, strip default ports."""
    try:
        p = urllib.parse.urlparse(url)
        scheme = p.scheme.lower()
        netloc = p.hostname.lower() if p.hostname else ''
        if p.port and p.port not in (80, 443):
            netloc = f"{netloc}:{p.port}"
        path = urllib.parse.quote(urllib.parse.unquote(p.path))
        query = ''  # strip query for normalization
        return urllib.parse.urlunparse((scheme, netloc, path, '', query, ''))
    except Exception:
        return url