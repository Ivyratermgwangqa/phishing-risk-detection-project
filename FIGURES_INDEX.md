# Complete Figures Index for Research Report

## Overview
This document provides a complete index of all visualizations available for your phishing risk detection research report.

---

## 📁 Chapters 1-3 Figures (Newly Generated)

### Location
`reports/chapters1-3/`

### Summary
- **Total Figures**: 10
- **Resolution**: 300 DPI
- **Format**: PNG
- **Total Size**: ~2.8 MB
- **Status**: ✅ Ready to use

### Chapter 1: Introduction

| Figure | Title | Filename | Purpose |
|--------|-------|----------|---------|
| 1.1 | Explainable Phishing Detection Framework Architecture | `chapter1/fig1_1_framework_architecture.png` | High-level framework overview showing all 5 layers |

### Chapter 2: Literature Review

| Figure | Title | Filename | Purpose |
|--------|-------|----------|---------|
| 2.1 | Overview of Machine Learning Approaches in Phishing Detection | `chapter2/fig2_1_ml_approaches_overview.png` | Categorization of ML approaches, highlighting chosen method |

### Chapter 3: Methodology

#### 3.1 System Architecture

| Figure | Title | Filename | Purpose |
|--------|-------|----------|---------|
| 3.1 | Complete Framework Architecture with Five Layers | `chapter3/fig3_1_complete_five_layer_architecture.png` | Detailed architectural diagram with all components |
| 3.2 | Data Flow Diagram from Input to Output | `chapter3/fig3_2_data_flow_diagram.png` | Step-by-step data transformation pipeline |
| 3.3 | Feature Extraction Pipeline | `chapter3/fig3_3_feature_extraction_pipeline.png` | Parallel feature extraction processes |

#### 3.2 Feature Engineering

| Figure | Title | Filename | Purpose |
|--------|-------|----------|---------|
| 3.4 | URL Feature Extraction Process | `chapter3/fig3_4_url_feature_extraction.png` | URL-based feature extraction with example |
| 3.5 | Graph-Based Feature Analysis | `chapter3/fig3_5_graph_feature_analysis.png` | Graph features with network visualization |
| 3.6 | VirusTotal Intelligence Integration | `chapter3/fig3_6_virustotal_integration.png` | VirusTotal API integration workflow |

#### 3.3 Machine Learning Models

| Figure | Title | Filename | Purpose |
|--------|-------|----------|---------|
| 3.7 | Random Forest Classifier Architecture | `chapter3/fig3_7_random_forest_architecture.png` | Random Forest model structure and voting |
| 3.8 | Authentication Risk Model Components | `chapter3/fig3_8_auth_risk_model.png` | Authentication risk scoring model |

---

## 📊 Chapters 4-5 Figures (Previously Generated)

### Location
`reports/chapter4/figures/`

### Summary
- **Total Figures**: 6
- **Resolution**: 300 DPI
- **Format**: PNG
- **Status**: ✅ Available

### Chapter 4: Implementation

| Figure | Title | Filename | Purpose |
|--------|-------|----------|---------|
| 4.1 | Training and Validation Workflow | `fig4_1_train_test_split.png` | Train/test split with label distribution |
| 4.2 | Data Preprocessing Pipeline | `fig4_2_preprocessing_stats.png` | Data preprocessing statistics |

### Chapter 5: Results and Analysis

| Figure | Title | Filename | Purpose |
|--------|-------|----------|---------|
| 5.1 | ROC Curve for Phishing Classifier | `fig5_1_roc_curve.png` | ROC curve showing AUC = 0.9888 |
| 5.15 | Model Performance Comparison Across Metrics | `fig5_15_performance_comparison.png` | Bar chart of performance metrics |
| 5.16 | Cross-Validation Scores Distribution | `fig5_16_cv_scores.png` | 5-fold CV scores with mean |
| - | Feature Categories Distribution | `feature_categories_pie.png` | Pie chart of feature categories |

---

## 🔍 SHAP Explanation Visualizations

### Location
`models/`

### Phishing Detection SHAP Plots

