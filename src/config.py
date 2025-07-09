# config.py
# Global settings and API keys
import os
from dotenv import load_dotenv

load_dotenv()  # read .env

PHISHTANK_KEY = os.getenv("PHISHTANK_KEY")
VIRUSTOTAL_KEY = os.getenv("VIRUSTOTAL_KEY")
ENRON_PATH = os.getenv("ENRON_PATH", "data/raw/enron_emails")
PHISHTANK_URL = os.getenv("PHISHTANK_URL", "http://data.phishtank.com/data/online-valid.csv")