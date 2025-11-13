# enrich_virustotal.py (enhanced)
import os, time, json, random, tempfile, requests, pandas as pd
from typing import Dict, Any

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPATH = os.environ.get('ALL_FEATURES') or os.path.join(PROJECT_ROOT, 'data', 'processed', 'phishing_graph_features.csv')
OUTPATH = os.path.join(PROJECT_ROOT, 'data', 'processed', 'phishing_graph_features_vt.csv')
CACHE = os.path.join(PROJECT_ROOT, 'data', 'processed', 'vt_cache.json')
AUDIT = os.path.join(PROJECT_ROOT, 'data', 'processed', 'vt_audit.jsonl')

VT_API_KEY = os.environ.get('VT_API_KEY')
if not VT_API_KEY:
    print("VT_API_KEY not set — skipping VirusTotal enrichment.")
    raise SystemExit(0)

DEFAULT_RATE_LIMIT_DELAY = float(os.environ.get("VT_RATE_DELAY", "15.0"))
SAVE_EVERY = int(os.environ.get("VT_SAVE_EVERY", "50"))
MAX_RETRIES = int(os.environ.get("VT_MAX_RETRIES", "3"))

def atomic_write(path: str, data: Any, mode: str = 'w', ensure_dir: bool = True):
    if ensure_dir:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path))
    try:
        with os.fdopen(fd, mode) as f:
            if isinstance(data, (dict, list)):
                json.dump(data, f)
            else:
                f.write(data)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try: os.remove(tmp)
            except Exception: pass

# --- Load dataset
df = pd.read_csv(INPATH)
if 'domain' not in df.columns:
    print("No 'domain' column found in input — nothing to enrich.")
    df.to_csv(OUTPATH, index=False)
    raise SystemExit(0)

domains = pd.Series(df['domain'].dropna().unique()).astype(str).tolist()

# --- Load cache
if os.path.exists(CACHE):
    try:
        with open(CACHE, 'r') as f:
            cache: Dict[str, Any] = json.load(f)
    except Exception:
        cache = {}
else:
    cache = {}

os.makedirs(os.path.dirname(AUDIT), exist_ok=True)
audit_fh = open(AUDIT, 'a', buffering=1)

session = requests.Session()
session.headers.update({"x-apikey": VT_API_KEY, "Accept": "application/json"})
base = "https://www.virustotal.com/api/v3/domains/{}"

def write_audit(rec: Dict[str, Any]):
    try:
        audit_fh.write(json.dumps(rec, default=str) + "\n")
    except Exception:
        pass

def fetch_domain(domain: str) -> Dict[str, Any]:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(base.format(domain), timeout=30)
            if resp.status_code == 200:
                data = resp.json().get('data', {}).get('attributes', {})
                stats = data.get('last_analysis_stats', {})
                rec = {
                    "query": domain,
                    "timestamp": int(time.time()),
                    "client_action": "report_fetch",
                    "vt_status_code": resp.status_code,
                    "vt_response_summary": {
                        "malicious_votes": stats.get("malicious", 0),
                        "suspicious_votes": stats.get("suspicious", 0)
                    },
                    "error": None
                }
                write_audit(rec)
                return {
                    "last_analysis_stats": stats,
                    "reputation": data.get("reputation"),
                    "last_analysis_date": data.get("last_analysis_date")
                }

            elif resp.status_code == 429:
                backoff = DEFAULT_RATE_LIMIT_DELAY * (2 ** (attempt - 1)) * random.uniform(0.5, 1.5)
                write_audit({
                    "query": domain, "timestamp": int(time.time()),
                    "client_action": "rate_limited", "vt_status_code": resp.status_code,
                    "wait_seconds": backoff
                })
                time.sleep(backoff)
                continue
            else:
                err = {
                    "query": domain, "timestamp": int(time.time()),
                    "client_action": "report_fetch",
                    "vt_status_code": resp.status_code,
                    "error_text": resp.text[:200]
                }
                write_audit(err)
                return {"error": f"status_{resp.status_code}"}
        except requests.RequestException as e:
            if attempt == MAX_RETRIES:
                write_audit({"query": domain, "timestamp": int(time.time()), "client_action": "exception", "error": str(e)})
                return {"error": str(e)}
            time.sleep(DEFAULT_RATE_LIMIT_DELAY * (2 ** (attempt - 1)) * random.uniform(0.5, 1.5))
    return {"error": "max_retries_exceeded"}

# --- Fetch and cache loop
processed = 0
try:
    for i, domain in enumerate(domains, start=1):
        if domain in cache and "last_analysis_stats" in cache[domain]:
            continue
        info = fetch_domain(domain)
        cache[domain] = info
        processed += 1
        if processed % 10 == 0:
            print(f"[{i}/{len(domains)}] {processed} new lookups done...")
        time.sleep(DEFAULT_RATE_LIMIT_DELAY)
        if processed and processed % SAVE_EVERY == 0:
            atomic_write(CACHE, cache)
            print(f"Processed {processed} new domains — cache saved.")
except KeyboardInterrupt:
    print("Interrupted — flushing cache.")
finally:
    atomic_write(CACHE, cache)
    audit_fh.close()

# --- Merge VT stats into dataframe
def vt_fields(domain):
    if pd.isna(domain): return (0, 0, 0, "Unknown")
    info = cache.get(str(domain), {})
    stats = info.get("last_analysis_stats", {}) or {}
    mal, susp = int(stats.get("malicious", 0) or 0), int(stats.get("suspicious", 0) or 0)
    if mal >= 5:
        score, flag = 2, "Malicious (VT)"
    elif mal > 0 or susp > 0:
        score, flag = 1, "Suspicious (VT)"
    else:
        score, flag = 0, "Benign"
    return (mal, susp, score, flag)

df[["vt_malicious_votes", "vt_suspicious_votes", "vt_threat_score", "vt_threat_flag"]] = (
    df["domain"].apply(vt_fields).apply(pd.Series)
)

df.to_csv(OUTPATH, index=False)
print("VirusTotal enrichment complete ✅ →", OUTPATH)