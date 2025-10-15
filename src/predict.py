"""
Prediction Module
=================
Functions for making predictions on new data.
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import shap


def load_trained_model(model_path="models/model.joblib"):
    """
    Load the trained model pipeline.
    
    Parameters:
    -----------
    model_path : str or Path
        Path to the saved model
    
    Returns:
    --------
    Pipeline
        Loaded model pipeline
    """
    try:
        pipeline = joblib.load(model_path)
        return pipeline
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Model not found at {model_path}. Please train the model first by running: python src/train.py"
        )


def predict_single(pipeline, customer_data):
    """
    Make prediction for a single customer.
    
    Parameters:
    -----------
    pipeline : Pipeline
        Trained model pipeline
    customer_data : dict or pd.DataFrame
        Customer features
    
    Returns:
    --------
    dict
        Prediction results with probability
    """
    # Convert to DataFrame if dict
    if isinstance(customer_data, dict):
        customer_df = pd.DataFrame([customer_data])
    else:
        customer_df = customer_data.copy()
    
    # Make prediction
    prediction = pipeline.predict(customer_df)[0]
    probability = pipeline.predict_proba(customer_df)[0]
    
    result = {
        'prediction': 'Churn' if prediction == 1 else 'No Churn',
        'prediction_label': int(prediction),
        'churn_probability': float(probability[1]),
        'no_churn_probability': float(probability[0])
    }
    
    return result


def predict_batch(pipeline, data):
    """
    Make predictions for multiple customers.
    
    Parameters:
    -----------
    pipeline : Pipeline
        Trained model pipeline
    data : pd.DataFrame
        Customer data
    
    Returns:
    --------
    pd.DataFrame
        Original data with predictions and probabilities
    """
    # Make predictions
    predictions = pipeline.predict(data)
    probabilities = pipeline.predict_proba(data)
    
    # Add predictions to dataframe
    result_df = data.copy()
    result_df['Churn_Prediction'] = ['Churn' if p == 1 else 'No Churn' for p in predictions]
    result_df['Churn_Probability'] = probabilities[:, 1]
    result_df['No_Churn_Probability'] = probabilities[:, 0]
    
    return result_df


def explain_prediction_shap(pipeline, customer_data, background_data=None):
    """
    Generate SHAP explanation for a prediction.
    
    Parameters:
    -----------
    pipeline : Pipeline
        Trained model pipeline
    customer_data : pd.DataFrame
        Customer data to explain (single row or multiple rows)
    background_data : pd.DataFrame, optional
        Background data for SHAP explainer (if None, uses customer_data)
    
    Returns:
    --------
    shap.Explanation
        SHAP explanation object
    """
    # Transform data using preprocessor
    X_transformed = pipeline.named_steps['preprocessor'].transform(customer_data)
    
    # Get the model
    model = pipeline.named_steps['model']
    
    # Create SHAP explainer
    if background_data is not None:
        X_background = pipeline.named_steps['preprocessor'].transform(background_data)
        explainer = shap.Explainer(model.predict_proba, X_background)
    else:
        explainer = shap.Explainer(model.predict_proba, X_transformed)
    
    # Calculate SHAP values
    shap_values = explainer(X_transformed)
    
    return shap_values


def get_feature_importance(pipeline, feature_names=None):
    """
    Get feature importance from the trained model.
    
    Parameters:
    -----------
    pipeline : Pipeline
        Trained model pipeline
    feature_names : list, optional
        List of feature names after preprocessing
    
    Returns:
    --------
    pd.DataFrame
        Feature importance dataframe
    """
    model = pipeline.named_steps['model']
    
    # Get feature importance based on model type
    if hasattr(model, 'feature_importances_'):
        # Tree-based models (RandomForest, XGBoost)
        importance = model.feature_importances_
    elif hasattr(model, 'coef_'):
        # Linear models (LogisticRegression)
        importance = np.abs(model.coef_[0])
    else:
        print("⚠ Model does not have feature importance attribute")
        return None
    
    # Create dataframe
    if feature_names is not None:
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importance
        })
    else:
        importance_df = pd.DataFrame({
            'Feature': [f'Feature_{i}' for i in range(len(importance))],
            'Importance': importance
        })
    
    importance_df = importance_df.sort_values('Importance', ascending=False)
    
    return importance_df


def prepare_customer_input(gender, senior_citizen, partner, dependents, tenure,
                          phone_service, multiple_lines, internet_service,
                          online_security, online_backup, device_protection,
                          tech_support, streaming_tv, streaming_movies,
                          contract, paperless_billing, payment_method,
                          monthly_charges, total_charges):
    """
    Prepare customer input data for prediction.
    
    Parameters:
    -----------
    All customer features as individual parameters
    
    Returns:
    --------
    pd.DataFrame
        Prepared customer data
    """
    customer_data = {
        'gender': gender,
        'SeniorCitizen': senior_citizen,
        'Partner': partner,
        'Dependents': dependents,
        'tenure': tenure,
        'PhoneService': phone_service,
        'MultipleLines': multiple_lines,
        'InternetService': internet_service,
        'OnlineSecurity': online_security,
        'OnlineBackup': online_backup,
        'DeviceProtection': device_protection,
        'TechSupport': tech_support,
        'StreamingTV': streaming_tv,
        'StreamingMovies': streaming_movies,
        'Contract': contract,
        'PaperlessBilling': paperless_billing,
        'PaymentMethod': payment_method,
        'MonthlyCharges': monthly_charges,
        'TotalCharges': total_charges
    }
    
    # Create DataFrame
    df = pd.DataFrame([customer_data])
    
    # Apply feature engineering (same as training)
    from features import engineer_features
    df_engineered = engineer_features(df)
    
    return df_engineered


def load_and_predict(customer_file_path, model_path="models/model.joblib", output_path=None):
    """
    Load customer data from file and make predictions.
    
    Parameters:
    -----------
    customer_file_path : str or Path
        Path to customer data CSV
    model_path : str or Path
        Path to trained model
    output_path : str or Path, optional
        Path to save predictions
    
    Returns:
    --------
    pd.DataFrame
        Predictions dataframe
    """
    print("\n" + "="*50)
    print("🔮 MAKING PREDICTIONS")
    print("="*50)
    
    # Load model
    print(f"\n📂 Loading model from: {model_path}")
    pipeline = load_trained_model(model_path)
    
    # Load customer data
    print(f"📂 Loading customer data from: {customer_file_path}")
    df = pd.read_csv(customer_file_path)
    print(f"✓ Loaded {len(df)} customers")
    
    # Apply feature engineering
    from features import engineer_features
    df_engineered = engineer_features(df)
    
    # Remove target column if present
    if 'Churn' in df_engineered.columns:
        df_features = df_engineered.drop('Churn', axis=1)
    else:
        df_features = df_engineered
    
    # Make predictions
    print("\n🔮 Generating predictions...")
    predictions_df = predict_batch(pipeline, df_features)
    
    print(f"✓ Predictions complete!")
    print(f"\nChurn Predictions Summary:")
    print(predictions_df['Churn_Prediction'].value_counts())
    print(f"\nAverage Churn Probability: {predictions_df['Churn_Probability'].mean():.2%}")
    
    # Save predictions
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        predictions_df.to_csv(output_path, index=False)
        print(f"\n✓ Predictions saved to: {output_path}")
    
    print("\n" + "="*50)
    
    return predictions_df


if __name__ == "__main__":
    # Example: Load model and make predictions
    model_path = "models/model.joblib"
    
    # Example single prediction
    sample_customer = {
        'gender': 'Male',
        'SeniorCitizen': 'No',
        'Partner': 'Yes',
        'Dependents': 'No',
        'tenure': 12,
        'PhoneService': 'Yes',
        'MultipleLines': 'No',
        'InternetService': 'Fiber optic',
        'OnlineSecurity': 'No',
        'OnlineBackup': 'No',
        'DeviceProtection': 'No',
        'TechSupport': 'No',
        'StreamingTV': 'Yes',
        'StreamingMovies': 'Yes',
        'Contract': 'Month-to-month',
        'PaperlessBilling': 'Yes',
        'PaymentMethod': 'Electronic check',
        'MonthlyCharges': 85.0,
        'TotalCharges': 1020.0
    }
    
    try:
        pipeline = load_trained_model(model_path)
        
        # Prepare data
        customer_df = prepare_customer_input(**sample_customer)
        
        # Predict
        result = predict_single(pipeline, customer_df)
        
        print("\n" + "="*50)
        print("🔮 SINGLE CUSTOMER PREDICTION")
        print("="*50)
        print(f"Prediction: {result['prediction']}")
        print(f"Churn Probability: {result['churn_probability']:.2%}")
        print("="*50)
        
    except FileNotFoundError:
        print("⚠ Model not found. Please train the model first:")
        print("   python src/train.py")
