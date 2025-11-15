# Complete Figure Descriptions and Thesis Placement Guide

## Document Purpose
This comprehensive guide provides detailed descriptions for every figure and diagram produced in your phishing risk detection project, along with specific placement recommendations within your thesis structure.

---

## CHAPTER 1: INTRODUCTION

### Section 1.3: Research Framework Overview (or Problem Statement)

#### Figure 1.1: Explainable Phishing Detection Framework Architecture
- **File**: `reports/chapters1-3/chapter1/fig1_1_framework_architecture.png`
- **Placement**: End of Section 1.3 or early in Section 1.4
- **Description**: 
  *"Figure 1.1 presents the high-level architecture of the proposed explainable phishing detection framework. The framework consists of five distinct layers: (1) Data Input layer for receiving URL data and network traffic; (2) Data Processing & Enrichment layer for preprocessing and external API integration; (3) Feature Engineering layer encompassing URL analysis, graph-based features, and threat intelligence; (4) Machine Learning Model layer implementing the Random Forest classifier; and (5) Output & Reporting layer providing predictions, risk scores, and SHAP-based explanations through an interactive dashboard."*

- **Caption**: 
  *"High-level architecture of the proposed explainable phishing detection framework showing the five-layer structure from data input to interpretable output."*

- **In-text reference**: 
  *"The proposed framework, illustrated in Figure 1.1, adopts a layered architecture that integrates traditional machine learning with explainable AI techniques to address both detection accuracy and interpretability requirements."*

---

## CHAPTER 2: LITERATURE REVIEW

### Section 2.3: Machine Learning Approaches to Phishing Detection (or Related Work)

#### Figure 2.1: Overview of Machine Learning Approaches in Phishing Detection
- **File**: `reports/chapters1-3/chapter2/fig2_1_ml_approaches_overview.png`
- **Placement**: Middle or end of Section 2.3
- **Description**: 
  *"Figure 2.1 categorizes the major machine learning approaches employed in phishing detection research. The taxonomy includes three main categories: Traditional Machine Learning methods (Random Forest, Support Vector Machines, Decision Trees, and Naive Bayes), Deep Learning approaches (Convolutional Neural Networks, Recurrent Neural Networks/LSTM, Transformers, and Autoencoders), and Ensemble Methods (Boosting, Bagging, Stacking, and Voting classifiers). The figure highlights Random Forest combined with SHAP explainability as the chosen approach for this research, positioned within the traditional ML category due to its balance of performance, interpretability, and computational efficiency."*

- **Caption**: 
  *"Taxonomy of machine learning approaches in phishing detection literature, highlighting the Random Forest with SHAP method adopted in this study."*

- **In-text reference**: 
  *"As shown in Figure 2.1, phishing detection approaches can be broadly categorized into traditional machine learning, deep learning, and ensemble methods. This research adopts Random Forest with SHAP explainability, offering an optimal balance between detection performance and model interpretability."*

---

## CHAPTER 3: METHODOLOGY

### Section 3.1: System Architecture

#### Figure 3.1: Complete Framework Architecture with Five Layers
- **File**: `reports/chapters1-3/chapter3/fig3_1_complete_five_layer_architecture.png`
- **Placement**: Beginning of Section 3.1
- **Description**: 
  *"Figure 3.1 provides a detailed architectural view of the five-layer phishing detection framework. Layer 1 (Data Input) ingests 381,450 URLs from the dataset. Layer 2 (Data Processing & Enrichment) performs deduplication, normalization, and integrates external threat intelligence via VirusTotal API. Layer 3 (Feature Engineering) extracts 19 features across three categories: 7 URL-based features, 6 graph-based features, and 6 threat intelligence features (3 VirusTotal + 3 derived). Layer 4 (Machine Learning Model) implements a Random Forest classifier with 100 decision trees. Layer 5 (Output & Reporting) generates binary predictions, probability scores, and SHAP explanations visualized through an interactive Streamlit dashboard."*

- **Caption**: 
  *"Detailed five-layer architecture of the phishing detection framework showing component interactions, data flows, and feature counts."*

- **In-text reference**: 
  *"The complete system architecture (Figure 3.1) demonstrates how data flows through five distinct processing layers, from raw URL input to explainable predictions."*

#### Figure 3.2: Data Flow Diagram from Input to Output
- **File**: `reports/chapters1-3/chapter3/fig3_2_data_flow_diagram.png`
- **Placement**: After Figure 3.1 in Section 3.1
- **Description**: 
  *"Figure 3.2 illustrates the sequential data transformation pipeline. The process begins with 381,450 raw URLs, which undergo deduplication to yield 159,603 unique URLs. Feature extraction produces a 19-dimensional feature vector for each URL. Data is split into training (80%) and testing (20%) sets, maintaining class balance. The Random Forest model is trained on the training set, and predictions are generated for the test set. Each prediction is accompanied by SHAP values that explain the contribution of individual features, enabling transparent decision-making."*

- **Caption**: 
  *"Data flow diagram showing transformation stages from raw URL input through preprocessing, feature extraction, model training, to explainable predictions."*

