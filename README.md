# Phishing Risk Detection Project

An explainable machine learning framework for detecting phishing URLs and assessing authentication risks using advanced threat intelligence integration and SHAP-based explanations.

## 🎯 Project Overview

This project implements a comprehensive phishing detection system that combines:
- **Machine Learning Models**: Random Forest for phishing detection, Isolation Forest for authentication risk
- **Threat Intelligence**: Real-time URL reputation checking and sender analysis
- **Explainable AI**: SHAP (SHapley Additive exPlanations) for model interpretability
- **Graph Features**: Network analysis of email sender relationships
- **Authentication Risk**: Anomaly detection in login patterns

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Ivyratermgwangqa/phishing-risk-detection-project.git
cd phishing-risk-detection-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up VirusTotal API:
```bash
cp .env.example .env
# Edit .env and add your VirusTotal API key
```

### Basic Usage

#### 1. Single URL Prediction (Interactive Mode)

Analyze a single URL with threat intelligence and explanations:

```bash
export SINGLE_PREDICT=1
python src/risk.py
```

Example interaction:
```
Enter URL to analyze: http://example.bad/login
Enter sender email (optional): attacker@bad.com

PREDICTION RESULTS
================================================================
URL: http://example.bad/login
Sender: attacker@bad.com

Predicted Label: 0 (Legitimate)
Probability: 0.1586

THREAT INTELLIGENCE
----------------------------------------------------------------
Malicious: False
Suspicious: True
Detection Engines: 1
Source: local_analysis

TOP CONTRIBUTING FEATURES (SHAP)
----------------------------------------------------------------
  url_length: 0.0234
  has_https: -0.0156
  num_dots: 0.0089
  domain_length: 0.0067
  path_length: 0.0045
```

#### 2. Programmatic Usage

Use the framework in your Python code:

```python
import sys
sys.path.append('src')
from risk import PhishingDetectionFramework

# Initialize framework
framework = PhishingDetectionFramework()

# Analyze a URL
result = framework.predict_single({
    "url": "http://example.com/login",
    "sender": "user@example.com"
}, return_shap=True)

print(result)
```

#### 3. Batch Processing

Process multiple URLs from the dataset:

```python
python src/risk.py
```

This will:
- Load trained models
- Run predictions on the processed dataset
- Generate SHAP explanations
- Display summary statistics

## 📁 Project Structure

```
phishing-risk-detection-project/
├── data/
│   ├── raw/              # Original datasets
│   ├── processed/        # Processed features and labels
│   └── external/         # External data sources
├── models/               # Trained models and metrics
│   ├── phishing_rf_model.pkl
│   ├── auth_risk_model.pkl
│   └── metrics/
├── notebooks/            # Jupyter notebooks for exploration
│   ├── 01-data-exploration.ipynb
│   ├── 02-feature-engineering.ipynb
│   ├── 03-graph-visuals.ipynb
│   ├── 04-model-training.ipynb
│   └── 05-auth-risk-model.ipynb
├── src/                  # Source code
│   ├── collect_data.py       # Data collection
│   ├── extract_features.py   # Feature engineering
│   ├── graph_features.py     # Graph-based features
│   ├── train_detector.py     # Model training
│   ├── train_auth_risk.py    # Auth risk model
│   ├── risk.py               # Main framework
│   └── utils.py              # Utilities
├── tests/                # Test suite
├── docs/                 # Documentation
│   └── PROJECT_REQUIREMENTS_ASSESSMENT.md
└── requirements.txt      # Python dependencies
```

## 🔧 Features

### Machine Learning Models

1. **Phishing Detection Model**
   - Algorithm: Random Forest Classifier
   - Features: 50+ URL, domain, and graph-based features
   - Model Size: 66MB
   - Training Data: 51MB processed features

2. **Authentication Risk Model**
   - Algorithm: Isolation Forest
   - Features: Location distance, login time, device fingerprint
   - Model Size: 1KB
   - Use Case: Anomaly detection in login attempts

### Feature Engineering

- **URL Features**: Length, structure, TLD analysis, special characters
- **Domain Features**: WHOIS data, DNS records, age
- **Graph Features**: Sender network metrics (degree centrality, clustering coefficient)
- **Behavioral Features**: Login patterns, location anomalies, device changes

### Explainability

- **SHAP Values**: Understand which features contribute most to each prediction
- **Visualizations**: Summary plots, force plots, feature importance rankings
- **Transparency**: Clear explanation of model decisions

### Threat Intelligence

- **Heuristic Analysis**: TLD reputation, suspicious keywords
- **Sender Analysis**: Domain comparison, email pattern detection
- **Extensible**: Ready for VirusTotal and other API integrations

## 📊 Model Performance

Current performance metrics (to be updated after full validation):

| Metric | Phishing Detector | Auth Risk Model |
|--------|-------------------|-----------------|
| Dataset Size | 51MB | 13KB |
| Features | 50+ | 3 |
| Algorithm | Random Forest | Isolation Forest |
| Prediction Time | <100ms | <50ms |

## 🛠️ Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests (when implemented)
pytest tests/
```

### Training Models

To retrain models with new data:

```bash
# Train phishing detector
python src/train_detector.py

# Train authentication risk model
python src/train_auth_risk.py
```

### Data Collection

To collect and process new data:

```bash
# Collect raw data
python src/collect_data.py

# Extract features
python src/extract_features.py

# Generate graph features
python src/graph_features.py
```

## 📖 Documentation

- [Project Requirements Assessment](docs/PROJECT_REQUIREMENTS_ASSESSMENT.md) - Detailed status and next steps
- [API References](docs/api_references.md) - API documentation (coming soon)
- [Data Dictionary](docs/data_dictionary.md) - Feature descriptions (coming soon)

## 🔮 Roadmap

### Completed ✅
- Data collection and processing pipeline
- Feature engineering framework
- Model training (phishing + auth risk)
- SHAP explainability integration
- Single URL prediction interface
- Basic threat intelligence

### In Progress 🚧
- Comprehensive test suite
- API reference documentation
- REST API development

### Planned 📋
- Web dashboard
- VirusTotal API integration
- Real-time monitoring
- Browser extension
- Docker containerization
- Production deployment guide

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Project Lead: Ivyratermgwangqa
- Contributors: See CONTRIBUTORS.md

## 🙏 Acknowledgments

- PhishTank for phishing URL datasets
- Enron email corpus for sender network analysis
- SHAP library for explainable AI
- scikit-learn for machine learning algorithms

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Status**: Beta - Ready for testing and feedback  
**Last Updated**: 2025-11-12  
**Version**: 1.0.0
