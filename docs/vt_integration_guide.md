# VirusTotal Integration Guide

## Overview
This guide explains how to integrate VirusTotal (VT) threat intelligence annotations into your phishing detection feature pipeline.

## VT Annotation Columns

The integration adds **4 VT-related columns** to your feature table:

| Column | Type | Description |
|--------|------|-------------|
| `vt_malicious_votes` | int | Number of VT engines flagging domain as malicious |
| `vt_suspicious_votes` | int | Number of VT engines flagging domain as suspicious |
| `vt_threat_score` | int | Threat score: 0=Benign, 1=Suspicious, 2=Malicious |
| `vt_threat_flag` | str | Human-readable flag: "Benign", "Suspicious (VT)", "Malicious (VT)", "Unknown" |

## Workflow

### Step 1: Fetch VT Data (One-time or Periodic)
```bash
# Set your VT API key
export VT_API_KEY="your_api_key_here"

# Run the enrichment script to fetch VT data for all domains
python src/enrich_virustotal.py
```

This creates:
- `data/processed/vt_cache.json` - Cached VT responses
- `data/processed/vt_audit.jsonl` - API call audit log

**Note:** This respects VT rate limits and caches results. You only need to run this periodically to update threat intelligence.

### Step 2: Merge VT Annotations into Features
```bash
# Merge VT annotations from cache into your feature table
python src/merge_vt_features.py
```

**Input:** `data/processed/phishing_graph_features.csv` (23 columns)  
**Output:** `data/processed/phishing_graph_features_vt.csv` (27 columns)

### Step 3: Use VT-Enriched Features in Training
```bash
# Train models using VT-enriched features
export ALL_FEATURES=data/processed/phishing_graph_features_vt.csv
python src/train_model.py
```

## Configuration

You can customize the merge process using environment variables:

```bash
# Custom input/output paths
export INPUT_FEATURES=data/processed/my_features.csv
export VT_CACHE=data/processed/vt_cache.json
export OUTPUT_FEATURES=data/processed/my_features_vt.csv

python src/merge_vt_features.py
```

## VT Cache Management

### Cache Structure
The VT cache (`vt_cache.json`) stores domain-level threat intelligence:

```json
{
  "example.com": {
    "last_analysis_stats": {
      "malicious": 5,
      "suspicious": 2,
      "undetected": 30,
      "harmless": 58,
      "timeout": 0
    },
    "reputation": -5,
    "last_analysis_date": 1699876543
  }
}
```

### Updating the Cache
To add new domains or refresh existing data:
```bash
export VT_API_KEY="your_api_key"
python src/enrich_virustotal.py
```

The script automatically:
- Skips domains already in cache
- Respects VT API rate limits (15s default delay)
- Saves progress every 50 lookups
- Handles interruptions gracefully (Ctrl+C)

## Threat Classification Logic

The merge script applies this classification:

```python
if malicious_votes >= 5:
    threat_score = 2
    threat_flag = "Malicious (VT)"
elif malicious_votes > 0 or suspicious_votes > 0:
    threat_score = 1
    threat_flag = "Suspicious (VT)"
else:
    threat_score = 0
    threat_flag = "Benign"
```

## Example: Current Statistics

From your latest merge (381,450 records):

| Threat Flag | Count | Percentage |
|-------------|-------|------------|
| Benign | 380,963 | 99.87% |
| Suspicious (VT) | 252 | 0.07% |
| Malicious (VT) | 232 | 0.06% |
| Unknown | 3 | <0.01% |

**Key Insights:**
- 484 domains (0.13%) flagged as potentially malicious or suspicious by VT
- Only 3 domains without VT data (likely uncached or lookup errors)
- Max malicious votes observed: 17
- Max suspicious votes observed: 3

## Integration with Existing Scripts

### Option 1: Update `extract_features.py` (Automatic)
The `extract_features.py` already has VT merge capability:

```python
df = extract_url_features(df)  # Automatically calls merge_virustotal_features()
```

### Option 2: Standalone Merge (Current Approach)
Use `merge_vt_features.py` as a separate pipeline step for more control:

```bash
python src/extract_features.py  # Generate base features
python src/compute_graph_features.py  # Add graph features
python src/merge_vt_features.py  # Add VT annotations
```

## Troubleshooting

### No VT cache found
```
⚠️  VT cache not found at: data/processed/vt_cache.json
```
**Solution:** Run `python src/enrich_virustotal.py` first to fetch VT data.

### Missing domain column
```
⚠️  No 'domain' column found in input — skipping VT merge.
```
**Solution:** Ensure your input CSV has a `domain` column with the domain to lookup.

### VT API rate limit
The enrichment script automatically handles rate limits with exponential backoff. Check `data/processed/vt_audit.jsonl` for detailed API call logs.

## Best Practices

1. **Cache First:** Always run `enrich_virustotal.py` before merging to build your VT cache
2. **Periodic Updates:** Refresh VT data monthly or when adding new domains
3. **Audit Logs:** Monitor `vt_audit.jsonl` for API errors or rate limit issues
4. **Feature Selection:** Include VT columns in your model training for enhanced detection
5. **Threshold Tuning:** Adjust the malicious vote threshold (currently 5) based on your risk tolerance

## Next Steps

1. ✅ VT annotations merged successfully
2. Use VT-enriched features in model training
3. Evaluate model performance with/without VT features
4. Consider VT reputation scores for additional signals
5. Monitor VT threat flag distribution in production data
