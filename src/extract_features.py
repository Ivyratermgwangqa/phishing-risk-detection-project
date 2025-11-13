# extract_features.py
# Lexical, WHOIS, and VirusTotal threat intelligence extraction
import re
import whois
import pandas as pd
import urllib.parse
import tldextract
import logging
import json
import os
from typing import Optional

try:
    # when imported as a package (e.g. `import src.extract_features`)
    from .utils import extract_urls, parse_domain_age
except Exception:
    # when run as a script (e.g. `python src/extract_features.py`)
    from utils import extract_urls, parse_domain_age

logging.basicConfig(level=logging.INFO)

# -----------------------------------------------------------
# 🧩 VIRUSTOTAL MERGE FUNCTION
# -----------------------------------------------------------
def merge_virustotal_features(df, vt_cache_path="data/processed/vt_cache.json"):
    """Merge cached VirusTotal intelligence into feature dataframe."""
    if not os.path.exists(vt_cache_path):
        print("⚠️ VT cache not found — skipping VirusTotal enrichment.")
        df["vt_malicious_votes"] = 0
        df["vt_suspicious_votes"] = 0
        df["vt_threat_score"] = 0
        df["vt_threat_flag"] = "Unknown"
        return df

    print("🔍 Merging VirusTotal intelligence from cache...")
    with open(vt_cache_path, "r") as f:
        cache = json.load(f)

    def vt_fields(domain):
        if pd.isna(domain):
            return (0, 0, 0, "Unknown")
        info = cache.get(str(domain), {})
        stats = info.get("last_analysis_stats", {}) or {}
        mal = int(stats.get("malicious", 0) or 0)
        susp = int(stats.get("suspicious", 0) or 0)

        # Threat classification based on VT votes
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

    print("✅ VirusTotal enrichment complete — columns added:")
    print("   → vt_malicious_votes, vt_suspicious_votes, vt_threat_score, vt_threat_flag")
    return df


# -----------------------------------------------------------
# 🌐 URL FEATURE EXTRACTION
# -----------------------------------------------------------
def _normalize_and_extract(url: str):
    try:
        p = urllib.parse.urlparse(url)
        host = p.hostname or ''
        domain = tldextract.extract(host).registered_domain
        path_len = len(p.path or '')
        query_len = len(p.query or '')
        return {
            'scheme': p.scheme,
            'host': host,
            'domain': domain,
            'path_len': path_len,
            'query_len': query_len,
            'url_len': len(url or '')
        }
    except Exception:
        return {
            'scheme': None,
            'host': None,
            'domain': None,
            'path_len': 0,
            'query_len': 0,
            'url_len': len(url or '')
        }


def extract_url_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract URL lexical and metadata features from column `url`.

    Returns a new DataFrame with appended columns: domain, path_len, query_len, url_len, scheme.
    """
    df = df.copy()
    cols = ['domain', 'path_len', 'query_len', 'url_len', 'scheme', 'host']
    for c in cols:
        df[c] = None

    for idx, row in df.iterrows():
        url = row.get('url')
        if not url:
            continue
        info = _normalize_and_extract(url)
        for k, v in info.items():
            df.at[idx, k] = v

    # 🔗 Add VirusTotal threat intelligence (if available)
    df = merge_virustotal_features(df)
    return df


# -----------------------------------------------------------
# 🧾 WHOIS AGE PARSER
# -----------------------------------------------------------
def parse_whois_age(domain: str) -> int:
    """Return domain age in days, or -1 on failure."""
    try:
        info = whois.whois(domain)
        date = info.creation_date
        if date is None:
            return -1
        if isinstance(date, list):
            date = date[0]
        ts = pd.to_datetime(date)
        return int((pd.Timestamp.now(tz=ts.tz) - ts).days)
    except Exception as e:
        logging.debug('whois lookup failed for %s: %s', domain, e)
        return -1


# -----------------------------------------------------------
# 🧮 SCRIPT MODE
# -----------------------------------------------------------
if __name__ == '__main__':
    try:
        from . import config
    except Exception:
        import config

    import argparse
    parser = argparse.ArgumentParser(description='Extract URL features (and merge VirusTotal intelligence)')
    parser.add_argument('--input', '-i', help='Input CSV path', default=getattr(config, 'PHISHTANK_CSV', 'data/raw/phishtank_urls.csv'))
    parser.add_argument('--output', '-o', help='Output CSV path', default=os.path.join('data', 'processed', 'url_features_vt.csv'))
    parser.add_argument('--sample', '-n', type=int, default=1000, help='Number of rows to process (0 = full, chunked)')
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)

    df = pd.read_csv(args.input, nrows=args.sample if args.sample > 0 else None)
    out = extract_url_features(df)
    out.to_csv(args.output, index=False)
    print(f'💾 Wrote {len(out)} rows to {args.output}')