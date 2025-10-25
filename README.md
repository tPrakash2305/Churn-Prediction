# Telecom Customer Churn Prediction System

A comprehensive machine learning project for predicting customer churn in telecom industry using advanced analytics, multiple ML models, and an interactive Streamlit dashboard.

## 🎯 Project Overview

This project implements a complete end-to-end machine learning pipeline for customer churn prediction, featuring:

- Data preprocessing and feature engineering
- Multiple ML models (Logistic Regression, Random Forest, XGBoost)
- Model explainability with SHAP
- Interactive web dashboard for business users
- Batch prediction capabilities

## Project Structure

```
telco-churn-project/
├── data/
│   ├── raw/              # Original dataset
│   └── processed/        # Cleaned and transformed data
├── notebooks/
│   ├── 01_EDA.ipynb      # Exploratory Data Analysis
│   ├── 02_Preprocessing_and_Features.ipynb
│   └── 03_Modeling_and_Evaluation.ipynb
├── src/
│   ├── data_prep.py      # Data loading and cleaning
│   ├── features.py       # Feature engineering
│   ├── train.py          # Model training
│   ├── eval.py           # Model evaluation
│   └── predict.py        # Prediction functions
├── models/               # Saved models and preprocessors
├── app/
│   └── app.py           # Streamlit dashboard
├── reports/             # Analysis reports
├── requirements.txt
└── README.md
```

## Quick Start

### 1. Clone or Download the Project

```bash
cd DMBI_MiniProject
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download Dataset

Download the **Telco Customer Churn** dataset from Kaggle:

- Link: https://www.kaggle.com/datasets/blastchar/telco-customer-churn
- Place the `WA_Fn-UseC_-Telco-Customer-Churn.csv` file in `data/raw/` folder
- Rename it to `telco_churn.csv`

### 4. Train the Model

```bash
python src/train.py
```

This will:

- Load and preprocess the data
- Train multiple models
- Save the best model and preprocessor
- Generate evaluation reports

### 5. Run the Streamlit Dashboard

```bash
streamlit run app/app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📊 Interactive Dashboard Features

The system includes a professional, production-ready web dashboard built with Streamlit, featuring a modern dark theme with gradient backgrounds and Font Awesome icons for an enterprise-grade user experience.

### 🏠 Home Dashboard

**Overview & Analytics**

- **Hero Section**: Welcome banner with project mission statement
- **Feature Cards**: Four gradient-styled cards showcasing core capabilities:
  - 📊 Data Analysis: Interactive exploratory visualizations
  - 🧠 AI Predictions: Real-time ML-powered churn scoring
  - 🏆 Performance Metrics: Model accuracy and validation tracking
  - 💼 Business Value: ROI and retention strategy insights
- **Dataset Metrics**: Real-time statistics dashboard displaying:
  - Total customer count (7,021 records)
  - Churned customer count and percentage
  - Overall churn rate (26.5%)
  - Number of analyzed features (24)
- **Key Insights Panel**: Business impact highlights and ML model overview
- **Sample Data Preview**: Expandable table with dataset inspection

### 📈 Exploratory Data Analysis (EDA)

**Visual Intelligence**

- **Churn Distribution Analysis**:
  - Interactive pie charts showing churn vs retention rates
  - Animated bar charts with Plotly for dynamic exploration
- **Feature Analytics**:
  - Numerical feature distributions with histograms
  - Categorical feature breakdowns by churn status
  - Cross-tabulation analysis for service adoption patterns
- **Correlation Heatmap**: Interactive matrix showing feature relationships
- **Segmentation Views**: Customer cohort analysis by:
  - Contract type (Month-to-month, One year, Two year)
  - Internet service (DSL, Fiber optic, No service)
  - Payment methods and tenure groups
- **Statistical Summaries**: Comprehensive descriptive statistics
- **Data Quality Dashboard**: Missing values and data integrity checks

### 🔮 Predict Churn

**Real-Time Prediction Engine**

#### Single Customer Prediction

- **Intelligent Input Form**: Organized in logical sections
  - 👤 **Demographics**: Gender, Senior Citizen status, Partner, Dependents
  - 📱 **Services**: Phone, Internet, Security, Backup, Streaming options
  - 💳 **Account Details**: Contract type, Billing method, Payment preferences
  - 💰 **Financial**: Monthly charges, Total charges, Tenure
- **Instant Predictions**: Submit button triggers real-time ML inference
- **Risk Assessment Output**:
  - Churn probability score (0-100%)
  - Risk level classification with color coding:
    - 🔴 **HIGH RISK**: >60% churn probability
    - 🟡 **MEDIUM RISK**: 30-60% churn probability
    - 🟢 **LOW RISK**: <30% churn probability
  - Confidence percentage and prediction certainty
- **Explainable AI (SHAP)**:
  - Feature importance waterfall chart
  - Top factors contributing to prediction
  - Why the model made this specific decision
  - Actionable insights for retention strategies

