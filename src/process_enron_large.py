import os
import re
import ipaddress
import pandas as pd
import numpy as np
import tldextract

# Resolve project root reliably and allow override via ENRON_INPUT env var
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT = os.environ.get('ENRON_INPUT') or os.path.join(PROJECT_ROOT, 'data', 'raw', 'enron_emails', 'emails.csv')
OUT_BENIGN = os.path.join(PROJECT_ROOT, 'data', 'processed', 'benign_features.csv')
CHUNKSIZE = 10000

if not os.path.exists(INPUT):
    raise FileNotFoundError(f"Enron input not found at: {INPUT}\nSet ENRON_INPUT env var or place the file at data/raw/enron_emails/emails.csv under project root.")

# Candidate column names
BODY_CANDIDATES = ['body', 'text', 'message', 'content', 'raw', 'email']
SENDER_CANDIDATES = ['sender', 'from', 'from_addr', 'from_email', 'sender_email']

def find_col(cols, candidates):
    for c in candidates:
        if c in cols:
            return c
    # try case-insensitive
    low = {x.lower(): x for x in cols}
    for c in candidates:
        if c.lower() in low:
            return low[c.lower()]
    return None

def extract_urls(text):
    if pd.isna(text) or not text:
        return []
    return re.findall(r'https?://[^\s"\'<>]+', str(text))

def get_domain(url):
    if pd.isna(url):
        return None
    ext = tldextract.extract(str(url))
    return f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain

def has_ip(url):
    if pd.isna(url):
        return 0
    try:
        host = re.findall(r"https?://([^/]+)/?", str(url))[0].split(':')[0]
        ipaddress.ip_address(host)
        return 1
    except Exception:
        return 0

# ensure output directory
os.makedirs(os.path.dirname(OUT_BENIGN), exist_ok=True)
if os.path.exists(OUT_BENIGN):
    os.remove(OUT_BENIGN)

first_chunk = True
reader = pd.read_csv(INPUT, chunksize=CHUNKSIZE, iterator=True, dtype=str, low_memory=True)

body_col = None
sender_col = None
for i, chunk in enumerate(reader, 1):
    if body_col is None:
        body_col = find_col(chunk.columns, BODY_CANDIDATES)
    if sender_col is None:
        sender_col = find_col(chunk.columns, SENDER_CANDIDATES)

    if body_col is None:
        print("No body column found in chunk; skipping this chunk")
        continue

    chunk[body_col] = chunk[body_col].fillna('')
    chunk['urls'] = chunk[body_col].apply(extract_urls)
    chunk = chunk.explode('urls').reset_index(drop=True)
    chunk = chunk[chunk['urls'].notna() & (chunk['urls'] != '')]
    if chunk.empty:
        if i % 10 == 0:
            print(f"chunk {i}: no urls")
        continue

    df = pd.DataFrame()
    df['url'] = chunk['urls'].astype(str)
    # lexical features
    df['num_dots'] = df['url'].str.count(r'\.')
    df['num_hyphens'] = df['url'].str.count(r'-')
    df['num_underscores'] = df['url'].str.count(r'_')
    df['num_qm'] = df['url'].str.count(r'\?')
    df['has_at'] = df['url'].str.contains('@').astype(int)
    df['path_length'] = df['url'].str.replace(r'https?://[\w\.]+', '', regex=True).str.len().fillna(0).astype(int)

    # domain info
    df['domain'] = df['url'].apply(get_domain)
    df['has_ip'] = df['url'].apply(has_ip)
    df['subdomain_count'] = df['url'].apply(lambda u: max(0, str(u).split('://')[-1].count('.') - 1))

    # sender info if available
    if sender_col and sender_col in chunk.columns:
        df['sender'] = chunk[sender_col].fillna('')
        df['sender_domain'] = df['sender'].str.split('@').str[-1].where(df['sender'].str.contains('@'), np.nan)
        df['sender_domain_mismatch'] = np.where(df['sender_domain'].notna() & df['domain'].notna(),
                                                (df['sender_domain'] != df['domain']).astype(int), 0)
    else:
        df['sender'] = np.nan
        df['sender_domain'] = np.nan
        df['sender_domain_mismatch'] = 0

    df['domain_age_days'] = np.nan
    df['label'] = 0  # benign

    # write chunk to CSV
    df.to_csv(OUT_BENIGN, mode='a', header=first_chunk, index=False)
    first_chunk = False

    if i % 5 == 0:
        print(f"processed chunks: {i}")

print("Finished processing Enron. Benign features saved to:", OUT_BENIGN)