# explain_shap.py
# SHAP explainability and visualization
import shap
import joblib
import pandas as pd


def explain_model(model_path: str, data_csv: str, output_plot: str):
    clf = joblib.load(model_path)
    df = pd.read_csv(data_csv)
    X = df.drop(columns=['label'])
    explainer = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(X)
    shap.summary_plot(shap_values, X, show=False)
    shap.plt.savefig(output_plot)