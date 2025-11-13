#!/usr/bin/env python3
"""
merge_vt_features.py
Merges VirusTotal threat intelligence annotations into the feature table.
This reads the VT cache and adds 4 VT-related columns to the base features.
"""
import os
import json
import pandas as pd
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPATH = os.environ.get('INPUT_FEATURES') or os.path.join(PROJECT_ROOT, 'data', 'processed', 'phishing_graph_features.csv')
VT_CACHE_PATH = os.environ.get('VT_CACHE') or os.path.join(PROJECT_ROOT, 'data', 'processed', 'vt_cache.json')
OUTPATH = os.environ.get('OUTPUT_FEATURES') or os.path.join(PROJECT_ROOT, 'data', 'processed', 'phishing_graph_features_vt.csv')


def load_vt_cache(cache_path):
    """Load VirusTotal cache from JSON file."""
    if not os.path.exists(cache_path):
        print(f"⚠️  VT cache not found at: {cache_path}")
        print("   Run `python src/enrich_virustotal.py` first to fetch VT data.")
        return None
    
    with open(cache_path, 'r') as f:
        cache = json.load(f)
    
    print(f"✅ Loaded VT cache with {len(cache)} domains")
    return cache


def vt_fields(domain, cache):
    """Extract VT threat intelligence fields for a domain.
    
    Returns:
        tuple: (malicious_votes, suspicious_votes, threat_score, threat_flag)
    """
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


def merge_vt_annotations(df, cache):
    """Merge VT annotations into the feature dataframe.
    
    Args:
        df: Input DataFrame with 'domain' column
        cache: VT cache dictionary
        
    Returns:
        DataFrame with added VT columns
    """
    if 'domain' not in df.columns:
        print("⚠️  No 'domain' column found in input — skipping VT merge.")
        return df
    
    print(f"🔍 Merging VT annotations for {len(df)} records...")
    
    # Apply VT fields extraction
    vt_data = df['domain'].apply(lambda d: vt_fields(d, cache))
    
    # Unpack into separate columns
    df[['vt_malicious_votes', 'vt_suspicious_votes', 'vt_threat_score', 'vt_threat_flag']] = pd.DataFrame(
        vt_data.tolist(), index=df.index
    )
    
    # Report statistics
    vt_cols = ['vt_malicious_votes', 'vt_suspicious_votes', 'vt_threat_score', 'vt_threat_flag']
    print(f"✅ Added VT columns: {', '.join(vt_cols)}")
    
    print("\n📊 VT Threat Flag Distribution:")
    print(df['vt_threat_flag'].value_counts())
    
    print("\n📊 VT Threat Score Distribution:")
    print(df['vt_threat_score'].value_counts())
    
    return df


def main():
    """Main execution function."""
    # Load input features
    if not os.path.exists(INPATH):
        print(f"❌ Input features not found: {INPATH}")
        sys.exit(1)
    
    print(f"📂 Loading features from: {INPATH}")
    df = pd.read_csv(INPATH)
    print(f"   Loaded {len(df)} records with {len(df.columns)} columns")
    
    # Load VT cache
    cache = load_vt_cache(VT_CACHE_PATH)
    if cache is None:
        print("❌ Cannot proceed without VT cache.")
        sys.exit(1)
    
    # Merge VT annotations
    df = merge_vt_annotations(df, cache)
    
    # Save output
    os.makedirs(os.path.dirname(OUTPATH), exist_ok=True)
    df.to_csv(OUTPATH, index=False)
    
    print(f"\n💾 Saved enriched features to: {OUTPATH}")
    print(f"   Final shape: {df.shape}")
    print(f"   Columns: {len(df.columns)}")
    
    # Show sample of VT columns
    vt_cols = ['domain', 'vt_malicious_votes', 'vt_suspicious_votes', 'vt_threat_score', 'vt_threat_flag']
    available_cols = [c for c in vt_cols if c in df.columns]
    if available_cols:
        print(f"\n📋 Sample VT annotations (first 10 rows):")
        print(df[available_cols].head(10).to_string(index=False))


if __name__ == '__main__':
    main()