#### Batch Prediction

- **CSV Upload Interface**: Drag-and-drop or browse functionality
- **Bulk Processing**: Handle multiple customers simultaneously (tested up to 1000+ records)
- **Progress Tracking**: Real-time processing status indicator
- **Results Table**: Comprehensive output with:
  - Original customer data preservation
  - Churn probability for each customer
  - Risk level categorization
  - Sortable and filterable columns
- **Export Capabilities**:
  - Download predictions as CSV
  - Ready for CRM/marketing system integration
  - Timestamp-stamped export files
- **Sample File Available**: `data/sample_customers.csv` with 20 test records

### 📊 Model Performance

**Advanced Analytics & Validation**

- **Model Comparison Dashboard**:
  - Side-by-side performance metrics for all 3 models
  - Highlighted best performers by metric
  - Interactive bar charts for visual comparison
- **Comprehensive Metrics**:
  - **Accuracy**: Overall prediction correctness (76.0%)
  - **Precision**: Positive prediction reliability (59.6%)
  - **Recall**: Actual churn detection rate (65.5%)
  - **F1-Score**: Harmonic mean of precision/recall (62.4%)
  - **ROC-AUC**: Discriminative ability score (83.5%)
- **Confusion Matrix**: True/False Positive/Negative visualization
- **ROC Curve**: Interactive plot with area under curve calculation
- **Classification Report**: Detailed per-class performance breakdown
- **Best Model Identification**: Champion model badge (XGBoost)
- **Cross-Validation Results**: K-fold validation scores and confidence intervals

### 🎨 User Experience Features

**Professional Design Elements**

- ✨ **Modern Dark Theme**: Rich gradient backgrounds (#1a1a2e → #0f3460)
- 🎯 **Font Awesome Icons**: Professional vector icons throughout (no emojis)
- 📱 **Responsive Layout**: Optimized for desktop, tablet, and mobile
- 🎭 **Glass Morphism**: Semi-transparent cards with backdrop blur effects
- 🌈 **Color-Coded Insights**: Gradient backgrounds for visual hierarchy
- ⚡ **Real-Time Updates**: Instant feedback on all interactions
- 🔄 **Smooth Animations**: Hover effects and transitions
- 📊 **Interactive Charts**: Plotly-powered visualizations with zoom/pan
- 🎛️ **Sidebar Navigation**: Persistent menu with quick access
- 🔍 **Search & Filter**: Built-in data exploration tools

### 🛡️ Enterprise-Ready Features

- **Error Handling**: Graceful error messages and validation
- **Data Validation**: Input sanitization and type checking
- **Session Management**: Persistent state across page navigation
- **Cache Optimization**: Fast load times with @st.cache decorators
- **Scalability**: Handles datasets with 10,000+ records
- **Accessibility**: Screen reader compatible and keyboard navigable
- **Security**: No data persistence, session-based processing
- **Performance**: <2 second prediction time for batch processing

## Technical Stack

- **Python**: 3.9+
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly
- **ML Models**: scikit-learn, XGBoost
- **Class Imbalance**: SMOTE (imbalanced-learn)
- **Explainability**: SHAP
- **Web Framework**: Streamlit
- **Model Persistence**: joblib

## Model Performance

The system trains and compares three models:

1. **Logistic Regression**: Baseline linear model
2. **Random Forest**: Ensemble tree-based model
3. **XGBoost**: Gradient boosting model (typically best performer)

Evaluation metrics include:

- Accuracy
- Precision & Recall
- F1-Score
- ROC-AUC Score
- Confusion Matrix

## Use Cases

- **Customer Retention**: Identify at-risk customers proactively
- **Marketing Strategy**: Target retention campaigns effectively
- **Revenue Protection**: Reduce churn-related revenue loss
- **Business Intelligence**: Understand factors driving customer attrition

## Dataset Information

The Telco Customer Churn dataset contains:

- **Rows**: ~7,000 customers
- **Features**: 20+ attributes including demographics, services, and account info
- **Target**: Churn (Yes/No)

Key features:

- Customer demographics (gender, age, dependents)
- Services subscribed (phone, internet, streaming)
- Account information (tenure, contract type, payment method)
- Charges (monthly, total)

## Feature Engineering

The pipeline includes:

- **Tenure Groups**: Categorizing customer lifetime
- **Charge Ratios**: Total charges per month
- **Service Bundles**: Number of services subscribed
- **Encoding**: One-hot encoding for categorical variables
- **Scaling**: StandardScaler for numerical features

## Contributing

Feel free to enhance this project by:

- Adding more ML models
- Implementing deep learning approaches
- Enhancing the dashboard UI
- Adding more feature engineering techniques

## License

This project is for educational and demonstration purposes.

## Author

Created as part of Data Mining and Business Intelligence Mini Project

---

**Note**: Make sure to download the dataset and place it in the correct location before running the training pipeline.
