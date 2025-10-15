"""
Setup Verification Script
=========================
Run this script to verify your environment is properly configured.
"""

import sys
import importlib
from pathlib import Path


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 9:
        print("✅ Python version is compatible (3.9+)")
        return True
    else:
        print("❌ Python 3.9+ is required")
        return False


def check_packages():
    """Check if required packages are installed."""
    required_packages = [
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'sklearn',
        'xgboost',
        'imblearn',
        'shap',
        'streamlit',
        'joblib',
        'plotly'
    ]
    
    print("\n" + "="*50)
    print("CHECKING REQUIRED PACKAGES")
    print("="*50)
    
    all_installed = True
    for package in required_packages:
        try:
            mod = importlib.import_module(package)
            version = getattr(mod, '__version__', 'unknown')
            print(f"✅ {package:15} - version {version}")
        except ImportError:
            print(f"❌ {package:15} - NOT INSTALLED")
            all_installed = False
    
    return all_installed


def check_directories():
    """Check if required directories exist."""
    required_dirs = [
        'data/raw',
        'data/processed',
        'models',
        'reports',
        'notebooks',
        'src',
        'app'
    ]
    
    print("\n" + "="*50)
    print("CHECKING DIRECTORY STRUCTURE")
    print("="*50)
    
    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} - NOT FOUND")
            all_exist = False
    
    return all_exist


def check_dataset():
    """Check if dataset exists."""
    dataset_path = Path('data/raw/telco_churn.csv')
    
    print("\n" + "="*50)
    print("CHECKING DATASET")
    print("="*50)
    
    if dataset_path.exists():
        print(f"✅ Dataset found: {dataset_path}")
        
        # Try to load and check
        try:
            import pandas as pd
            df = pd.read_csv(dataset_path)
            print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
            
            if df.shape[0] > 7000 and df.shape[1] >= 20:
                print("✅ Dataset appears correct")
                return True
            else:
                print("⚠️  Dataset size seems incorrect")
                return False
        except Exception as e:
            print(f"⚠️  Could not read dataset: {str(e)}")
            return False
    else:
        print("❌ Dataset not found")
        print("\n📥 Download Instructions:")
        print("   1. Visit: https://www.kaggle.com/datasets/blastchar/telco-customer-churn")
        print("   2. Download the CSV file")
        print("   3. Place it as: data/raw/telco_churn.csv")
        return False


def check_models():
    """Check if trained models exist."""
    model_path = Path('models/model.joblib')
    
    print("\n" + "="*50)
    print("CHECKING TRAINED MODELS")
    print("="*50)
    
    if model_path.exists():
        print(f"✅ Model found: {model_path}")
        return True
    else:
        print("⚠️  Model not found (this is OK if you haven't trained yet)")
        print("\n📊 To train models, run:")
        print("   python src/train.py")
        return False


def main():
    """Run all checks."""
    print("\n" + "="*70)
    print("🔍 CHURN PREDICTION SYSTEM - SETUP VERIFICATION")
    print("="*70 + "\n")
    
    checks = {
        'Python Version': check_python_version(),
        'Required Packages': check_packages(),
        'Directory Structure': check_directories(),
        'Dataset': check_dataset(),
        'Trained Model': check_models()
    }
    
    # Summary
    print("\n" + "="*70)
    print("📊 VERIFICATION SUMMARY")
    print("="*70)
    
    for check_name, result in checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:25} {status}")
    
    # Overall status
    critical_checks = ['Python Version', 'Required Packages', 'Directory Structure', 'Dataset']
    critical_passed = all(checks[check] for check in critical_checks if check in checks)
    
    print("\n" + "="*70)
    
    if critical_passed:
        print("✅ SETUP COMPLETE! You're ready to start.")
        print("\n📋 Next Steps:")
        if not checks.get('Trained Model', False):
            print("   1. Train models: python src/train.py")
            print("   2. Launch dashboard: streamlit run app/app.py")
        else:
            print("   1. Launch dashboard: streamlit run app/app.py")
            print("   2. Make predictions!")
    else:
        print("⚠️  SETUP INCOMPLETE - Please fix the issues above")
        print("\n📋 Required Actions:")
        if not checks['Python Version']:
            print("   - Install Python 3.9 or higher")
        if not checks['Required Packages']:
            print("   - Run: pip install -r requirements.txt")
        if not checks['Directory Structure']:
            print("   - Ensure you're in the project root directory")
        if not checks['Dataset']:
            print("   - Download dataset (see instructions above)")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
