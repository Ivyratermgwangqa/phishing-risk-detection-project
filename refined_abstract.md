# Refined Abstract

## Background
Phishing attacks continue to evolve rapidly, evading traditional signature-based and heuristic defenses. Current detection systems often operate as opaque classifiers, providing minimal actionable context to Security Operations Center (SOC) analysts and failing to correlate email-based threats with subsequent authentication anomalies.

## Aim
This study develops an operational explainable phishing detection framework that integrates metadata-driven graph features, real-time threat intelligence, and post-event behavioral signals to enhance both detection performance and analyst interpretability.

## Method
The framework combines email metadata and lexical features with NetworkX-derived graph metrics constructed from sender→URL→domain relationships. Samples were enriched with VirusTotal threat intelligence and synthetic authentication logs to simulate post-compromise behavior. A Random Forest classifier employing median imputation was trained using group-aware data splits to prevent URL leakage, with SHAP TreeExplainer generating model interpretations. Evaluation employed stratified and grouped cross-validation alongside standard performance metrics (ROC-AUC, precision, recall, F1-score), with results delivered through reproducible artifacts and an interactive Streamlit dashboard.

## Findings
Experiments on curated phishing and benign email corpora demonstrated strong discriminative performance (ROC-AUC ≈ 0.989) with high precision and recall (0.92–0.96) following leakage mitigation strategies. SHAP analyses consistently identified graph-derived and targeted lexical features as primary contributors, demonstrating both predictive power and human-interpretable rationale. VirusTotal integration enhanced contextual threat awareness where cyber threat intelligence (CTI) coverage existed, while authentication risk signals provided complementary validation in simulated post-event scenarios.

## Conclusion
This integrated framework significantly advances phishing detection capabilities by delivering per-sample, analyst-friendly explanations alongside operational artifacts suited for SOC workflows. Future research should focus on operationalizing live CTI feeds, expanding behavioral datasets with real-world authentication logs, and implementing continuous model monitoring with automated retraining pipelines to maintain efficacy against evolving adversarial tactics.

---

## Key Improvements Made:

1. **Language refinement**: Removed hyphenation inconsistencies (e.g., "signature based" → "signature-based")
2. **Clarity enhancement**: Improved flow and readability while maintaining technical precision
3. **Academic tone**: Strengthened formal academic writing style
4. **Specificity**: Added clarifying terms (e.g., "cyber threat intelligence (CTI)", "ROC-AUC")
5. **Conciseness**: Tightened sentences without losing essential information
6. **Structure**: Maintained clear section divisions with improved transitions
7. **Technical accuracy**: Ensured proper terminology (e.g., "cross-validation", "F1-score")
8. **Future work**: Expanded with more specific actionable recommendations