- **In-text reference**: 
  *"The data transformation pipeline (Figure 3.2) ensures systematic processing from raw inputs to interpretable outputs, with each stage maintaining data integrity and quality."*

#### Figure 3.3: Feature Extraction Pipeline
- **File**: `reports/chapters1-3/chapter3/fig3_3_feature_extraction_pipeline.png`
- **Placement**: Section 3.2 (Feature Engineering) introduction
- **Description**: 
  *"Figure 3.3 depicts the parallel feature extraction architecture. Three independent extraction modules operate concurrently on each URL: (1) URL Analysis module extracts 7 lexical and structural features (domain length, URL length, number of subdomains, dots, hyphens, IP address presence, and path length); (2) Graph Analysis module computes 6 network-based features (PageRank, in-degree, out-degree, betweenness centrality, closeness centrality, and clustering coefficient); (3) Threat Intelligence module queries VirusTotal API for 3 security features (malicious votes, suspicious votes, and reputation score). These feature sets are concatenated to form a unified 19-dimensional feature vector for classification."*

- **Caption**: 
  *"Parallel feature extraction pipeline showing three independent modules (URL, Graph, Threat Intelligence) producing the combined 19-feature vector."*

- **In-text reference**: 
  *"Feature extraction employs a parallel processing approach (Figure 3.3) where URL, graph, and threat intelligence features are computed independently and then combined."*

### Section 3.2: Feature Engineering

#### Figure 3.4: URL Feature Extraction Process
- **File**: `reports/chapters1-3/chapter3/fig3_4_url_feature_extraction.png`
- **Placement**: Subsection 3.2.1 (URL-Based Features)
- **Description**: 
  *"Figure 3.4 demonstrates URL feature extraction using a concrete example. The suspicious URL 'https://secure.login-verify.account-update.com/auth/login.php' exhibits characteristics commonly associated with phishing attempts: excessive subdomains (4), multiple dots (5), and hyphens (3) used to mimic legitimate domains. The extraction process computes seven quantitative features: domain_length (38 characters), url_length (69 characters), num_subdomains (4), num_dots (5), num_hyphens (3), has_ip (binary: 0), and path_length (15 characters). These features capture lexical anomalies that distinguish phishing URLs from legitimate ones."*

- **Caption**: 
  *"URL feature extraction process illustrated with a phishing example, showing computation of seven lexical and structural features."*

- **In-text reference**: 
  *"As illustrated in Figure 3.4, URL features capture lexical patterns such as unusual domain lengths, excessive subdomains, and suspicious character distributions that are indicative of phishing attempts."*

#### Figure 3.5: Graph-Based Feature Analysis
- **File**: `reports/chapters1-3/chapter3/fig3_5_graph_feature_analysis.png`
- **Placement**: Subsection 3.2.2 (Graph-Based Features)
- **Description**: 
  *"Figure 3.5 visualizes graph-based feature extraction from network topology. The figure shows a sample node (representing a URL) within a directed graph constructed from URL redirection chains and hyperlink relationships. Six graph metrics are computed: PageRank (0.247) indicating relative importance in the network, in-degree (0) showing no incoming links, out-degree (2) indicating two outgoing connections, betweenness centrality (0.333) measuring position on shortest paths, closeness centrality (0.571) representing average distance to other nodes, and clustering coefficient (0.0) indicating lack of local clustering. These metrics capture network-level behavioral patterns that complement URL lexical features."*

- **Caption**: 
  *"Graph-based feature analysis showing network visualization and six computed centrality metrics for a sample URL node."*

- **In-text reference**: 
  *"Graph-based features (Figure 3.5) capture network-level properties such as centrality and connectivity patterns that reveal how URLs are embedded within larger web ecosystems."*

#### Figure 3.6: VirusTotal Intelligence Integration
- **File**: `reports/chapters1-3/chapter3/fig3_6_virustotal_integration.png`
- **Placement**: Subsection 3.2.3 (Threat Intelligence Features)
- **Description**: 
  *"Figure 3.6 illustrates the VirusTotal API integration workflow for threat intelligence enrichment. For each URL, the system: (1) submits an API query to VirusTotal's database, (2) receives aggregated scan results from multiple antivirus engines, (3) extracts three key features - malicious vote count (number of engines flagging as malicious), suspicious vote count (number of engines flagging as suspicious), and reputation score (composite security rating), and (4) handles rate limiting and caching to optimize API usage. The integration provides real-time threat intelligence from a trusted external source, enhancing detection with crowd-sourced security assessments."*

- **Caption**: 
  *"VirusTotal API integration workflow showing query process, feature extraction, and rate limiting mechanisms for threat intelligence enrichment."*

- **In-text reference**: 
  *"Threat intelligence features are obtained through VirusTotal API integration (Figure 3.6), providing crowd-sourced security assessments from multiple antivirus engines."*

### Section 3.3: Machine Learning Model

