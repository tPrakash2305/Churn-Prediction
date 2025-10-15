# Dataset Information

## Telco Customer Churn Dataset

### Download Instructions

**Option 1: Kaggle (Recommended)**

1. Visit: https://www.kaggle.com/datasets/blastchar/telco-customer-churn
2. Click "Download" button
3. Extract the CSV file
4. Rename to `telco_churn.csv`
5. Place in `data/raw/` folder

**Option 2: IBM Sample Data**

- Alternative source: https://community.ibm.com/community/user/businessanalytics/blogs/steven-macko/2019/07/11/telco-customer-churn-1113

### Dataset Overview

**Size:** ~7,043 rows × 21 columns

**Features:**

- **customerID**: Unique customer identifier
- **gender**: Male/Female
- **SeniorCitizen**: Whether customer is 65+
- **Partner**: Whether customer has a partner
- **Dependents**: Whether customer has dependents
- **tenure**: Number of months with company
- **PhoneService**: Whether customer has phone service
- **MultipleLines**: Whether customer has multiple lines
- **InternetService**: DSL, Fiber optic, or No
- **OnlineSecurity**: Whether customer has online security
- **OnlineBackup**: Whether customer has online backup
- **DeviceProtection**: Whether customer has device protection
- **TechSupport**: Whether customer has tech support
- **StreamingTV**: Whether customer streams TV
- **StreamingMovies**: Whether customer streams movies
- **Contract**: Month-to-month, One year, or Two year
- **PaperlessBilling**: Whether customer uses paperless billing
- **PaymentMethod**: Payment method used
- **MonthlyCharges**: Monthly charge amount
- **TotalCharges**: Total amount charged
- **Churn**: Whether customer churned (Yes/No) - TARGET

### File Placement

After downloading, your structure should be:

```
DMBI_MiniProject/
├── data/
│   ├── raw/
│   │   └── telco_churn.csv  ← Place file here
│   └── processed/
```

### Data Characteristics

- **Target Variable**: Churn (Yes/No)
- **Imbalance**: ~73% No Churn, ~27% Churn
- **Missing Values**: TotalCharges may have some blanks
- **Data Types**: Mix of categorical and numerical features

### Quick Verification

After placing the file, you can verify it's correct by checking:

- File size: ~950 KB
- Number of rows: 7,043 (including header)
- Number of columns: 21
- First column: customerID

### Need Help?

If you cannot access the dataset:

1. Search for "Telco Customer Churn dataset" on Google
2. Look for IBM Watson or Kaggle sources
3. Ensure the file has all 21 columns mentioned above

---

**Note:** This project is for educational purposes. The dataset is publicly available and commonly used for learning data science and machine learning.
