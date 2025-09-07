# collect_data.py
# Download and parse PhishTank & Enron data
import os
import csv
import requests
import email

try:
    # when imported as a package (e.g., `import src.collect_data`)
    from .config import PHISHTANK_KEY, PHISHTANK_URL, ENRON_PATH
except Exception:
    # when run as a script (e.g., `python src/collect_data.py`)
    from config import PHISHTANK_KEY, PHISHTANK_URL, ENRON_PATH


def download_phishtank(output_path: str):
    """Download phishing URLs dump and save as CSV"""
    response = requests.get(PHISHTANK_URL)
    with open(output_path, 'wb') as f:
        f.write(response.content)


def parse_enron(maildir_path: str, output_csv: str):
    """Walk Enron maildir, extract headers and body"""
    with open(output_csv, 'w', newline='', encoding='utf-8') as out:
        writer = csv.DictWriter(out, fieldnames=["sender","subject","body"])
        writer.writeheader()
        for root, _, files in os.walk(maildir_path):
            for fname in files:
                try:
                    path = os.path.join(root, fname)
                    with open(path, 'r', errors='ignore') as f:
                        msg = email.message_from_file(f)
                        writer.writerow({
                            "sender": msg.get('From'),
                            "subject": msg.get('Subject', ''),
                            "body": msg.get_payload()
                        })
                except Exception:
                    continue