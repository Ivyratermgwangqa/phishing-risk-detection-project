# train_auth_risk.py
# Train authentication risk scoring model
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score


def train_risk_model(log_csv: str, model_path: str):
    df = pd.read_csv(log_csv)
    X = df[['lat','lon']]
    y = df['anomaly'].astype(int)
    clf = LogisticRegression()
    clf.fit(X, y)
    joblib.dump(clf, model_path)
    print(classification_report(y, clf.predict(X)))
    print("ROC AUC:", roc_auc_score(y, clf.predict_proba(X)[:,1]))