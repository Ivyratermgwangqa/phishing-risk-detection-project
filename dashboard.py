import streamlit as st
import os
st.set_page_config(page_title="Explainable Phishing Detection Dashboard", layout="wide")

MODEL_DIR = "/home/lerato/phishing-risk-detection-project/models"
st.title("Explainable Phishing Detection Dashboard")

st.header("Phishing SHAP (Top 5)")
for i in range(5):
    # fallback: list files
    import glob
    pngs = glob.glob(os.path.join(MODEL_DIR, f"phishing_shap_bar_sample_{i}_idx_*.png"))
    htmls = glob.glob(os.path.join(MODEL_DIR, f"phishing_shap_force_sample_{i}_idx_*.html"))
    if pngs:
        st.image(pngs[0], caption=os.path.basename(pngs[0]))
    if htmls:
        st.markdown(f"[Interactive plot]({htmls[0]})")

st.header("Authentication SHAP (Top 5)")
for i in range(5):
    import glob
    pngs = glob.glob(os.path.join(MODEL_DIR, f"auth_shap_bar_sample_{i}_idx_*.png"))
    htmls = glob.glob(os.path.join(MODEL_DIR, f"auth_shap_force_sample_{i}_idx_*.html"))
    if pngs:
        st.image(pngs[0], caption=os.path.basename(pngs[0]))
    if htmls:
        st.markdown(f"[Interactive plot]({htmls[0]})")

st.markdown("---")
st.markdown("Interactive HTML files open in your browser. If you run Streamlit remotely, make sure your environment can serve the 'models' directory or copy files locally.")
