# extract_features.py
# Lexical & metadata extraction (URLs, WHOIS, etc.)
import re
import whois
import pandas as pd
import urllib.parse
import tldextract

from utils import extract_urls, parse_domain_age


def extract_url_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract URL lexical and metadata features"""
    # Implement parsing for each URL in df['url']
    return df


def parse_whois_age(domain: str) -> int:
    """Return domain age in days"""
    try:
        info = whois.whois(domain)
        date = info.creation_date
        # handle list
        if isinstance(date, list): date = date[0]
        return (pd.Timestamp.now() - pd.Timestamp(date)).days
    except:
        return -1