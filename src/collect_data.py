# collect_data.py
# Download and parse PhishTank & Enron data
import os
import csv
import requests
import email
from email import policy
from email.parser import BytesParser
from email.utils import parseaddr
import logging

try:
    # import the config module (package or script context) to avoid unused-name warnings
    from . import config
except Exception:
    import config

logging.basicConfig(level=logging.INFO)


def download_phishtank(output_path: str, url: str = None, timeout: int = 10, api_key: str = None):
    """Download phishing URLs dump and save as CSV.

    If `url` is None the function will use the project config value.
    """
    url = url or config.PHISHTANK_URL
    api_key = api_key or getattr(config, 'PHISHTANK_KEY', None)
    # safe download with timeout and streaming
    headers = {}
    if api_key:
        headers['X-API-Key'] = api_key
    resp = requests.get(url, timeout=timeout, stream=True, headers=headers)
    resp.raise_for_status()
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)


def parse_enron(maildir_path: str = None, output_csv: str = None):
    """Walk Enron maildir, extract headers and body.

    If `maildir_path` or `output_csv` are not provided the function will use
    values from the project config when available.
    """
    maildir_path = maildir_path or getattr(config, 'ENRON_PATH', None)
    if maildir_path is None:
        raise ValueError('maildir_path must be provided or config.ENRON_PATH must be set')
    output_csv = output_csv or os.path.join('..', 'data', 'processed', 'enron_emails.csv')

    os.makedirs(os.path.dirname(output_csv) or ".", exist_ok=True)
    with open(output_csv, 'w', newline='', encoding='utf-8') as out:
        writer = csv.DictWriter(out, fieldnames=["sender","subject","body"])
        writer.writeheader()
        for root, _, files in os.walk(maildir_path):
            for fname in files:
                path = os.path.join(root, fname)
                try:
                    # read as binary and use the email parser for robustness
                    with open(path, 'rb') as f:
                        raw = f.read()
                    try:
                        # best-effort decode to text for legacy files
                        text = raw.decode('utf-8', errors='ignore')
                    except Exception:
                        text = ''
                    msg = email.message_from_string(text)
                    writer.writerow({
                        "sender": msg.get('From'),
                        "subject": msg.get('Subject', ''),
                        "body": msg.get_payload()
                    })
                except Exception:
                    # keep parsing robust but don't fail the whole run
                    continue


def extract_senders_from_enron_csv(input_csv: str = None, output_csv: str = None, chunksize: int = 100000, sample_n: int = 1000):
    """Extract sender addresses from a large Enron CSV in chunks.

    - `input_csv`: path to the Enron CSV (defaults to data/raw/enron_emails/emails.csv)
    - `output_csv`: path to write sender samples (defaults to data/processed/enron_senders_sample.csv)
    - `chunksize`: rows per pandas chunk read
    - `sample_n`: stop after extracting this many senders (useful for quick tests)

    The function appends rows to `output_csv` as it processes chunks and is safe
    to run on very large files because it never loads the whole CSV into memory.
    """
    import pandas as pd
    import re

    input_csv = input_csv or os.path.join('data', 'raw', 'enron_emails', 'emails.csv')
    output_csv = output_csv or os.path.join('data', 'processed', 'enron_senders_sample.csv')
    os.makedirs(os.path.dirname(output_csv) or '.', exist_ok=True)

    def _extract_sender(text: str):
        if not isinstance(text, str) or not text:
            return None
        try:
            # try to parse using the email library first
            m = email.message_from_string(text)
            addr = parseaddr(m.get('From') or '')[1]
            if addr:
                return addr
        except Exception:
            pass
        # fallback regex search for a From: header
        m = re.search(r"^From:\s*(.+)$", text, flags=re.IGNORECASE | re.MULTILINE)
        if m:
            return m.group(1).strip().strip('<>')
        return None

    written = 0
    # write header then append rows as we find them
    with open(output_csv, 'w', newline='', encoding='utf-8') as out:
        w = csv.writer(out)
        w.writerow(['file', 'sender'])

        for chunk in pd.read_csv(input_csv, chunksize=chunksize, usecols=['file', 'message']):
            for _, row in chunk.iterrows():
                sender = _extract_sender(row.get('message', ''))
                w.writerow([row.get('file'), sender])
                written += 1
                if sample_n and written >= sample_n:
                    logging.info('Wrote %d sample sender rows to %s', written, output_csv)
                    return output_csv
    logging.info('Finished writing %d sender rows to %s', written, output_csv)
    return output_csv