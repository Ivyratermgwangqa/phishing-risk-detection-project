# config.py
# Global settings and API keys
import os
from dotenv import load_dotenv

load_dotenv()  # read .env

# API keys (can be None)
PHISHTANK_KEY = os.getenv("PHISHTANK_KEY")
VIRUSTOTAL_KEY = os.getenv("VIRUSTOTAL_KEY")

# Paths and URLs (override via environment if needed)
ENRON_PATH = os.getenv("ENRON_PATH", "data/raw/enron_emails")
ENRON_CSV = os.getenv("ENRON_CSV", os.path.join('data', 'raw', 'enron_emails', 'emails.csv'))
PHISHTANK_URL = os.getenv("PHISHTANK_URL", "http://data.phishtank.com/data/online-valid.csv")
PHISHTANK_CSV = os.getenv("PHISHTANK_CSV", os.path.join('data', 'raw', 'phishtank_urls.csv'))

# Processed outputs
PROCESSED_ENRON_SENDERS = os.getenv("PROCESSED_ENRON_SENDERS", os.path.join('data', 'processed', 'enron_senders.csv'))
PROCESSED_AUTH_LOGS = os.getenv("PROCESSED_AUTH_LOGS", os.path.join('data', 'processed', 'auth_logs.csv'))
# config.py
# Global settings and API keys
import os
from dotenv import load_dotenv

load_dotenv()  # read .env

PHISHTANK_KEY = os.getenv("PHISHTANK_KEY")
VIRUSTOTAL_KEY = os.getenv("VIRUSTOTAL_KEY")
ENRON_PATH = os.getenv("ENRON_PATH", "data/raw/enron_emails")
PHISHTANK_URL = os.getenv("PHISHTANK_URL", "http://data.phishtank.com/data/online-valid.csv")