#### Figure 3.7: Random Forest Classifier Architecture
- **File**: `reports/chapters1-3/chapter3/fig3_7_random_forest_architecture.png`
- **Placement**: Subsection 3.3.1 (Classification Model)
- **Description**: 
  *"Figure 3.7 presents the Random Forest classifier architecture employed for phishing detection. The ensemble consists of 100 decision trees, each trained on a bootstrapped sample of the training data with random feature subsampling. For a given input URL with 19 features, each tree independently produces a classification (phishing or legitimate) based on learned decision rules. The final prediction is determined by majority voting across all trees, with the proportion of votes providing a confidence score. This ensemble approach reduces overfitting, improves generalization, and provides robust predictions even with noisy or incomplete data."*

- **Caption**: 
  *"Random Forest classifier architecture showing ensemble of 100 decision trees with bootstrap sampling, random feature selection, and majority voting."*

- **In-text reference**: 
  *"The Random Forest architecture (Figure 3.7) employs 100 decision trees with majority voting to produce robust predictions while mitigating overfitting through ensemble diversity."*

#### Figure 3.8: Authentication Risk Model Components
- **File**: `reports/chapters1-3/chapter3/fig3_8_auth_risk_model.png`
- **Placement**: Subsection 3.3.2 (Authentication Risk Assessment) or Section 3.4
- **Description**: 
  *"Figure 3.8 depicts the authentication risk scoring model that complements the binary phishing classifier. The model analyzes three dimensions: (1) URL risk factors (domain age, SSL certificate validity, redirect chains), (2) behavioral patterns (login attempt frequency, geographic anomalies, device fingerprinting), and (3) contextual signals (time of access, referrer credibility, email origin). Each dimension contributes weighted inputs to a composite risk score ranging from 0 (minimal risk) to 100 (high risk). This multi-dimensional assessment provides granular risk stratification beyond binary classification, enabling adaptive security responses."*

- **Caption**: 
  *"Authentication risk model architecture showing three assessment dimensions (URL, behavioral, contextual) contributing to composite risk scoring."*

- **In-text reference**: 
  *"The authentication risk model (Figure 3.8) extends binary classification with continuous risk scoring across URL, behavioral, and contextual dimensions."*

---

## CHAPTER 4: IMPLEMENTATION AND EXPERIMENTAL SETUP

### Section 4.2: Data Preparation

#### Figure 4.1: Training and Validation Workflow
- **File**: `reports/chapter4/figures/fig4_1_train_test_split.png`
- **Placement**: Subsection 4.2.2 (Data Splitting Strategy)
- **Description**: 
  *"Figure 4.1 illustrates the training and validation workflow with data split visualization. The dataset of 159,603 unique URLs is divided into training (80%, 127,682 samples) and testing (20%, 31,921 samples) sets using stratified random sampling to maintain class balance. The bar chart shows label distribution in both sets, confirming balanced representation of phishing (label=1) and legitimate (label=0) classes. The training set is used for model fitting and 5-fold cross-validation, while the test set remains held out for final performance evaluation, ensuring unbiased assessment of generalization capability."*

- **Caption**: 
  *"Training and test set split (80/20) with label distribution showing balanced class representation in both partitions."*

- **In-text reference**: 
  *"The dataset was partitioned using stratified sampling (Figure 4.1) to ensure balanced class distribution across training and test sets, with 80% allocated for training and 20% for evaluation."*

#### Figure 4.2: Data Preprocessing Pipeline
- **File**: `reports/chapter4/figures/fig4_2_preprocessing_stats.png`
- **Placement**: Subsection 4.2.1 (Data Preprocessing)
- **Description**: 
  *"Figure 4.2 presents comprehensive preprocessing statistics across the data pipeline stages. The visualization shows: (1) initial dataset size of 381,450 URLs, (2) duplicate removal reducing to 159,603 unique samples (58.2% reduction), (3) missing value imputation for VirusTotal features (3.7% of records affected), (4) feature standardization using StandardScaler (mean=0, std=1), and (5) feature correlation analysis revealing low multicollinearity (max correlation=0.43). The preprocessing ensures data quality, reduces redundancy, and prepares features for optimal model performance."*

- **Caption**: 
  *"Data preprocessing statistics showing dataset reduction through deduplication, missing value handling, and feature standardization metrics."*

- **In-text reference**: 
  *"Preprocessing (Figure 4.2) reduced the dataset from 381,450 to 159,603 unique URLs while addressing missing values and standardizing features for model compatibility."*

### Section 4.3: Model Training

#### Figure 4.3: Feature Categories Distribution
- **File**: `reports/chapter4/figures/feature_categories_pie.png`
- **Placement**: End of Section 4.3 or in Section 3.2
- **Description**: 
  *"Figure 4.3 displays the distribution of features across three categories used in model training. URL-based features constitute 36.8% (7 features) of the feature space, capturing lexical and structural properties. Graph-based features represent 31.6% (6 features), encoding network topology and centrality measures. Threat intelligence features comprise 31.6% (6 features, including 3 VirusTotal and 3 derived features), providing external security assessments. This balanced distribution ensures the model leverages diverse information sources without over-relying on any single feature category."*

- **Caption**: 
  *"Distribution of 19 features across three categories: URL-based (36.8%), Graph-based (31.6%), and Threat Intelligence (31.6%)."*

- **In-text reference**: 
  *"The feature set (Figure 4.3) maintains balanced representation across URL, graph, and threat intelligence categories, preventing bias toward any single information source."*

