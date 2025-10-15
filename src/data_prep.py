"""
Data Preparation Module
=======================
Functions for loading, cleaning, and basic preprocessing of telecom churn data.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_data(filepath):
    """
    Load the Telco Customer Churn dataset.
    
    Parameters:
    -----------
    filepath : str or Path
        Path to the CSV file
    
    Returns:
    --------
    pd.DataFrame
        Loaded dataset
    """
    try:
        df = pd.read_csv(filepath)
        print(f"✓ Data loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset not found at {filepath}. Please ensure the file exists.")
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")


def clean_data(df):
    """
    Clean the dataset by handling missing values and data type issues.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw dataset
    
    Returns:
    --------
    pd.DataFrame
        Cleaned dataset
    """
    df_clean = df.copy()
    
    # Remove customer ID (not useful for prediction)
    if 'customerID' in df_clean.columns:
        df_clean = df_clean.drop('customerID', axis=1)
    
    # Handle TotalCharges - sometimes stored as string with spaces
    if 'TotalCharges' in df_clean.columns:
        df_clean['TotalCharges'] = pd.to_numeric(df_clean['TotalCharges'], errors='coerce')
        
        # Fill missing TotalCharges with 0 (likely new customers)
        df_clean['TotalCharges'].fillna(0, inplace=True)
    
    # Handle SeniorCitizen (convert to Yes/No for consistency)
    if 'SeniorCitizen' in df_clean.columns:
        df_clean['SeniorCitizen'] = df_clean['SeniorCitizen'].map({0: 'No', 1: 'Yes'})
    
    # Remove any duplicate rows
    initial_shape = df_clean.shape[0]
    df_clean = df_clean.drop_duplicates()
    removed = initial_shape - df_clean.shape[0]
    
    if removed > 0:
        print(f"✓ Removed {removed} duplicate rows")
    
    # Handle any other missing values
    missing_summary = df_clean.isnull().sum()
    if missing_summary.sum() > 0:
        print("\n⚠ Missing values found:")
        print(missing_summary[missing_summary > 0])
        
        # Fill remaining missing values with mode for categorical
        for col in df_clean.select_dtypes(include=['object']).columns:
            if df_clean[col].isnull().sum() > 0:
                df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
    
    print(f"✓ Data cleaned: {df_clean.shape[0]} rows, {df_clean.shape[1]} columns")
    
    return df_clean


def get_feature_types(df, target_col='Churn'):
    """
    Identify numerical and categorical features in the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset
    target_col : str
        Name of the target column
    
    Returns:
    --------
    dict
        Dictionary with 'numerical' and 'categorical' feature lists
    """
    # Separate features and target
    features = df.drop(target_col, axis=1).columns.tolist()
    
    # Identify numerical and categorical features
    numerical_features = df[features].select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = df[features].select_dtypes(include=['object']).columns.tolist()
    
    feature_dict = {
        'numerical': numerical_features,
        'categorical': categorical_features
    }
    
    print(f"\n📊 Feature Types:")
    print(f"  - Numerical features: {len(numerical_features)}")
    print(f"  - Categorical features: {len(categorical_features)}")
    
    return feature_dict


def save_processed_data(df, output_path):
    """
    Save the processed dataset to CSV.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Processed dataset
    output_path : str or Path
        Output file path
    """
    # Create directory if it doesn't exist
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"✓ Processed data saved to: {output_path}")


def load_and_prepare_data(raw_data_path, save_processed=True, processed_path=None):
    """
    Complete pipeline to load and prepare data.
    
    Parameters:
    -----------
    raw_data_path : str or Path
        Path to raw data file
    save_processed : bool
        Whether to save the processed data
    processed_path : str or Path
        Path to save processed data (if save_processed=True)
    
    Returns:
    --------
    pd.DataFrame
        Cleaned and prepared dataset
    """
    print("\n" + "="*50)
    print("🔄 DATA PREPARATION PIPELINE")
    print("="*50)
    
    # Load data
    df = load_data(raw_data_path)
    
    # Clean data
    df_clean = clean_data(df)
    
    # Get feature types
    feature_types = get_feature_types(df_clean)
    
    # Save if requested
    if save_processed and processed_path:
        save_processed_data(df_clean, processed_path)
    
    print("\n✅ Data preparation complete!")
    print("="*50 + "\n")
    
    return df_clean


if __name__ == "__main__":
    # Example usage
    raw_data_path = "../data/raw/telco_churn.csv"
    processed_path = "../data/processed/telco_churn_clean.csv"
    
    df = load_and_prepare_data(raw_data_path, save_processed=True, processed_path=processed_path)
    print(f"\nDataset shape: {df.shape}")
    print(f"Target distribution:\n{df['Churn'].value_counts()}")
