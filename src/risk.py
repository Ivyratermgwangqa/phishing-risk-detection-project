# risk.py
import os
import joblib
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# === Resolve Project Paths ===
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
MODEL_DIR = os.path.join(PROJECT_ROOT, 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

PHISH_FEATURES_CSV = os.path.join(DATA_DIR, 'phishing_graph_features.csv')
AUTH_LOGS_CSV = os.path.join(DATA_DIR, 'auth_logs.csv')
PHISH_MODEL_PATH = os.path.join(MODEL_DIR, 'phishing_rf_model.pkl')
FEATURES_PATH = os.path.join(MODEL_DIR, 'feature_names.json')
AUTH_MODEL_PATH = os.path.join(MODEL_DIR, 'auth_risk_model.pkl')


class PhishingDetectionFramework:
    """
    Explainable Phishing Detection Framework with:
      - multi-sample SHAP generation (PNG + interactive HTML)
      - threat-intel enrichment (annotation-only)
      - Streamlit dashboard file generation
    """

    def __init__(self):
        print("Loading trained models and datasets...")

        # === Load Phishing Model ===
        ph_payload = joblib.load(PHISH_MODEL_PATH)
        if isinstance(ph_payload, dict):
            self.phish_model = ph_payload.get('model')
            self.phish_imputer = ph_payload.get('imputer', None)
        else:
            self.phish_model = ph_payload
            self.phish_imputer = None

        # === Load Expected Feature Names ===
        if os.path.exists(FEATURES_PATH):
            try:
                with open(FEATURES_PATH, 'r') as f:
                    self.phish_feature_names = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load feature names ({e})")
                self.phish_feature_names = None
        else:
            self.phish_feature_names = None

        # === Load Feature Table ===
        if os.path.exists(PHISH_FEATURES_CSV):
            self.phish_features = pd.read_csv(PHISH_FEATURES_CSV)
        else:
            raise FileNotFoundError(f"Missing phishing features CSV at {PHISH_FEATURES_CSV}")

        # === Load Authentication Model (Optional) ===
        if os.path.exists(AUTH_MODEL_PATH) and os.path.exists(AUTH_LOGS_CSV):
            auth_payload = joblib.load(AUTH_MODEL_PATH)
            if isinstance(auth_payload, dict):
                self.auth_model = auth_payload.get('model')
                self.auth_imputer = auth_payload.get('imputer', None)
            else:
                self.auth_model = auth_payload
                self.auth_imputer = None
            self.auth_logs = pd.read_csv(AUTH_LOGS_CSV)
        else:
            self.auth_model = None
            self.auth_logs = None

        # place-holders for predictions (populated after predict_* calls)
        self.phish_preds = None
        self.phish_probs = None
        self.auth_preds = None
        self.auth_probs = None

    # === Helper: Choose appropriate SHAP explainer ===
    def get_shap_explainer(self, model, background_data):
        import shap
        model_name = type(model).__name__.lower()
        # tree-based
        if "forest" in model_name or "boost" in model_name or "xgboost" in model_name or "catboost" in model_name or "lgbm" in model_name or "tree" in model_name:
            return shap.TreeExplainer(model, feature_perturbation="interventional")
        # linear/logistic
        elif "logistic" in model_name or "linear" in model_name or "regression" in model_name:
            # LinearExplainer sometimes expects background data (or None)
            try:
                return shap.LinearExplainer(model, background_data, feature_perturbation="interventional")
            except Exception:
                return shap.LinearExplainer(model, feature_perturbation="interventional")
        # fallback
        else:
            return shap.Explainer(model, background_data)

    # === Threat Intel Enrichment (annotation-only) ===
    def enrich_with_threat_intel(self, df, domain_col="sender_domain"):
        """
        Enrich DataFrame with threat intelligence from VirusTotal cache/audit logs.
        Requires 'vt_cache.json' or 'vt_audit.jsonl' in data/processed.
        Adds: 'vt_malicious', 'vt_suspicious', 'threat_score', 'threat_flag'.
        """
        vt_cache_path = os.path.join(DATA_DIR, "vt_cache.json")
        vt_audit_path = os.path.join(DATA_DIR, "vt_audit.jsonl")

        vt_data = {}

        # --- Load VirusTotal data (cache preferred) ---
        if os.path.exists(vt_cache_path):
            try:
                with open(vt_cache_path, "r") as f:
                    vt_data = json.load(f)
            except Exception as e:
                print(f"Warning: Could not read vt_cache.json ({e})")

        elif os.path.exists(vt_audit_path):
            try:
                with open(vt_audit_path, "r") as f:
                    for line in f:
                        rec = json.loads(line)
                        d = rec.get("query")
                        summ = rec.get("vt_response_summary", {})
                        if d:
                            vt_data[d.lower()] = summ
            except Exception as e:
                print(f"Warning: Could not read vt_audit.jsonl ({e})")

        # --- Apply enrichment ---
        def lookup(domain):
            if pd.isna(domain):
                return (0, 0, 0, "Unknown")

            key = str(domain).lower()
            vt_entry = vt_data.get(key)
            if vt_entry:
                mal = vt_entry.get("malicious_votes", 0)
                susp = vt_entry.get("suspicious_votes", 0)
            else:
                mal = susp = 0

            # threat scoring heuristic
            if mal >= 5:
                score, flag = 2, "Malicious (VT)"
            elif mal > 0 or susp > 0:
                score, flag = 1, "Suspicious (VT)"
            else:
                score, flag = 0, "Benign"
            return (mal, susp, score, flag)

        out = df.copy()
        res = out[domain_col].apply(lookup).apply(pd.Series)
        res.columns = ["vt_malicious", "vt_suspicious", "threat_score", "threat_flag"]
        out = pd.concat([out, res], axis=1)
        return out


    # === PHISHING PREDICTION ===
    def predict_phishing(self, X=None):
        """Predict phishing risk using the loaded model."""
        if X is None:
            if self.phish_feature_names:
                feats = list(self.phish_feature_names)
                X_raw = pd.DataFrame(index=self.phish_features.index)
                for f in feats:
                    if f in self.phish_features.columns:
                        X_raw[f] = self.phish_features[f]
                    else:
                        X_raw[f] = np.nan
                X_raw = X_raw.apply(pd.to_numeric, errors='coerce')
            else:
                X_raw = self.phish_features.select_dtypes(include=[np.number]).drop(columns=['label'], errors='ignore').fillna(0)
        else:
            X_raw = X.copy()

        # keep a copy of raw features for enrichment/annotation only
        self.phish_features_raw = X_raw.copy()

        if self.phish_imputer is not None:
            if self.phish_feature_names:
                X_proc_in = X_raw[self.phish_feature_names]
            else:
                X_proc_in = X_raw
            X_proc = pd.DataFrame(
                self.phish_imputer.transform(X_proc_in),
                columns=X_proc_in.columns,
                index=X_proc_in.index
            )
        else:
            X_proc = X_raw.fillna(0)

        if hasattr(self.phish_model, "feature_names_in_"):
            missing = set(self.phish_model.feature_names_in_) - set(X_proc.columns)
            for f in missing:
                X_proc[f] = 0
            X_proc = X_proc[self.phish_model.feature_names_in_]

        preds = self.phish_model.predict(X_proc)
        probs = self.phish_model.predict_proba(X_proc)[:, 1] if hasattr(self.phish_model, 'predict_proba') else preds

        # store
        self.phish_preds = preds
        self.phish_probs = probs
        self.phish_features_proc = X_proc

        return preds, probs

    # === AUTHENTICATION RISK PREDICTION ===
    def predict_auth_risk(self, X=None):
        """Predict authentication risk using the loaded model."""
        if self.auth_model is None or self.auth_logs is None:
            print("Auth model or logs not loaded.")
            return None, None

        features = ['distance_km', 'login_hour', 'new_device']
        if X is None:
            X_raw = self.auth_logs[features].copy()
        else:
            X_raw = X[features].copy()

        if self.auth_imputer is not None:
            X_proc = pd.DataFrame(self.auth_imputer.transform(X_raw), columns=X_raw.columns, index=X_raw.index)
        else:
            X_proc = X_raw.fillna(0)

        preds = self.auth_model.predict(X_proc)
        probs = self.auth_model.predict_proba(X_proc)[:, 1] if hasattr(self.auth_model, 'predict_proba') else preds

        # store
        self.auth_preds = preds
        self.auth_probs = probs
        self.auth_features_proc = X_proc

        return preds, probs

    # === Generate SHAP for multiple top-risk samples ===
    def explain_top_samples(self, model_type="phishing", top_n=5, save_png=True, save_html=True):
        """
        Generate SHAP PNG + interactive HTML for top_n risky samples of model_type.
        model_type: "phishing" or "auth"
        """
        import shap

        if model_type == "phishing":
            if self.phish_model is None or self.phish_probs is None or self.phish_features_proc is None:
                raise RuntimeError("Please run predict_phishing() before explain_top_samples('phishing').")
            model = self.phish_model
            X = self.phish_features_proc
            probs = np.asarray(self.phish_probs)
            out_prefix = "phishing_shap"
            # optional annotation: original rows (for linking domain/email)
            raw = getattr(self, "phish_features_raw", None)
        elif model_type == "auth":
            if self.auth_model is None or self.auth_probs is None or self.auth_features_proc is None:
                raise RuntimeError("Please run predict_auth_risk() before explain_top_samples('auth').")
            model = self.auth_model
            X = self.auth_features_proc
            probs = np.asarray(self.auth_probs)
            out_prefix = "auth_shap"
            raw = getattr(self, "auth_logs", None)
        else:
            raise ValueError("model_type must be 'phishing' or 'auth'.")

        n_samples = len(probs)
        if n_samples == 0:
            print("No samples to explain.")
            return

        # find indices of top-n highest probability (risky) samples
        top_idx = np.argsort(probs)[-top_n:][::-1]
        top_idx = [int(i) for i in top_idx]

        # background data: use sample of X (or X itself if small)
        background = X.sample(n=min(200, len(X)), random_state=42)

        explainer = self.get_shap_explainer(model, background)
        shap_values = explainer.shap_values(X.iloc[top_idx])

        # Normalize various SHAP return shapes into array (n_samples, n_features)
        def _normalize_shap_batch(sv, n_samples, n_features):
            import numpy as _np
            # list per-class -> pick positive class if present
            if isinstance(sv, list):
                idx = 1 if len(sv) > 1 else 0
                arr = _np.asarray(sv[idx])
            else:
                arr = _np.asarray(sv)

            # common: (n_samples, n_features)
            if arr.ndim == 2 and arr.shape[0] == n_samples and arr.shape[1] >= n_features:
                return arr[:, :n_features]

            # case: (n_features, n_classes) -> pick positive class column -> shape (1, n_features)
            if arr.ndim == 2 and arr.shape[0] == n_features and arr.shape[1] > 1:
                col = 1 if arr.shape[1] > 1 else 0
                return arr[:, col].reshape(1, -1)

            # single-sample vector (n_features,)
            if arr.ndim == 1 and arr.shape[0] == n_features:
                return arr.reshape(1, -1)

            # fallback: flatten and pad/truncate to (n_samples * n_features)
            flat = arr.flatten()
            total = n_samples * n_features
            if flat.size >= total:
                flat = flat[:total]
            else:
                pad = _np.zeros(total - flat.size)
                flat = _np.concatenate([flat, pad])
            return flat.reshape(n_samples, n_features)

        sv = _normalize_shap_batch(shap_values, n_samples=len(top_idx), n_features=X.shape[1])

        # For each top sample, save PNG and HTML
        for i, row_idx in enumerate(top_idx):
            try:
                sv_i = sv[i]
            except Exception:
                # fallback: try to index from full X
                sv_i = sv if sv.shape[0] == 1 else sv[i % sv.shape[0]]

            sample_X = X.iloc[[row_idx]]
            # --- PNG bar plot (single-sample SHAP sorted by absolute impact) ---
            # Build series aligned to feature names
            feat_names = list(sample_X.columns)
            try:
                s = pd.Series(np.asarray(sv_i).reshape(-1)[:len(feat_names)], index=feat_names)
            except Exception:
                # last-resort: zero-pad/truncate
                tmp = np.asarray(sv_i).reshape(-1)
                if tmp.shape[0] < len(feat_names):
                    pad = np.zeros(len(feat_names) - tmp.shape[0])
                    tmp = np.hstack([tmp, pad])
                s = pd.Series(tmp[:len(feat_names)], index=feat_names)

            TOP_K = min(20, len(s))
            top_feats = s.abs().sort_values(ascending=False).head(TOP_K).index
            plot_vals = s.loc[top_feats]

            plt.figure(figsize=(8, max(4, 0.25 * TOP_K)))
            # color by sign
            colors = ['#d62728' if v < 0 else '#1f77b4' for v in plot_vals.values]
            plot_vals.sort_values().plot.barh(color=colors)
            plt.xlabel("SHAP value (impact on model output)")
            plt.title(f"{model_type.title()} SHAP Top-{i+1} (idx={row_idx})")
            plt.tight_layout()
            out_png = os.path.join(MODEL_DIR, f"{out_prefix}_bar_sample_{i}_idx_{row_idx}.png")
            if save_png:
                plt.savefig(out_png, bbox_inches='tight')
                print(f"Saved PNG: {out_png}")
            plt.close()

            # --- Interactive HTML force plot (best-effort) ---
            if save_html:
                try:
                    ev = explainer.expected_value
                    # pick class expected value if array-like
                    if hasattr(ev, "__len__") and not np.isscalar(ev):
                        # if returned as array per-class, try second element (positive class) else first
                        ev_use = ev[1] if len(ev) > 1 else ev[0]
                    else:
                        ev_use = float(ev)
                    # shap.force_plot accepts 1D shap values for single sample
                    import shap as _shap
                    fp = _shap.force_plot(ev_use, sv_i, sample_X, matplotlib=False)
                    out_html = os.path.join(MODEL_DIR, f"{out_prefix}_force_sample_{i}_idx_{row_idx}.html")
                    try:
                        _shap.save_html(out_html, fp)
                    except Exception:
                        # sometimes shap.save_html fails for unusual fp objects -> fallback to string
                        with open(out_html, "w") as fh:
                            fh.write(str(fp))
                    print(f"Saved interactive HTML: {out_html}")
                except Exception as e:
                    print(f"Could not save interactive HTML for sample idx {row_idx}: {e}")

            # Optionally annotate with threat intel if raw data present
            if raw is not None and model_type == "phishing":
                try:
                    raw_row = raw.iloc[row_idx:row_idx+1]
                    annotated = self.enrich_with_threat_intel(raw_row)
                    # save annotation CSV for this sample
                    ann_path = os.path.join(MODEL_DIR, f"{out_prefix}_sample_{i}_idx_{row_idx}_annot.csv")
                    annotated.to_csv(ann_path, index=False)
                except Exception:
                    pass

    # === Convenience: generate a Streamlit dashboard file that displays saved PNGs ===
    def write_streamlit_dashboard(self, out_path=None, phishing_n=5, auth_n=5):
        """
        Writes a minimal Streamlit app 'dashboard.py' to PROJECT_ROOT (or out_path if provided).
        The generated dashboard displays PNGs created by explain_top_samples and links to HTML interactive plots.
        """
        if out_path is None:
            out_path = os.path.join(PROJECT_ROOT, "dashboard.py")

        # avoid backslashes inside f-string expressions by pre-encoding the path
        import json
        model_dir_json = json.dumps(MODEL_DIR)
        template = f'''\
import streamlit as st
import os
st.set_page_config(page_title="Explainable Phishing Detection Dashboard", layout="wide")

MODEL_DIR = {model_dir_json}
st.title("Explainable Phishing Detection Dashboard")

st.header("Phishing SHAP (Top {phishing_n})")
for i in range({phishing_n}):
    # fallback: list files
    import glob
    pngs = glob.glob(os.path.join(MODEL_DIR, f"phishing_shap_bar_sample_{{i}}_idx_*.png"))
    htmls = glob.glob(os.path.join(MODEL_DIR, f"phishing_shap_force_sample_{{i}}_idx_*.html"))
    if pngs:
        st.image(pngs[0], caption=os.path.basename(pngs[0]))
    if htmls:
        st.markdown(f"[Interactive plot]({{htmls[0]}})")

st.header("Authentication SHAP (Top {auth_n})")
for i in range({auth_n}):
    import glob
    pngs = glob.glob(os.path.join(MODEL_DIR, f"auth_shap_bar_sample_{{i}}_idx_*.png"))
    htmls = glob.glob(os.path.join(MODEL_DIR, f"auth_shap_force_sample_{{i}}_idx_*.html"))
    if pngs:
        st.image(pngs[0], caption=os.path.basename(pngs[0]))
    if htmls:
        st.markdown(f"[Interactive plot]({{htmls[0]}})")

st.markdown("---")
st.markdown("Interactive HTML files open in your browser. If you run Streamlit remotely, make sure your environment can serve the 'models' directory or copy files locally.")
'''
        with open(out_path, "w") as fh:
            fh.write(template)
        print(f"Wrote Streamlit dashboard to: {out_path}")

    # === SINGLE SAMPLE PREDICTION ===
    def predict_single(self, input_row: dict, domain_field="sender_domain", return_shap=True, save_artifacts=False):
        """
        Predict phishing risk for a single input (input_row is a dict of feature values or identifiers).
        - input_row: e.g. {"url": "...", "sender": "...", "sender_domain": "...", "url_length": 123, ...}
        - domain_field: which key contains domain to use for threat-intel lookup
        Returns a dict with prediction, probability, threat intel annotation and (optionally) SHAP values.
        """
        # helper to extract domain from URL if domain not provided
        from urllib.parse import urlparse
        input_copy = dict(input_row)

        if domain_field not in input_copy or not input_copy.get(domain_field):
            url = input_copy.get("url") or input_copy.get("link")
            if url:
                try:
                    parsed = urlparse(url)
                    hostname = parsed.hostname or ""
                    input_copy[domain_field] = hostname
                except Exception:
                    input_copy[domain_field] = ""

        # Build a DataFrame aligned to the training feature manifest if available
        if self.phish_feature_names:
            cols = list(self.phish_feature_names)
        else:
            # fall back: use numeric columns from loaded feature table (minus label)
            cols = [c for c in self.phish_features.select_dtypes(include=[np.number]).columns if c != "label"]

        X_raw = pd.DataFrame(index=[0], columns=cols)
        for c in cols:
            if c in input_copy:
                X_raw.at[0, c] = input_copy[c]
            else:
                X_raw.at[0, c] = np.nan

        X_raw = X_raw.apply(pd.to_numeric, errors='coerce')

        # keep raw copy for annotation
        raw_for_annotation = X_raw.copy()
        # impute / process
        if self.phish_imputer is not None:
            X_proc_in = X_raw[self.phish_feature_names] if self.phish_feature_names else X_raw
            X_proc = pd.DataFrame(self.phish_imputer.transform(X_proc_in), columns=X_proc_in.columns, index=X_proc_in.index)
        else:
            X_proc = X_raw.fillna(0)

        # align to model expected feature order
        if hasattr(self.phish_model, "feature_names_in_"):
            for f in self.phish_model.feature_names_in_:
                if f not in X_proc.columns:
                    X_proc[f] = 0
            X_proc = X_proc[self.phish_model.feature_names_in_]

        pred = int(self.phish_model.predict(X_proc)[0])
        prob = float(self.phish_model.predict_proba(X_proc)[:, 1][0]) if hasattr(self.phish_model, "predict_proba") else float(pred)

        # threat intel enrichment (annotation-only)
        try:
            ann_df = self.enrich_with_threat_intel(raw_for_annotation, domain_col=domain_field)
            ann = ann_df.iloc[0].to_dict()
        except Exception:
            ann = {"vt_malicious": 0, "vt_suspicious": 0, "threat_score": 0, "threat_flag": "Unknown"}

        result = {
            "prediction": pred,
            "probability": prob,
            "annotation": ann,
            "input": input_copy
        }

        # SHAP (optional) - robust normalization of various shap return shapes
        if return_shap:
            try:
                background = self.phish_features_proc.sample(n=min(200, len(self.phish_features_proc)), random_state=42) if hasattr(self, "phish_features_proc") else X_proc
                expl = self.get_shap_explainer(self.phish_model, background)
                raw_sv = expl.shap_values(X_proc)

                # normalize shap values to a 1D array of length n_features for this single sample
                def _normalize_shap(sv, n_features):
                    # case: list per class -> pick positive class if available
                    if isinstance(sv, list):
                        # prefer index 1 (positive class) if present
                        idx = 1 if len(sv) > 1 else 0
                        arr = np.asarray(sv[idx])
                        # expected shape (n_samples, n_features)
                        if arr.ndim == 2:
                            return arr[0]
                        # fallback: if (n_features, ) return directly
                        if arr.ndim == 1 and arr.shape[0] == n_features:
                            return arr
                    # case: ndarray
                    arr = np.asarray(sv)
                    if arr.ndim == 2:
                        # common shapes:
                        # (n_samples, n_features) -> take first row
                        if arr.shape[0] == 1:
                            return arr[0]
                        # (n_features, n_classes) -> choose positive class column if exists
                        if arr.shape[0] == n_features and arr.shape[1] > 1:
                            return arr[:, 1]
                        # (n_features, ) as 2-D with second dim 1
                        if arr.shape[1] == 1 and arr.shape[0] == n_features:
                            return arr[:, 0]
                        # (n_samples, n_features) fallback: take first row
                        return arr[0]
                    if arr.ndim == 1 and arr.shape[0] == n_features:
                        return arr
                    # unknown shape: attempt flatten and truncate/pad
                    flat = arr.flatten()
                    if flat.size >= n_features:
                        return flat[:n_features]
                    # pad with zeros
                    pad = np.zeros(n_features - flat.size)
                    return np.concatenate([flat, pad])

                sv_use = _normalize_shap(raw_sv, X_proc.shape[1])

                feat_names = list(X_proc.columns)
                shap_series = pd.Series(sv_use[:len(feat_names)], index=feat_names).sort_values(key=lambda s: s.abs(), ascending=False)
                result["shap_values"] = shap_series.head(20).to_dict()

                if save_artifacts:
                    import matplotlib.pyplot as plt
                    vals = shap_series.head(20).sort_values()
                    plt.figure(figsize=(8, max(3, 0.25 * len(vals))))
                    colors = ['#d62728' if v < 0 else '#1f77b4' for v in vals.values]
                    vals.plot.barh(color=colors)
                    plt.xlabel("SHAP value (impact)")
                    plt.title(f"Single-sample SHAP (prob={prob:.4f})")
                    plt.tight_layout()
                    png_path = os.path.join(MODEL_DIR, "shap_single_sample.png")
                    plt.savefig(png_path, bbox_inches="tight")
                    plt.close()
                    result["shap_png"] = png_path
            except Exception as e:
                result["shap_error"] = str(e)

        return result

# === Example Usage ===
if __name__ == "__main__":
    print("=== Explainable Phishing Detection Framework ===")
    print("Initializing framework...")

    framework = PhishingDetectionFramework()

    # interactive quick-predict mode if environment variable set
    if os.environ.get("SINGLE_PREDICT") == "1":
        # prompt user for minimal inputs
        print("Interactive single-sample prediction mode.")
        url = input("Enter URL (or press Enter to skip): ").strip()
        sender = input("Enter sender email (or press Enter to skip): ").strip()
        domain = input("Enter domain (optional, will be extracted from URL if blank): ").strip()
        inp = {}
        if url:
            inp["url"] = url
        if sender:
            inp["sender"] = sender
            # derive sender_domain if possible
            try:
                inp["sender_domain"] = sender.split("@", 1)[1]
            except Exception:
                pass
        if domain:
            inp["sender_domain"] = domain
        # call single predict (do not save artifacts by default)
        res = framework.predict_single(inp, domain_field="sender_domain", return_shap=True, save_artifacts=False)
        print("\nPrediction result:")
        print(f"  - Predicted label: {res['prediction']}")
        print(f"  - Probability: {res['probability']:.4f}")
        print(f"  - Threat intel: {res['annotation']}")
        if "shap_values" in res:
            print("  - Top SHAP contributors:")
            for k, v in list(res["shap_values"].items())[:10]:
                print(f"    {k}: {v:.4f}")
        else:
            print("  - SHAP not available:", res.get("shap_error"))
        raise SystemExit(0)

    # 1) Predictions
    print("\nPhishing model predictions on loaded features:")
    preds, probs = framework.predict_phishing()
    print(pd.Series(preds).value_counts())
    print("Sample predicted probabilities:", np.asarray(probs)[:5])

    if framework.auth_model is not None:
        print("\nAuth risk model predictions on loaded logs:")
        apreds, aprobs = framework.predict_auth_risk()
        print(pd.Series(apreds).value_counts())
        print("Sample auth risk probabilities:", np.asarray(aprobs)[:5])

    # 2) Generate SHAP explanations for top samples (both models)
    TOP_N = 5
    print(f"\nGenerating SHAP explanations for top {TOP_N} phishing samples...")
    try:
        framework.explain_top_samples(model_type="phishing", top_n=TOP_N, save_png=True, save_html=True)
    except Exception as e:
        print("Error generating phishing SHAP explanations:", e)

    if framework.auth_model is not None:
        print(f"\nGenerating SHAP explanations for top {TOP_N} auth samples...")
        try:
            framework.explain_top_samples(model_type="auth", top_n=TOP_N, save_png=True, save_html=True)
        except Exception as e:
            print("Error generating auth SHAP explanations:", e)

    # 3) Write Streamlit dashboard scaffold
    try:
        framework.write_streamlit_dashboard(phishing_n=TOP_N, auth_n=TOP_N)
    except Exception as e:
        print("Could not write dashboard file:", e)

    print("\nDone. See outputs in the 'models' directory:")
    print(" - PNG files: phishing_shap_bar_sample_*.png, auth_shap_bar_sample_*.png")
    print(" - Interactive HTMLs: phishing_shap_force_sample_*.html, auth_shap_force_sample_*.html")
    print(" - Dashboard script: dashboard.py (run with: streamlit run dashboard.py)")