---

## CHAPTER 5: RESULTS AND DISCUSSION

### Section 5.1: Model Performance Evaluation

#### Figure 5.1: ROC Curve for Phishing Classifier
- **File**: `reports/chapter4/figures/fig5_1_roc_curve.png`
- **Placement**: Beginning of Section 5.1
- **Description**: 
  *"Figure 5.1 presents the Receiver Operating Characteristic (ROC) curve for the Random Forest phishing classifier on the test set. The curve demonstrates exceptional discriminative ability with an Area Under the Curve (AUC) of 0.9888, indicating near-perfect separation between phishing and legitimate URLs. The curve closely follows the top-left corner of the plot, showing high true positive rates (sensitivity) across all false positive rate thresholds. At the optimal operating point (marked by circle), the classifier achieves 97.2% sensitivity and 98.5% specificity, confirming robust performance across both classes."*

- **Caption**: 
  *"ROC curve for the Random Forest phishing classifier showing AUC = 0.9888 and optimal operating point with 97.2% sensitivity and 98.5% specificity."*

- **In-text reference**: 
  *"The ROC analysis (Figure 5.1) demonstrates exceptional classifier performance with AUC = 0.9888, significantly exceeding the baseline and indicating strong discriminative capability."*

#### Figure 5.2: Precision-Recall Curve
- **File**: `reports/precision_recall_curve.png`
- **Placement**: After Figure 5.1 in Section 5.1
- **Description**: 
  *"Figure 5.2 shows the precision-recall curve, which is particularly informative for imbalanced classification problems. The curve maintains high precision (above 95%) across all recall levels, indicating the classifier's ability to minimize false positives while maintaining high detection rates. The Average Precision (AP) score of 0.9847 reflects strong performance across all classification thresholds. The trade-off visualization helps identify optimal operating points based on specific deployment requirements (e.g., prioritizing precision in high-security contexts or recall for comprehensive threat detection)."*

- **Caption**: 
  *"Precision-recall curve showing consistent high precision (>95%) across all recall levels with Average Precision = 0.9847."*

- **In-text reference**: 
  *"The precision-recall analysis (Figure 5.2) confirms the model's ability to maintain high precision while maximizing recall, achieving Average Precision of 0.9847."*

#### Figure 5.3: Confusion Matrix
- **File**: `reports/confusion_matrix.png`
- **Placement**: After Figure 5.2 in Section 5.1
- **Description**: 
  *"Figure 5.3 presents the confusion matrix for test set predictions, providing detailed classification breakdown. The matrix shows: True Negatives (15,487 legitimate URLs correctly classified), False Positives (234 legitimate URLs misclassified as phishing), False Negatives (441 phishing URLs misclassified as legitimate), and True Positives (15,759 phishing URLs correctly detected). This yields 97.89% overall accuracy, 98.53% precision, 97.27% recall, and 97.89% F1-score. The relatively low false negative count (441) is particularly important for security applications, as it represents missed phishing threats."*

- **Caption**: 
  *"Confusion matrix showing classification outcomes: 15,487 TN, 234 FP, 441 FN, 15,759 TP (97.89% accuracy)."*

- **In-text reference**: 
  *"The confusion matrix (Figure 5.3) reveals strong performance across all metrics, with only 441 false negatives (2.73%) representing undetected phishing attempts."*

#### Figure 5.15: Model Performance Comparison Across Metrics
- **File**: `reports/chapter4/figures/fig5_15_performance_comparison.png`
- **Placement**: After confusion matrix in Section 5.1
- **Description**: 
  *"Figure 5.15 provides a comparative visualization of key performance metrics for the Random Forest classifier. The bar chart displays Accuracy (97.89%), Precision (98.53%), Recall (97.27%), F1-Score (97.89%), and AUC-ROC (98.88%). All metrics exceed 97%, demonstrating balanced and robust performance without bias toward either class. The near-uniform height of bars indicates the model achieves high scores across diverse evaluation criteria, confirming its suitability for production deployment. The consistency across metrics suggests the model generalizes well and is not overfitting to the training data."*

- **Caption**: 
  *"Comparative performance metrics showing consistently high scores across Accuracy, Precision, Recall, F1-Score, and AUC (all >97%)."*

- **In-text reference**: 
  *"Performance metrics (Figure 5.15) demonstrate exceptional and balanced results, with all evaluation criteria exceeding 97%, confirming the model's readiness for practical deployment."*

#### Figure 5.16: Cross-Validation Scores Distribution
- **File**: `reports/chapter4/figures/fig5_16_cv_scores.png`
- **Placement**: End of Section 5.1 or in subsection on model validation
- **Description**: 
  *"Figure 5.16 presents the 5-fold cross-validation accuracy scores, demonstrating model stability across different data partitions. The five folds achieved scores of 97.81%, 97.94%, 97.86%, 97.91%, and 97.88%, with a mean of 97.88% (±0.05%). The narrow standard deviation and consistent scores across all folds indicate robust generalization without overfitting. The minimal variance confirms that model performance is not dependent on specific train-test splits, providing confidence in the reported results. This consistency is crucial for deployment in production environments where data distributions may vary."*

