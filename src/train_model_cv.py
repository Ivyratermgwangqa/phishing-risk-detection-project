import os, json
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold, cross_val_score
from sklearn.impute import SimpleImputer

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPATH = os.path.join(PROJECT_ROOT, 'data', 'processed', 'phishing_graph_features.csv')

df = pd.read_csv(INPATH)

# preprocess similar to train_model.py
if 'url' in df.columns:
    df = df.drop_duplicates(subset=['url'])

exclude = {'label','url','sender','sender_domain','domain'}
# drop deterministic leakers if present
for col in [c for c in df.columns if c not in exclude]:
    s = df[col].fillna('__NA__')
    try:
        if s.nunique()>1 and df.groupby(s)['label'].nunique().max()==1:
            df = df.drop(columns=[col])
    except Exception:
        # skip problematic columns
        continue

X = df.drop(columns=[c for c in ['label','url','sender_domain','domain','sender'] if c in df.columns])
y = df['label'].astype(int)

# coerce non-numeric
non_num = X.select_dtypes(exclude=[np.number]).columns.tolist()
if non_num:
    X[non_num] = X[non_num].apply(pd.to_numeric, errors='coerce')

# --- Changed: drop all-NA columns before imputation to avoid shape mismatch ---
# keep track of columns that have at least one non-missing value
cols_with_data = [c for c in X.columns if X[c].notna().any()]
cols_all_na = [c for c in X.columns if c not in cols_with_data]
if cols_all_na:
    print("Dropping all-NA columns before imputation:", cols_all_na)

X_reduced = X[cols_with_data]

imp = SimpleImputer(strategy='median')
X_imp_vals = imp.fit_transform(X_reduced)

# Build DataFrame from actual transformed shape and columns
X_imp = pd.DataFrame(X_imp_vals, columns=cols_with_data, index=X_reduced.index)

# If you want the final feature set to include the dropped all-NA columns as zeros:
for c in cols_all_na:
    X_imp[c] = 0.0

# Reorder to original column order
X_imp = X_imp[X.columns.tolist()]

groups = df['url'].fillna('').astype(str).values if 'url' in df.columns else None
clf = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced', n_jobs=-1)
cv = GroupKFold(n_splits=5)
scores = cross_val_score(clf, X_imp, y, groups=groups, cv=cv, scoring='roc_auc', n_jobs=-1)
print('GroupKFold CV ROC AUC mean/std:', scores.mean(), scores.std(), 'scores:', scores.tolist())
os.makedirs(os.path.join(PROJECT_ROOT,'reports'), exist_ok=True)
with open(os.path.join(PROJECT_ROOT,'reports','cv_scores.json'),'w') as f:
    json.dump({'scores': [float(s) for s in scores], 'mean': float(scores.mean()), 'std': float(scores.std())}, f)
print('Saved CV results to reports/cv_scores.json')