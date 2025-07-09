# train_detector.py
# Train RandomForest phishing detection model
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score


def train_phishing_model(feature_csv: str, model_path: str):
    df = pd.read_csv(feature_csv)
    X = df.drop(columns=['label'])
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    joblib.dump(clf, model_path)
    print(classification_report(y_test, clf.predict(X_test)))
    print("ROC AUC:", roc_auc_score(y_test, clf.predict_proba(X_test)[:,1]))