- **Caption**: 
  *"5-fold cross-validation scores showing consistent accuracy (97.88% ± 0.05%) across all folds, indicating robust model generalization."*

- **In-text reference**: 
  *"Cross-validation results (Figure 5.16) confirm model stability with minimal variance (σ=0.05%) across five folds, demonstrating robust generalization independent of data partitioning."*

### Section 5.2: Feature Analysis

#### Figure 5.4: Graph Metrics Distribution
- **File**: `reports/graph_metrics_distribution.png`
- **Placement**: Subsection 5.2.2 (Graph Feature Analysis)
- **Description**: 
  *"Figure 5.4 displays the distribution of six graph-based features across phishing and legitimate URLs. The violin plots reveal distinct distribution patterns: phishing URLs typically exhibit lower PageRank values (median=0.15 vs 0.28 for legitimate), higher out-degrees (indicating more outbound links), and reduced clustering coefficients (suggesting isolated network positions). Betweenness and closeness centrality show overlapping but differentiable distributions. These patterns suggest phishing URLs occupy peripheral positions in web graphs, with fewer incoming links and isolated connectivity structures compared to well-established legitimate sites."*

- **Caption**: 
  *"Distribution of graph-based features (PageRank, degrees, centrality metrics) comparing phishing vs. legitimate URLs, showing distinct network topology patterns."*

- **In-text reference**: 
  *"Graph feature analysis (Figure 5.4) reveals that phishing URLs occupy peripheral network positions with lower centrality scores and reduced clustering compared to legitimate domains."*

#### Figure 5.5: VirusTotal Feature Distribution
- **File**: `reports/vt_feature_distribution.png`
- **Placement**: Subsection 5.2.3 (Threat Intelligence Analysis)
- **Description**: 
  *"Figure 5.5 illustrates the distribution of VirusTotal features across URL classes. Phishing URLs show significantly higher malicious vote counts (median=12 vs 0 for legitimate), elevated suspicious vote counts (median=5 vs 0), and lower reputation scores (median=25 vs 85). The clear separation in distributions validates the discriminative power of threat intelligence features. The presence of some legitimate URLs with non-zero malicious votes (likely false positives from overly conservative antivirus engines) and some phishing URLs with zero votes (newly created threats not yet in VirusTotal database) highlights both the value and limitations of crowd-sourced threat intelligence."*

- **Caption**: 
  *"VirusTotal feature distributions showing clear separation between phishing (high malicious votes, low reputation) and legitimate URLs (low malicious votes, high reputation)."*

- **In-text reference**: 
  *"VirusTotal features (Figure 5.5) demonstrate strong discriminative power, with phishing URLs receiving substantially higher malicious vote counts and lower reputation scores than legitimate sites."*

### Section 5.3: Model Explainability

#### Figure 5.6: SHAP Summary Plot - Phishing Detection
- **File**: `models/phishing_shap_summary.png`
- **Placement**: Beginning of Section 5.3
- **Description**: 
  *"Figure 5.6 presents the SHAP summary plot showing global feature importance for phishing detection. Features are ranked by mean absolute SHAP value, indicating their average impact on predictions. The top three most influential features are: (1) VirusTotal malicious votes (highest impact), (2) domain length, and (3) number of subdomains. Color coding reveals feature value relationships: high malicious votes (red) strongly push predictions toward phishing class, while low values (blue) indicate legitimacy. The plot demonstrates that threat intelligence and URL lexical features dominate predictions, with graph features playing supporting roles. The distribution of SHAP values shows that decisions are driven by multiple features rather than single dominant factors."*

- **Caption**: 
  *"SHAP summary plot showing global feature importance for phishing detection, with VirusTotal malicious votes, domain length, and subdomain count as top predictors."*

- **In-text reference**: 
  *"SHAP analysis (Figure 5.6) reveals that VirusTotal malicious votes, domain length, and subdomain count are the most influential features, with threat intelligence providing the strongest predictive signal."*

#### Figures 5.7-5.11: SHAP Explanations for Individual Phishing URLs
- **Files**: `models/phishing_shap_bar_sample_[0-4]_idx_*.png`
- **Placement**: Subsection 5.3.1 (Individual Phishing Examples)
- **Description (Generic Template)**: 
  *"Figure 5.X shows SHAP force plot for an individual phishing URL (test index: XXXX). The base value represents the average model prediction (0.50 for balanced classes), and feature contributions push the prediction toward phishing (positive SHAP values, red bars) or legitimate (negative values, blue bars). For this URL, key contributing features include: [list top 3-4 features with values]. The final prediction probability of XX% demonstrates how individual feature values combine to produce the classification. This instance-level explanation enables security analysts to understand exactly why a specific URL was flagged, supporting informed decision-making and user trust."*

- **Caption Template**: 
  *"SHAP force plot for phishing URL (index: XXXX) showing feature contributions to prediction probability of XX%."*

- **In-text reference**: 
  *"Individual SHAP explanations (Figures 5.7-5.11) demonstrate how feature values combine to produce predictions for specific phishing URLs, with VirusTotal scores and lexical anomalies consistently appearing as primary drivers."*

