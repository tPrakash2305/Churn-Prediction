"""
Streamlit Dashboard for Customer Churn Prediction
===================================================
Interactive web application for churn prediction and analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import joblib

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from predict import load_trained_model, predict_single, predict_batch, prepare_customer_input
from features import engineer_features

# Page configuration
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS for enhanced UI with Font Awesome icons
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    /* Dark theme main background with rich gradient */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .main {
        background: transparent;
    }
    
    .block-container {
        background: rgba(30, 30, 50, 0.8);
        border-radius: 1rem;
        padding: 2rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    /* Icon styling */
    .icon {
        display: inline-block;
        width: 1.2em;
        margin-right: 0.5rem;
        text-align: center;
    }
    
    .icon-large {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    /* Main text styling for dark theme with better typography */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 1rem 0;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    
    .sub-header {
        font-size: 1.6rem;
        color: #667eea;
        margin-top: 2.5rem;
        margin-bottom: 1.2rem;
        font-weight: 600;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.6rem;
        letter-spacing: -0.3px;
        line-height: 1.3;
    }
    
    /* All text elements in white for dark theme */
    .stApp, .stApp p, .stApp span, .stApp label, .stApp div {
        color: #e5e7eb !important;
        line-height: 1.6;
    }
    
    /* Headings in lighter colors with better spacing */
    h1, h2, h3, h4, h5, h6 {
        color: #f9fafb !important;
        font-weight: 600;
        letter-spacing: -0.3px;
    }
    
    h1 { font-size: 2.5rem; line-height: 1.2; margin-bottom: 1.5rem; }
    h2 { font-size: 2rem; line-height: 1.3; margin-bottom: 1.2rem; }
    h3 { font-size: 1.6rem; line-height: 1.4; margin-bottom: 1rem; }
    h4 { font-size: 1.3rem; line-height: 1.4; margin-bottom: 0.8rem; }
    
    /* Markdown text with better readability */
    .stMarkdown {
        color: #e5e7eb !important;
    }
    
    .stMarkdown p {
        margin-bottom: 1rem;
        line-height: 1.7;
        font-size: 1.05rem;
    }
    
    .stMarkdown strong {
        color: #f9fafb !important;
        font-weight: 600;
    }
    
    .stMarkdown ul, .stMarkdown ol {
        margin-left: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .stMarkdown li {
        margin-bottom: 0.5rem;
        line-height: 1.6;
    }
    
    /* Sidebar seamlessly matching main background */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        box-shadow: 2px 0 15px rgba(0, 0, 0, 0.3);
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Sidebar text styling - all white */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] p {
        color: #f0f0f0 !important;
    }
    
    /* Sidebar radio buttons - exact match to technology stack boxes */
    [data-testid="stSidebar"] [role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.08);
        padding: 1rem 1.2rem !important;
        border-radius: 0.6rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
        border-left: 4px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.12);
        transform: translateX(3px);
        border-left: 4px solid rgba(102, 126, 234, 0.8);
        box-shadow: 0 4px 10px rgba(102, 126, 234, 0.15);
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] [data-checked="true"] {
        background: rgba(255, 255, 255, 0.15);
        font-weight: 600;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
    }
    
    /* Sidebar markdown content */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: white !important;
    }
    
    /* Metric cards with animated hover effects */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        transform: translate(-50%, -50%);
        transition: width 0.6s ease, height 0.6s ease;
    }
    
    .metric-card:hover::after {
        width: 300px;
        height: 300px;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.5), 0 0 20px rgba(118, 75, 162, 0.3);
    }
    
    /* Custom buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Churn status */
    .churn-positive {
        color: #ef4444;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .churn-negative {
        color: #10b981;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    /* Info boxes with pop-up effects */
    .info-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    
    .info-box:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 20px 40px rgba(240, 147, 251, 0.5);
    }
    
    .success-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    
    .success-box:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 20px 40px rgba(79, 172, 254, 0.5);
    }
    
    /* Card styling for dark theme with professional hover effects */
    .card {
        background: rgba(40, 40, 60, 0.9);
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        margin: 1rem 0;
        border: 1px solid rgba(102, 126, 234, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .card:hover::before {
        left: 100%;
    }
    
    .card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4), 0 0 30px rgba(118, 75, 162, 0.3);
        border: 1px solid rgba(102, 126, 234, 0.6);
        background: rgba(50, 50, 70, 0.95);
    }
    
    .card h3, .card p, .card span {
        color: #e5e7eb !important;
        transition: color 0.3s ease;
    }
    
    .card:hover h3 {
        color: #667eea !important;
    }
    
    /* Metric cards with better visibility and hover effects */
    [data-testid="stMetric"] {
        background: rgba(40, 40, 60, 0.9);
        padding: 1rem;
        border-radius: 0.8rem;
        border: 1px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(102, 126, 234, 0.6);
        background: rgba(50, 50, 70, 0.95);
    }
    
    [data-testid="stMetricLabel"] {
        color: #9ca3af !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #f9fafb !important;
        font-size: 2rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricDelta"] {
        color: #10b981 !important;
    }
    
    /* Input fields for dark theme */
    .stSelectbox, .stNumberInput, .stTextInput {
        background: rgba(40, 40, 60, 0.9) !important;
    }
    
    .stSelectbox label, .stNumberInput label, .stTextInput label {
        color: #e5e7eb !important;
    }
    
    input, select, textarea {
        background: rgba(30, 30, 50, 0.8) !important;
        color: #f9fafb !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Dataframe styling with hover effects */
    .stDataFrame {
        background: rgba(40, 40, 60, 0.9);
        border-radius: 0.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    
    .stDataFrame:hover {
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        transform: scale(1.01);
    }
    
    .stDataFrame [data-testid="stDataFrameResizable"] {
        color: #e5e7eb !important;
    }
    
    /* Hide Streamlit branding and deploy button */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    
    /* Metric improvements */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Expander styling for dark theme with hover animation */
    .streamlit-expanderHeader {
        background: rgba(40, 40, 60, 0.9) !important;
        border-radius: 0.5rem;
        font-weight: 600;
        color: #f9fafb !important;
        border: 1px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(50, 50, 70, 0.95) !important;
        border: 1px solid rgba(102, 126, 234, 0.6);
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .streamlit-expanderContent {
        background: rgba(30, 30, 50, 0.8);
        border: 1px solid rgba(102, 126, 234, 0.2);
        color: #e5e7eb !important;
        animation: slideDown 0.3s ease;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Input fields */
    .stSelectbox, .stNumberInput {
        border-radius: 0.5rem;
    }
    
    /* Tab styling with hover effects */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        border-radius: 0.5rem 0.5rem 0 0;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-3px);
        background: rgba(102, 126, 234, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Scrollbar styling for dark theme */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
        background: rgba(20, 20, 35, 0.9);
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 30, 50, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        border: 2px solid rgba(102, 126, 234, 0.2);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Tab styling for dark theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(30, 30, 50, 0.8);
        border-radius: 0.5rem;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        border-radius: 0.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        color: #9ca3af !important;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.1);
        color: #e5e7eb !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Professional animations and effects */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7);
        }
        50% {
            box-shadow: 0 0 0 15px rgba(102, 126, 234, 0);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    /* Column hover effects */
    [data-testid="column"] {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 0.5rem;
        padding: 0.5rem;
    }
    
    [data-testid="column"]:hover {
        background: rgba(102, 126, 234, 0.05);
        transform: translateY(-3px);
    }
    
    /* Image hover effects */
    img {
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 0.5rem;
    }
    
    img:hover {
        transform: scale(1.05) rotate(2deg);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
    }
    
    /* Chart containers hover */
    [data-testid="stPlotlyChart"] {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 0.5rem;
        padding: 1rem;
        background: rgba(40, 40, 60, 0.5);
    }
    
    [data-testid="stPlotlyChart"]:hover {
        background: rgba(50, 50, 70, 0.7);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        transform: scale(1.01);
    }
    
    /* File uploader hover */
    [data-testid="stFileUploader"] {
        transition: all 0.3s ease;
        border-radius: 0.5rem;
    }
    
    [data-testid="stFileUploader"]:hover {
        background: rgba(102, 126, 234, 0.1);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.2);
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 0.8rem;
        animation: fadeInUp 0.5s ease;
        border-left: 4px solid #667eea;
    }
    
    /* Progress bar animation */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        animation: shimmer 2s infinite;
    }
    
    /* Success message animation */
    .stSuccess {
        animation: fadeInUp 0.5s ease, pulse 2s infinite;
    }
    
    /* Loading spinner container */
    .stSpinner > div {
        border-color: #667eea !important;
    }
    
    /* Disable hover effects for specific elements */
    .no-hover,
    .no-hover * {
        transition: none !important;
        cursor: default !important;
        pointer-events: none !important;
    }
    
    .no-hover:hover,
    .no-hover *:hover {
        transform: none !important;
        box-shadow: none !important;
        scale: 1 !important;
    }
    
    /* Specifically target matplotlib/seaborn chart images */
    .element-container:has(.no-hover) img {
        transition: none !important;
        pointer-events: none !important;
    }
    
    .element-container:has(.no-hover) img:hover {
        transform: none !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Load the trained model (cached)."""
    try:
        model_path = Path(__file__).parent.parent / "models" / "model.joblib"
        pipeline = load_trained_model(str(model_path))
        return pipeline
    except FileNotFoundError:
        st.error("❌ Model not found. Please train the model first by running: `python src/train.py`")
        return None


