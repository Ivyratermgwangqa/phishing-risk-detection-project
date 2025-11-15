#!/usr/bin/env python3
import os, json, joblib, numpy as np, matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, precision_recall_curve

MODEL_PATH = os.path.join('models', 'phishing_rf_model.pkl')
X_TEST_NPY = os.path.join('models', 'X_test.npy')
Y_TEST_NPY = os.path.join('models', 'y_test.npy')
OUTDIR = 'reports'
os.makedirs(OUTDIR, exist_ok=True)

if not os.path.exists(MODEL_PATH):
    raise SystemExit("Model not found: "+MODEL_PATH)
if not os.path.exists(X_TEST_NPY) or not os.path.exists(Y_TEST_NPY):
    raise SystemExit("X_test.npy / y_test.npy not found in models/. Re-run training with exports.")

model_payload = joblib.load(MODEL_PATH)
model = model_payload.get('model') if isinstance(model_payload, dict) else model_payload

X_test = np.load(X_TEST_NPY, allow_pickle=True)
y_test = np.load(Y_TEST_NPY, allow_pickle=True)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:,1] if hasattr(model, 'predict_proba') else None

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6,5)); plt.imshow(cm, cmap='Blues'); plt.colorbar(); plt.title('Confusion Matrix'); plt.xlabel('Predicted'); plt.ylabel('Actual'); plt.tight_layout()
plt.savefig(os.path.join(OUTDIR,'confusion_matrix.png'), dpi=300)
print("Saved:", os.path.join(OUTDIR,'confusion_matrix.png'))

print("\nCLASSIFICATION REPORT:\n")
print(classification_report(y_test, y_pred, digits=4))

if y_prob is not None:
    precision, recall, _ = precision_recall_curve(y_test, y_prob)
    plt.figure(figsize=(6,4)); plt.plot(recall, precision, lw=2); plt.title("Precision–Recall Curve"); plt.xlabel("Recall"); plt.ylabel("Precision"); plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR,'precision_recall_curve.png'), dpi=300)
    print("Saved:", os.path.join(OUTDIR,'precision_recall_curve.png'))
else:
    print("Model has no predict_proba; PR curve skipped.")
print("Done.")