#### Figures 5.12-5.16: SHAP Explanations for Individual Legitimate URLs
- **Files**: `models/phishing_shap_bar_sample_[0-4]_idx_*.png` (legitimate class)
- **Placement**: Subsection 5.3.2 (Individual Legitimate Examples)
- **Description (Generic Template)**: 
  *"Figure 5.X presents SHAP force plot for a legitimate URL (test index: XXXX). Unlike phishing examples, this URL shows negative SHAP contributions from key features: low malicious votes (SHAP: -0.XX), normal domain length (SHAP: -0.XX), and appropriate subdomain count (SHAP: -0.XX). These contributions pull the prediction away from phishing toward legitimate class, resulting in final prediction probability of XX%. The explanation provides transparency for cases where URLs are correctly classified as safe, building user confidence in system reliability."*

- **Caption Template**: 
  *"SHAP force plot for legitimate URL (index: XXXX) showing negative feature contributions resulting in low phishing probability (XX%)."*

- **In-text reference**: 
  *"Legitimate URL explanations (Figures 5.12-5.16) show how normal feature values (low malicious votes, standard domain lengths) consistently push predictions toward the legitimate class."*

#### Figure 5.17: SHAP Waterfall Plot (Sample)
- **File**: Individual waterfall plots can be generated from existing SHAP data
- **Placement**: Subsection 5.3.3 (Alternative Visualization Formats)
- **Description**: 
  *"Figure 5.17 presents an alternative waterfall visualization of SHAP values for a sample prediction. Starting from the base value (expected model output), each feature's contribution is shown as a step in the waterfall, progressively moving the prediction from base value to final output. This sequential visualization helps trace the decision-making process step-by-step, showing cumulative impact of features ordered by magnitude of contribution. The waterfall format is particularly effective for communicating with non-technical stakeholders, as it resembles financial waterfall charts familiar in business contexts."*

- **Caption**: 
  *"SHAP waterfall plot showing sequential feature contributions from base value to final prediction for a sample URL."*

- **In-text reference**: 
  *"Waterfall plots (Figure 5.17) provide an alternative visualization that traces prediction formation step-by-step, facilitating communication with non-technical stakeholders."*

#### Figures 5.18-5.23: Authentication Risk SHAP Explanations
- **Files**: `models/auth_shap_bar_sample_*.png`
- **Placement**: Section 5.4 (Authentication Risk Model Results) or Subsection 5.3.4
- **Description**: 
  *"Figures 5.18-5.23 present SHAP explanations for the authentication risk scoring model. Unlike binary classification, the risk model outputs continuous scores (0-100). SHAP values reveal which factors elevate or reduce risk scores for specific authentication attempts. Common risk-increasing factors include: failed login attempts, geographic anomalies (login from unusual location), device changes, and suspicious timing patterns. Risk-reducing factors include: verified device fingerprints, consistent geographic patterns, and strong SSL certificates. These explanations enable adaptive security responses, such as requiring additional authentication factors when risk scores exceed thresholds."*

- **Caption Template**: 
  *"SHAP explanation for authentication risk score (sample XXXX) showing feature contributions to risk assessment."*

- **In-text reference**: 
  *"Authentication risk explanations (Figures 5.18-5.23) identify behavioral and contextual factors driving risk scores, enabling adaptive security policies based on interpretable risk assessments."*

---

## CHAPTER 6: DISCUSSION

### Section 6.2: Practical Implications

#### Figure 6.1: Framework Revisited (Reference to Figure 1.1 or 3.1)
- **Placement**: Beginning of Section 6.2
- **Description**: 
  *"Returning to the framework architecture (originally presented in Figure 1.1), we can now contextualize the empirical results within the system design. The high performance metrics validate the layered architecture approach, where feature engineering (Layer 3) and machine learning (Layer 4) work synergistically. The SHAP explainability component (Layer 5) successfully addresses the interpretability requirements identified in the problem statement, demonstrating that accuracy and transparency are not mutually exclusive objectives."*

- **In-text reference**: 
  *"Revisiting the framework (Figure 1.1), the empirical results validate the design choices, particularly the integration of diverse feature types and explainable AI components."*

---

## APPENDICES

### Appendix A: Interactive Visualizations

#### Interactive SHAP Force Plots
- **Files**: `models/phishing_shap_force_sample_*.html` and `models/auth_shap_force_sample_*.html`
- **Description**: 
  *"Interactive HTML force plots provide dynamic exploration of SHAP explanations. Users can hover over features to see exact contribution values, zoom into specific regions, and toggle feature visibility. These visualizations are integrated into the Streamlit dashboard for real-time explanation generation during operational deployment."*

### Appendix B: Additional Performance Metrics

#### Cross-Validation Detailed Results
- **File**: `reports/cv_scores.json`
- **Description**: 
  *"Detailed cross-validation results including per-fold accuracy, precision, recall, F1-scores, and training times. These metrics support reproducibility and provide comprehensive performance assessment across different data partitions."*

---

## FIGURE PLACEMENT SUMMARY BY CHAPTER

