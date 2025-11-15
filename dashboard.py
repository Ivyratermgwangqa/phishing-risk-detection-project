import streamlit as st
import os
import json
import glob
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Explainable Phishing Detection Dashboard", layout="wide")

MODEL_DIR = "/home/lerato/phishing-risk-detection-project/models"
METRICS_PATH = os.path.join(MODEL_DIR, "training_metrics.json")

st.title("🛡️ Explainable Phishing Detection Dashboard")

# Tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Model Training", "🔍 Phishing SHAP", "🔐 Authentication SHAP", "🏗️ Framework", "ℹ️ About"])

# Tab 1: Model Training Metrics
with tab1:
    st.header("Model Training Metrics & Performance")
    
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, 'r') as f:
            metrics = json.load(f)
        
        # Data Statistics Section
        st.subheader("📈 Dataset Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        data_stats = metrics.get('data_stats', {})
        with col1:
            st.metric("Total Rows", data_stats.get('total_rows', 'N/A'))
        with col2:
            st.metric("Unique URLs", data_stats.get('unique_urls', 'N/A'))
        with col3:
            st.metric("Duplicate Rows", data_stats.get('duplicate_rows', 'N/A'))
        with col4:
            initial_shape = data_stats.get('initial_shape', [0, 0])
            st.metric("Initial Features", initial_shape[1] if len(initial_shape) > 1 else 0)
        
        # Label Distribution
        st.subheader("🏷️ Label Distribution")
        label_counts = data_stats.get('label_counts', {})
        if label_counts:
            label_df = pd.DataFrame({
                'Label': [f"Class {k} ({'Benign' if k == '0' else 'Phishing'})" for k in label_counts.keys()],
                'Count': list(label_counts.values())
            })
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.dataframe(label_df, hide_index=True)
            with col2:
                fig = px.pie(label_df, values='Count', names='Label', 
                           title='Class Distribution',
                           color_discrete_sequence=['#00cc96', '#ef553b'])
                st.plotly_chart(fig, use_container_width=True)
        
        # Data Preprocessing
        st.subheader("🔧 Data Preprocessing")
        dropped_cols = data_stats.get('dropped_leakage_cols', [])
        if dropped_cols:
            st.warning(f"**Dropped {len(dropped_cols)} potential leakage columns:** {', '.join(dropped_cols)}")
        else:
            st.success("No data leakage columns detected")
        
        final_shape = data_stats.get('final_shape', [0, 0])
        st.info(f"**Final dataset shape:** {final_shape[0]} samples × {final_shape[1]} features")
        
        # Train/Test Split
        st.subheader("✂️ Train/Test Split")
        split_data = metrics.get('train_test_split', {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Training Set**")
            train_shape = split_data.get('train_shape', [0, 0])
            st.metric("Samples", train_shape[0])
            train_dist = split_data.get('train_label_dist', {})
            if train_dist:
                train_df = pd.DataFrame({
                    'Class': [f"{k} ({'Benign' if k == 0 else 'Phishing'})" for k in train_dist.keys()],
                    'Count': list(train_dist.values())
                })
                st.dataframe(train_df, hide_index=True)
        
        with col2:
            st.markdown("**Test Set**")
            test_shape = split_data.get('test_shape', [0, 0])
            st.metric("Samples", test_shape[0])
            test_dist = split_data.get('test_label_dist', {})
            if test_dist:
                test_df = pd.DataFrame({
                    'Class': [f"{k} ({'Benign' if k == 0 else 'Phishing'})" for k in test_dist.keys()],
                    'Count': list(test_dist.values())
                })
                st.dataframe(test_df, hide_index=True)
        
        # Model Performance
        st.subheader("🎯 Model Performance Metrics")
        perf = metrics.get('model_performance', {})
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            auc = perf.get('auc', 0)
            st.metric("AUC-ROC", f"{auc:.4f}", 
                     delta="Excellent" if auc > 0.95 else ("Good" if auc > 0.85 else "Fair"),
                     delta_color="normal" if auc > 0.85 else "inverse")
        with col2:
            precision = perf.get('precision', 0)
            st.metric("Precision", f"{precision:.4f}")
        with col3:
            recall = perf.get('recall', 0)
            st.metric("Recall", f"{recall:.4f}")
        with col4:
            f1 = perf.get('f1', 0)
            st.metric("F1 Score", f"{f1:.4f}")
        
        # Performance visualization
        metrics_df = pd.DataFrame({
            'Metric': ['Precision', 'Recall', 'F1 Score', 'AUC'],
            'Score': [precision, recall, f1, auc]
        })
        
        fig = go.Figure(data=[
            go.Bar(x=metrics_df['Metric'], y=metrics_df['Score'],
                  marker_color=['#636EFA', '#EF553B', '#00CC96', '#AB63FA'],
                  text=metrics_df['Score'].round(4),
                  textposition='outside')
        ])
        fig.update_layout(
            title='Model Performance Overview',
            yaxis_title='Score',
            yaxis_range=[0, 1.1],
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # ROC Curve Visualization
        roc_data = metrics.get('roc_curve', {})
        if roc_data and 'fpr' in roc_data and 'tpr' in roc_data:
            st.subheader("📈 ROC Curve")
            
            fpr = roc_data['fpr']
            tpr = roc_data['tpr']
            
            fig_roc = go.Figure()
            
            # Add ROC curve
            fig_roc.add_trace(go.Scatter(
                x=fpr, 
                y=tpr,
                mode='lines',
                name=f'ROC Curve (AUC = {auc:.4f})',
                line=dict(color='#636EFA', width=3),
                hovertemplate='FPR: %{x:.3f}<br>TPR: %{y:.3f}<extra></extra>'
            ))
            
            # Add diagonal reference line (random classifier)
            fig_roc.add_trace(go.Scatter(
                x=[0, 1], 
                y=[0, 1],
                mode='lines',
                name='Random Classifier',
                line=dict(color='gray', width=2, dash='dash'),
                hovertemplate='Random Classifier<extra></extra>'
            ))
            
            fig_roc.update_layout(
                title='Receiver Operating Characteristic (ROC) Curve',
                xaxis_title='False Positive Rate',
                yaxis_title='True Positive Rate',
                xaxis=dict(range=[0, 1]),
                yaxis=dict(range=[0, 1]),
                showlegend=True,
                legend=dict(x=0.6, y=0.1),
                hovermode='closest'
            )
            
            st.plotly_chart(fig_roc, use_container_width=True)
            
            # Add interpretation guide
            with st.expander("ℹ️ Understanding the ROC Curve"):
                st.markdown("""
                The **ROC (Receiver Operating Characteristic) Curve** shows the trade-off between:
                - **True Positive Rate (TPR)**: Sensitivity - how many actual phishing URLs are correctly identified
                - **False Positive Rate (FPR)**: 1 - Specificity - how many benign URLs are incorrectly flagged as phishing
                
                **Interpretation:**
                - **Area Under Curve (AUC)**: Ranges from 0 to 1
                  - AUC = 1.0: Perfect classifier
                  - AUC = 0.9-1.0: Excellent performance ✅
                  - AUC = 0.8-0.9: Good performance
                  - AUC = 0.5: Random guessing (diagonal line)
                
                **Current Model:**
                - AUC = {:.4f} indicates {} performance
                - The curve's distance from the diagonal shows the model's discriminative ability
                """.format(auc, "excellent" if auc > 0.95 else ("good" if auc > 0.85 else "fair")))
        
        # Feature Information
        with st.expander("📋 Feature Information"):
            feature_info = metrics.get('features', {})
            st.write(f"**Total numeric features used:** {feature_info.get('numeric_features_count', 0)}")
            feature_names = feature_info.get('feature_names', [])
            if feature_names:
                st.write("**Feature names:**")
                st.code(', '.join(feature_names))
    else:
        st.warning("⚠️ Training metrics not found. Please run `train_model.py` first to generate metrics.")
        st.code("export ALL_FEATURES=data/processed/phishing_graph_features_vt.csv\npython src/train_model.py")

# Tab 2: Phishing SHAP
with tab2:
    st.header("Phishing Model SHAP Explanations (Top 5)")
    shap_found = False
    for i in range(5):
        pngs = glob.glob(os.path.join(MODEL_DIR, f"phishing_shap_bar_sample_{i}_idx_*.png"))
        htmls = glob.glob(os.path.join(MODEL_DIR, f"phishing_shap_force_sample_{i}_idx_*.html"))
        if pngs or htmls:
            shap_found = True
            st.subheader(f"Sample {i+1}")
            if pngs:
                st.image(pngs[0], caption=os.path.basename(pngs[0]))
            if htmls:
                st.markdown(f"[View Interactive Force Plot]({htmls[0]})")
            st.markdown("---")
    
    if not shap_found:
        st.info("No SHAP visualizations found. Run predictions to generate SHAP explanations.")

# Tab 3: Authentication SHAP
with tab3:
    st.header("Authentication Model SHAP Explanations (Top 5)")
    shap_found = False
    for i in range(5):
        pngs = glob.glob(os.path.join(MODEL_DIR, f"auth_shap_bar_sample_{i}_idx_*.png"))
        htmls = glob.glob(os.path.join(MODEL_DIR, f"auth_shap_force_sample_{i}_idx_*.html"))
        if pngs or htmls:
            shap_found = True
            st.subheader(f"Sample {i+1}")
            if pngs:
                st.image(pngs[0], caption=os.path.basename(pngs[0]))
            if htmls:
                st.markdown(f"[View Interactive Force Plot]({htmls[0]})")
            st.markdown("---")
    
    if not shap_found:
        st.info("No authentication SHAP visualizations found.")

# Tab 4: Framework Visualization
with tab4:
    st.header("🏗️ Explainable Phishing Detection Framework")
    
    st.markdown("""
    This framework integrates multiple components to provide comprehensive, explainable phishing detection 
    with threat intelligence enrichment and risk scoring.
    """)
    
    # Framework Architecture Diagram
    st.subheader("📐 Framework Architecture")
    
    # Create a visual flow using Plotly
    fig_flow = go.Figure()
    
    # Define nodes (components)
    nodes = [
        # Layer 1: Input
        {"name": "URL Input", "x": 0.5, "y": 1.0, "color": "#636EFA", "layer": "Input"},
        
        # Layer 2: Feature Extraction
        {"name": "URL Features", "x": 0.2, "y": 0.8, "color": "#EF553B", "layer": "Feature Extraction"},
        {"name": "Graph Features", "x": 0.5, "y": 0.8, "color": "#EF553B", "layer": "Feature Extraction"},
        {"name": "VirusTotal Intel", "x": 0.8, "y": 0.8, "color": "#EF553B", "layer": "Feature Extraction"},
        
        # Layer 3: ML Models
        {"name": "Phishing Classifier", "x": 0.3, "y": 0.6, "color": "#00CC96", "layer": "ML Models"},
        {"name": "Auth Risk Model", "x": 0.7, "y": 0.6, "color": "#00CC96", "layer": "ML Models"},
        
        # Layer 4: Explainability
        {"name": "SHAP Explanations", "x": 0.5, "y": 0.4, "color": "#AB63FA", "layer": "Explainability"},
        
        # Layer 5: Output
        {"name": "Risk Score & Report", "x": 0.5, "y": 0.2, "color": "#FFA15A", "layer": "Output"},
    ]
    
    # Add nodes as scatter points
    for node in nodes:
        fig_flow.add_trace(go.Scatter(
            x=[node["x"]],
            y=[node["y"]],
            mode='markers+text',
            marker=dict(size=60, color=node["color"], line=dict(width=2, color='white')),
            text=node["name"],
            textposition="middle center",
            textfont=dict(size=10, color='white', family='Arial Black'),
            name=node["layer"],
            showlegend=False,
            hovertemplate=f"<b>{node['name']}</b><br>{node['layer']}<extra></extra>"
        ))
    
    # Define edges (connections)
    edges = [
        # Input to Features
        (0, 1), (0, 2), (0, 3),
        # Features to Models
        (1, 4), (2, 4), (3, 4),
        (1, 5), (2, 5), (3, 5),
        # Models to Explainability
        (4, 6), (5, 6),
        # Explainability to Output
        (6, 7),
    ]
    
    # Add edges as lines
    for edge in edges:
        fig_flow.add_trace(go.Scatter(
            x=[nodes[edge[0]]["x"], nodes[edge[1]]["x"]],
            y=[nodes[edge[0]]["y"], nodes[edge[1]]["y"]],
            mode='lines',
            line=dict(color='rgba(150,150,150,0.4)', width=2),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    fig_flow.update_layout(
        title="Phishing Detection Framework Pipeline",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.1, 1.1]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1.1]),
        height=600,
        plot_bgcolor='rgba(240,240,240,0.5)',
        hovermode='closest'
    )
    
    st.plotly_chart(fig_flow, use_container_width=True)
    
    # Detailed Component Explanations
    st.subheader("🔧 Framework Components")
    
    with st.expander("1️⃣ Input Layer - URL Collection", expanded=True):
        st.markdown("""
        **Purpose:** Initial URL data collection from various sources
        
        **Sources:**
        - Email security gateways
        - Web proxy logs
        - User reports
        - Threat intelligence feeds
        
        **Processing:**
        - URL normalization and validation
        - Duplicate detection
        - Initial filtering
        """)
    
    with st.expander("2️⃣ Feature Extraction Layer", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **URL Features**
            - Domain characteristics
            - Path structure
            - Parameter analysis
            - Character patterns
            - String entropy
            """)
        
        with col2:
            st.markdown("""
            **Graph Features**
            - Redirect chain analysis
            - Network topology
            - Node centrality metrics
            - Community detection
            - Temporal patterns
            """)
        
        with col3:
            st.markdown("""
            **VirusTotal Intelligence**
            - Malicious score
            - Harmless score
            - Suspicious score
            - Vendor detections
            - Historical reputation
            """)
    
    with st.expander("3️⃣ Machine Learning Models", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Phishing Classifier**
            - Algorithm: Random Forest
            - Features: URL + Graph + VT data
            - Output: Phishing probability
            - Class weights: Balanced
            - Performance: AUC > 0.98
            """)
        
        with col2:
            st.markdown("""
            **Authentication Risk Model**
            - Credential harvesting detection
            - Login page identification
            - Brand impersonation analysis
            - Form analysis
            - SSL/TLS validation
            """)
    
    with st.expander("4️⃣ Explainability Layer - SHAP", expanded=True):
        st.markdown("""
        **SHAP (SHapley Additive exPlanations)**
        
        Provides interpretable explanations for model predictions:
        
        - **Feature Importance:** Which features contributed most to the prediction
        - **Direction:** Whether features pushed toward phishing or benign classification
        - **Magnitude:** How much each feature influenced the decision
        
        **Visualization Types:**
        - **Bar Plots:** Top contributing features for each prediction
        - **Force Plots:** Interactive visualization showing feature impact
        - **Waterfall Plots:** Step-by-step contribution breakdown
        
        **Benefits for SOC Teams:**
        - Understand *why* a URL was flagged
        - Validate model decisions
        - Identify false positives quickly
        - Build trust in automated detection
        """)
    
    with st.expander("5️⃣ Output Layer - Risk Scoring", expanded=True):
        st.markdown("""
        **Risk Score Calculation:**
        - Combines phishing probability with authentication risk
        - Incorporates VirusTotal threat intelligence
        - Provides confidence intervals
        
        **Report Generation:**
        - Detailed risk assessment
        - SHAP explanation visualizations
        - Actionable recommendations
        - Evidence summary
        
        **Integration Points:**
        - SIEM systems
        - Email gateways
        - Incident response platforms
        - Threat intelligence platforms
        """)
    
    # Application Workflow
    st.subheader("🔄 Application Workflow")
    
    workflow_steps = {
        "Step 1": {
            "title": "Data Preparation",
            "description": "Process and merge URL features with VirusTotal intelligence",
            "command": "python src/merge_vt_features.py",
            "output": "data/processed/phishing_graph_features_vt.csv"
        },
        "Step 2": {
            "title": "Model Training",
            "description": "Train Random Forest classifier on enriched dataset",
            "command": "export ALL_FEATURES=data/processed/phishing_graph_features_vt.csv\npython src/train_model.py",
            "output": "models/phishing_rf_model.pkl + training_metrics.json"
        },
        "Step 3": {
            "title": "Risk Prediction",
            "description": "Generate predictions with SHAP explanations for new URLs",
            "command": "python src/risk.py",
            "output": "SHAP visualizations + risk scores"
        },
        "Step 4": {
            "title": "Dashboard Analysis",
            "description": "Visualize results and model performance",
            "command": "streamlit run dashboard.py",
            "output": "Interactive web dashboard"
        }
    }
    
    for step, details in workflow_steps.items():
        with st.container():
            st.markdown(f"### {step}: {details['title']}")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {details['description']}")
                st.code(details['command'], language='bash')
            
            with col2:
                st.markdown(f"**Output:**")
                st.info(details['output'])
            
            st.markdown("---")
    
    # Use Cases
    st.subheader("💼 Real-World Use Cases")
    
    use_case_col1, use_case_col2 = st.columns(2)
    
    with use_case_col1:
        st.markdown("""
        **🏢 SOC Operations**
        - Automated URL triage
        - Reduce false positive rate
        - Prioritize high-risk threats
        - Validate alerts with explanations
        
        **📧 Email Security**
        - Real-time link scanning
        - Malicious URL blocking
        - User warning systems
        - Phishing campaign detection
        """)
    
    with use_case_col2:
        st.markdown("""
        **🔍 Incident Response**
        - Forensic URL analysis
        - Attack chain reconstruction
        - IOC enrichment
        - Evidence documentation
        
        **📊 Threat Intelligence**
        - URL reputation scoring
        - Threat actor profiling
        - Campaign tracking
        - Intelligence sharing
        """)
    
    # Performance Metrics
    st.subheader("📈 Framework Performance")
    
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, 'r') as f:
            metrics = json.load(f)
        
        perf = metrics.get('model_performance', {})
        
        metrics_summary = pd.DataFrame({
            'Metric': ['AUC-ROC', 'Precision', 'Recall', 'F1 Score'],
            'Score': [
                perf.get('auc', 0),
                perf.get('precision', 0),
                perf.get('recall', 0),
                perf.get('f1', 0)
            ],
            'Interpretation': [
                'Excellent discrimination capability',
                'High accuracy when flagging phishing',
                'Catches most phishing attempts',
                'Balanced precision and recall'
            ]
        })
        
        st.dataframe(metrics_summary, use_container_width=True, hide_index=True)
        
        st.success(f"""
        **Framework Effectiveness:** The model achieves {perf.get('auc', 0):.2%} AUC-ROC, 
        demonstrating excellent ability to distinguish between phishing and benign URLs. 
        With {perf.get('recall', 0):.2%} recall, it catches the vast majority of phishing attempts 
        while maintaining {perf.get('precision', 0):.2%} precision to minimize false positives.
        """)
    else:
        st.info("Train the model to see performance metrics")
    
    # Technical Stack
    with st.expander("🛠️ Technical Stack"):
        tech_col1, tech_col2, tech_col3 = st.columns(3)
        
        with tech_col1:
            st.markdown("""
            **Machine Learning**
            - scikit-learn
            - Random Forest
            - SHAP
            - pandas/numpy
            """)
        
        with tech_col2:
            st.markdown("""
            **Threat Intelligence**
            - VirusTotal API
            - URL analysis
            - Domain reputation
            - Historical data
            """)
        
        with tech_col3:
            st.markdown("""
            **Visualization**
            - Streamlit
            - Plotly
            - Matplotlib
            - Interactive dashboards
            """)

# Tab 5: About
with tab5:
    st.header("About This Dashboard")
    st.markdown("""
    This dashboard provides comprehensive insights into the Explainable Phishing Detection Framework.
    
    ### Features:
    - **Model Training Metrics**: View detailed statistics about data preprocessing, train/test splits, and model performance
    - **SHAP Explanations**: Understand model predictions through SHAP (SHapley Additive exPlanations) visualizations
    - **Interactive Visualizations**: Explore data distributions and performance metrics
    
    ### Data Sources:
    - Training data includes URL features, graph features, and VirusTotal threat intelligence
    - Model uses Random Forest classifier with balanced class weights
    - SHAP values provide local explanations for individual predictions
    
    ### Usage:
    1. Train the model: `python src/train_model.py`
    2. Generate predictions: `python src/risk.py`
    3. View this dashboard: `streamlit run dashboard.py`
    
    ---
    *For more information, see the project README.*
    """)
