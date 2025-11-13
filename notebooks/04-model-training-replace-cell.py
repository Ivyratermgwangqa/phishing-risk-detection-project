# Replace the "Load Data and Augment with Synthetic Negatives" cell with this code

import os
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import classification_report, roc_auc_score, roc_curve

COMBINED_PATH = os.path.join('..','data','processed','phishing_graph_features.csv')
if not os.path.exists(COMBINED_PATH):
    raise SystemExit(f"Combined features not found: {COMBINED_PATH}")

df_full = pd.read_csv(COMBINED_PATH)
print("Loaded combined feature file:", COMBINED_PATH)
print("Shape:", df_full.shape)
print("Label counts:\n", df_full['label'].value_counts())

# 1) Detect deterministic / leaky columns: each value maps to single label
exclude = {'label','url','sender','sender_domain','domain'}
leakers = []
for col in [c for c in df_full.columns if c not in exclude]:
    s = df_full[col].fillna('__NA__')
    if s.nunique() > 1:
        mapped = df_full.groupby(s)['label'].nunique()
        if mapped.max() == 1:
            leakers.append(col)
# also flag obvious phishtank metadata names
leakers += [c for c in df_full.columns if any(k in c.lower() for k in ['phish_id','phish_detail','submission_time','verified','target','online'])]
leakers = sorted(set(leakers))
if leakers:
    print("Potential leakage columns detected (will drop):", leakers)
    df_full = df_full.drop(columns=[c for c in leakers if c in df_full.columns])
else:
    print("No obvious single-column deterministic leakers found.")

# 2) Detect URLs labeled both 0 and 1 and drop them (label noise)
if 'url' in df_full.columns:
    url_label_counts = df_full.groupby('url')['label'].nunique()
    conflicted = url_label_counts[url_label_counts > 1]
    print("URLs with conflicting labels:", len(conflicted))
    if len(conflicted) > 0:
        conflicted_set = set(conflicted.index)
        df_full = df_full[~df_full['url'].isin(conflicted_set)]
        print("Dropped conflicted URLs; new shape:", df_full.shape)

# 3) Deduplicate by URL (keep first) to avoid near-duplicate leakage
if 'url' in df_full.columns:
    before = df_full.shape[0]
    df_full = df_full.drop_duplicates(subset=['url'])
    print(f"Dropped {before - df_full.shape[0]} duplicate URL rows; new shape: {df_full.shape}")

# 4) Prepare features X, target y and group by url for splitting
non_feature_cols = ['label','url','sender_domain','domain','sender']
X = df_full.drop(columns=[c for c in non_feature_cols if c in df_full.columns])
y = df_full['label'].astype(int)

# Ensure no leftover non-numeric columns in X (coerce where reasonable)
X = X.copy()
non_num = X.select_dtypes(exclude=[np.number]).columns.tolist()
if non_num:
    print("Coercing non-numeric columns to numeric where possible:", non_num)
    X[non_num] = X[non_num].apply(pd.to_numeric, errors='coerce')

# 5) Split using GroupShuffleSplit by URL so same URL not in both sets
groups = df_full['url'].fillna('').astype(str).values if 'url' in df_full.columns else None
if groups is not None:
    gss = GroupShuffleSplit(n_splits=1, test_size=0.3, random_state=42)
    train_idx, test_idx = next(gss.split(X, y, groups=groups))
else:
    # fallback
    from sklearn.model_selection import train_test_split
    train_idx, test_idx = train_test_split(np.arange(len(X)), test_size=0.3, random_state=42, stratify=y)

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

print("Train labels:", y_train.value_counts().to_dict(), "Test labels:", y_test.value_counts().to_dict())

# 6) Train and evaluate
clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced', n_jobs=-1)
clf.fit(X_train.fillna(0), y_train)
joblib.dump(clf, os.path.join('..','models','phishing_rf_model_notebook.pkl'))
print("Model saved to ../models/phishing_rf_model_notebook.pkl")

y_pred = clf.predict(X_test.fillna(0))
print(classification_report(y_test, y_pred))

# ROC AUC if both classes present
if y_test.nunique() > 1:
    if hasattr(clf, 'predict_proba'):
        scores = clf.predict_proba(X_test.fillna(0))[:,1]
    else:
        scores = clf.predict(X_test.fillna(0))
    try:
        roc_auc = roc_auc_score(y_test, scores)
        fpr, tpr, _ = roc_curve(y_test, scores)
        print(f"ROC AUC: {roc_auc:.3f}")
        plt.figure()
        plt.plot(fpr, tpr, label=f'RF (AUC = {roc_auc:.3f})')
        plt.plot([0,1],[0,1],'k--')
        plt.xlabel('FPR'); plt.ylabel('TPR'); plt.title('ROC Curve')
        plt.show()
    except Exception as e:
        print("Could not compute ROC AUC:", e)
else:
    print("Only one class in test set; cannot compute ROC AUC.")