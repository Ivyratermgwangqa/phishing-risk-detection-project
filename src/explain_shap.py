# explain_shap.py
# SHAP explainability and visualization
import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt


def explain_model(model_path: str, data_csv: str, output_plot: str):
    clf = joblib.load(model_path)
    df = pd.read_csv(data_csv)
    X = df.drop(columns=['label'])
    # TreeExplainer works for tree-based models; fallback to KernelExplainer otherwise
    try:
        explainer = shap.TreeExplainer(clf)
    except Exception:
        explainer = shap.KernelExplainer(lambda x: clf.predict_proba(x)[:, 1], X.sample(100))
    shap_values = explainer.shap_values(X)
    plt.figure()
    shap.summary_plot(shap_values, X, show=False)
    plt.savefig(output_plot)