# Streamlit Dashboard Guide

## Overview
The enhanced Streamlit dashboard now visualizes your complete model training pipeline and performance metrics.

## What's New

### 1. Model Training Metrics Tab
Displays comprehensive training statistics including:
- **Dataset Statistics**: Total rows, unique URLs, duplicates, feature counts
- **Label Distribution**: Pie chart and table showing class balance (Benign vs Phishing)
- **Data Preprocessing**: Lists dropped leakage columns and final dataset shape
- **Train/Test Split**: Shows distribution across training and test sets
- **Model Performance**: AUC, Precision, Recall, F1 scores with visual bar chart

### 2. SHAP Explanation Tabs
- Phishing Model SHAP visualizations
- Authentication Model SHAP visualizations

### 3. About Tab
Project information and usage instructions

## Running the Dashboard

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the dashboard
streamlit run dashboard.py
```

The dashboard will be available at:
- Local: http://localhost:8501
- Network: http://172.24.246.132:8501

## Data Flow

1. **Training**: `python src/train_model.py` generates:
   - Model file: `models/phishing_rf_model.pkl`
   - Metrics file: `models/training_metrics.json`
   - Feature names: `models/feature_names.json`

2. **Dashboard**: Reads `training_metrics.json` and displays interactive visualizations

## Current Performance Metrics

Based on your latest training run with VirusTotal features:

- **AUC-ROC**: 0.9888 (Excellent)
- **Precision**: 0.9236
- **Recall**: 0.9632
- **F1 Score**: 0.9430

### Dataset Statistics
- Total samples: 159,603 (after deduplication)
- Training set: 111,722 samples
- Test set: 47,881 samples
- Features used: 19 numeric features
- Dropped leakage column: `url_length`

### Label Distribution
- Class 0 (Benign): 105,962 samples (66.4%)
- Class 1 (Phishing): 53,641 samples (33.6%)

## Features

The dashboard uses Plotly for interactive visualizations including:
- Pie charts for label distribution
- Bar charts for performance metrics
- Expandable sections for detailed feature information
- Color-coded metric cards with status indicators

## Dependencies

Required packages (already installed):
- streamlit
- plotly
- pandas
- numpy
