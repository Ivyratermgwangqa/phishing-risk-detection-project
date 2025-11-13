import os
import sys
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHISH_PATH = os.environ.get('PHISH_FEATURES') or os.path.join(PROJECT_ROOT, 'data', 'processed', 'phishing_features.csv')
BENIGN_PATH = os.environ.get('BENIGN_FEATURES') or os.path.join(PROJECT_ROOT, 'data', 'processed', 'benign_features.csv')
OUT_PATH = os.environ.get('ALL_FEATURES') or os.path.join(PROJECT_ROOT, 'data', 'processed', 'phishing_graph_features.csv')

def load_or_exit(path, name):
    if not os.path.exists(path):
        print(f"ERROR: {name} not found at: {path}", file=sys.stderr)
        sys.exit(2)
    return pd.read_csv(path)

def main():
    ph = load_or_exit(PHISH_PATH, "Phishing features")
    bg = load_or_exit(BENIGN_PATH, "Benign features")

    # Optional: align columns (keep union, fill missing)
    all_cols = sorted(set(ph.columns).union(set(bg.columns)))
    ph = ph.reindex(columns=all_cols)
    bg = bg.reindex(columns=all_cols)

    combined = pd.concat([ph, bg], ignore_index=True)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    combined.to_csv(OUT_PATH, index=False)
    print(f"Saved combined features to: {OUT_PATH}  shape={combined.shape}")
    if 'label' in combined.columns:
        print("Label distribution:")
        print(combined['label'].value_counts(dropna=False))

if __name__ == "__main__":
    main()