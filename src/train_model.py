import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import roc_auc_score, precision_recall_fscore_support
from sklearn.impute import SimpleImputer

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPATH = os.environ.get('ALL_FEATURES') or os.path.join(PROJECT_ROOT, 'data', 'processed', 'phishing_graph_features.csv')
MODELDIR = os.path.join(PROJECT_ROOT, 'models')
MODEL_PATH = os.path.join(MODELDIR, 'phishing_rf_model.pkl')
FEATURES_PATH = os.path.join(MODELDIR, 'feature_names.json')

os.makedirs(MODELDIR, exist_ok=True)

df = pd.read_csv(INPATH)
if 'label' not in df.columns:
    raise SystemExit("Input features file missing 'label' column: " + INPATH)

# Basic checks: class balance and duplicates
print('Shape:', df.shape)
print('Label counts:\n', df['label'].value_counts(dropna=False))
print('Duplicate rows:', df.duplicated().sum())
print('Unique URLs:', df['url'].nunique() if 'url' in df.columns else 0)
print('Total rows:', len(df))

# Detect URLs that have conflicting labels (same url labeled both 0 and 1)
if 'url' in df.columns:
    url_label_counts = df.groupby('url')['label'].nunique()
    conflicted = url_label_counts[url_label_counts > 1]
    print('URLs with conflicting labels:', len(conflicted))
    if len(conflicted) > 0:
        # drop all rows for conflicted URLs to avoid label noise
        conflicted_urls = set(conflicted.index)
        df = df[~df['url'].isin(conflicted_urls)]
        print(f"Dropped {len(conflicted_urls)} conflicted URLs and their rows. New shape: {df.shape}")

# Drop exact duplicate rows
df = df.drop_duplicates()
print('After drop_duplicates shape:', df.shape)

# Identify columns that deterministically map to the label (perfect leakage)
leak_candidates = []
exclude = {'label', 'url', 'sender', 'sender_domain', 'domain'}
for col in [c for c in df.columns if c not in exclude]:
    series = df[col].fillna('__NA__')
    # if every unique value maps to a single label, this column is a deterministic mapping -> leak
    groups = df.groupby(series)['label'].nunique()
    if groups.max() == 1 and series.nunique() > 1:
        leak_candidates.append(col)

# Add some known likely-leak columns by name
by_name = [c for c in df.columns if any(k in c.lower() for k in ['phish_id', 'phish_detail', 'submission_time', 'verified', 'target', 'online'])]
for c in by_name:
    if c not in leak_candidates:
        leak_candidates.append(c)

if leak_candidates:
    print('Detected potential leakage columns (dropping):', leak_candidates)
    df = df.drop(columns=[c for c in leak_candidates if c in df.columns])
else:
    print('No single-column deterministic leakers detected.')

# Optionally deduplicate by URL (keep first) to reduce duplicate-url bias
if 'url' in df.columns:
    dup_urls = df.duplicated(subset=['url']).sum()
    print('Duplicate URL rows remaining:', dup_urls)
    # keep first occurrence of each URL
    df = df.drop_duplicates(subset=['url'])
    print('After dedup by url shape:', df.shape)

# Select numeric feature columns (exclude label and known non-features)
non_feature_cols = {'label', 'url', 'sender', 'sender_domain', 'domain'}
numeric = df.select_dtypes(include=[np.number]).columns.tolist()
if 'label' in numeric:
    numeric.remove('label')

# Filter out numeric columns that are all-missing
numeric = [c for c in numeric if df[c].notna().any()]

if not numeric:
    possible = [c for c in df.columns if c not in non_feature_cols and c != 'label']
    df_num = df[possible].apply(pd.to_numeric, errors='coerce')
    numeric = df_num.select_dtypes(include=[np.number]).columns.tolist()
    df[numeric] = df_num[numeric]

if not numeric:
    raise SystemExit("No numeric features found in input. Check preprocessing.")

print('Using numeric features count:', len(numeric))

X = df[numeric].copy()
y = df['label'].astype(int)

# Impute
imp = SimpleImputer(strategy='median')
X_vals = imp.fit_transform(X)
X_imputed = pd.DataFrame(X_vals, columns=numeric[: X_vals.shape[1]])

# Use GroupShuffleSplit to ensure same URL not in both train and test (if url exists)
groups = df['url'].fillna('').astype(str).values if 'url' in df.columns else None
if groups is not None:
    gss = GroupShuffleSplit(n_splits=1, test_size=0.3, random_state=42)
    train_idx, test_idx = next(gss.split(X_imputed, y, groups=groups))
else:
    # fallback to simple split
    from sklearn.model_selection import train_test_split
    train_idx, test_idx = train_test_split(np.arange(len(X_imputed)), test_size=0.3, random_state=42, stratify=y)

X_train, X_test = X_imputed.iloc[train_idx], X_imputed.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

print('Train shape:', X_train.shape, 'Test shape:', X_test.shape)
print('Train label dist:', y_train.value_counts().to_dict(), 'Test label dist:', y_test.value_counts().to_dict())

# Train
clf = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced', n_jobs=-1)
clf.fit(X_train, y_train)

# Save model and feature names + imputer
joblib.dump({'model': clf, 'imputer': imp}, MODEL_PATH)
with open(FEATURES_PATH, 'w') as f:
    json.dump(list(X_imputed.columns), f)

# Evaluate on test
proba = clf.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, proba)
prec, recall, f1, _ = precision_recall_fscore_support(y_test, clf.predict(X_test), average='binary', zero_division=0)

print(f"Model saved to: {MODEL_PATH}")
print(f"AUC: {auc:.4f}  Precision: {prec:.4f}  Recall: {recall:.4f}  F1: {f1:.4f}")