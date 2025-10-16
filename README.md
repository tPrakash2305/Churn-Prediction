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

## Dashboard Features

### Home Tab

- Project overview and objectives
- Dataset summary statistics
- Quick insights

### EDA Tab

- Churn distribution visualizations
- Feature correlations
- Customer segmentation analysis
- Interactive charts

### Predict Churn Tab

- Single customer prediction with manual input
- Batch prediction via CSV upload
- Churn probability scores
- SHAP explanations for predictions
- Download predictions as CSV

### Model Performance Tab

- Accuracy, Precision, Recall, F1-Score
- ROC-AUC curves
- Confusion matrix
- Model comparison metrics

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