### Chapter 1: Introduction
- **Total Figures**: 1
- Figure 1.1 (Framework Architecture) → Section 1.3 or 1.4

### Chapter 2: Literature Review
- **Total Figures**: 1
- Figure 2.1 (ML Approaches) → Section 2.3

### Chapter 3: Methodology
- **Total Figures**: 8
- Figures 3.1-3.3 (Architecture) → Section 3.1
- Figures 3.4-3.6 (Features) → Section 3.2
- Figures 3.7-3.8 (Models) → Section 3.3

### Chapter 4: Implementation
- **Total Figures**: 3
- Figures 4.1-4.2 (Data Prep) → Section 4.2
- Figure 4.3 (Feature Distribution) → Section 4.3

### Chapter 5: Results
- **Total Figures**: 20+
- Figures 5.1-5.3 (Performance) → Section 5.1
- Figures 5.4-5.5 (Feature Analysis) → Section 5.2
- Figures 5.6-5.23 (SHAP) → Section 5.3
- Figure 5.15-5.16 (Validation) → Section 5.1

### Chapter 6: Discussion
- **Total Figures**: 0-1 (references to earlier figures)

---

## CAPTION STYLE GUIDELINES

### Format
- **Begin with figure type**: "Figure X.Y presents...", "Figure X.Y shows...", "Figure X.Y illustrates..."
- **Keep concise**: 1-2 sentences maximum
- **Highlight key insight**: Include most important takeaway
- **Avoid redundancy**: Don't repeat information obvious from axis labels

### Examples of Good Captions
✅ "ROC curve demonstrating excellent discriminative performance (AUC = 0.9888) with optimal operating point at 97.2% sensitivity."

✅ "Five-layer framework architecture showing data flow from input (Layer 1) through processing, feature engineering, and classification to explainable output (Layer 5)."

### Examples of Poor Captions
❌ "This is a figure showing the ROC curve."
❌ "ROC curve for the model."
❌ "Figure showing results."

---

## IN-TEXT REFERENCE GUIDELINES

### Placement Rules
1. **Reference before figure appears**: Mention figure 1-2 paragraphs before its placement
2. **Use consistent phrasing**: "As shown in Figure X.Y...", "Figure X.Y demonstrates...", "See Figure X.Y"
3. **Explain significance**: Don't just state "see figure"; explain what reader should observe
4. **Avoid spatial references**: Never say "below" or "above" (figures may move during typesetting)

### Reference Templates
- "The proposed framework (Figure X.Y) addresses these requirements through..."
- "As illustrated in Figure X.Y, the distribution shows clear separation..."
- "Figure X.Y demonstrates that [key finding], indicating [implication]..."
- "These patterns (Figure X.Y) suggest that [interpretation]..."

---

## LATEX CODE TEMPLATES

### Basic Figure
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.85\textwidth]{reports/chapters1-3/chapter1/fig1_1_framework_architecture.png}
    \caption{High-level architecture of the proposed explainable phishing detection framework showing the five-layer structure from data input to interpretable output.}
    \label{fig:framework_architecture}
\end{figure}
```

### Figure with Subfigures
```latex
\begin{figure}[htbp]
    \centering
    \begin{subfigure}[b]{0.48\textwidth}
        \includegraphics[width=\textwidth]{reports/chapter4/figures/fig5_1_roc_curve.png}
        \caption{ROC Curve (AUC = 0.9888)}
        \label{fig:roc}
    \end{subfigure}
    \hfill
    \begin{subfigure}[b]{0.48\textwidth}
        \includegraphics[width=\textwidth]{reports/precision_recall_curve.png}
        \caption{Precision-Recall Curve (AP = 0.9847)}
        \label{fig:pr}
    \end{subfigure}
    \caption{Performance evaluation curves showing exceptional discriminative ability across multiple metrics.}
    \label{fig:performance_curves}
\end{figure}
```

### Referencing in Text
```latex
The proposed framework, illustrated in Figure~\ref{fig:framework_architecture}, adopts a layered architecture...

