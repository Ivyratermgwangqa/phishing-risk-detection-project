# utils.py
# Shared helper functions
import re
import urllib.parse
import tldextract


def extract_urls(text: str) -> list:
    """Extract all URLs from a text string"""
    regex = r'https?://[^\s]+'  # simple pattern
    return re.findall(regex, text)


def parse_domain_age(domain: str) -> int:
    """Stub for domain age calculation"""
    # Implement as needed
    return 0