@st.cache_data
def load_dataset():
    """Load the dataset for EDA (cached)."""
    try:
        data_path = Path(__file__).parent.parent / "data" / "processed" / "telco_churn_clean.csv"
        if not data_path.exists():
            data_path = Path(__file__).parent.parent / "data" / "raw" / "telco_churn.csv"
        
        df = pd.read_csv(data_path)
        return df
    except FileNotFoundError:
        st.error("❌ Dataset not found. Please ensure the dataset is in the data folder.")
        return None


def home_page():
    """Display the home page with Font Awesome icons."""
    st.markdown('<h1 class="main-header"><i class="fas fa-chart-line"></i> Customer Churn Prediction System</h1>', unsafe_allow_html=True)
    
    # Hero section
    st.markdown("""
    <div style='text-align: center; padding: 2.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 1rem; color: white; margin-bottom: 2.5rem; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);'>
        <i class='fas fa-bullseye' style='font-size: 3rem; margin-bottom: 1rem; display: block;'></i>
        <h2 style='color: white; margin-bottom: 1rem; font-size: 2rem; font-weight: 700; letter-spacing: -0.5px;'>
            Predict Customer Churn with AI
        </h2>
        <p style='font-size: 1.1rem; color: #f0f0f0; line-height: 1.6; max-width: 800px; margin: 0 auto;'>
            Leverage advanced machine learning to identify at-risk customers and implement proactive retention strategies
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards with Font Awesome icons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 1rem; 
                    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4); 
                    text-align: center; min-height: 240px; color: white;
                    transition: transform 0.3s ease;'>
            <i class='fas fa-chart-bar' style='font-size: 3.5rem; margin-bottom: 1.2rem; display: block;'></i>
            <h3 style='color: white; margin-bottom: 0.8rem; font-weight: 600; font-size: 1.3rem; letter-spacing: -0.3px;'>
                Data Analysis
            </h3>
            <p style='color: #f0f0f0; font-size: 1rem; line-height: 1.5;'>
                Explore customer patterns and churn trends with interactive visualizations
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 2rem; border-radius: 1rem; 
                    box-shadow: 0 8px 20px rgba(240, 147, 251, 0.4); 
                    text-align: center; min-height: 240px; color: white;
                    transition: transform 0.3s ease;'>
            <i class='fas fa-brain' style='font-size: 3.5rem; margin-bottom: 1.2rem; display: block;'></i>
            <h3 style='color: white; margin-bottom: 0.8rem; font-weight: 600; font-size: 1.3rem; letter-spacing: -0.3px;'>
                AI Predictions
            </h3>
            <p style='color: #f0f0f0; font-size: 1rem; line-height: 1.5;'>
                Machine learning-powered churn probability scoring and insights
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                    padding: 2rem; border-radius: 1rem; 
                    box-shadow: 0 8px 20px rgba(250, 112, 154, 0.4); 
                    text-align: center; min-height: 240px; color: white;
                    transition: transform 0.3s ease;'>
            <i class='fas fa-trophy' style='font-size: 3.5rem; margin-bottom: 1.2rem; display: block;'></i>
            <h3 style='color: white; margin-bottom: 0.8rem; font-weight: 600; font-size: 1.3rem; letter-spacing: -0.3px;'>
                Performance
            </h3>
            <p style='color: #f0f0f0; font-size: 1rem; line-height: 1.5;'>
                Track model accuracy metrics and validation scores
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 2rem; border-radius: 1rem; 
                    box-shadow: 0 8px 20px rgba(79, 172, 254, 0.4); 
                    text-align: center; min-height: 240px; color: white;
                    transition: transform 0.3s ease;'>
            <i class='fas fa-chart-line' style='font-size: 3.5rem; margin-bottom: 1.2rem; display: block;'></i>
            <h3 style='color: white; margin-bottom: 0.8rem; font-weight: 600; font-size: 1.3rem; letter-spacing: -0.3px;'>
                Business Value
            </h3>
            <p style='color: #f0f0f0; font-size: 1rem; line-height: 1.5;'>
                Reduce customer churn and maximize revenue retention
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Dataset summary
    df = load_dataset()
    if df is not None:
        st.markdown('<h2 class="sub-header"><i class="fas fa-database icon"></i>Dataset Overview</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 2rem; border-radius: 1rem; text-align: center; color: white;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                <i class='fas fa-users' style='font-size: 2rem; margin-bottom: 0.8rem; display: block;'></i>
                <div style='font-size: 2.5rem; font-weight: bold;'>{len(df):,}</div>
                <div style='font-size: 1rem; margin-top: 0.5rem; letter-spacing: 0.3px;'>Total Customers</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if 'Churn' in df.columns:
                churn_count = (df['Churn'] == 'Yes').sum()
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            padding: 2rem; border-radius: 1rem; text-align: center; color: white;
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                    <i class='fas fa-user-minus' style='font-size: 2rem; margin-bottom: 0.8rem; display: block;'></i>
                    <div style='font-size: 2.5rem; font-weight: bold;'>{churn_count:,}</div>
                    <div style='font-size: 1rem; margin-top: 0.5rem; letter-spacing: 0.3px;'>Churned Customers</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            if 'Churn' in df.columns:
                churn_rate = (df['Churn'] == 'Yes').mean() * 100
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                            padding: 2rem; border-radius: 1rem; text-align: center; color: white;
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                    <i class='fas fa-percentage' style='font-size: 2rem; margin-bottom: 0.8rem; display: block;'></i>
                    <div style='font-size: 2.5rem; font-weight: bold;'>{churn_rate:.1f}%</div>
                    <div style='font-size: 1rem; margin-top: 0.5rem; letter-spacing: 0.3px;'>Churn Rate</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 2rem; border-radius: 1rem; text-align: center; color: white;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                <i class='fas fa-table' style='font-size: 2rem; margin-bottom: 0.8rem; display: block;'></i>
                <div style='font-size: 2.5rem; font-weight: bold;'>{len(df.columns)}</div>
                <div style='font-size: 1rem; margin-top: 0.5rem; letter-spacing: 0.3px;'>Features</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Show sample data
        with st.expander("📋 View Sample Data", expanded=False):
            st.dataframe(df.head(10), use_container_width=True)
        
        # Key insights with gradient backgrounds
        st.markdown('<h2 class="sub-header"><i class="fas fa-lightbulb icon"></i>Key Insights</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 2.5rem; border-radius: 1rem; 
                        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4); 
                        min-height: 320px; color: white;'>
                <h3 style='color: white; margin-top: 0; font-weight: 600; font-size: 1.5rem; letter-spacing: -0.3px;'>
                    <i class='fas fa-bullseye icon'></i>Business Impact
                </h3>
                <ul style='font-size: 1.05rem; line-height: 2; color: #f0f0f0; list-style: none; padding-left: 0;'>
                    <li style='margin-bottom: 1rem;'>
                        <i class='fas fa-check-circle' style='margin-right: 0.8rem; color: #4ade80;'></i>
                        <strong>Reduce</strong> customer acquisition costs
                    </li>
                    <li style='margin-bottom: 1rem;'>
                        <i class='fas fa-check-circle' style='margin-right: 0.8rem; color: #4ade80;'></i>
                        <strong>Improve</strong> customer lifetime value
                    </li>
                    <li style='margin-bottom: 1rem;'>
                        <i class='fas fa-check-circle' style='margin-right: 0.8rem; color: #4ade80;'></i>
                        <strong>Enable</strong> targeted retention campaigns
                    </li>
                    <li style='margin-bottom: 1rem;'>
                        <i class='fas fa-check-circle' style='margin-right: 0.8rem; color: #4ade80;'></i>
                        <strong>Drive</strong> data-driven decision making
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 2.5rem; border-radius: 1rem; 
                        box-shadow: 0 8px 20px rgba(240, 147, 251, 0.4); 
                        min-height: 320px; color: white;'>
                <h3 style='color: white; margin-top: 0; font-weight: 600; font-size: 1.5rem; letter-spacing: -0.3px;'>
                    <i class='fas fa-robot icon'></i>ML Models Used
                </h3>
                <ul style='font-size: 1.05rem; line-height: 2; color: #f0f0f0; list-style: none; padding-left: 0;'>
                    <li style='margin-bottom: 1rem;'>
                        <i class='fas fa-chart-line' style='margin-right: 0.8rem; color: #fbbf24;'></i>
                        <strong>Logistic Regression</strong> (Baseline)
                    </li>
                    <li style='margin-bottom: 1rem;'>
                        <i class='fas fa-tree' style='margin-right: 0.8rem; color: #fbbf24;'></i>
                        <strong>Random Forest</strong> (Ensemble)
                    </li>
                    <li style='margin-bottom: 1rem;'>
                        <i class='fas fa-bolt' style='margin-right: 0.8rem; color: #fbbf24;'></i>
                        <strong>XGBoost</strong> (Gradient Boosting)
                    </li>
                    <li style='margin-bottom: 1rem;'>
                        <i class='fas fa-lightbulb' style='margin-right: 0.8rem; color: #fbbf24;'></i>
                        <strong>SHAP</strong> for Explainability
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True)


def eda_page():
    """Display the EDA page with Font Awesome icons."""
    st.markdown('<h1 class="main-header"><i class="fas fa-chart-bar"></i> Exploratory Data Analysis</h1>', unsafe_allow_html=True)
    
    df = load_dataset()
    if df is None:
        return
    
    # Churn distribution
    st.markdown('<h2 class="sub-header">🎯 Churn Distribution</h2>', unsafe_allow_html=True)
    
    if 'Churn' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            churn_counts = df['Churn'].value_counts()
            fig = px.pie(values=churn_counts.values, names=churn_counts.index,
                        title='Customer Churn Distribution',
                        color_discrete_sequence=['#2ca02c', '#d62728'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Bar chart
            fig = px.bar(x=churn_counts.index, y=churn_counts.values,
                        title='Churn Count',
                        labels={'x': 'Churn', 'y': 'Count'},
                        color=churn_counts.index,
                        color_discrete_sequence=['#2ca02c', '#d62728'])
            st.plotly_chart(fig, use_container_width=True)
    
    # Churn by categorical features
    st.markdown('<h2 class="sub-header">📈 Churn by Features</h2>', unsafe_allow_html=True)
    
    categorical_features = ['Contract', 'InternetService', 'PaymentMethod', 'gender']
    available_features = [f for f in categorical_features if f in df.columns]
    
    if available_features and 'Churn' in df.columns:
        selected_feature = st.selectbox("Select a feature to analyze:", available_features)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Churn rate by feature
            churn_by_feature = df.groupby(selected_feature)['Churn'].apply(
                lambda x: (x == 'Yes').sum() / len(x) * 100
            ).sort_values(ascending=False)
            
            fig = px.bar(x=churn_by_feature.index, y=churn_by_feature.values,
                        title=f'Churn Rate by {selected_feature}',
                        labels={'x': selected_feature, 'y': 'Churn Rate (%)'},
                        color=churn_by_feature.values,
                        color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Count by feature and churn
            count_data = df.groupby([selected_feature, 'Churn']).size().reset_index(name='Count')
            fig = px.bar(count_data, x=selected_feature, y='Count', color='Churn',
                        title=f'Customer Count by {selected_feature} and Churn',
                        barmode='group',
                        color_discrete_sequence=['#2ca02c', '#d62728'])
            st.plotly_chart(fig, use_container_width=True)
    
    # Numerical features
    st.markdown('<h2 class="sub-header">💰 Numerical Features Analysis</h2>', unsafe_allow_html=True)
    
    numerical_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
    available_num_features = [f for f in numerical_features if f in df.columns]
    
    if available_num_features and 'Churn' in df.columns:
        selected_num_feature = st.selectbox("Select a numerical feature:", available_num_features)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribution by churn
            fig = px.histogram(df, x=selected_num_feature, color='Churn',
                             title=f'Distribution of {selected_num_feature} by Churn',
                             barmode='overlay', nbins=30,
                             color_discrete_sequence=['#2ca02c', '#d62728'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Box plot
            fig = px.box(df, x='Churn', y=selected_num_feature,
                        title=f'{selected_num_feature} by Churn Status',
                        color='Churn',
                        color_discrete_sequence=['#2ca02c', '#d62728'])
            st.plotly_chart(fig, use_container_width=True)
    
    # Correlation heatmap
    st.markdown('<h2 class="sub-header">🔥 Feature Correlations</h2>', unsafe_allow_html=True)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        
        # Use Plotly heatmap to match other charts (no hover effects)
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            hoverinfo='skip',  # Disable hover
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title='Feature Correlation Matrix',
            title_font_size=14,
            xaxis_title='',
            yaxis_title='',
            height=500,
            margin=dict(l=100, r=50, t=80, b=100)
        )
        
        # Use same container width as other Plotly charts
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def predict_page():
    """Display the prediction page."""
    st.markdown('<h1 class="main-header">🔮 Predict Customer Churn</h1>', unsafe_allow_html=True)
    
    # Load model
    pipeline = load_model()
    if pipeline is None:
        return
    
    # Prediction mode selection
    prediction_mode = st.radio(
        "Select Prediction Mode:",
        ["Single Customer Prediction", "Batch Prediction (Upload CSV)"],
        horizontal=True
    )
    
    if prediction_mode == "Single Customer Prediction":
        single_customer_prediction(pipeline)
    else:
        batch_prediction(pipeline)


def single_customer_prediction(pipeline):
    """Handle single customer prediction."""
    st.markdown('<h2 class="sub-header">👤 Enter Customer Details</h2>', unsafe_allow_html=True)
    
    st.info("💡 Fill in the customer information below to predict churn probability")
    
    # Create input form with better organization
    with st.form("prediction_form"):
        st.markdown("### 👥 Demographics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            gender = st.selectbox("Gender", ["Male", "Female"])
        with col2:
            senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
        with col3:
            partner = st.selectbox("Partner", ["No", "Yes"])
        with col4:
            dependents = st.selectbox("Dependents", ["No", "Yes"])
        
        st.markdown("### 📞 Phone Services")
        col1, col2 = st.columns(2)
        
        with col1:
            phone_service = st.selectbox("Phone Service", ["No", "Yes"])
        with col2:
            multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
        
        st.markdown("### 🌐 Internet Services")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        with col2:
            online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
        with col3:
            online_backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
        with col2:
            tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
        with col3:
            streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
        
        streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])
        
        st.markdown("### 💳 Account Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        with col2:
            paperless_billing = st.selectbox("Paperless Billing", ["No", "Yes"])
        with col3:
            payment_method = st.selectbox("Payment Method", 
                                          ["Electronic check", "Mailed check", 
                                           "Bank transfer (automatic)", "Credit card (automatic)"])
        
        st.markdown("### 💰 Financial Details")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12)
        with col2:
            monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, max_value=200.0, value=50.0, step=0.5)
        with col3:
            total_charges = st.number_input("Total Charges ($)", min_value=0.0, max_value=10000.0, 
                                            value=float(tenure * monthly_charges), step=1.0)
        
        # Submit button
        submitted = st.form_submit_button("🔮 Predict Churn", use_container_width=True, type="primary")
    
    if submitted:
        # Prepare input
        customer_df = prepare_customer_input(
            gender, senior_citizen, partner, dependents, tenure,
            phone_service, multiple_lines, internet_service,
            online_security, online_backup, device_protection,
            tech_support, streaming_tv, streaming_movies,
            contract, paperless_billing, payment_method,
            monthly_charges, total_charges
        )
        
        # Make prediction
        with st.spinner("🤖 Analyzing customer data..."):
            result = predict_single(pipeline, customer_df)
        
        # Display results with enhanced styling
        st.markdown('<h2 class="sub-header">📊 Prediction Results</h2>', unsafe_allow_html=True)
        
        # Main result card
        prediction_color = "#ef4444" if result['prediction'] == "Churn" else "#10b981"
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {prediction_color} 0%, {prediction_color}dd 100%); 
                    padding: 2rem; border-radius: 1rem; text-align: center; color: white; margin: 1rem 0;
                    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);'>
            <h2 style='color: white; margin-bottom: 1rem;'>Prediction: {result['prediction']}</h2>
            <div style='font-size: 3rem; font-weight: bold;'>{result['churn_probability']:.1%}</div>
            <div style='font-size: 1.2rem; margin-top: 0.5rem;'>Churn Probability</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            risk_level = "🔴 High Risk" if result['churn_probability'] > 0.7 else \
                        "🟡 Medium Risk" if result['churn_probability'] > 0.4 else "🟢 Low Risk"
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 2rem; border-radius: 1rem; text-align: center;
                        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4); 
                        min-height: 180px; color: white;'>
                <h3 style='color: white; margin-top: 0; font-weight: 600;'>Risk Level</h3>
                <div style='font-size: 2rem; margin-top: 1rem;'>{risk_level}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            confidence = abs(result['churn_probability'] - 0.5) * 200
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 2rem; border-radius: 1rem; text-align: center;
                        box-shadow: 0 8px 20px rgba(240, 147, 251, 0.4); 
                        min-height: 180px; color: white;'>
                <h3 style='color: white; margin-top: 0; font-weight: 600;'>Confidence</h3>
                <div style='font-size: 2rem; margin-top: 1rem; color: white;'>{confidence:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            action_priority = "🚨 Urgent" if result['churn_probability'] > 0.7 else \
                            "⚠️ Monitor" if result['churn_probability'] > 0.4 else "✅ Stable"
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                        padding: 2rem; border-radius: 1rem; text-align: center;
                        box-shadow: 0 8px 20px rgba(250, 112, 154, 0.4); 
                        min-height: 180px; color: white;'>
                <h3 style='color: white; margin-top: 0; font-weight: 600;'>Action Priority</h3>
                <div style='font-size: 2rem; margin-top: 1rem;'>{action_priority}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Probability gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=result['churn_probability'] * 100,
            title={'text': "Churn Probability (%)", 'font': {'size': 24}},
            delta={'reference': 50, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue", 'thickness': 0.3},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 40], 'color': '#10b981'},
                    {'range': [40, 70], 'color': '#fbbf24'},
                    {'range': [70, 100], 'color': '#ef4444'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            paper_bgcolor="white",
            font={'size': 14}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.markdown('<h2 class="sub-header">💡 Recommended Actions</h2>', unsafe_allow_html=True)
        
        if result['churn_probability'] > 0.7:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
                        padding: 2rem; border-radius: 1rem; color: white; margin: 1rem 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                <h3 style='color: white;'>🚨 High Churn Risk - Immediate Action Required!</h3>
                <ul style='font-size: 1.1rem; line-height: 2;'>
                    <li><strong>Priority 1:</strong> Contact customer within 24 hours</li>
                    <li><strong>Priority 2:</strong> Offer personalized retention package</li>
                    <li><strong>Priority 3:</strong> Investigate recent service quality issues</li>
                    <li><strong>Priority 4:</strong> Consider contract upgrade with incentives</li>
                    <li><strong>Priority 5:</strong> Assign to dedicated retention specialist</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        elif result['churn_probability'] > 0.4:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); 
                        padding: 2rem; border-radius: 1rem; color: white; margin: 1rem 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                <h3 style='color: white;'>⚠️ Medium Churn Risk - Proactive Monitoring</h3>
                <ul style='font-size: 1.1rem; line-height: 2;'>
                    <li>Schedule follow-up call within 1 week</li>
                    <li>Send customer satisfaction survey</li>
                    <li>Monitor usage patterns closely</li>
                    <li>Offer loyalty rewards or discounts</li>
                    <li>Ensure service quality is maintained</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                        padding: 2rem; border-radius: 1rem; color: white; margin: 1rem 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                <h3 style='color: white;'>✅ Low Churn Risk - Customer Satisfaction Focus</h3>
                <ul style='font-size: 1.1rem; line-height: 2;'>
                    <li>Maintain excellent service quality</li>
                    <li>Send thank you message for loyalty</li>
                    <li>Offer referral program incentives</li>
                    <li>Introduce premium service upgrades</li>
                    <li>Continue regular engagement</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)


def batch_prediction(pipeline):
    """Handle batch prediction from CSV upload."""
    st.markdown('<h2 class="sub-header">📁 Upload Customer Data</h2>', unsafe_allow_html=True)
    
    st.info("""
    **Instructions:**
    1. Upload a CSV file with customer data
    2. Ensure all required features are present
    3. Download predictions with churn probabilities
    """)
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Load data
        df = pd.read_csv(uploaded_file)
        
        st.success(f"✅ File uploaded successfully! {len(df)} customers found.")
        
        with st.expander("📋 Preview uploaded data"):
            st.dataframe(df.head(), use_container_width=True)
        
        if st.button("🔮 Generate Predictions", type="primary"):
            with st.spinner("Generating predictions..."):
                # Apply feature engineering
                df_engineered = engineer_features(df)
                
                # Remove target if present
                if 'Churn' in df_engineered.columns:
                    df_features = df_engineered.drop('Churn', axis=1)
                else:
                    df_features = df_engineered
                
                # Make predictions
                predictions_df = predict_batch(pipeline, df_features)
                
                # Display results
                st.markdown('<h2 class="sub-header">📊 Prediction Results</h2>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    churn_count = (predictions_df['Churn_Prediction'] == 'Churn').sum()
                    st.metric("Predicted Churns", f"{churn_count}")
                
                with col2:
                    churn_rate = (predictions_df['Churn_Prediction'] == 'Churn').mean() * 100
                    st.metric("Churn Rate", f"{churn_rate:.1f}%")
                
                with col3:
                    avg_prob = predictions_df['Churn_Probability'].mean() * 100
                    st.metric("Avg Churn Probability", f"{avg_prob:.1f}%")
                
                # Show predictions
                with st.expander("📋 View All Predictions"):
                    st.dataframe(predictions_df, use_container_width=True)
                
                # Download button
                csv = predictions_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Predictions",
                    data=csv,
                    file_name="churn_predictions.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # Visualization
                st.markdown('<h2 class="sub-header">📈 Prediction Distribution</h2>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.pie(predictions_df, names='Churn_Prediction',
                                title='Prediction Distribution',
                                color_discrete_sequence=['#2ca02c', '#d62728'])
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = px.histogram(predictions_df, x='Churn_Probability',
                                      title='Churn Probability Distribution',
                                      nbins=30, color_discrete_sequence=['#1f77b4'])
                    st.plotly_chart(fig, use_container_width=True)


def model_performance_page():
    """Display model performance metrics."""
    st.markdown('<h1 class="main-header">📈 Model Performance</h1>', unsafe_allow_html=True)
    
    try:
        # Load results
        results_path = Path(__file__).parent.parent / "models" / "all_results.joblib"
        results = joblib.load(results_path)
        
        # Model comparison
        st.markdown('<h2 class="sub-header">🏆 Model Comparison</h2>', unsafe_allow_html=True)
        
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
        
        # Display metrics table
        st.dataframe(comparison_df.style.highlight_max(axis=0, subset=['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']),
                    use_container_width=True)
        
        # Visualize comparison
        fig = go.Figure()
        
        metrics_to_plot = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
        
        for metric in metrics_to_plot:
            fig.add_trace(go.Bar(
                name=metric,
                x=comparison_df['Model'],
                y=comparison_df[metric],
                text=comparison_df[metric].round(3),
                textposition='auto',
            ))
        
        fig.update_layout(
            title='Model Performance Comparison',
            xaxis_title='Model',
            yaxis_title='Score',
            barmode='group',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Best model highlight
        best_model_idx = comparison_df['F1-Score'].idxmax()
        best_model = comparison_df.loc[best_model_idx, 'Model']
        
        st.success(f"🏆 **Best Model:** {best_model} (F1-Score: {comparison_df.loc[best_model_idx, 'F1-Score']:.4f})")
        
    except FileNotFoundError:
        st.warning("⚠️ Model evaluation results not found. Please train the models first by running: `python src/train.py`")


def main():
    """Main application."""
    # Sidebar with enhanced styling and Font Awesome icons
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem; background: rgba(255, 255, 255, 0.15); 
                    border-radius: 1rem; margin-bottom: 1.5rem; color: white;
                    backdrop-filter: blur(10px); box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);'>
            <i class='fas fa-chart-line icon-large' style='font-size: 3rem; margin-bottom: 0.5rem; color: white;'></i>
            <h2 style='color: white; font-size: 1.5rem; margin: 0; font-weight: 700; letter-spacing: -0.3px;'>
                Churn Prediction System
            </h2>
            <p style='color: #f0f0f0; font-size: 0.9rem; margin: 0.5rem 0 0 0; letter-spacing: 0.5px;'>
                AI-POWERED ANALYTICS
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='color: white; font-size: 1.1rem; margin-bottom: 1rem; font-weight: 600;'><i class='fas fa-compass icon'></i>Navigation</h3>", unsafe_allow_html=True)
        page = st.radio(
            "Select Page:",
            ["Home", "Exploratory Analysis", "Predict Churn", "Model Performance"],
            label_visibility="collapsed",
            format_func=lambda x: {
                "Home": "🏠 Home",
                "Exploratory Analysis": "📊 Exploratory Analysis", 
                "Predict Churn": "🔮 Predict Churn",
                "Model Performance": "📈 Model Performance"
            }[x]
        )
        
        st.markdown("---")
        
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.15); padding: 1.5rem; border-radius: 0.8rem; 
                    margin: 1rem 0; backdrop-filter: blur(10px); 
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); color: white;'>
            <h3 style='margin-top: 0; color: white; font-weight: 600; font-size: 1.1rem; letter-spacing: -0.2px;'>
                <i class='fas fa-info-circle icon'></i>About Project
            </h3>
            <p style='font-size: 0.95rem; line-height: 1.7; color: #f0f0f0; margin-bottom: 0;'>
                Enterprise-grade customer churn prediction system powered by advanced machine learning algorithms 
                and explainable AI technology.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.15); padding: 1.5rem; border-radius: 0.8rem;
                    backdrop-filter: blur(10px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); color: white;'>
            <h4 style='margin-top: 0; color: white; font-weight: 600; font-size: 1.05rem; letter-spacing: -0.2px;'>
                <i class='fas fa-cogs icon'></i>Technology Stack
            </h4>
            <div style='font-size: 0.95rem; color: #f0f0f0; line-height: 1.8;'>
                <div style='margin: 0.5rem 0; padding: 0.6rem; background: rgba(255, 255, 255, 0.1); border-radius: 0.5rem; border-left: 3px solid rgba(255, 255, 255, 0.4);'>
                    <i class='fab fa-python icon'></i><strong>Python</strong> & <strong>Streamlit</strong>
                </div>
                <div style='margin: 0.5rem 0; padding: 0.6rem; background: rgba(255, 255, 255, 0.1); border-radius: 0.5rem; border-left: 3px solid rgba(255, 255, 255, 0.4);'>
                    <i class='fas fa-brain icon'></i><strong>Scikit-learn</strong>
                </div>
                <div style='margin: 0.5rem 0; padding: 0.6rem; background: rgba(255, 255, 255, 0.1); border-radius: 0.5rem; border-left: 3px solid rgba(255, 255, 255, 0.4);'>
                    <i class='fas fa-rocket icon'></i><strong>XGBoost</strong>
                </div>
                <div style='margin: 0.5rem 0; padding: 0.6rem; background: rgba(255, 255, 255, 0.1); border-radius: 0.5rem; border-left: 3px solid rgba(255, 255, 255, 0.4);'>
                    <i class='fas fa-lightbulb icon'></i><strong>SHAP</strong> (Explainable AI)
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.15); padding: 1.5rem; border-radius: 0.8rem;
                    backdrop-filter: blur(10px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); color: white;'>
            <h4 style='margin-top: 0; color: white; font-weight: 600; font-size: 1.05rem; letter-spacing: -0.2px;'>
                <i class='fas fa-robot icon'></i>ML Models
            </h4>
            <div style='font-size: 0.95rem; color: #f0f0f0; line-height: 1.8;'>
                <div style='margin: 0.5rem 0; padding: 0.6rem; background: rgba(255, 255, 255, 0.1); border-radius: 0.5rem; border-left: 3px solid rgba(255, 255, 255, 0.4);'>
                    <i class='fas fa-chart-line icon'></i><strong>Logistic Regression</strong>
                </div>
                <div style='margin: 0.5rem 0; padding: 0.6rem; background: rgba(255, 255, 255, 0.1); border-radius: 0.5rem; border-left: 3px solid rgba(255, 255, 255, 0.4);'>
                    <i class='fas fa-tree icon'></i><strong>Random Forest</strong>
                </div>
                <div style='margin: 0.5rem 0; padding: 0.6rem; background: rgba(255, 255, 255, 0.1); border-radius: 0.5rem; border-left: 3px solid rgba(255, 255, 255, 0.4);'>
                    <i class='fas fa-bolt icon'></i><strong>XGBoost</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Add a stats badge
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem; background: rgba(255, 255, 255, 0.2); 
                    border-radius: 0.8rem; color: white; backdrop-filter: blur(10px);
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);'>
            <i class='fas fa-microchip' style='font-size: 2.5rem; margin-bottom: 0.8rem; display: block;'></i>
            <div style='font-size: 1.3rem; font-weight: 700; letter-spacing: -0.3px;'>AI POWERED</div>
            <div style='font-size: 0.9rem; color: #f0f0f0; margin-top: 0.3rem; letter-spacing: 0.5px;'>
                Real-time Predictions
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Route to pages
    if page == "Home":
        home_page()
    elif page == "Exploratory Analysis":
        eda_page()
    elif page == "Predict Churn":
        predict_page()
    elif page == "Model Performance":
        model_performance_page()


if __name__ == "__main__":
    main()