| Type | Filename Pattern | Count | Purpose |
|------|------------------|-------|---------|
| Summary Plot | `phishing_shap_summary.png` | 1 | Global feature importance |
| Bar Plots (Benign) | `phishing_shap_bar_sample_[0-4]_idx_*.png` | 5 | Individual benign URL explanations |
| Bar Plots (Phishing) | `phishing_shap_bar_sample_[0-4]_idx_*.png` | 5 | Individual phishing URL explanations |
| Force Plots | `phishing_shap_force_sample_*.html` | 5 | Interactive force plots |

**Total Phishing SHAP Visualizations**: 16 files

### Authentication Risk SHAP Plots

| Type | Filename Pattern | Count | Purpose |
|------|------------------|-------|---------|
| Bar Plots | `auth_shap_bar_sample_*.png` | 6 | Individual prediction explanations |
| Force Plots | `auth_shap_force_sample_*.html` | 5 | Interactive force plots |

**Total Auth SHAP Visualizations**: 11 files

---

## 📈 Additional Visualizations

### Location
`reports/`

| Filename | Purpose |
|----------|---------|
| `confusion_matrix.png` | Test set confusion matrix |
| `precision_recall_curve.png` | Precision-recall curve |
| `graph_metrics_distribution.png` | Distribution of graph features |
| `vt_feature_distribution.png` | VirusTotal feature distribution |

### ROC Curves

| Filename | Location | Purpose |
|----------|----------|---------|
| `phishing_roc_curve.png` | `src/` | Phishing classifier ROC |
| `auth_risk_holdout_roc.png` | `models/` | Auth risk model ROC |

---

## 🎯 Complete Figure Count

| Category | Count | Status |
|----------|-------|--------|
| Chapters 1-3 (Introduction, Lit Review, Methodology) | 10 | ✅ Generated |
| Chapters 4-5 (Implementation, Results) | 6 | ✅ Available |
| SHAP Visualizations (Phishing) | 16 | ✅ Available |
| SHAP Visualizations (Auth Risk) | 11 | ✅ Available |
| Additional Metrics Plots | 5 | ✅ Available |
| **Total** | **48** | **✅ Ready** |

---

## 🚀 Quick Access Commands

### View Chapters 1-3 Figures
```bash
source .venv/bin/activate
python view_chapters1_3_figures.py
```

### Regenerate Chapters 1-3 Figures
```bash
source .venv/bin/activate
python generate_chapters1_3_viz.py
```

### Regenerate Chapters 4-5 Figures
```bash
source .venv/bin/activate
python generate_chapter4_viz.py
```

### View Interactive Dashboard
```bash
source .venv/bin/activate
python dashboard.py
```

### List All Figures
```bash
# Chapters 1-3
find reports/chapters1-3 -name "*.png"

# Chapters 4-5
find reports/chapter4 -name "*.png"

# SHAP plots
ls models/*shap*.png

# All figures
find . -name "*.png" | grep -E "(reports|models)" | sort
```

---

## 📚 Documentation Files

| Document | Description |
|----------|-------------|
| `CHAPTERS1-3_FIGURES_GUIDE.md` | Comprehensive guide for Chapters 1-3 figures |
| `CHAPTERS1-3_SUMMARY.md` | Summary of generated figures and usage |
| `QUICK_START_FIGURES.txt` | Quick reference card |
| `FIGURES_INDEX.md` | This file - complete index |
| `README_CHAPTER4.md` | Guide for Chapter 4 visualizations |
| `DASHBOARD_GUIDE.md` | Dashboard usage instructions |

---

## 🎨 Figure Specifications

### Technical Details
- **Resolution**: 300 DPI (all figures)
- **Format**: PNG (lossless compression)
- **Color Space**: RGB
- **Background**: White or transparent where appropriate

