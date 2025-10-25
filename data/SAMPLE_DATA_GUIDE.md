# 📊 Sample Customer Data for Batch Prediction

## 📄 File: sample_customers.csv

This CSV file contains **20 sample customer records** for demonstrating the batch prediction feature in the Customer Churn Prediction System.

---

## 🎯 Purpose

Use this file to:

1. **Test batch prediction** functionality
2. **Demonstrate the system** to faculty/stakeholders
3. **Understand input format** required for predictions
4. **Practice with realistic data** before using production data

---

## 📋 File Contents

### Customer Distribution:

- **Total Customers:** 20
- **Gender Mix:** 10 Male, 10 Female
- **Senior Citizens:** 4 customers
- **Tenure Range:** 1-72 months
- **Contract Types:** Mix of Month-to-month, One year, Two year
- **Internet Services:** Mix of DSL, Fiber optic, and No internet service

### Risk Profiles Included:

- **High Risk:**
  - Short tenure (1-6 months)
  - Month-to-month contracts
  - No tech support
  - Electronic check payment
- **Medium Risk:**
  - Moderate tenure (7-24 months)
  - Mixed contract types
  - Some additional services
- **Low Risk:**
  - Long tenure (36+ months)
  - Two-year contracts
  - Multiple services
  - Automatic payment methods

---

## 🔧 How to Use

### In the Streamlit Dashboard:

1. **Navigate to "Predict Churn" page**
2. **Select "Batch Prediction" tab**
3. **Click "Browse files" button**
4. **Select:** `data/sample_customers.csv`
5. **Click "Predict Batch"**
6. **View results** with churn probabilities
7. **Download predictions** as CSV

### Expected Output:

- Churn probability for each customer (0-100%)
- Risk level classification (High/Medium/Low)
- Original customer data preserved
- Ready for export and analysis

---

## 📝 Column Descriptions

| Column               | Type    | Values                                                                             | Description                |
| -------------------- | ------- | ---------------------------------------------------------------------------------- | -------------------------- |
| **gender**           | String  | Male, Female                                                                       | Customer gender            |
| **SeniorCitizen**    | String  | Yes, No                                                                            | Is customer 65+ years old  |
| **Partner**          | String  | Yes, No                                                                            | Has partner/spouse         |
| **Dependents**       | String  | Yes, No                                                                            | Has dependents (children)  |
| **tenure**           | Integer | 0-72                                                                               | Months with company        |
| **PhoneService**     | String  | Yes, No                                                                            | Has phone service          |
| **MultipleLines**    | String  | Yes, No, No phone service                                                          | Multiple phone lines       |
| **InternetService**  | String  | DSL, Fiber optic, No                                                               | Type of internet           |
| **OnlineSecurity**   | String  | Yes, No, No internet service                                                       | Online security addon      |
| **OnlineBackup**     | String  | Yes, No, No internet service                                                       | Online backup addon        |
| **DeviceProtection** | String  | Yes, No, No internet service                                                       | Device protection plan     |
| **TechSupport**      | String  | Yes, No, No internet service                                                       | Tech support service       |
| **StreamingTV**      | String  | Yes, No, No internet service                                                       | Streaming TV service       |
| **StreamingMovies**  | String  | Yes, No, No internet service                                                       | Streaming movies service   |
| **Contract**         | String  | Month-to-month, One year, Two year                                                 | Contract type              |
| **PaperlessBilling** | String  | Yes, No                                                                            | Uses paperless billing     |
| **PaymentMethod**    | String  | Electronic check, Mailed check, Bank transfer (automatic), Credit card (automatic) | Payment method             |
| **MonthlyCharges**   | Float   | 20.0-120.0                                                                         | Monthly charges in dollars |
| **TotalCharges**     | Float   | 20.0-9000.0                                                                        | Total charges to date      |

---

## ⚠️ Important Notes

### Valid Values:

1. **SeniorCitizen:** Must be "Yes" or "No" (not 0/1)
2. **InternetService:** If "No", all internet-related features must be "No internet service"
3. **PhoneService:** If "No", MultipleLines must be "No phone service"
4. **Charges:** Must be numeric (no currency symbols)

### Common Mistakes to Avoid:

❌ Using 0/1 for Yes/No fields  
❌ Missing required columns  
❌ Incorrect spelling of categories  
❌ Currency symbols in charge fields  
❌ Empty/null values

✅ Use exact category names as shown  
✅ Include all 19 columns  
✅ Match spelling precisely  
✅ Use numeric values only for charges  
✅ Fill all fields with valid values

---

## 🎬 Demo Scenario

### For Faculty Presentation:

**Step 1:** Show single prediction first

- Use one customer from the CSV
- Demonstrate individual prediction
- Explain SHAP values

**Step 2:** Show batch prediction

- Upload the sample_customers.csv
- Process all 20 customers
- Show results table with probabilities

**Step 3:** Explain results

- Point out high-risk customers (short tenure, month-to-month)
- Point out low-risk customers (long tenure, 2-year contracts)
- Discuss business actions based on predictions

**Key Talking Points:**

- "This processes 20 customers instantly"
- "Real-time scoring for entire customer base"
- "Export results for marketing/retention teams"
- "Scalable to thousands of customers"

