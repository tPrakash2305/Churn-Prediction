"""
Model Evaluation Module
========================
Functions for evaluating model performance with various metrics.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report
)
from pathlib import Path


def evaluate_model(pipeline, X_test, y_test, model_name="Model"):
    """
    Evaluate a trained model on test data.
    
    Parameters:
    -----------
    pipeline : Pipeline
        Trained pipeline
    X_test : pd.DataFrame
        Test features
    y_test : pd.Series
        Test targets
    model_name : str
        Name of the model for display
    
    Returns:
    --------
    dict
        Dictionary of evaluation metrics
    """
    # Make predictions
    y_pred = pipeline.predict(X_test)
    y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_pred_proba)
    }
    
    # Print metrics
    print(f"\n📊 {model_name} Performance:")
    print(f"  - Accuracy:  {metrics['accuracy']:.4f}")
    print(f"  - Precision: {metrics['precision']:.4f}")
    print(f"  - Recall:    {metrics['recall']:.4f}")
    print(f"  - F1-Score:  {metrics['f1_score']:.4f}")
    print(f"  - ROC-AUC:   {metrics['roc_auc']:.4f}")
    
    return metrics


def plot_confusion_matrix(y_test, y_pred, model_name="Model", save_path=None):
    """
    Plot confusion matrix for model predictions.
    
    Parameters:
    -----------
    y_test : array-like
        True labels
    y_pred : array-like
        Predicted labels
    model_name : str
        Model name for title
    save_path : str or Path, optional
        Path to save the figure
    
    Returns:
    --------
    matplotlib.figure.Figure
        The confusion matrix figure
    """
    cm = confusion_matrix(y_test, y_pred)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True,
                xticklabels=['No Churn', 'Churn'],
                yticklabels=['No Churn', 'Churn'])
    
    ax.set_xlabel('Predicted Label')
    ax.set_ylabel('True Label')
    ax.set_title(f'Confusion Matrix - {model_name}')
    
    plt.tight_layout()
    
    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Confusion matrix saved to: {save_path}")
    
    return fig


def plot_roc_curve(y_test, y_pred_proba, model_name="Model", save_path=None):
    """
    Plot ROC curve for model predictions.
    
    Parameters:
    -----------
    y_test : array-like
        True labels
    y_pred_proba : array-like
        Predicted probabilities for positive class
    model_name : str
        Model name for title
    save_path : str or Path, optional
        Path to save the figure
    
    Returns:
    --------
    matplotlib.figure.Figure
        The ROC curve figure
    """
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    auc = roc_auc_score(y_test, y_pred_proba)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {auc:.4f})')
    ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
    
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title(f'ROC Curve - {model_name}')
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ ROC curve saved to: {save_path}")
    
    return fig


def get_classification_report(y_test, y_pred):
    """
    Generate a detailed classification report.
    
    Parameters:
    -----------
    y_test : array-like
        True labels
    y_pred : array-like
        Predicted labels
    
    Returns:
    --------
    str
        Classification report as string
    """
    report = classification_report(y_test, y_pred, 
                                   target_names=['No Churn', 'Churn'])
    return report


def compare_models(results):
    """
    Compare multiple models side by side.
    
    Parameters:
    -----------
    results : dict
        Dictionary of model results from training
    
    Returns:
    --------
    pd.DataFrame
        Comparison dataframe
    """
    comparison_data = []
    
    for model_name, result in results.items():
        metrics = result['metrics']
        comparison_data.append({
            'Model': model_name,
            'Accuracy': metrics['accuracy'],
            'Precision': metrics['precision'],
            'Recall': metrics['recall'],
            'F1-Score': metrics['f1_score'],
            'ROC-AUC': metrics['roc_auc']
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    comparison_df = comparison_df.sort_values('F1-Score', ascending=False)
    
    print("\n" + "="*70)
    print("📊 MODEL COMPARISON")
    print("="*70)
    print(comparison_df.to_string(index=False))
    print("="*70)
    
    return comparison_df


def plot_model_comparison(comparison_df, save_path=None):
    """
    Plot bar chart comparing model metrics.
    
    Parameters:
    -----------
    comparison_df : pd.DataFrame
        Comparison dataframe from compare_models
    save_path : str or Path, optional
        Path to save the figure
    
    Returns:
    --------
    matplotlib.figure.Figure
        The comparison figure
    """
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(comparison_df))
    width = 0.15
    
    for i, metric in enumerate(metrics):
        offset = width * (i - 2)
        ax.bar(x + offset, comparison_df[metric], width, label=metric)
    
    ax.set_xlabel('Model')
    ax.set_ylabel('Score')
    ax.set_title('Model Performance Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(comparison_df['Model'], rotation=15, ha='right')
    ax.legend(loc='lower right')
    ax.set_ylim([0, 1.05])
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Comparison plot saved to: {save_path}")
    
    return fig


def generate_evaluation_report(pipeline, X_test, y_test, model_name="Model", output_dir="reports"):
    """
    Generate a complete evaluation report with all metrics and plots.
    
    Parameters:
    -----------
    pipeline : Pipeline
        Trained pipeline
    X_test : pd.DataFrame
        Test features
    y_test : pd.Series
        Test targets
    model_name : str
        Model name
    output_dir : str or Path
        Directory to save outputs
    """
    print("\n" + "="*50)
    print("📄 GENERATING EVALUATION REPORT")
    print("="*50)
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Make predictions
    y_pred = pipeline.predict(X_test)
    y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
    
    # Generate metrics
    metrics = evaluate_model(pipeline, X_test, y_test, model_name)
    
    # Classification report
    print("\n📊 Classification Report:")
    report = get_classification_report(y_test, y_pred)
    print(report)
    
    # Save classification report
    report_path = output_dir / f"{model_name.replace(' ', '_')}_classification_report.txt"
    with open(report_path, 'w') as f:
        f.write(f"Classification Report - {model_name}\n")
        f.write("="*50 + "\n")
        f.write(report)
    print(f"✓ Classification report saved to: {report_path}")
    
    # Plot confusion matrix
    cm_path = output_dir / f"{model_name.replace(' ', '_')}_confusion_matrix.png"
    plot_confusion_matrix(y_test, y_pred, model_name, save_path=cm_path)
    
    # Plot ROC curve
    roc_path = output_dir / f"{model_name.replace(' ', '_')}_roc_curve.png"
    plot_roc_curve(y_test, y_pred_proba, model_name, save_path=roc_path)
    
    print("\n✅ Evaluation report complete!")
    print("="*50)
    
    plt.close('all')  # Close all figures
    
    return metrics


if __name__ == "__main__":
    print("This module provides evaluation functions.")
    print("Run train.py to train models and generate evaluation reports.")