### Color Scheme (Chapters 1-3)
- **Purple (#9b59b6)**: Input layer
- **Orange (#f39c12)**: Processing layer
- **Red (#e74c3c)**: Feature engineering layer
- **Blue (#3498db)**: Machine learning layer
- **Green (#2ecc71)**: Output layer

### Typography
- **Font Family**: Arial, DejaVu Sans
- **Title Size**: 14-16pt
- **Body Text**: 8-11pt
- **Labels**: 7-9pt

---

## 📝 Using Figures in Your Report

### Microsoft Word
1. Insert → Pictures
2. Navigate to appropriate folder
3. Select figure
4. Resize to 90% page width
5. Add caption: Insert → Caption
6. Reference: "As shown in Figure X.Y..."

### LaTeX
```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.9\textwidth]{path/to/figure.png}
    \caption{Your caption here}
    \label{fig:your_label}
\end{figure}

% Reference: Figure~\ref{fig:your_label}
```

### Markdown
```markdown
![Figure X.Y: Title](path/to/figure.png)
*Figure X.Y: Your caption here*
```

---

## 🔄 Workflow for Report Writing

1. **Introduction (Chapter 1)**
   - Use Figure 1.1 to introduce framework
   
2. **Literature Review (Chapter 2)**
   - Use Figure 2.1 to contextualize approach
   
3. **Methodology (Chapter 3)**
   - Use Figures 3.1-3.8 to explain system in detail
   - Order: Architecture → Data Flow → Features → Models
   
4. **Implementation (Chapter 4)**
   - Use Figures 4.1-4.2 for training workflow
   - Reference preprocessing statistics
   
5. **Results (Chapter 5)**
   - Use Figures 5.1, 5.15, 5.16 for performance
   - Include SHAP plots for explainability
   - Use confusion matrix and PR curves
   
6. **Discussion**
   - Reference framework figures again
   - Highlight key SHAP insights

---

## 🎓 Tips for Academic Writing

### Figure Captions
- Keep captions concise (2-3 sentences)
- Explain what the figure shows
- Highlight key findings or patterns
- Use consistent formatting

### Figure References
- Always reference before the figure appears
- Use "Figure X.Y shows..." or "As shown in Figure X.Y..."
- Don't say "below" or "above" (figures may move)

### Figure Placement
- Place near first reference in text
- Group related figures together
- Use consistent sizing throughout
- Ensure readability at printed size

---

## 📊 Suggested Figure Usage by Section

### Thesis/Dissertation
Use all 48+ figures distributed across chapters

### Journal Paper (Page Limited)
Focus on core figures:
- Figure 1.1 (Framework)
- Figure 3.1 (Architecture)
- Figure 3.3 (Pipeline)
- Figure 5.1 (ROC)
- Figure 5.15 (Performance)
- 2-3 SHAP plots

### Conference Paper (Strict Limits)
Essential figures only:
- Figure 1.1 (Framework)
- Figure 5.1 (ROC)
- 1 SHAP plot
- Figure 5.15 (Performance)

### Presentation
- Extract key figures
- Simplify complex diagrams
- Increase font sizes
- Use landscape orientation

---

## ✨ Quality Checklist

Before including figures in final report:

- [ ] All figures are high resolution (300 DPI)
- [ ] Captions are clear and informative
- [ ] Figure numbers are sequential
- [ ] All figures are referenced in text
- [ ] Consistent sizing and formatting
- [ ] Readable when printed at target size
- [ ] Color scheme is consistent
- [ ] Labels and annotations are clear
- [ ] Files are in correct format (PNG/PDF)
- [ ] No copyright issues (all generated)

---

## 🆘 Support Resources

### Regeneration Scripts
- `generate_chapters1_3_viz.py` - Chapters 1-3
- `generate_chapter4_viz.py` - Chapters 4-5
- `dashboard.py` - Interactive visualizations

### Viewing Tools
- `view_chapters1_3_figures.py` - Interactive figure browser
- Any image viewer for individual files
- Web browser for HTML force plots

### Documentation
- All guide files in project root
- Inline comments in generation scripts
- README files for specific components

---

**Last Updated**: 2025-11-15  
**Total Figures Available**: 48+  
**Status**: ✅ All figures ready for use

Your complete visualization suite is ready to enhance your research report! 🎉
