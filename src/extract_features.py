# extract_features.py
# Lexical & metadata extraction (URLs, WHOIS, etc.)
import re
import whois
import pandas as pd
import urllib.parse
import tldextract
import logging
from typing import Optional

try:
    # when imported as a package (e.g. `import src.extract_features`)
    from .utils import extract_urls, parse_domain_age
except Exception:
    # when run as a script (e.g. `python src/extract_features.py`)
    from utils import extract_urls, parse_domain_age

logging.basicConfig(level=logging.INFO)


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

    return df


def parse_whois_age(domain: str) -> int:
    """Return domain age in days, or -1 on failure.

    Uses python-whois but avoids swallowing all exceptions. Returns -1 if
    creation date isn't available or parsing fails.
    """
    try:
        info = whois.whois(domain)
        date = info.creation_date
        if date is None:
            return -1
        # handle list of dates
        if isinstance(date, list):
            date = date[0]
        # coerce to pandas Timestamp for timezone-aware subtraction
        ts = pd.to_datetime(date)
        return int((pd.Timestamp.now(tz=ts.tz) - ts).days)
    except Exception as e:
        logging.debug('whois lookup failed for %s: %s', domain, e)
        return -1


if __name__ == '__main__':
    # allow running as a script with package or script import
    try:
        from . import config
    except Exception:
        import config

    import argparse

    parser = argparse.ArgumentParser(description='Extract URL features from a CSV (column `url`)')
    parser.add_argument('--input', '-i', help='Input CSV path', default=getattr(config, 'PHISHTANK_CSV', 'data/raw/phishtank_urls.csv'))
    parser.add_argument('--output', '-o', help='Output CSV path', default=getattr(config, 'PROCESSED_ENRON_SENDERS', 'data/processed/url_features.csv'))
    parser.add_argument('--sample', '-n', type=int, default=1000, help='Number of rows to process (0 = full, chunked)')
    parser.add_argument('--chunksize', type=int, default=50000, help='Chunk size for full processing')
    args = parser.parse_args()

    import pandas as pd
    import os
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)

    if args.sample and args.sample > 0:
        df = pd.read_csv(args.input, nrows=args.sample)
        out = extract_url_features(df)
        out.to_csv(args.output, index=False)
        print(f'Wrote {len(out)} rows to {args.output}')
    else:
        # full, chunked processing
        first = True
        for chunk in pd.read_csv(args.input, chunksize=args.chunksize):
            out = extract_url_features(chunk)
            out.to_csv(args.output, index=False, mode='w' if first else 'a', header=first)
            first = False
        print(f'Finished writing features to {args.output}')