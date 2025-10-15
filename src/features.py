"""
Feature Engineering Module
===========================
Functions for creating new features and preparing data for modeling.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline


def create_tenure_groups(df):
    """
    Create tenure group categories based on customer lifetime.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with 'tenure' column
    
    Returns:
    --------
    pd.DataFrame
        Dataset with additional 'TenureGroup' column
    """
    df_new = df.copy()
    
    if 'tenure' in df_new.columns:
        # Create tenure groups
        bins = [0, 12, 24, 48, 60, 100]
        labels = ['0-1 year', '1-2 years', '2-4 years', '4-5 years', '5+ years']
        df_new['TenureGroup'] = pd.cut(df_new['tenure'], bins=bins, labels=labels, include_lowest=True)
        
        print("✓ Created tenure groups")
    
    return df_new


def create_charge_features(df):
    """
    Create features related to charges and spending patterns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with charge-related columns
    
    Returns:
    --------
    pd.DataFrame
        Dataset with additional charge features
    """
    df_new = df.copy()
    
    # Average monthly charges (TotalCharges / tenure)
    if 'TotalCharges' in df_new.columns and 'tenure' in df_new.columns:
        # Avoid division by zero
        df_new['AvgMonthlyCharges'] = df_new.apply(
            lambda row: row['TotalCharges'] / row['tenure'] if row['tenure'] > 0 else row['MonthlyCharges'],
            axis=1
        )
        
        # Charge ratio (how much of monthly charge is the total)
        df_new['ChargeRatio'] = df_new.apply(
            lambda row: row['TotalCharges'] / row['MonthlyCharges'] if row['MonthlyCharges'] > 0 else 0,
            axis=1
        )
        
        print("✓ Created charge-related features")
    
    return df_new


def create_service_features(df):
    """
    Create features based on service subscriptions.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with service columns
    
    Returns:
    --------
    pd.DataFrame
        Dataset with service bundle features
    """
    df_new = df.copy()
    
    # List of service columns
    service_cols = ['PhoneService', 'MultipleLines', 'InternetService', 
                    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                    'TechSupport', 'StreamingTV', 'StreamingMovies']
    
    # Count number of services (Yes answers)
    available_cols = [col for col in service_cols if col in df_new.columns]
    
    if available_cols:
        df_new['TotalServices'] = df_new[available_cols].apply(
            lambda row: sum(row == 'Yes'), axis=1
        )
        
        print(f"✓ Created service bundle features ({len(available_cols)} services)")
    
    return df_new


def engineer_features(df):
    """
    Apply all feature engineering steps.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned dataset
    
    Returns:
    --------
    pd.DataFrame
        Dataset with engineered features
    """
    print("\n" + "="*50)
    print("🔧 FEATURE ENGINEERING")
    print("="*50)
    
    df_engineered = df.copy()
    
    # Create tenure groups
    df_engineered = create_tenure_groups(df_engineered)
    
    # Create charge features
    df_engineered = create_charge_features(df_engineered)
    
    # Create service features
    df_engineered = create_service_features(df_engineered)
    
    print("\n✅ Feature engineering complete!")
    print(f"Total features: {df_engineered.shape[1]}")
    print("="*50 + "\n")
    
    return df_engineered


def get_preprocessor(numerical_features, categorical_features):
    """
    Create a preprocessing pipeline for numerical and categorical features.
    
    Parameters:
    -----------
    numerical_features : list
        List of numerical feature names
    categorical_features : list
        List of categorical feature names
    
    Returns:
    --------
    ColumnTransformer
        Preprocessing pipeline
    """
    # Numerical transformer: StandardScaler
    numerical_transformer = StandardScaler()
    
    # Categorical transformer: OneHotEncoder
    categorical_transformer = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')
    
    # Combine transformers
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='drop'  # Drop columns not specified
    )
    
    print("✓ Preprocessing pipeline created")
    print(f"  - Numerical features: {len(numerical_features)}")
    print(f"  - Categorical features: {len(categorical_features)}")
    
    return preprocessor


def prepare_features_for_modeling(df, target_col='Churn'):
    """
    Prepare features and target for modeling.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with engineered features
    target_col : str
        Name of target column
    
    Returns:
    --------
    tuple
        (X, y, feature_names, numerical_features, categorical_features)
    """
    # Separate features and target
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    
    # Encode target variable (Yes=1, No=0)
    y = y.map({'Yes': 1, 'No': 0})
    
    # Identify feature types
    numerical_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
    
    print(f"\n📊 Features prepared for modeling:")
    print(f"  - Total features: {X.shape[1]}")
    print(f"  - Numerical: {len(numerical_features)}")
    print(f"  - Categorical: {len(categorical_features)}")
    print(f"  - Target classes: {y.value_counts().to_dict()}")
    
    return X, y, X.columns.tolist(), numerical_features, categorical_features


def get_feature_names_after_preprocessing(preprocessor, categorical_features):
    """
    Get feature names after one-hot encoding.
    
    Parameters:
    -----------
    preprocessor : ColumnTransformer
        Fitted preprocessor
    categorical_features : list
        Original categorical feature names
    
    Returns:
    --------
    list
        Feature names after preprocessing
    """
    try:
        # Get numerical feature names (unchanged)
        num_features = preprocessor.transformers_[0][2]
        
        # Get categorical feature names after one-hot encoding
        cat_encoder = preprocessor.named_transformers_['cat']
        cat_features = cat_encoder.get_feature_names_out(categorical_features)
        
        # Combine all feature names
        feature_names = list(num_features) + list(cat_features)
        
        return feature_names
    except Exception as e:
        print(f"⚠ Could not extract feature names: {str(e)}")
        return None


if __name__ == "__main__":
    # Example usage
    from data_prep import load_data
    
    df = load_data("../data/raw/telco_churn.csv")
    df_engineered = engineer_features(df)
    
    X, y, feature_names, num_features, cat_features = prepare_features_for_modeling(df_engineered)
    
    preprocessor = get_preprocessor(num_features, cat_features)
    
    print(f"\n✅ Features ready for modeling!")
    print(f"Shape: X={X.shape}, y={y.shape}")
