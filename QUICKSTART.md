# Quick Start Guide

## Customer Churn Prediction System

This guide will help you get the project up and running in minutes!

---

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- 500 MB free disk space

---

## 🚀 Step-by-Step Setup

### Step 1: Install Dependencies

Open PowerShell in the project directory and run:

```powershell
pip install -r requirements.txt
```

This will install all required packages:

- pandas, numpy (data processing)
- matplotlib, seaborn, plotly (visualization)
- scikit-learn, xgboost (machine learning)
- streamlit (web dashboard)
- shap (explainability)
- imbalanced-learn (handling imbalanced data)

⏱️ **Time:** 2-3 minutes

---

### Step 2: Download Dataset

1. **Visit Kaggle:**

   - Go to: https://www.kaggle.com/datasets/blastchar/telco-customer-churn
   - Click "Download" (you may need a free Kaggle account)

2. **Extract and Place:**

   - Extract the downloaded ZIP file
   - Rename the CSV file to `telco_churn.csv`
   - Place it in: `data/raw/telco_churn.csv`

3. **Verify:**
   - File should be ~950 KB
   - Should have 7,043 rows and 21 columns

⏱️ **Time:** 2-3 minutes

---

### Step 3: Train the Models

Run the training script:

```powershell
python src/train.py
```

This will:

- Load and clean the data
- Engineer features
- Train 3 models (Logistic Regression, Random Forest, XGBoost)
- Evaluate and compare models
- Save the best model to `models/` folder

⏱️ **Time:** 2-5 minutes (depending on your computer)

**Expected Output:**

```
✓ Data loaded successfully
✓ Feature engineering complete
🤖 Training Logistic Regression...
🤖 Training Random Forest...
🤖 Training XGBoost...
✅ All models trained!
🏆 Best Model: XGBoost (F1-Score: 0.6234)
💾 Model saved to models/model.joblib
```

---

### Step 4: Launch the Dashboard

Start the Streamlit web application:

```powershell
streamlit run app/app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

If it doesn't open automatically, manually navigate to the URL shown in the terminal.

⏱️ **Time:** 10 seconds

---

## 🎯 Using the Dashboard

### Home Tab 🏠

- Overview of the project
- Dataset statistics
- Quick insights

### EDA Tab 📊

- Interactive visualizations
- Churn distribution analysis
- Feature correlations
- Customer segmentation

### Predict Churn Tab 🔮

- **Single Prediction:** Enter customer details manually
- **Batch Prediction:** Upload CSV file with multiple customers
- Get churn probability and risk level
- Download predictions

### Model Performance Tab 📈

- View accuracy, precision, recall, F1-score
- Compare all models
- ROC curves
- Confusion matrices

---

## 📓 Jupyter Notebooks (Optional)

Explore the analysis in detail:

### 1. Exploratory Data Analysis

```powershell
jupyter notebook notebooks/01_EDA.ipynb
```

### 2. Preprocessing and Features

```powershell
jupyter notebook notebooks/02_Preprocessing_and_Features.ipynb
```

### 3. Modeling and Evaluation

```powershell
jupyter notebook notebooks/03_Modeling_and_Evaluation.ipynb
```

---

## 🎓 Understanding the Output

### Model Metrics Explained

- **Accuracy**: Overall correctness (e.g., 80% = 80% of predictions are correct)
- **Precision**: Of predicted churners, how many actually churned
- **Recall**: Of actual churners, how many did we catch
- **F1-Score**: Balanced measure combining precision and recall
- **ROC-AUC**: Model's ability to distinguish between classes (higher is better)

### Risk Levels

- 🟢 **Low Risk**: Churn probability < 40%
- 🟡 **Medium Risk**: Churn probability 40-70%
- 🔴 **High Risk**: Churn probability > 70%

---

## 🔧 Troubleshooting

### Issue: "Model not found"

**Solution:** Run `python src/train.py` first to train the model

### Issue: "Dataset not found"

**Solution:** Ensure `telco_churn.csv` is in `data/raw/` folder

### Issue: Module import errors

**Solution:** Run `pip install -r requirements.txt` again

### Issue: Streamlit won't start

**Solution:** Try: `python -m streamlit run app/app.py`

### Issue: Port already in use

**Solution:** Run: `streamlit run app/app.py --server.port 8502`

---

## 📁 Project Structure Overview

```
DMBI_MiniProject/
├── app/
│   └── app.py                 # Streamlit dashboard
├── data/
│   ├── raw/                   # Place dataset here
│   └── processed/             # Generated during training
├── models/                    # Trained models saved here
├── notebooks/                 # Jupyter notebooks for analysis
├── src/                       # Core Python modules
│   ├── data_prep.py          # Data loading and cleaning
│   ├── features.py           # Feature engineering
│   ├── train.py              # Model training
│   ├── eval.py               # Model evaluation
│   └── predict.py            # Prediction functions
├── reports/                   # Evaluation reports
├── requirements.txt           # Python dependencies
└── README.md                  # Main documentation
```

---

## 🎉 Success Checklist

- [ ] Dependencies installed
- [ ] Dataset downloaded and placed correctly
- [ ] Models trained successfully
- [ ] Dashboard launches without errors
- [ ] Can make predictions
- [ ] Can view model performance

---

## 📚 What's Next?

1. **Experiment:** Try different customer profiles in the prediction tab
2. **Analyze:** Explore the EDA visualizations
3. **Learn:** Review the Jupyter notebooks
4. **Extend:** Add more features or try different models
5. **Deploy:** Consider deploying to cloud (Streamlit Cloud, Heroku, etc.)

---

## 💡 Tips

- **First Run:** Train the model once, then use the dashboard repeatedly
- **Batch Predictions:** Prepare CSV with same columns as training data
- **Model Updates:** Retrain periodically with new data
- **Explainability:** Use SHAP values to understand predictions

---

## 🆘 Need Help?

1. Check the main README.md for detailed documentation
2. Review error messages carefully
3. Ensure all prerequisites are met
4. Try the troubleshooting section above

---

**Total Setup Time:** ~10-15 minutes

**Ready to predict churn!** 🚀
