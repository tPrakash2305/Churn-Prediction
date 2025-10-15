# Project Documentation

## Customer Churn Prediction System - Technical Details

---

## 📖 Table of Contents

1. [Project Architecture](#project-architecture)
2. [Data Pipeline](#data-pipeline)
3. [Feature Engineering](#feature-engineering)
4. [Machine Learning Models](#machine-learning-models)
5. [Evaluation Metrics](#evaluation-metrics)
6. [API Reference](#api-reference)
7. [Deployment Guide](#deployment-guide)
8. [Performance Optimization](#performance-optimization)

---

## 🏗️ Project Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                    │
│          (Interactive Dashboard + Predictions)           │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│                   Prediction Layer                       │
│         (predict.py - Model Inference)                   │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│                  Trained ML Pipeline                     │
│    (Preprocessor + Best Model from train.py)            │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│                  Training Pipeline                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 1. Data Prep (data_prep.py)                      │  │
│  │    - Load CSV                                     │  │
│  │    - Clean data                                   │  │
│  │    - Handle missing values                        │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 2. Feature Engineering (features.py)              │  │
│  │    - Create tenure groups                         │  │
│  │    - Engineer charge features                     │  │
│  │    - Create service bundles                       │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 3. Model Training (train.py)                      │  │
│  │    - Train multiple models                        │  │
│  │    - Evaluate performance                         │  │
│  │    - Select best model                            │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Pipeline

### 1. Data Ingestion

**Input:** `data/raw/telco_churn.csv`

**Process:**

```python
from data_prep import load_data
df = load_data('data/raw/telco_churn.csv')
```

**Output:** Pandas DataFrame with 7,043 rows × 21 columns

### 2. Data Cleaning

**Transformations:**

- Remove `customerID` (not predictive)
- Convert `TotalCharges` to numeric (handle spaces)
- Fill missing `TotalCharges` with 0 (new customers)
- Convert `SeniorCitizen` from 0/1 to No/Yes
- Remove duplicates

**Code:**

```python
from data_prep import clean_data
df_clean = clean_data(df)
```

### 3. Feature Engineering

**Created Features:**

| Feature Name        | Description                   | Formula/Logic                          |
| ------------------- | ----------------------------- | -------------------------------------- |
| `TenureGroup`       | Customer lifetime category    | Bins: 0-1yr, 1-2yr, 2-4yr, 4-5yr, 5+yr |
| `AvgMonthlyCharges` | Average monthly spend         | TotalCharges / tenure                  |
| `ChargeRatio`       | Spending pattern indicator    | TotalCharges / MonthlyCharges          |
| `TotalServices`     | Number of services subscribed | Count of "Yes" in service columns      |

### 4. Preprocessing Pipeline

**Numerical Features:**

- StandardScaler (mean=0, std=1)

**Categorical Features:**

- OneHotEncoder (drop_first=True)
- Handle unknown categories

**Implementation:**

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(drop='first'), categorical_features)
    ]
)
```

---

## 🎯 Feature Engineering

### Tenure Groups

**Purpose:** Capture customer lifecycle stages

**Implementation:**

```python
bins = [0, 12, 24, 48, 60, 100]
labels = ['0-1 year', '1-2 years', '2-4 years', '4-5 years', '5+ years']
df['TenureGroup'] = pd.cut(df['tenure'], bins=bins, labels=labels)
```

**Business Insight:** Early-stage customers (0-1 year) show highest churn rates

### Charge Features

**Average Monthly Charges:**

```python
df['AvgMonthlyCharges'] = df['TotalCharges'] / df['tenure']
```

**Charge Ratio:**

```python
df['ChargeRatio'] = df['TotalCharges'] / df['MonthlyCharges']
```

**Business Insight:** Higher ratios indicate longer customer relationships

### Service Bundles

**Total Services:**

```python
service_cols = ['PhoneService', 'MultipleLines', 'InternetService', ...]
df['TotalServices'] = df[service_cols].apply(lambda row: sum(row == 'Yes'), axis=1)
```

**Business Insight:** Customers with more services show lower churn

---

## 🤖 Machine Learning Models

### 1. Logistic Regression

**Type:** Linear classifier

**Configuration:**

```python
LogisticRegression(
    random_state=42,
    max_iter=1000,
    class_weight='balanced'
)
```

**Pros:**

- Fast training and inference
- Interpretable coefficients
- Good baseline model

**Cons:**

- Assumes linear relationships
- May underfit complex patterns

### 2. Random Forest

**Type:** Ensemble of decision trees

**Configuration:**

```python
RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    max_depth=10,
    class_weight='balanced',
    n_jobs=-1
)
```

**Pros:**

- Handles non-linear relationships
- Provides feature importance
- Robust to outliers

**Cons:**

- Slower inference than linear models
- Can overfit with deep trees

### 3. XGBoost

**Type:** Gradient boosting

**Configuration:**

```python
XGBClassifier(
    n_estimators=100,
    random_state=42,
    max_depth=6,
    learning_rate=0.1,
    scale_pos_weight=3,
    n_jobs=-1
)
```

**Pros:**

- Often best performance
- Built-in regularization
- Handles missing values

**Cons:**

- More parameters to tune
- Longer training time

---

## 📊 Evaluation Metrics

### Confusion Matrix

```
                 Predicted
              No Churn  Churn
Actual No        TN       FP
       Yes       FN       TP
```

### Metrics Explained

**Accuracy:**

```
(TP + TN) / (TP + TN + FP + FN)
```

Overall correctness

**Precision:**

```
TP / (TP + FP)
```

Of predicted churners, how many actually churned?

**Recall (Sensitivity):**

```
TP / (TP + FN)
```

Of actual churners, how many did we catch?

**F1-Score:**

```
2 × (Precision × Recall) / (Precision + Recall)
```

Harmonic mean of precision and recall

**ROC-AUC:**
Area under the ROC curve

- 0.5 = Random guessing
- 1.0 = Perfect classifier

### Class Imbalance Handling

**Problem:** ~73% No Churn, ~27% Churn

**Solutions Implemented:**

1. `class_weight='balanced'` in models
2. `scale_pos_weight=3` in XGBoost
3. Stratified train-test split

---

## 🔌 API Reference

### Data Preparation Module

```python
from data_prep import load_data, clean_data, load_and_prepare_data

# Load data
df = load_data('path/to/data.csv')

# Clean data
df_clean = clean_data(df)

# Complete pipeline
df = load_and_prepare_data(
    raw_data_path='data/raw/telco_churn.csv',
    save_processed=True,
    processed_path='data/processed/telco_churn_clean.csv'
)
```

### Feature Engineering Module

```python
from features import (
    engineer_features,
    prepare_features_for_modeling,
    get_preprocessor
)

# Engineer features
df_engineered = engineer_features(df)

# Prepare for modeling
X, y, feature_names, num_features, cat_features = prepare_features_for_modeling(df)

# Get preprocessor
preprocessor = get_preprocessor(num_features, cat_features)
```

### Training Module

```python
from train import train_full_pipeline, load_model

# Train complete pipeline
output = train_full_pipeline(
    raw_data_path='data/raw/telco_churn.csv',
    test_size=0.2,
    use_smote=False,
    save_models=True
)

# Load trained model
pipeline = load_model('models/model.joblib')
```

### Prediction Module

```python
from predict import (
    load_trained_model,
    predict_single,
    predict_batch,
    prepare_customer_input
)

# Load model
pipeline = load_trained_model('models/model.joblib')

# Single prediction
customer_data = prepare_customer_input(
    gender='Male',
    senior_citizen='No',
    # ... other features
)
result = predict_single(pipeline, customer_data)

# Batch prediction
predictions_df = predict_batch(pipeline, customers_df)
```

---

## 🚀 Deployment Guide

### Option 1: Streamlit Cloud (Free)

1. Push code to GitHub
2. Visit https://streamlit.io/cloud
3. Connect your repository
4. Deploy!

### Option 2: Heroku

```bash
# Create Procfile
echo "web: streamlit run app/app.py --server.port=$PORT" > Procfile

# Deploy
heroku create churn-prediction-app
git push heroku main
```

### Option 3: Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app/app.py"]
```

Build and run:

```bash
docker build -t churn-app .
docker run -p 8501:8501 churn-app
```

### Option 4: AWS EC2

1. Launch EC2 instance (t2.medium recommended)
2. Install Python and dependencies
3. Clone repository
4. Run: `streamlit run app/app.py --server.port 80`
5. Configure security group for port 80

---

## ⚡ Performance Optimization

### Model Inference

**Current:** ~50-100ms per prediction
**Optimization:** Batch predictions for multiple customers

```python
# Instead of loop
for customer in customers:
    predict_single(pipeline, customer)  # Slow

# Use batch
predict_batch(pipeline, all_customers)  # Fast
```

### Memory Usage

**Large Dataset Handling:**

```python
# Use chunking for very large files
chunk_size = 10000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    predictions = predict_batch(pipeline, chunk)
```

### Caching in Streamlit

```python
@st.cache_resource
def load_model():
    return load_trained_model('models/model.joblib')

@st.cache_data
def load_dataset():
    return pd.read_csv('data/processed/telco_churn_clean.csv')
```

---

## 🔐 Security Considerations

### Data Privacy

- Never commit actual customer data to version control
- Use `.gitignore` to exclude sensitive files
- Implement data anonymization for demos

### Model Security

- Validate input data before prediction
- Implement rate limiting for API endpoints
- Use authentication for production deployments

---

## 📈 Model Monitoring

### Metrics to Track

1. **Model Performance:**

   - Accuracy, Precision, Recall
   - Monitor drift over time

2. **Data Drift:**

   - Feature distributions
   - Missing value patterns

3. **Business Metrics:**
   - Churn rate predictions vs actual
   - Cost savings from interventions

### Retraining Strategy

**Trigger retraining when:**

- Performance degrades below threshold
- New data patterns emerge
- Business requirements change
- Quarterly scheduled updates

---

## 🛠️ Maintenance

### Regular Tasks

**Weekly:**

- Monitor model performance
- Check for errors in logs

**Monthly:**

- Review prediction accuracy
- Update documentation

**Quarterly:**

- Retrain models with new data
- Evaluate new features
- Update dependencies

---

## 📚 Additional Resources

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [SHAP Documentation](https://shap.readthedocs.io/)

---

**Last Updated:** October 2025
**Version:** 1.0.0