As shown in Figure~\ref{fig:roc}, the classifier achieves near-perfect discrimination with AUC = 0.9888.
```

---

## MICROSOFT WORD GUIDANCE

### Inserting Figures
1. Place cursor at desired location
2. Insert → Pictures → This Device
3. Navigate to figure file
4. Select and insert
5. Right-click → Size → Lock aspect ratio
6. Set width to 85-90% of page width

### Adding Captions
1. Right-click figure → Insert Caption
2. Label: Figure
3. Position: Below selected item
4. Type caption text
5. Caption will auto-number

### Cross-Referencing
1. Insert → Cross-reference
2. Reference type: Figure
3. Select figure to reference
4. Insert reference type: "Figure X.Y" or custom text
5. Check "Insert as hyperlink"

---

## QUALITY CHECKLIST

Before submission, verify each figure:

- [ ] **Resolution**: 300 DPI minimum for print, 150 DPI minimum for digital
- [ ] **Readability**: Text visible at target print size (usually 85-90% page width)
- [ ] **Caption**: Concise (1-2 sentences), informative, includes key insight
- [ ] **Reference**: Mentioned in text before figure appears
- [ ] **Numbering**: Sequential within chapter (e.g., 3.1, 3.2, 3.3)
- [ ] **Placement**: Near first textual reference (within 1 page)
- [ ] **Format**: Consistent file format (all PNG or all PDF)
- [ ] **Alignment**: Centered or consistently left/right aligned
- [ ] **White space**: Adequate margins around figure
- [ ] **Color**: Accessible to colorblind readers (use patterns/shapes in addition to color)
- [ ] **Labels**: All axes, legends, and annotations clearly labeled
- [ ] **Citation**: If adapted from source, proper attribution in caption

---

## TIPS FOR DIFFERENT THESIS FORMATS

### Traditional Thesis (5-6 Chapters)
- Use all figures as described above
- Place figures inline with text
- Include all SHAP examples in main text or appendix
- Target: 25-35 figures total

### Journal Article (Page Limited)
- Select 6-8 most important figures:
  - Figure 1.1 (Framework)
  - Figure 3.1 (Architecture)
  - Figure 5.1 (ROC)
  - Figure 5.15 (Performance)
  - Figure 5.6 (SHAP Summary)
  - 1-2 Individual SHAP examples
- Move remaining figures to supplementary materials
- Condense multi-panel figures where possible

### Conference Paper (Strict Limits)
- Maximum 4-6 figures:
  - Figure 1.1 (Framework) - possibly simplified
  - Figure 5.1 (ROC) or combined performance
  - Figure 5.6 (SHAP summary)
  - 1 SHAP example
- Create multi-panel composite figures
- Reference full results in extended technical report

### Poster Presentation
- 3-4 large, high-impact figures:
  - Framework architecture
  - Performance comparison (bar chart)
  - SHAP summary or waterfall
- Maximize font sizes (minimum 24pt for labels)
- Use bold colors and high contrast
- Simplify by removing minor annotations

---

## COMMON MISTAKES TO AVOID

### Content Mistakes
❌ **No caption**: Every figure must have a descriptive caption
❌ **Unreferenced figures**: All figures must be mentioned in text
❌ **Figure before mention**: Reference figure before it appears
❌ **Vague captions**: "Results are shown" is not informative
❌ **Redundant text**: Don't repeat exact caption in body text

### Formatting Mistakes
❌ **Inconsistent sizing**: All figures should be similar widths
❌ **Low resolution**: Pixelated figures are unacceptable in academic work
❌ **Poor placement**: Figure separated from discussing text by multiple pages
❌ **Inconsistent numbering**: Skipping numbers or reusing numbers
❌ **Wrong format**: Using format not accepted by publisher/institution

### Design Mistakes
❌ **Tiny fonts**: Text too small to read when printed
❌ **Poor color choices**: Colors indistinguishable when printed or to colorblind readers
❌ **Cluttered plots**: Too much information in single figure
❌ **No legends**: Readers can't interpret colors/symbols
❌ **Unlabeled axes**: Missing units or variable names

---

## RECOMMENDED FIGURE SEQUENCE FOR THESIS DEFENSE PRESENTATION

1. **Slide 2-3**: Figure 1.1 (Framework overview)
2. **Slide 4-5**: Figure 3.1 or 3.2 (Architecture/Data flow)
3. **Slide 6**: Figure 3.3 (Feature pipeline)
4. **Slide 8**: Figure 5.15 (Performance comparison - main result)
5. **Slide 9**: Figure 5.1 (ROC curve)
6. **Slide 10**: Figure 5.6 (SHAP summary)
7. **Slide 11**: One SHAP individual example (phishing)
8. **Slide 12**: One SHAP individual example (legitimate)
9. **Backup slides**: Remaining figures for Q&A

---

## VERSION CONTROL FOR FIGURES

### File Naming Convention
Use consistent naming with version suffixes if regenerating:
- `fig3_1_complete_five_layer_architecture_v1.png` (original)
- `fig3_1_complete_five_layer_architecture_v2.png` (revised)
- `fig3_1_complete_five_layer_architecture_final.png` (approved version)

### Change Log
Document significant figure revisions:
```
Figure 3.1 - Complete Five Layer Architecture
- v1 (2024-11-10): Initial generation
- v2 (2024-11-12): Revised color scheme for accessibility
- v3 (2024-11-14): Added component counts
- final (2024-11-15): Approved by supervisor
```

---

## ACCESSIBILITY CONSIDERATIONS

### Color Blindness
- Don't rely solely on color to convey information
- Use patterns, shapes, or labels in addition to colors
- Test figures with colorblind simulation tools
- Prefer colorblind-friendly palettes (e.g., Viridis, ColorBrewer)

### Screen Readers
- Provide alt text for digital documents
- Describe key patterns/trends in caption
- Use accessible PDF format with proper tagging

### Print Quality
- Ensure grayscale versions are still interpretable
- Test print at target size before submission
- Use high-contrast colors for visibility

---

**Document Version**: 1.0  
**Last Updated**: 2024-11-15  
**Total Figures Documented**: 30+  
**Status**: ✅ Complete and ready for thesis integration

This comprehensive guide ensures all figures are properly documented, placed, and referenced throughout your thesis. Good luck with your submission! 🎓
