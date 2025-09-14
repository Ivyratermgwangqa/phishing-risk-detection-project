# enrich_virustotal.py
# Add VirusTotal enrichment to feature table
import vt
import pandas as pd
import logging
from config import VIRUSTOTAL_KEY

logging.basicConfig(level=logging.INFO)

# create client only if key is present and valid
_vt_client = None
if isinstance(VIRUSTOTAL_KEY, str) and VIRUSTOTAL_KEY:
    try:
        _vt_client = vt.Client(VIRUSTOTAL_KEY)
    except Exception as e:
        logging.warning('VirusTotal client creation failed: %s', e)
        _vt_client = None
else:
    logging.info('No VirusTotal API key configured; enrich_urls will be a no-op')


def enrich_urls(df: pd.DataFrame) -> pd.DataFrame:
    """Query VirusTotal for URL/domain reputation and add features.

    If VirusTotal client is not available the function returns the input DataFrame
    unmodified.
    """
    if _vt_client is None:
        return df

    # implementation note: real code should be rate-limited and cached
    # placeholder implementation: add empty vt_* columns
    df = df.copy()
    df['vt_malicious_votes'] = None
    df['vt_total_votes'] = None
    return df