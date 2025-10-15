"""
Model Training Module
=====================
Functions for training multiple ML models and saving the best one.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from data_prep import load_and_prepare_data
from features import engineer_features, prepare_features_for_modeling, get_preprocessor
from eval import evaluate_model, compare_models


def create_models():
    """
    Create instances of all models to train.
    
    Returns:
    --------
    dict
        Dictionary of model name and model instance
    """
    models = {
        'Logistic Regression': LogisticRegression(
            random_state=42,
            max_iter=1000,
            class_weight='balanced'
        ),
        'Random Forest': RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10,
            class_weight='balanced',
            n_jobs=-1
        ),
        'XGBoost': XGBClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=6,
            learning_rate=0.1,
            scale_pos_weight=3,  # Handle class imbalance
            n_jobs=-1,
            eval_metric='logloss'
        )
    }
    
    return models


def create_pipeline(preprocessor, model, use_smote=False):
    """
    Create a complete pipeline with preprocessing and model.
    
    Parameters:
    -----------
    preprocessor : ColumnTransformer
        Preprocessing pipeline
    model : estimator
        Machine learning model
    use_smote : bool
        Whether to use SMOTE for handling class imbalance
    
    Returns:
    --------
    Pipeline
        Complete ML pipeline
    """
    if use_smote:
        # Use imblearn pipeline for SMOTE
        pipeline = ImbPipeline([
            ('preprocessor', preprocessor),
            ('smote', SMOTE(random_state=42)),
            ('model', model)
        ])
    else:
        # Regular pipeline
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('model', model)
        ])
    
    return pipeline


def train_and_evaluate_models(X_train, X_test, y_train, y_test, preprocessor, use_smote=False):
    """
    Train all models and evaluate their performance.
    
    Parameters:
    -----------
    X_train, X_test : pd.DataFrame
        Training and test features
    y_train, y_test : pd.Series
        Training and test targets
    preprocessor : ColumnTransformer
        Preprocessing pipeline
    use_smote : bool
        Whether to use SMOTE
    
    Returns:
    --------
    dict
        Dictionary of trained pipelines and their results
    """
    print("\n" + "="*50)
    print("🤖 MODEL TRAINING & EVALUATION")
    print("="*50)
    
    models = create_models()
    results = {}
    
    for model_name, model in models.items():
        print(f"\n📊 Training {model_name}...")
        
        # Create pipeline
        pipeline = create_pipeline(preprocessor, model, use_smote=use_smote)
        
        # Train model
        pipeline.fit(X_train, y_train)
        
        # Evaluate model
        metrics = evaluate_model(pipeline, X_test, y_test, model_name=model_name)
        
        # Store results
        results[model_name] = {
            'pipeline': pipeline,
            'metrics': metrics
        }
    
    print("\n" + "="*50)
    print("✅ All models trained and evaluated!")
    print("="*50)
    
    return results


def select_best_model(results):
    """
    Select the best model based on F1-score.
    
    Parameters:
    -----------
    results : dict
        Dictionary of model results
    
    Returns:
    --------
    tuple
        (best_model_name, best_pipeline, best_metrics)
    """
    best_f1 = 0
    best_model_name = None
    
    for model_name, result in results.items():
        f1_score = result['metrics']['f1_score']
        if f1_score > best_f1:
            best_f1 = f1_score
            best_model_name = model_name
    
    best_pipeline = results[best_model_name]['pipeline']
    best_metrics = results[best_model_name]['metrics']
    
    print(f"\n🏆 Best Model: {best_model_name}")
    print(f"   F1-Score: {best_f1:.4f}")
    
    return best_model_name, best_pipeline, best_metrics


def save_model(pipeline, model_path, preprocessor_path=None):
    """
    Save the trained pipeline to disk.
    
    Parameters:
    -----------
    pipeline : Pipeline
        Trained pipeline
    model_path : str or Path
        Path to save the model
    preprocessor_path : str or Path, optional
        Path to save preprocessor separately
    """
    # Create directory if it doesn't exist
    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save complete pipeline
    joblib.dump(pipeline, model_path)
    print(f"✓ Model saved to: {model_path}")
    
    # Optionally save preprocessor separately
    if preprocessor_path:
        preprocessor_path = Path(preprocessor_path)
        preprocessor = pipeline.named_steps['preprocessor']
        joblib.dump(preprocessor, preprocessor_path)
        print(f"✓ Preprocessor saved to: {preprocessor_path}")


def load_model(model_path):
    """
    Load a trained pipeline from disk.
    
    Parameters:
    -----------
    model_path : str or Path
        Path to the saved model
    
    Returns:
    --------
    Pipeline
        Loaded pipeline
    """
    try:
        pipeline = joblib.load(model_path)
        print(f"✓ Model loaded from: {model_path}")
        return pipeline
    except FileNotFoundError:
        raise FileNotFoundError(f"Model not found at {model_path}")


def train_full_pipeline(raw_data_path, test_size=0.2, use_smote=False, save_models=True):
    """
    Complete training pipeline from raw data to trained model.
    
    Parameters:
    -----------
    raw_data_path : str or Path
        Path to raw data
    test_size : float
        Proportion of test set
    use_smote : bool
        Whether to use SMOTE
    save_models : bool
        Whether to save trained models
    
    Returns:
    --------
    dict
        Dictionary containing best pipeline, results, and data splits
    """
    print("\n" + "="*70)
    print("🚀 COMPLETE TRAINING PIPELINE")
    print("="*70)
    
    # Step 1: Load and prepare data
    df = load_and_prepare_data(raw_data_path, save_processed=True, 
                               processed_path="data/processed/telco_churn_clean.csv")
    
    # Step 2: Engineer features
    df_engineered = engineer_features(df)
    
    # Step 3: Prepare features for modeling
    X, y, feature_names, num_features, cat_features = prepare_features_for_modeling(df_engineered)
    
    # Step 4: Create preprocessor
    preprocessor = get_preprocessor(num_features, cat_features)
    
    # Step 5: Train-test split
    print("\n📊 Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    print(f"  - Training set: {X_train.shape[0]} samples")
    print(f"  - Test set: {X_test.shape[0]} samples")
    
    # Step 6: Train and evaluate models
    results = train_and_evaluate_models(X_train, X_test, y_train, y_test, 
                                       preprocessor, use_smote=use_smote)
    
    # Step 7: Compare models
    compare_models(results)
    
    # Step 8: Select best model
    best_model_name, best_pipeline, best_metrics = select_best_model(results)
    
    # Step 9: Save models
    if save_models:
        print("\n💾 Saving models...")
        save_model(best_pipeline, "models/model.joblib", "models/preproc.joblib")
        
        # Save all results for comparison
        joblib.dump(results, "models/all_results.joblib")
        print("✓ All results saved")
    
    print("\n" + "="*70)
    print("✅ TRAINING PIPELINE COMPLETE!")
    print("="*70)
    
    return {
        'best_model_name': best_model_name,
        'best_pipeline': best_pipeline,
        'best_metrics': best_metrics,
        'all_results': results,
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test
    }


if __name__ == "__main__":
    # Train the complete pipeline
    raw_data_path = "data/raw/telco_churn.csv"
    
    output = train_full_pipeline(
        raw_data_path=raw_data_path,
        test_size=0.2,
        use_smote=False,  # We're using class_weight='balanced' instead
        save_models=True
    )
    
    print("\n🎉 Training complete! You can now run the Streamlit app.")
    print("   Command: streamlit run app/app.py")