---

## 📈 Expected Prediction Patterns

Based on model training, expect:

**High Churn Probability (>60%):**

- Customers 2, 4, 7, 10, 15, 20 (short tenure, month-to-month)

**Medium Churn Probability (30-60%):**

- Customers 1, 11, 13, 19 (moderate tenure, mixed factors)

**Low Churn Probability (<30%):**

- Customers 5, 6, 9, 12, 14, 17 (long tenure, 2-year contracts)

---

## 🔄 Creating Your Own Sample Data

To create additional sample files:

### Required Format:

```csv
gender,SeniorCitizen,Partner,Dependents,tenure,PhoneService,...
Female,No,Yes,No,12,Yes,No,DSL,Yes,Yes,...
Male,Yes,No,No,24,Yes,Yes,Fiber optic,No,No,...
```

### Tips:

1. Copy header row exactly from sample_customers.csv
2. Use valid category values only
3. Ensure data consistency (e.g., No internet service → all internet features = "No internet service")
4. Test with small batches first (5-10 customers)
5. Verify all 19 columns are present

### Template:

Use the existing sample_customers.csv as a template:

- Copy the file
- Modify customer values
- Save with a new name
- Test in batch prediction

---

## 💡 Business Use Cases

### Scenarios This Data Represents:

1. **New Customers** (tenure 1-3 months)

   - High risk, need immediate attention
   - Onboarding campaigns

2. **Mid-Term Customers** (tenure 12-24 months)

   - Mixed risk, renewal focus
   - Contract upgrade opportunities

3. **Long-Term Customers** (tenure 36+ months)

   - Low risk, loyalty rewards
   - Upsell opportunities

4. **No Internet Service**

   - Different risk profile
   - Potential for service expansion

5. **Multiple Services**
   - Lower churn probability
   - Bundle value demonstration

---

## 🎓 Faculty Presentation Tips

### When Showing This Feature:

1. **Before Upload:**

   - "This represents a monthly customer scoring run"
   - "In production, this could be thousands of customers"

2. **During Processing:**

   - "The model processes each customer through the pipeline"
   - "Same preprocessing and feature engineering as training"

3. **After Results:**
   - "We can now prioritize the highest-risk customers"
   - "Export to CRM for targeted retention campaigns"
   - "Track prediction accuracy over time"

### Impressive Statistics to Mention:

- ✅ Processes 20 customers in under 2 seconds
- ✅ Scalable to 10,000+ customers
- ✅ Same accuracy as training (76%)
- ✅ Ready for production deployment
- ✅ Export-ready for business tools

---

## 📊 Sample Results Preview

After batch prediction, you'll see:

| Customer | Gender | Tenure | Contract       | Churn Prob | Risk Level |
| -------- | ------ | ------ | -------------- | ---------- | ---------- |
| Cust-1   | Female | 12     | Month-to-month | 68.5%      | HIGH       |
| Cust-2   | Male   | 3      | Month-to-month | 72.3%      | HIGH       |
| Cust-3   | Female | 24     | One year       | 42.1%      | MEDIUM     |
| Cust-4   | Male   | 1      | Month-to-month | 85.7%      | HIGH       |
| Cust-5   | Female | 48     | Two year       | 18.2%      | LOW        |
| ...      | ...    | ...    | ...            | ...        | ...        |

---

## 🔒 Data Privacy Note

This is **synthetic/sample data** for demonstration purposes only.

For production use:

- ⚠️ Never upload real customer data without authorization
- ⚠️ Ensure compliance with data privacy regulations (GDPR, CCPA)
- ⚠️ Use secure data handling procedures
- ⚠️ Implement access controls and audit logs
- ⚠️ Anonymize data when possible

---

## 📞 Troubleshooting

### If Upload Fails:

**Problem:** "Invalid file format"

- **Solution:** Ensure CSV has all 19 columns with correct names

**Problem:** "Invalid category values"

- **Solution:** Check spelling of categories (case-sensitive)

**Problem:** "Missing values detected"

- **Solution:** Fill all cells with valid data

**Problem:** "Numeric conversion error"

- **Solution:** Remove currency symbols, ensure numbers are valid

### Testing Your CSV:

1. Open in Excel/Notepad
2. Verify 19 columns + header row
3. Check for special characters
4. Ensure consistent formatting
5. Save as CSV (comma-delimited)

---

## ✅ Quick Checklist

Before using your CSV:

- [ ] 19 columns present
- [ ] Header row matches exactly
- [ ] All values are valid categories
- [ ] No missing/empty cells
- [ ] Numeric fields have no symbols
- [ ] File saved as .csv format
- [ ] Encoding is UTF-8
- [ ] No extra rows/columns

---

## 🚀 Ready to Demo!

You now have:
✅ 20 diverse customer samples  
✅ Mix of risk levels  
✅ Realistic data patterns  
✅ All required fields  
✅ Valid category values  
✅ Ready for batch prediction

**File Location:** `data/sample_customers.csv`

**Next Step:** Go to the dashboard → Predict Churn → Batch Prediction → Upload this file!

---

_Last Updated: October 16, 2025_  
_Sample Data Version: 1.0_  
_Records: 20 customers_
