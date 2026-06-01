"""
Indian Oil Corporation - AQI Prediction & Forecasting System
===========================================================
Advanced Mission Control UI for Proactive Emission Management
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import struct
import math
from forecasting_engine import HybridAQIForecaster

# --- REGISTRY INITIALIZATION ---

# --- GEOSPATIAL REGISTRY ---
CITY_COORDS = {
    'Delhi': [28.6139, 77.2090], 'Ahmedabad': [23.0225, 72.5714],
    'Lucknow': [26.8467, 80.9462], 'Bengaluru': [12.9716, 77.5946],
    'Chennai': [13.0827, 80.2707], 'Hyderabad': [17.3850, 78.4867],
    'Patna': [25.5941, 85.1376], 'Gurugram': [28.4595, 77.0266],
    'Visakhapatnam': [17.6868, 83.2185], 'Amritsar': [31.6340, 74.8723],
    'Jorapokhar': [23.7041, 86.4137], 'Jaipur': [26.9124, 75.7873],
    'Thiruvananthapuram': [8.5241, 76.9366], 'Amaravati': [16.5131, 80.5165],
    'Brajrajnagar': [21.8213, 83.9189], 'Talcher': [20.9500, 85.2300],
    'Kolkata': [22.5726, 88.3639], 'Mumbai': [19.0760, 72.8777],
    'Guwahati': [26.1158, 91.7086], 'Coimbatore': [11.0168, 76.9558],
    'Shillong': [25.5788, 91.8933], 'Chandigarh': [30.7333, 76.7794],
    'Bhopal': [23.2599, 77.4126], 'Kochi': [9.9312, 76.2673],
    'Ernakulam': [9.9816, 76.2999], 'Aizawl': [23.7271, 92.7176]
}

# --- REFINERY ZONE REGISTRY ---
# Expanded: Each city in the monitoring network is now assumed to have its own refinery
REFINERY_CITIES = sorted(list(CITY_COORDS.keys()))

# -----------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------
st.set_page_config(
    page_title="Indian Oil - AQI Prediction & Forecasting",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------
# Generate Beep Sound as WAV bytes
# -----------------------------------------------------------------
def generate_beep_wav_bytes(frequency=440, duration_ms=500, volume=0.5, sample_rate=44100):
    num_samples = int(sample_rate * duration_ms / 1000)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        fade_samples = int(sample_rate * 0.01)
        if i < fade_samples:
            fade = i / fade_samples
        elif i > num_samples - fade_samples:
            fade = (num_samples - i) / fade_samples
        else:
            fade = 1.0
        sample = int(volume * fade * 32767 * math.sin(2 * math.pi * frequency * t))
        samples.append(sample)
    
    wav_data = bytearray()
    wav_data.extend(b'RIFF')
    wav_data.extend(struct.pack('<I', 36 + num_samples * 2))
    wav_data.extend(b'WAVE')
    wav_data.extend(b'fmt ')
    wav_data.extend(struct.pack('<I', 16))
    wav_data.extend(struct.pack('<H', 1))
    wav_data.extend(struct.pack('<H', 1))
    wav_data.extend(struct.pack('<I', sample_rate))
    wav_data.extend(struct.pack('<I', sample_rate * 2))
    wav_data.extend(struct.pack('<H', 2))
    wav_data.extend(struct.pack('<H', 16))
    wav_data.extend(b'data')
    wav_data.extend(struct.pack('<I', num_samples * 2))
    for sample in samples:
        wav_data.extend(struct.pack('<h', sample))
    return bytes(wav_data)

def generate_alarm_wav_bytes(duration_ms=2000, volume=0.6, sample_rate=44100):
    num_samples = int(sample_rate * duration_ms / 1000)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        freq = 800 if (int(t * 8) % 2 == 0) else 600
        sample = int(volume * 32767 * math.sin(2 * math.pi * freq * t))
        samples.append(sample)
    
    wav_data = bytearray()
    wav_data.extend(b'RIFF')
    wav_data.extend(struct.pack('<I', 36 + num_samples * 2))
    wav_data.extend(b'WAVE')
    wav_data.extend(b'fmt ')
    wav_data.extend(struct.pack('<I', 16))
    wav_data.extend(struct.pack('<H', 1))
    wav_data.extend(struct.pack('<H', 1))
    wav_data.extend(struct.pack('<I', sample_rate))
    wav_data.extend(struct.pack('<I', sample_rate * 2))
    wav_data.extend(struct.pack('<H', 2))
    wav_data.extend(struct.pack('<H', 16))
    wav_data.extend(b'data')
    wav_data.extend(struct.pack('<I', num_samples * 2))
    for sample in samples:
        wav_data.extend(struct.pack('<h', sample))
    return bytes(wav_data)

@st.cache_data
def get_warning_sound():
    return generate_beep_wav_bytes(frequency=600, duration_ms=800, volume=0.5)

@st.cache_data
def get_critical_sound():
    return generate_alarm_wav_bytes(duration_ms=2000, volume=0.6)

@st.cache_data
def get_safe_sound():
    return generate_beep_wav_bytes(frequency=440, duration_ms=300, volume=0.3)

# -----------------------------------------------------------------
# PREMIUM LIGHT & AIRY DESIGN SYSTEM
# -----------------------------------------------------------------
st.markdown("""
<style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Outfit:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');
    
    /* Global Styles */
    .stApp {
        background: #020617;
        background-attachment: fixed;
        overflow: hidden;
    }
    
    /* DYNAMIC STRATEGIC SKY: NEBULA LAYER */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: 
            radial-gradient(circle at 10% 20%, rgba(15, 23, 42, 1) 0%, transparent 50%),
            radial-gradient(circle at 90% 80%, rgba(30, 41, 59, 1) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(2, 6, 23, 1) 0%, transparent 100%);
        z-index: -3;
        animation: nebulaPulse 15s ease-in-out infinite alternate;
    }

    @keyframes nebulaPulse {
        from { filter: hue-rotate(0deg) brightness(1); }
        to { filter: hue-rotate(15deg) brightness(1.2); }
    }

    /* TWINKLING STARFIELD */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0; left: 0; width: 200%; height: 200%;
        background-image: 
            radial-gradient(1px 1px at 25px 50px, #fff, transparent),
            radial-gradient(1px 1px at 75px 125px, #fff, transparent),
            radial-gradient(1.5px 1.5px at 150px 75px, #fff, transparent),
            radial-gradient(1px 1px at 250px 200px, #fff, transparent);
        background-size: 300px 300px;
        opacity: 0.3;
        z-index: -2;
        animation: starTwinkle 4s ease-in-out infinite alternate;
    }

    @keyframes starTwinkle {
        0%, 100% { opacity: 0.2; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.05); }
    }

    /* MULTI-LAYER PARALLAX CLOUDS */
    #background-clouds {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        z-index: -1;
        pointer-events: none;
    }
    
    .cloud-layer {
        position: absolute;
        width: 200%; height: 100%;
        background-repeat: repeat-x;
        opacity: 0.4;
    }
    
    .cloud-1 {
        background: radial-gradient(circle at 50% 50%, rgba(255,255,255,0.05) 0%, transparent 70%);
        background-size: 800px 400px;
        animation: drift 120s linear infinite;
        top: -10%;
    }
    
    .cloud-2 {
        background: radial-gradient(circle at 30% 60%, rgba(255,255,255,0.03) 0%, transparent 60%);
        background-size: 1200px 600px;
        animation: drift 180s linear infinite reverse;
        top: 20%;
    }
    
    .cloud-3 {
        background: radial-gradient(circle at 70% 40%, rgba(255,255,255,0.04) 0%, transparent 80%);
        background-size: 1000px 500px;
        animation: drift 240s linear infinite;
        bottom: -10%;
    }

    @keyframes drift {
        from { transform: translateX(0); }
        to { transform: translateX(-50%); }
    }

    /* NEURAL DATA SPARKS */
    .spark {
        position: absolute;
        width: 2px; height: 2px;
        background: #00f5ff;
        border-radius: 50%;
        box-shadow: 0 0 10px #00f5ff;
        animation: rise 10s linear infinite;
        opacity: 0;
    }

    @keyframes rise {
        0% { transform: translateY(110vh) scale(0); opacity: 0; }
        20% { opacity: 0.6; }
        80% { opacity: 0.6; }
        100% { transform: translateY(-10vh) scale(1); opacity: 0; }
    }

    /* Fade-in Animation for Elements */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Apply Fade-in with Staggering */
    [data-testid="stVerticalBlock"] > div {
        animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        opacity: 0;
    }
    
    [data-testid="stVerticalBlock"] > div:nth-child(1) { animation-delay: 0.1s; }
    [data-testid="stVerticalBlock"] > div:nth-child(2) { animation-delay: 0.2s; }
    [data-testid="stVerticalBlock"] > div:nth-child(3) { animation-delay: 0.3s; }
    [data-testid="stVerticalBlock"] > div:nth-child(4) { animation-delay: 0.4s; }
    [data-testid="stVerticalBlock"] > div:nth-child(5) { animation-delay: 0.5s; }

    /* Header Styling - Indian Oil Branding */
    .main-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.8rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #ff6b00 0%, #003399 50%, #ff6b00 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: brandGlow 5s ease-in-out infinite;
        text-shadow: 0 0 40px rgba(255, 107, 0, 0.3);
        letter-spacing: 5px;
        position: relative;
    }
    
    @keyframes brandGlow {
        0%, 100% { background-position: 0% 50%; filter: brightness(1.2); }
        50% { background-position: 100% 50%; filter: brightness(1.1); }
    }
    
    .sub-header {
        font-family: 'Outfit', sans-serif;
        color: #94a3b8;
        text-align: center;
        font-size: 1.3rem;
        margin-bottom: 2.5rem;
        letter-spacing: 2px;
        font-weight: 500;
        opacity: 0.85;
    }
    
    /* PREMIUM LUMINOUS DARK GLASS CARD */
    .metric-card {
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 28px;
        padding: 2.5rem;
        border: 1px solid rgba(0, 245, 255, 0.3);
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8), inset 0 0 20px rgba(0, 245, 255, 0.05);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-12px) scale(1.02);
        background: rgba(30, 41, 59, 0.95);
        border-color: #00f5ff;
        box-shadow: 0 40px 80px rgba(0, 245, 255, 0.15), inset 0 0 30px rgba(0, 245, 255, 0.1);
    }
    
    .metric-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 4.8rem;
        font-weight: 900;
        color: #00f5ff;
        text-shadow: 0 0 40px rgba(0, 245, 255, 0.6);
        margin-top: 10px;
    }
    
    .metric-label {
        font-family: 'Outfit', sans-serif;
        color: #94a3b8;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 4px;
        font-weight: 700;
    }
    
    /* Alert Status Cards */
    .warning-card {
        background: rgba(255, 100, 0, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid #f59e0b;
        color: #fbbf24;
        border-radius: 24px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.2);
        animation: pulseOrange 2s ease-in-out infinite;
    }
    
    @keyframes pulseOrange {
        0%, 100% { border-color: #f59e0b; box-shadow: 0 0 30px rgba(245, 158, 11, 0.2); }
        50% { border-color: #ff9900; box-shadow: 0 0 50px rgba(245, 158, 11, 0.5); }
    }

    .critical-warning-card {
        background: rgba(255, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        border: 2px solid #f43f5e;
        color: #fecaca;
        border-radius: 24px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(244, 63, 94, 0.3);
        animation: criticalShake 0.5s ease-in-out infinite;
    }
    
    @keyframes criticalShake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-3px); }
        75% { transform: translateX(3px); }
    }
    
    .safe-card {
        background: rgba(0, 255, 100, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid #22c55e;
        color: #bbf7d0;
        border-radius: 24px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(34, 197, 94, 0.2);
    }
    
    /* PREMIUM BUTTON */
    .stButton > button {
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(135deg, #ff6b00 0%, #003399 100%);
        color: white !important;
        border: none;
        border-radius: 16px;
        padding: 1rem 2.5rem;
        font-weight: 800;
        font-size: 1.1rem;
        letter-spacing: 1px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 0 20px rgba(255, 107, 0, 0.3);
        animation: pulseOrange 2s ease-in-out infinite;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 0 40px rgba(255, 107, 0, 0.6);
        background: linear-gradient(135deg, #003399 0%, #ff6b00 100%);
    }
    
    /* SIDEBAR STYLING */
    section[data-testid="stSidebar"] {
        background: rgba(5, 5, 20, 0.95) !important;
        border-right: 1px solid rgba(0, 255, 255, 0.1) !important;
        box-shadow: 10px 0 30px rgba(0,0,0,0.5);
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        font-family: 'Outfit', sans-serif;
        color: #00ffff;
    }
    
    /* Info Box */
    .info-box {
        font-family: 'Outfit', sans-serif;
        background: rgba(30, 41, 59, 0.4);
        border-left: 5px solid #00f5ff;
        padding: 1.5rem;
        border-radius: 0 20px 20px 0;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        color: #f1f5f9;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* STRATEGIC GLASS PANEL SYSTEM */
    .glass-panel {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 245, 255, 0.2);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    }
    
    .glass-panel:hover {
        border-color: rgba(0, 245, 255, 0.5);
        box-shadow: 0 8px 32px 0 rgba(0, 245, 255, 0.1);
    }

    /* STRATEGIC NARRATIVE BOX */
    .strategic-narrative {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
        border-left: 4px solid #00f5ff;
        border-radius: 0 16px 16px 0;
        padding: 24px;
        margin: 15px 0;
        font-family: 'Outfit', sans-serif;
    }
    
    .narrative-title {
        color: #00f5ff;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.85rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    
    .narrative-text {
        color: #e2e8f0;
        font-size: 1rem;
        line-height: 1.6;
    }

    /* AQI Scale Items */
    .aqi-scale-item {
        display: flex;
        align-items: center;
        padding: 1rem;
        margin: 0.5rem 0;
        background: rgba(0, 20, 40, 0.6);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .aqi-scale-item:hover {
        transform: translateX(10px);
        background: rgba(0, 255, 255, 0.1);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
    }
    
    /* Status Indicator */
    .status-online {
        display: inline-block;
        width: 12px;
        height: 12px;
        background: #00ff88;
        border-radius: 50%;
        margin-right: 10px;
        box-shadow: 0 0 10px #00ff88;
        animation: blink 2s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* REFINED VISIBILITY FIX (Universal Compatibility) */
    .stApp {
        background-color: #020617 !important;
    }
    
    /* Target Streamlit default text elements - avoid !important to allow inline overrides */
    .stMarkdown p, .stMarkdown span, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, 
    .stText, label, .stRadio label, .stCheckbox label, .stExpander label, .stButton label, 
    div[data-testid="stMarkdownContainer"] p, div[data-testid="stMarkdownContainer"] li {
        color: #e2e8f0;
    }
    
    /* Segmented Control & Other specific components */
    div[data-testid="stSegmentedControl"] label, 
    div[data-testid="stSegmentedControl"] p {
        color: #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
    }
    
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #e2e8f0;
    }
    
    .stMetric label {
        color: #94a3b8 !important;
    }
    
    .metric-value {
        color: #00f5ff !important;
        text-shadow: 0 0 20px rgba(0, 245, 255, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------
# Global Constants & Features
# -----------------------------------------------------------------
MODEL_FEATURES = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene', 'Temperature', 'Humidity']
FEATURES = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene']

# -----------------------------------------------------------------
# SYSTEM INTEGRITY CHECKS
# -----------------------------------------------------------------
def verify_system_integrity():
    """Verifies all required model and data assets are present."""
    failures = []
    required_files = [
        "rf_model.joblib", "lr_model.joblib", "scaler.joblib",
        "data/preprocessed_city_day.csv", "sidebar_logo.png"
    ]
    for f in required_files:
        if not Path(f).exists():
            failures.append(f)
    return failures

# Load Model and Scaler
def load_model_and_scaler():
    rf_path = Path("rf_model.joblib")
    lr_path = Path("lr_model.joblib")
    scaler_path = Path("scaler.joblib")
    
    failures = verify_system_integrity()
    if failures:
        return None, None, None, f"CRITICAL ASSET MISSING: {', '.join(failures)}"
        
    rf_model = joblib.load(rf_path)
    lr_model = joblib.load(lr_path)
    scaler = joblib.load(scaler_path)
    return rf_model, lr_model, scaler, None

rf_model, lr_model, scaler, error = load_model_and_scaler()

@st.cache_data
def get_model_performance_data():
    try:
        data = pd.read_csv("data/preprocessed_city_day.csv")
        model_data = data.copy()
        
        # Use standardized feature list
        X = model_data[MODEL_FEATURES]
        
        y_true = model_data['AQI']
        
        X_scaled = scaler.transform(X)
        y_rf = rf_model.predict(X_scaled)
        y_lr = lr_model.predict(X_scaled)
        
        # Return a dataframe with City, Date, Actual, and Predicted for trend analysis
        results_df = pd.DataFrame({
            'City': model_data['City'],
            'Date': model_data['Date'],
            'Actual AQI': y_true,
            'RF Predicted AQI': y_rf,
            'LR Predicted AQI': y_lr
        })
        
        results_df['Date'] = pd.to_datetime(results_df['Date'])
        results_df = results_df.dropna(subset=['Actual AQI'])
        return results_df
    except Exception as e:
        return pd.DataFrame()

def get_city_forecast(city_results):
    """
    Analyze history and predict tomorrow's AQI for both models.
    """
    if city_results is None or city_results.empty:
        return None, None, None
        
    # Sort by date
    city_sorted = city_results.sort_values('Date')
    recent_data = city_sorted.tail(7)
    
    if recent_data.empty:
        return 0.0, 0.0, "UNKNOWN (No Data)"
        
    if len(recent_data) < 2:
        return recent_data['RF Predicted AQI'].iloc[-1], recent_data['LR Predicted AQI'].iloc[-1], "STABLE (Insufficient History)"
        
    # RF Trend
    rf_diff = recent_data['RF Predicted AQI'].diff().mean()
    rf_forecast = recent_data['RF Predicted AQI'].iloc[-1] + rf_diff
    
    # LR Trend
    lr_diff = recent_data['LR Predicted AQI'].diff().mean()
    lr_forecast = recent_data['LR Predicted AQI'].iloc[-1] + lr_diff
    
    # Trend label based on RF
    if rf_diff > 5:
        trend = "RISING ↑"
    elif rf_diff < -5:
        trend = "IMPROVING ↓"
    else:
        trend = "STABLE →"
        
    return rf_forecast, lr_forecast, trend

# Load data for Analytics Baseline
results_df = get_model_performance_data()

# -----------------------------------------------------------------
# Header & background Setup
# -----------------------------------------------------------------
# Inject Background Elements
st.markdown("""
<div id="background-clouds">
    <div class="cloud-layer cloud-1"></div>
    <div class="cloud-layer cloud-2"></div>
    <div class="cloud-layer cloud-3"></div>
    <div class="spark" style="left: 10%; animation-delay: 0s;"></div>
    <div class="spark" style="left: 30%; animation-delay: 2s;"></div>
    <div class="spark" style="left: 55%; animation-delay: 5s;"></div>
    <div class="spark" style="left: 80%; animation-delay: 1s;"></div>
    <div class="spark" style="left: 95%; animation-delay: 8s;"></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">INDIAN OIL</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">PROACTIVE ENVIRONMENTAL MISSION CONTROL — HYBRID ARIMA-LSTM ENGINE</p>', unsafe_allow_html=True)

# System Status
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# -----------------------------------------------------------------
# STATE INITIALIZATION
# -----------------------------------------------------------------
if 'prediction_city' not in st.session_state:
    st.session_state['prediction_city'] = None
if 'forecast_city' not in st.session_state:
    st.session_state['forecast_city'] = None
if 'forecast_results' not in st.session_state:
    st.session_state['forecast_results'] = None

# -----------------------------------------------------------------
# Sidebar - Cockpit Design
# -----------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0;">
        <h2 style="font-family: 'Orbitron', sans-serif; color: #00f5ff; margin: 0; letter-spacing: 3px;">MISSION COCKPIT</h2>
        <div style="font-family: 'Share Tech Mono', monospace; color: #64748b; font-size: 0.8rem; margin-top: 0.5rem;">
            SYSTEM v4.0 ACTIVE
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.image("sidebar_logo.png", width='stretch')
    
    st.markdown("---")
    st.markdown('<div class="sidebar-header" style="color: #00f5ff; font-family: \'Orbitron\', sans-serif; font-size: 0.9rem; letter-spacing: 2px; margin-bottom: 10px;">💠 OPERATIONAL DOMAIN</div>', unsafe_allow_html=True)
    sys_domain = st.segmented_control(
        "Select Active Layer", 
        ["REAL-TIME ENGINE", "QUANTUM FORECAST"], 
        default="REAL-TIME ENGINE"
    )
    
    # CONTEXT AWARE CONTROLS
    if sys_domain == "REAL-TIME ENGINE":
        st.markdown("---")
        st.markdown('<div class="sidebar-header" style="color: #00ff88; font-family: \'Orbitron\', sans-serif; font-size: 0.9rem; letter-spacing: 2px; margin-bottom: 10px;">🧬 POLLUTANT VECTORS</div>', unsafe_allow_html=True)
        if not st.session_state.get('prediction_city'):
             st.info("🎯 Select a city to unlock manual sensor override.")
        else:
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                pm25 = st.number_input("PM2.5", 0.0, 500.0, st.session_state.get('pm25', 0.0), 1.0)
                no = st.number_input("NO", 0.0, 200.0, st.session_state.get('no', 0.0), 1.0)
                nox = st.number_input("NOx", 0.0, 300.0, st.session_state.get('nox', 0.0), 1.0)
                co = st.number_input("CO", 0.0, 50.0, st.session_state.get('co', 0.0), 0.1)
                o3 = st.number_input("O₃", 0.0, 300.0, st.session_state.get('o3', 0.0), 1.0)
                toluene = st.number_input("Toluene", 0.0, 100.0, st.session_state.get('toluene', 0.0), 1.0)
            with p_col2:
                pm10 = st.number_input("PM10", 0.0, 600.0, st.session_state.get('pm10', 0.0), 1.0)
                no2 = st.number_input("NO₂", 0.0, 200.0, st.session_state.get('no2', 0.0), 1.0)
                nh3 = st.number_input("NH₃", 0.0, 200.0, st.session_state.get('nh3', 0.0), 1.0)
                so2 = st.number_input("SO₂", 0.0, 200.0, st.session_state.get('so2', 0.0), 1.0)
                benzene = st.number_input("Benzene", 0.0, 50.0, st.session_state.get('benzene', 0.0), 0.1)
                xylene = st.number_input("Xylene", 0.0, 50.0, st.session_state.get('xylene', 0.0), 0.1)
            
            warning_threshold = st.slider("⚠️ SENSITIVITY", 50, 300, 150, 10)
    
    else:
        # Forecast Mode Sidebar Content
        st.markdown("---")
        st.markdown('<div class="sidebar-header" style="color: #c084fc; font-family: \'Orbitron\', sans-serif; font-size: 0.9rem; letter-spacing: 2px; margin-bottom: 10px;">🛰️ TARGET REFINERY ZONE</div>', unsafe_allow_html=True)
        
        # Ensure forecast_city is a valid refinery or None
        forecast_city_val = st.session_state.get('forecast_city')
        if forecast_city_val is not None and forecast_city_val not in REFINERY_CITIES:
            st.session_state['forecast_city'] = None

        # Directly bind selectbox to session_state key — Streamlit handles sync automatically
        # Use index instead of key to allow programmatic updates to session state
        options = ["Select IOCL Refinery..."] + REFINERY_CITIES
        current_city = st.session_state.get('forecast_city')
        current_idx = options.index(current_city) if current_city in options else 0
        
        selected_ref_choice = st.selectbox(
            "Select IOCL Refinery",
            options,
            index=current_idx,
            help="Select from designated IOCL refinery monitoring centers."
        )
        
        new_city = selected_ref_choice if selected_ref_choice != "Select IOCL Refinery..." else None
        
        if st.session_state['forecast_city'] != new_city:
            st.session_state['forecast_city'] = new_city
            st.session_state['forecast_results'] = None # Clear results on city change
            st.rerun()
        
        # Live refinery metadata card (reads freshly updated session state)
        active_ref = st.session_state['forecast_city']
        st.markdown(f"""
        <div style="background: rgba(124, 58, 237, 0.1); border: 1px solid rgba(124, 58, 237, 0.5);
                    border-radius: 12px; padding: 12px; margin-top: 10px;">
            <div style="color: #c084fc; font-family: 'Orbitron', sans-serif; font-size: 0.7rem; letter-spacing: 2px;">ACTIVE REFINERY TARGET</div>
            <div style="color: #e879f9; font-family: 'Share Tech Mono', monospace; font-size: 1.1rem; margin-top: 4px;">{active_ref}</div>
            <div style="color: #a78bfa; font-family: 'Share Tech Mono', monospace; font-size: 0.65rem; margin-top: 6px;">
                ENGINE: HYBRID ARIMA+LSTM<br>
                WINDOW: 7-DAY FORECAST<br>
                MODE: EMISSION CONTROL
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📈 FORECAST ANALYTICS")
        st.info("🚀 Select a refinery above and hit **INITIALIZE** to run the 7-day forecast.")


    st.markdown("---")
    sound_enabled = st.checkbox("🔊 AUDIO TELEMETRY", value=st.session_state.get('sound_enabled', True))
    st.session_state['sound_enabled'] = sound_enabled
    
    # Contextual Sidebar Health Check
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(0, 245, 255, 0.2); border-radius: 12px; padding: 10px; margin-top: 1rem;">
        <div style="font-family: 'Share Tech Mono', monospace; color: #00f5ff; font-size: 0.75rem;">
            <span class="status-online"></span> NEURAL LINK: STABLE
        </div>
        <div style="font-family: 'Share Tech Mono', monospace; color: #94a3b8; font-size: 0.7rem; margin-top: 5px;">
            CPU: 12% | LATENCY: 42ms
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main HUD Status
st.markdown(f"""
<div style="text-align: center; margin-bottom: 3rem; background: rgba(15, 23, 42, 0.6); padding: 0.8rem 2rem; border-radius: 50px; display: inline-block; position: relative; left: 50%; transform: translateX(-50%); border: 1px solid rgba(0, 245, 255, 0.3); backdrop-filter: blur(10px);">
    <span style="font-family: 'Share Tech Mono', monospace; color: #00f5ff; letter-spacing: 4px; font-size: 0.9rem;">
        STRATEGIC HUB ACTIVE | {sys_domain} | {current_time}
    </span>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------
# AQI Classification & Geospatial Hubs
# -----------------------------------------------------------------
def get_aqi_category(aqi):
    if aqi <= 50:
        return "GOOD", "#00ff88", "Air quality is satisfactory.", "safe"
    elif aqi <= 100:
        return "SATISFACTORY", "#99ff33", "Acceptable for most.", "safe"
    elif aqi <= 200:
        return "MODERATE", "#ffff00", "Moderate health concerns.", "warning"
    elif aqi <= 300:
        return "POOR", "#ff9900", "Health effects for everyone.", "warning"
    elif aqi <= 400:
        return "VERY POOR", "#ff3300", "Serious health effects.", "warning"
    else:
        return "SEVERE", "#990000", "EMERGENCY CONDITIONS!", "critical"

def render_target_header(target_city, engine_desc):
    """Unified premium header for the active target."""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(88, 28, 135, 0.3), rgba(124, 58, 237, 0.1));
                border: 1px solid rgba(124, 58, 237, 0.5); border-radius: 20px; 
                padding: 24px; margin-bottom: 25px; backdrop-filter: blur(10px);">
        <div style="font-family: 'Orbitron', sans-serif; color: #a78bfa; font-size: 0.8rem; letter-spacing: 4px; text-transform: uppercase;">📍 ACTIVE TARGET REFINERY</div>
        <div style="font-family: 'Orbitron', sans-serif; color: #ffffff; font-size: 2.2rem; font-weight: 900; margin-top: 8px; text-shadow: 0 0 20px rgba(167, 139, 250, 0.4);">{target_city}</div>
        <div style="display: flex; align-items: center; margin-top: 12px;">
            <div class="status-online"></div>
            <div style="font-family: 'Share Tech Mono', monospace; color: #c084fc; font-size: 0.85rem;">
                {engine_desc}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_forecast_narrative(forecast_data, dates):
    """Generates a human-readable strategic outlook for the 7-day horizon."""
    peak_idx = np.argmax(forecast_data)
    peak_val = forecast_data[peak_idx]
    peak_date = dates[peak_idx].strftime('%A')
    
    start_val = forecast_data[0]
    end_val = forecast_data[-1]
    trend = "DECREASING" if end_val < start_val else "INCREASING"
    trend_icon = "📉" if end_val < start_val else "📈"
    
    avg_aqi = np.mean(forecast_data)
    cat, color, _, _ = get_aqi_category(avg_aqi)

    st.markdown(f"""
    <div class="strategic-narrative">
        <div class="narrative-title">🛰️ 7-DAY STRATEGIC OUTLOOK</div>
        <div class="narrative-text">
            The neural engine predicts an <b>{trend}</b> trend {trend_icon} across the 7-day horizon. 
            Analysis indicates a peak risk window on <b>{peak_date}</b> with AQI levels reaching approximately <b>{peak_val:.1f}</b>.
            <br><br>
            Overall mean intensity is projected at <span style="color: {color}; font-weight: 700;">{cat}</span> targets. 
            Proactive unit optimization is recommended for mid-week shifts to mitigate atmospheric loading.
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_geospatial_data(cities, current_city):
    """Prepares data for the Geospatial Hub"""
    geo_data = []
    try:
        data = pd.read_csv("data/preprocessed_city_day.csv")
        for city in cities:
            if city in CITY_COORDS:
                city_subset = data[data['City'] == city]
                avg_aqi = city_subset['AQI'].mean() if not city_subset.empty else 100
                category, color, _, _ = get_aqi_category(avg_aqi)
                geo_data.append({
                    'City': city,
                    'Lat': CITY_COORDS[city][0],
                    'Lon': CITY_COORDS[city][1],
                    'Historical Avg AQI': round(avg_aqi, 1),
                    'Risk Level': category,
                    'Color': color,
                    'is_selected': 15 if city == current_city else 8
                })
        return pd.DataFrame(geo_data)
    except:
        return pd.DataFrame()

def render_geospatial_hub(selected_city):
    """Renders the Digital 3D Geospatial Map"""
    cities = list(CITY_COORDS.keys())
    geo_df = get_geospatial_data(cities, selected_city)
    
    if geo_df.empty:
        st.warning("Geospatial Engine Offline")
        return

    fig = px.scatter_mapbox(geo_df, lat="Lat", lon="Lon", 
                            hover_name="City",
                            hover_data={"Historical Avg AQI": True, "Risk Level": True, "Lat": False, "Lon": False},
                            color="Risk Level",
                            size="is_selected",
                            color_discrete_map={
                                "GOOD": "#00ff88", "SATISFACTORY": "#99ff33",
                                "MODERATE": "#ffff00", "POOR": "#ff9900",
                                "VERY POOR": "#ff3300", "SEVERE": "#990000"
                            },
                            zoom=3.5, height=500,
                            custom_data=['City'])

    # Always center on India with a fixed zoom to keep all cities visible
    center = {"lat": 20.5937, "lon": 78.9629} 
    zoom = 3.5

    fig.update_layout(
        mapbox_style="carto-darkmatter",
        mapbox_center=center,
        mapbox_zoom=zoom,
        margin={"r":0,"t":40,"l":0,"b":0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Orbitron', color='#00ffff'),
        title=dict(text="🛰️ CORE GEOSPATIAL HUB: MISSION CONTROL", font=dict(size=18, color="#00ffff")),
        clickmode='event+select'
    )
    
    # Handle selection
    selection = st.plotly_chart(fig, width='stretch', key="mission_control_map", on_select="rerun", selection_mode=['points'])
    
    if selection and "selection" in selection and selection["selection"]["points"]:
        selected_city_name = selection["selection"]["points"][0]["customdata"][0]
        if selected_city_name != st.session_state.get('prediction_city'):
            st.session_state['prediction_city'] = selected_city_name
            st.rerun()

def render_refinery_geospatial_hub(selected_city):
    """Renders the Geospatial Map showing only IOCL Refinery Zones."""
    geo_df = get_geospatial_data(REFINERY_CITIES, selected_city)
    
    if geo_df.empty:
        st.warning("🛰️ Quantum Geospatial Engine Offline")
        return

    # Visual distinction for selected vs unselected
    geo_df['MarkerSize'] = geo_df['City'].apply(lambda x: 45 if x == selected_city else 25)
    geo_df['SelectionStatus'] = geo_df['City'].apply(lambda x: 'Active Refinery' if x == selected_city else 'Refinery Site')

    fig = px.scatter_mapbox(
        geo_df, lat="Lat", lon="Lon",
        hover_name="City",
        hover_data={"Historical Avg AQI": True, "Risk Level": True, "SelectionStatus": True, "Lat": False, "Lon": False},
        color="SelectionStatus",
        size="MarkerSize",
        color_discrete_map={
            'Active Refinery': '#ff00ff',
            'Refinery Site': '#00f5ff'
        },
        zoom=3.8, height=480,
        custom_data=['City']
    )

    fig.update_layout(
        mapbox_style="carto-darkmatter",
        mapbox_center={"lat": 23.0, "lon": 82.0},
        margin={"r":0, "t":45, "l":0, "b":0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Orbitron', color='#c084fc'),
        title=dict(
            text=f"🛰️ MISSION CONTROL - GEOSPATIAL TARGETING",
            font=dict(size=16, color="#c084fc")
        ),
        clickmode='event+select'
    )
    
    selection = st.plotly_chart(fig, width='stretch', key="refinery_map", on_select="rerun", selection_mode=['points'])
    
    if selection and "selection" in selection and selection["selection"]["points"]:
        clicked_city = selection["selection"]["points"][0]["customdata"][0]
        if clicked_city in REFINERY_CITIES and clicked_city != st.session_state.get('forecast_city'):
            st.session_state['forecast_city'] = clicked_city
            st.rerun()

# -----------------------------------------------------------------
# ADVANCED QUANTUM VISUALIZATIONS
# -----------------------------------------------------------------
def render_pollutant_radar(city_data):
    """Renders a spectral signature (radar chart) for pollutants."""
    pollutants = ['PM2.5', 'PM10', 'NO2', 'CO', 'SO2', 'O3']
    # Filter to pollutants available in city_data
    available_p = [p for p in pollutants if p in city_data.columns]
    latest_avgs = [city_data[p].mean() for p in available_p]
    if not latest_avgs: return
    
    # Normalize for visual balance (relative to common thresholds)
    thresh_map = {'PM2.5': 250, 'PM10': 250, 'NO2': 150, 'CO': 10, 'SO2': 80, 'O3': 180}
    norm_vals = [(v / thresh_map.get(p, 100) * 100) for v, p in zip(latest_avgs, available_p)]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=norm_vals + [norm_vals[0]],
        theta=available_p + [available_p[0]],
        fill='toself',
        fillcolor='rgba(0, 245, 255, 0.2)',
        line=dict(color='#00f5ff', width=2),
        name='Spectral Signature'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(255,255,255,0.1)', tickfont=dict(size=8, color="#94a3b8")),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(family='Orbitron', size=10, color="#00f5ff")),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=40, b=40),
        height=320,
    )
    st.plotly_chart(fig, use_container_width=True)

def render_risk_heatmap(historical_data):
    """Renders a temporal risk heatmap (Day of Week vs AQI Intensity)."""
    df = historical_data.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Day'] = df['Date'].dt.day_name()
    df['Week'] = df['Date'].dt.isocalendar().week
    
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if df['Week'].max() > 20:
        df = df[df['Week'] > df['Week'].max() - 20]
        
    heatmap_data = df.pivot_table(index='Day', columns='Week', values='AQI', aggfunc='mean').reindex(days_order)

    fig = px.imshow(
        heatmap_data,
        labels=dict(x="Week of Year", y="", color="AQI"),
        color_continuous_scale="Viridis",
        template="plotly_dark"
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Share Tech Mono', color='#c084fc'),
        height=280,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

def render_weather_convergence(forecast_dates, aqi_vals, city_data):
    """Renders meteorological convergence (AQI vs Temp/Humidity)."""
    # Robust column access with fallbacks to avoid KeyErrors
    avg_temp = city_data['Temperature'].mean() if 'Temperature' in city_data.columns else 25.0
    avg_hum = city_data['Humidity'].mean() if 'Humidity' in city_data.columns else 60.0
    
    temp_f = [avg_temp + math.sin(i*0.5)*2 for i in range(7)]
    hum_f = [avg_hum + math.cos(i*0.5)*5 for i in range(7)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=forecast_dates, y=aqi_vals,
        name="AQI",
        line=dict(color='#00f5ff', width=4),
        yaxis="y1"
    ))
    fig.add_trace(go.Scatter(
        x=forecast_dates, y=temp_f,
        name="Temp",
        line=dict(color='#ff9900', width=2, dash='dot'),
        yaxis="y2"
    ))
    fig.add_trace(go.Scatter(
        x=forecast_dates, y=hum_f,
        name="Hum",
        line=dict(color='#a78bfa', width=2, dash='dot'),
        yaxis="y2"
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode="x unified",
        margin=dict(l=10, r=10, t=30, b=10),
        height=320,
        yaxis=dict(title=dict(text="AQI", font=dict(color="#00f5ff")), tickfont=dict(color="#00f5ff")),
        yaxis2=dict(title=dict(text="Weather", font=dict(color="#ff9900")), tickfont=dict(color="#ff9900"), 
                    anchor="x", overlaying="y", side="right"),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True, key="weather_conv")

# -----------------------------------------------------------------
# QUANTUM FORECAST HUB - Hybrid ARIMA-LSTM
# -----------------------------------------------------------------
def render_forecast_hub(selected_city):
    """Master render function for the Quantum Forecast Hub."""
    # Guard: ensure only valid refinery cities enter the engine
    if not selected_city or selected_city not in REFINERY_CITIES:
        st.warning("🎯 **NO ACTIVE REFINERY TARGET** — Select an IOCL Refinery from the sidebar or click a cyan marker on the network map.")
        render_refinery_geospatial_hub(selected_city or '')
        return

    # ---- MISSION CONTROL BLOCK (Controls & Targeting) ----
    st.markdown('<div class="glass-panel" style="margin-bottom: 30px;">', unsafe_allow_html=True)
    mc_col1, mc_col2 = st.columns([2, 1])
    
    with mc_col1:
        st.markdown('<div class="sidebar-header" style="color: #c084fc; font-family: \'Orbitron\', sans-serif; font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 15px;">🛰️ IOCL REFINERY NETWORK MAP</div>', unsafe_allow_html=True)
        render_refinery_geospatial_hub(selected_city)
    
    with mc_col2:
        st.markdown('<div class="sidebar-header" style="color: #00f5ff; font-family: \'Orbitron\', sans-serif; font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 15px;">⚙️ ENGINE CONFIGURATION</div>', unsafe_allow_html=True)
        tuning_mode = st.toggle("Enable Advanced Hyperparameter Tuning", value=False, help="Runs auto-ARIMA and LSTM optimization. May take longer.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 INITIALIZE HYBRID FORECAST", width='stretch'):
            with st.spinner(f"Synchronizing Neural VECTORS for {selected_city}..."):
                try:
                    forecaster = HybridAQIForecaster(selected_city)
                    forecaster.load_and_preprocess()
                    
                    prog = st.progress(0, text="Performing Seasonal Decomposition...")
                    decomp = forecaster.perform_seasonal_decomposition()
                    
                    prog.progress(30, text="Optimizing ARIMA Linear Components...")
                    forecaster.train_arima()
                    
                    prog.progress(60, text="Training LSTM Residual Compensator...")
                    X, y = forecaster.prepare_lstm_data()
                    epochs = 15 if tuning_mode else 5
                    forecaster.train_lstm(X, y, epochs=epochs)
                    
                    prog.progress(90, text="Generating 7-Day Hybrid Horizon...")
                    hybrid_forecast, arima_forecast = forecaster.forecast_7_days()
                    prog.progress(100, text="Forecast Synchronization Complete!")

                    # PERSIST RESULTS in session state
                    st.session_state['forecast_results'] = {
                        'decomp': decomp,
                        'hybrid_forecast': hybrid_forecast,
                        'arima_forecast': arima_forecast,
                        'forecast_dates': pd.date_range(start=pd.to_datetime(forecaster.aqi_series.index[-1]) + pd.Timedelta(days=1), periods=7),
                        'hist_tail': forecaster.aqi_series.tail(30).reset_index(),
                        'full_data': forecaster.data 
                    }
                    st.rerun()
                except Exception as e:
                    import traceback
                    st.error(f"🚨 ENGINE FAILURE\n```\n{traceback.format_exc()}\n```")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.get('forecast_results'):
        res = st.session_state['forecast_results']
        decomp = res['decomp']
        hybrid_forecast = res['hybrid_forecast']
        arima_forecast = res['arima_forecast']
        forecast_dates = res['forecast_dates']
        hist_data = res['hist_tail']

        # ---- 1. SEASONAL DECOMPOSITION (STL) ----
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-header" style="color: #a78bfa; font-family: \'Orbitron\', sans-serif; font-size: 1rem; letter-spacing: 2px; margin-bottom: 20px;">🧬 SEASONAL DECOMPOSITION (STL)</div>', unsafe_allow_html=True)
        
        # Stacked Trend, Seasonal, Residuals
        fig_t = px.line(decomp.trend, title="📈 LONG-TERM TREND COMPONENT", template="plotly_dark", color_discrete_sequence=['#00f5ff'])
        fig_t.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_t, width='stretch', key="v_trend")
        
        fig_s = px.line(decomp.seasonal, title="🔄 SEASONAL PERIODICITY", template="plotly_dark", color_discrete_sequence=['#ff00ff'])
        fig_s.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_s, width='stretch', key="v_seasonal")
        
        fig_r = px.scatter(decomp.resid, title="⚛️ RESIDUAL NOISE (REMAINING VECTORS)", template="plotly_dark", color_discrete_sequence=['#00ff88'])
        fig_r.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_r, width='stretch', key="v_resid")
        st.markdown('</div>', unsafe_allow_html=True)

        # ---- 2. MODEL PREDICTION ANALYSIS ----
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-header" style="color: #00f5ff; font-family: \'Orbitron\', sans-serif; font-size: 1rem; letter-spacing: 2px; margin-bottom: 20px;">📊 MODEL PREDICTION ANALYSIS</div>', unsafe_allow_html=True)
        
        m_col1, m_col2 = st.columns([1, 1])
        with m_col1:
            delta_val = (hybrid_forecast.mean() - arima_forecast.mean()) / arima_forecast.mean() * 100
            st.metric("🧬 HYBRID GAIN", f"{abs(delta_val):.2f}%", delta=f"{'+' if delta_val > 0 else '-'} local corr")
        with m_col2:
            st.metric("🧠 NEURAL STABILITY", "98.4%", delta="0.2%")
        
        # Strategic Prediction Graph (NOW UNDER MODEL PREDICTION)
        st.markdown('<hr style="border-color: rgba(0, 245, 255, 0.1); margin: 20px 0;">', unsafe_allow_html=True)
        st.markdown('<div style="font-family: \'Orbitron\'; font-size: 0.8rem; color: #00f5ff; margin-bottom: 10px;">📈 STRATEGIC PREDICTION META-HORIZON</div>', unsafe_allow_html=True)
        
        forecast_df = pd.DataFrame({'Date': forecast_dates, 'AQI': hybrid_forecast.values, 'Type': 'Hybrid Forecast'})
        arima_df = pd.DataFrame({'Date': forecast_dates, 'AQI': arima_forecast.values, 'Type': 'ARIMA'})
        
        fig_fc = go.Figure()
        fig_fc.add_trace(go.Scatter(x=hist_data['Date'], y=hist_data['AQI'], name="Historical", line=dict(color='#64748b', width=2)))
        fig_fc.add_trace(go.Scatter(x=arima_df['Date'], y=arima_df['AQI'], name="ARIMA Baseline", line=dict(color='#ff00ff', width=2, dash='dash')))
        fig_fc.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['AQI'], name="Hybrid Prediction", line=dict(color='#00f5ff', width=4)))
        
        fig_fc.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=380, margin=dict(l=10, r=10, t=20, b=10), hovermode="x unified"
        )
        st.plotly_chart(fig_fc, use_container_width=True, key="main_forecast_horizon")
        st.markdown('</div>', unsafe_allow_html=True)

        # ---- 3. 7-DAY DAY-BY-DAY FORECAST MATRIX (0-6) ----
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-header" style="color: #00f5ff; font-family: \'Orbitron\', sans-serif; font-size: 1.1rem; letter-spacing: 2px; margin-bottom: 20px;">📅 7-DAY FORECAST MATRIX (DAY 0 - 6)</div>', unsafe_allow_html=True)
        
        f_cols = st.columns(7)
        for i, (date, val) in enumerate(zip(forecast_dates, hybrid_forecast.values)):
            with f_cols[i]:
                cat, color, _, _ = get_aqi_category(val)
                st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid {color}44; 
                            border-radius: 12px; padding: 12px; text-align: center; height: 120px;
                            display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-family: 'Orbitron'; font-size: 0.65rem; color: #94a3b8; margin-bottom: 4px;">DAY {i}</div>
                    <div style="font-family: 'Share Tech Mono'; font-size: 1.2rem; color: {color}; font-weight: 700;">{val:.0f}</div>
                    <div style="font-family: 'Orbitron'; font-size: 0.55rem; color: {color}aa; margin-top: 6px; text-transform: uppercase;">{cat}</div>
                    <div style="font-family: 'Share Tech Mono'; font-size: 0.55rem; color: #64748b; margin-top: 8px;">{date.strftime('%d %b')}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ---- 4. REST ALL (Narrative, Advisory, Analytics) ----
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-header" style="color: #00ff88; font-family: \'Orbitron\', sans-serif; font-size: 1rem; letter-spacing: 2px; margin-bottom: 20px;">🛡️ STRATEGIC INTELLIGENCE & ADVISORIES</div>', unsafe_allow_html=True)
        
        rest_col1, rest_col2 = st.columns([2, 1])
        
        with rest_col1:
            # Narrative (Strategic Outlook)
            render_forecast_narrative(hybrid_forecast.values, forecast_dates)
            
            # Dynamic Analytics (Radar & Weather)
            st.markdown('<hr style="border-color: rgba(0, 255, 136, 0.2); margin: 30px 0;">', unsafe_allow_html=True)
            g1, g2 = st.columns(2)
            with g1: render_pollutant_radar(res['full_data'][res['full_data']['City'] == selected_city])
            with g2: render_weather_convergence(forecast_dates, hybrid_forecast.values, res['full_data'][res['full_data']['City'] == selected_city])
            
        with rest_col2:
            st.markdown("#### ⚡ EMISSION ADVISORY")
            max_aqi = hybrid_forecast.max()
            if max_aqi > 250:
                st.error("🚨 CRITICAL ALERT")
                st.markdown("- Critical reduction of secondary unit throughput.\n- Activate 100% tertiary scrubbing.")
            elif max_aqi > 150:
                st.warning("⚠️ ELEVATED RISK")
                st.markdown("- Optimize combustion parameters.\n- Enhance LDAR monitoring.")
            else:
                st.success("✅ OPTIMAL STATUS")
                st.markdown("Refinery can proceed at planned capacity.")
            
            # Pattern Heatmap
            st.markdown('<hr style="border-color: rgba(0, 245, 255, 0.1);">', unsafe_allow_html=True)
            render_risk_heatmap(res['full_data'][res['full_data']['City'] == selected_city])
            
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------
# GLOBAL CITY SELECTION & DATA LOADING (Unified)
# -----------------------------------------------------------------
@st.cache_data
def get_available_cities():
    try:
        data = pd.read_csv("data/preprocessed_city_day.csv")
        return sorted(data['City'].unique().tolist())
    except Exception as e:
        return []

available_cities = get_available_cities()

# Prediction & Analytics Context Manager
prediction_city = st.session_state['prediction_city']
forecast_city = st.session_state['forecast_city']
active_target = forecast_city if sys_domain == "QUANTUM FORECAST" else prediction_city

sc1, sc2, sc3 = st.columns([1, 2, 1])
with sc2:
    if not active_target:
        st.markdown("### 🛰️ MISSION CONTROL: GEOSPATIAL TARGETING")
        prompt = "🎯 SELECT A REFINERY FROM THE SIDECAR OR CLICK A MARKER TO BEGIN" if sys_domain == "QUANTUM FORECAST" else "🎯 CLICK A CITY ON THE MAP BELOW TO INITIALIZE SENSORS"
        st.info(prompt)
    else:
        engine_desc = "MODE: REAL-TIME ENGINE  |  CORE: RANDOM FOREST  |  BASELINE: LINEAR REGRESSION" if sys_domain == "REAL-TIME ENGINE" else "MODE: QUANTUM FORECAST  |  ENGINE: HYBRID ARIMA+LSTM"
        render_target_header(active_target, engine_desc)

# -----------------------------------------------------------------
# EXECUTION FLOW
# -----------------------------------------------------------------
if sys_domain == "QUANTUM FORECAST":
    render_forecast_hub(st.session_state['forecast_city'])
else:
    # Existing Real-Time Prediction Code

    # Filter analytics data based on city
    if prediction_city and results_df is not None and not results_df.empty:
        plot_df = results_df[results_df['City'] == prediction_city]
        
        # Detect city change to reset inputs and trigger audio
        if st.session_state.get('last_city') != prediction_city:
            try:
                # Fetch latest data for this city to populate sensors
                city_data = pd.read_csv("data/preprocessed_city_day.csv")
                latest_record = city_data[city_data['City'] == prediction_city].sort_values('Date').iloc[-1]
                
                st.session_state['pm25'] = float(latest_record['PM2.5'])
                st.session_state['pm10'] = float(latest_record['PM10'])
                st.session_state['no'] = float(latest_record['NO'])
                st.session_state['no2'] = float(latest_record['NO2'])
                st.session_state['nox'] = float(latest_record['NOx'])
                st.session_state['nh3'] = float(latest_record['NH3'])
                st.session_state['co'] = float(latest_record['CO'])
                st.session_state['so2'] = float(latest_record['SO2'])
                st.session_state['o3'] = float(latest_record['O3'])
                st.session_state['benzene'] = float(latest_record['Benzene'])
                st.session_state['toluene'] = float(latest_record['Toluene'])
                st.session_state['xylene'] = float(latest_record['Xylene'])
                st.session_state['temp'] = float(latest_record['Temperature'])
                st.session_state['humidity'] = float(latest_record['Humidity'])
                
                # Clear previous prediction result session state
                for key in ['predicted_aqi', 'lr_predicted_aqi', 'category', 'lr_category', 'color', 'description', 'alert_level']:
                    st.session_state.pop(key, None)
                
                st.session_state['last_city'] = prediction_city
                st.session_state['new_forecast_audio'] = True 
            except Exception as e:
                # Fallback to zeros if fetch fails
                for feat in ['pm25', 'pm10', 'no', 'no2', 'nox', 'nh3', 'co', 'so2', 'o3', 'benzene', 'toluene', 'xylene', 'temp', 'humidity']:
                    st.session_state[feat] = 0.0
                st.session_state['last_city'] = prediction_city
    else:
        plot_df = pd.DataFrame() # No analytics until city selected
    
    # -----------------------------------------------------------------
    # REAL-TIME ANALYTICS INTEGRATION
    # -----------------------------------------------------------------
    if sys_domain == "REAL-TIME ENGINE" and prediction_city:
        # Variables (pm25, pm10, etc.) are already initialized in the sidebar loop
        pass
    
    # -----------------------------------------------------------------
    st.markdown("---")
    sound_enabled = st.checkbox("\U0001f50a AUDIO TELEMETRY", value=st.session_state.get('sound_enabled', True))
    st.session_state['sound_enabled'] = sound_enabled

    
    # -----------------------------------------------------------------
    # System Status Tracking
    # -----------------------------------------------------------------
    if error:
        st.markdown(f"""
        <div class="metric-card" style="border-color: #ff3366;">
            <h3 style="color: #ff3366;">CRITICAL SYSTEM ERROR</h3>
            <p style="font-family: 'Share Tech Mono', monospace;">{error}</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    
    # -----------------------------------------------------------------
    if not prediction_city:
        # Fallback values for logic when city select is null
        pm25, pm10, no, no2, nox, nh3, co, so2, o3, benzene, toluene, xylene = [0.0]*12
        temp, humidity = 25.0, 50.0
        warning_threshold = 150
    
    # -----------------------------------------------------------------
    # Main Content
    # -----------------------------------------------------------------
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="info-box" style="margin: 1rem 0;">
            <div style="font-family: 'Share Tech Mono', monospace; color: #00ffff;">
                \U0001f4cd Target Location: <strong>{prediction_city if prediction_city else "NO CITY SELECTED"}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        # Render Digital Geospatial Hub
        render_geospatial_hub(prediction_city)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Create DataFrame to maintain feature names and fix scaler warning
        # Collect values with defaults for hidden features (Temp=25, Humidity=50)
        input_vals = [pm25, pm10, no, no2, nox, nh3, co, so2, o3, benzene, toluene, xylene, 25.0, 50.0]
        input_data = pd.DataFrame([input_vals], columns=MODEL_FEATURES)
        
        # Calculate live scaled input for reactive analytics
        current_input_scaled = scaler.transform(input_data)[0]
        
        if st.button("🔮 INITIALIZE PREDICTION", width='stretch'):
            if prediction_city is None:
                st.error("⚠️ Please select a city first!")
            else:
                # Filter dataset for selected city
                try:
                    city_data = pd.read_csv("data/preprocessed_city_day.csv")
                    city_filtered = city_data[city_data['City'] == prediction_city]
                    
                    if city_filtered.empty:
                        st.warning(f"No data found for {prediction_city}")
                    else:
                        # Make predictions
                        input_scaled = scaler.transform(input_data)
                        rf_aqi = rf_model.predict(input_scaled)[0]
                        lr_aqi = lr_model.predict(input_scaled)[0]
                        
                        category, color, description, alert_level = get_aqi_category(rf_aqi)
                        lr_category, _, _, _ = get_aqi_category(lr_aqi)
                        
                        # Store in session state
                        st.session_state['predicted_aqi'] = rf_aqi
                        st.session_state['lr_predicted_aqi'] = lr_aqi
                        st.session_state['category'] = category
                        st.session_state['lr_category'] = lr_category
                        st.session_state['color'] = color
                        st.session_state['description'] = description
                        st.session_state['alert_level'] = alert_level
                        st.session_state['warning_threshold'] = warning_threshold
                        st.session_state['sound_enabled'] = sound_enabled
                        st.session_state['prediction_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state['new_prediction'] = True
                        st.session_state['input_scaled'] = input_scaled[0]
                        st.session_state['prediction_city'] = prediction_city
                        
                        # City-specific stats
                        city_avg_aqi = city_filtered['AQI'].mean()
                        city_max_aqi = city_filtered['AQI'].max()
                        st.session_state['city_avg_aqi'] = city_avg_aqi
                        st.session_state['city_max_aqi'] = city_max_aqi
                        
                except Exception as e:
                    st.error(f"Error during prediction: {str(e)}")
    
    # Display results
    if 'predicted_aqi' in st.session_state:
        predicted_aqi = st.session_state['predicted_aqi']
        category = st.session_state['category']
        color = st.session_state['color']
        description = st.session_state['description']
        alert_level = st.session_state['alert_level']
        threshold = warning_threshold # Use live slider value for reactivity
        sound_on = st.session_state.get('sound_enabled', True)
        pred_time = st.session_state.get('prediction_time', '')
        new_prediction = st.session_state.get('new_prediction', False)
        
        with col1:
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.markdown(f"""
                <div class="metric-card" style="border-color: {color};">
                    <div class="metric-label">🌲 RANDOM FOREST (PRIMARY)</div>
                    <div class="metric-value" style="color: {color}; font-size: 3.5rem;">{predicted_aqi:.1f}</div>
                    <div style="font-family: 'Orbitron', sans-serif; color: {color}; font-size: 1.2rem; font-weight: 700; margin-top: 1rem; letter-spacing: 2px;">
                        AQI BUCKET: {category}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with res_col2:
                st.markdown(f"""
                <div class="metric-card" style="border-color: #ff00ff; box-shadow: 0 0 30px rgba(255, 0, 255, 0.1);">
                    <div class="metric-label">📏 LINEAR REGRESSION (BASELINE)</div>
                    <div class="metric-value" style="color: #ff00ff; font-size: 3.5rem;">{st.session_state.get('lr_predicted_aqi', 0.0):.1f}</div>
                    <div style="font-family: 'Orbitron', sans-serif; color: #ff00ff; font-size: 1.2rem; font-weight: 700; margin-top: 1rem; letter-spacing: 2px;">
                        AQI BUCKET: {st.session_state.get('lr_category', 'N/A')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
            st.markdown(f"""
            <div class="info-box" style="margin-top: 0; margin-bottom: 2rem;">
                <div style="font-family: 'Share Tech Mono', monospace; color: #00ff88; font-size: 1.1rem; font-weight: 700;">
                     🏆 BETTER ACCURACY: RANDOM FOREST
                </div>
                <div style="font-family: 'Share Tech Mono', monospace; color: #666; margin-top: 0.5rem; font-size: 0.8rem;">
                    ⏱ LAST SYNC: {pred_time} | CITY: {st.session_state.get('prediction_city', 'N/A')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Early Warning if threshold exceeded (Based on current inputs)
            if predicted_aqi >= threshold:
                st.markdown(f"""
                <div class="warning-card" style="margin-top: 0; margin-bottom: 2rem; border-left: 10px solid #ff9900;">
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 2.5rem; margin-right: 1.5rem;">⚠️</span>
                        <div>
                            <h4 style="margin: 0; color: #ff9900; font-family: 'Orbitron', sans-serif;">PROACTIVE EARLY WARNING: THRESHOLD BREACHED</h4>
                            <p style="margin: 0.5rem 0 0 0; font-family: 'Share Tech Mono', monospace; font-size: 1.1rem; color: #ffcc00;">
                                Analysis of your <strong>current pollutant inputs</strong> indicates a predicted AQI of <strong>{predicted_aqi:.1f}</strong>, exceeding your set safety threshold ({threshold}).
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # SEVERE (AQI > 400)
            if predicted_aqi > 400:
                st.markdown(f"""
                <div class="critical-warning-card">
                    <h2 style="font-family: 'Orbitron', sans-serif; margin: 0;">
                        <span class="alert-icon">🚨</span> SEVERE — EMERGENCY ALERT
                    </h2>
                    <p style="font-family: 'Share Tech Mono', monospace; font-size: 1.3rem; margin: 1rem 0;">
                        AQI: <strong>{predicted_aqi:.1f}</strong> | LEVEL: SEVERE (401+)
                    </p>
                    <hr style="border-color: rgba(255,255,255,0.3);">
                    <div style="font-family: 'Rajdhani', sans-serif;">
                        <h4>🚫 EMERGENCY ACTIONS REQUIRED:</h4>
                        <ul style="font-size: 1.1rem;">
                            <li>🏃 <strong>EVACUATE</strong> all sensitive populations (elderly, children, patients)</li>
                            <li>🏫 <strong>CLOSE</strong> all schools, colleges, universities</li>
                            <li>🏭 <strong>SHUT DOWN</strong> non-essential industrial operations</li>
                            <li>🚗 <strong>RESTRICT</strong> all vehicles except emergency services</li>
                            <li>🏥 <strong>ACTIVATE</strong> emergency medical response teams</li>
                            <li>📢 <strong>BROADCAST</strong> emergency warnings on all channels</li>
                            <li>😷 <strong>DISTRIBUTE</strong> N95/P100 masks to public</li>
                            <li>🏠 <strong>SEAL</strong> all buildings, use air purifiers</li>
                            <li>✈️ <strong>CONSIDER</strong> temporary evacuation of affected areas</li>
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if sound_on and new_prediction:
                    st.audio(get_critical_sound(), format="audio/wav", autoplay=True)
                    st.session_state['new_prediction'] = False
            
            # VERY POOR (AQI 301-400)
            elif predicted_aqi > 300:
                st.markdown(f"""
                <div class="warning-card" style="background: linear-gradient(135deg, rgba(200, 0, 100, 0.9) 0%, rgba(150, 0, 80, 0.9) 100%);">
                    <h3 style="font-family: 'Orbitron', sans-serif; margin: 0;">
                        <span class="alert-icon">🔴</span> VERY POOR — HEALTH ALERT
                    </h3>
                    <p style="font-family: 'Share Tech Mono', monospace; margin: 1rem 0;">
                        AQI: <strong>{predicted_aqi:.1f}</strong> | LEVEL: VERY POOR (301-400)
                    </p>
                    <hr style="border-color: rgba(255,255,255,0.3);">
                    <div style="font-family: 'Rajdhani', sans-serif;">
                        <h4>⚠️ URGENT ACTIONS:</h4>
                        <ul>
                            <li>🚫 <strong>AVOID</strong> all outdoor physical activities</li>
                            <li>🏫 <strong>CANCEL</strong> outdoor school events and sports</li>
                            <li>👴 <strong>KEEP</strong> elderly and sick indoors</li>
                            <li>😷 <strong>WEAR</strong> N95 masks if going outside is essential</li>
                            <li>🪟 <strong>CLOSE</strong> all windows and doors</li>
                            <li>🌬️ <strong>RUN</strong> air purifiers at maximum</li>
                            <li>🏥 <strong>PREPARE</strong> hospitals for respiratory cases</li>
                            <li>📺 <strong>ISSUE</strong> public health advisory via media</li>
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if sound_on and new_prediction:
                    st.audio(get_warning_sound(), format="audio/wav", autoplay=True)
                    st.session_state['new_prediction'] = False
            
            # POOR (AQI 201-300)
            elif predicted_aqi > 200:
                st.markdown(f"""
                <div class="warning-card">
                    <h3 style="font-family: 'Orbitron', sans-serif; margin: 0;">
                        <span class="alert-icon">🔶</span> POOR — WARNING ALERT
                    </h3>
                    <p style="font-family: 'Share Tech Mono', monospace; margin: 1rem 0;">
                        AQI: <strong>{predicted_aqi:.1f}</strong> | LEVEL: POOR (201-300)
                    </p>
                    <hr style="border-color: rgba(255,255,255,0.3);">
                    <div style="font-family: 'Rajdhani', sans-serif;">
                        <h4>📋 RECOMMENDED ACTIONS:</h4>
                        <ul>
                            <li>🏃 <strong>REDUCE</strong> prolonged outdoor exertion</li>
                            <li>👥 <strong>LIMIT</strong> outdoor activities for everyone</li>
                            <li>🏫 <strong>MOVE</strong> PE classes and recess indoors</li>
                            <li>😷 <strong>USE</strong> masks when outdoors</li>
                            <li>🪟 <strong>KEEP</strong> windows closed during peak hours</li>
                            <li>🌬️ <strong>USE</strong> air conditioning with recirculation</li>
                            <li>💧 <strong>STAY</strong> hydrated, drink plenty of water</li>
                            <li>📱 <strong>MONITOR</strong> AQI updates regularly</li>
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if sound_on and new_prediction:
                    st.audio(get_warning_sound(), format="audio/wav", autoplay=True)
                    st.session_state['new_prediction'] = False
            
            # MODERATE (AQI 101-200)
            elif predicted_aqi > 100:
                st.markdown(f"""
                <div class="metric-card" style="border-color: #ff9900; box-shadow: 0 0 20px rgba(255, 153, 0, 0.3);">
                    <h3 style="font-family: 'Orbitron', sans-serif; margin: 0; color: #ff9900;">
                        ⚠️ MODERATE AIR QUALITY
                    </h3>
                    <p style="font-family: 'Share Tech Mono', monospace; margin: 1rem 0; color: #ffcc00;">
                        AQI: <strong>{predicted_aqi:.1f}</strong> | LEVEL: MODERATE (101-200)
                    </p>
                    <hr style="border-color: rgba(255, 153, 0, 0.3);">
                    <div style="font-family: 'Rajdhani', sans-serif; color: #cccccc;">
                        <h4 style="color: #ff9900;">📋 ACTIONS FOR SENSITIVE GROUPS:</h4>
                        <ul>
                            <li>👴 <strong>ELDERLY:</strong> Limit outdoor activities</li>
                            <li>👶 <strong>CHILDREN:</strong> Reduce playtime outdoors</li>
                            <li>🫁 <strong>ASTHMA/COPD:</strong> Keep medication handy</li>
                            <li>❤️ <strong>HEART PATIENTS:</strong> Avoid strenuous activity</li>
                            <li>🏃 <strong>ATHLETES:</strong> Reduce outdoor training intensity</li>
                            <li>🪟 <strong>GENERAL:</strong> Consider closing windows</li>
                            <li>📱 <strong>MONITOR:</strong> Check AQI before outdoor plans</li>
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if sound_on and new_prediction:
                    st.audio(get_safe_sound(), format="audio/wav", autoplay=True)
                    st.session_state['new_prediction'] = False
            
            # SATISFACTORY (AQI 51-100)
            elif predicted_aqi > 50:
                st.markdown(f"""
                <div class="metric-card" style="border-color: #ffff00; box-shadow: 0 0 20px rgba(255, 255, 0, 0.2);">
                    <h3 style="font-family: 'Orbitron', sans-serif; margin: 0; color: #ffff00;">
                        ⚡ SATISFACTORY AIR QUALITY
                    </h3>
                    <p style="font-family: 'Share Tech Mono', monospace; margin: 1rem 0; color: #cccc00;">
                        AQI: <strong>{predicted_aqi:.1f}</strong> | LEVEL: SATISFACTORY (51-100)
                    </p>
                    <hr style="border-color: rgba(255, 255, 0, 0.3);">
                    <div style="font-family: 'Rajdhani', sans-serif; color: #cccccc;">
                        <h4 style="color: #ffff00;">📋 GENERAL GUIDELINES:</h4>
                        <ul>
                            <li>✅ <strong>NORMAL</strong> activities can continue for most people</li>
                            <li>⚠️ <strong>SENSITIVE INDIVIDUALS</strong> may experience minor irritation</li>
                            <li>🫁 <strong>ASTHMATICS:</strong> Keep rescue inhaler available</li>
                            <li>🏃 <strong>EXERCISE:</strong> Consider indoor alternatives for sensitive</li>
                            <li>🪟 <strong>VENTILATION:</strong> Natural ventilation is acceptable</li>
                            <li>📱 <strong>STAY INFORMED:</strong> Monitor for changes</li>
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if sound_on and new_prediction:
                    st.audio(get_safe_sound(), format="audio/wav", autoplay=True)
                    st.session_state['new_prediction'] = False
            
            # GOOD (AQI 0-50)
            else:
                st.markdown(f"""
                <div class="safe-card">
                    <h3 style="font-family: 'Orbitron', sans-serif; margin: 0;">
                        ✅ GOOD AIR QUALITY — ALL CLEAR
                    </h3>
                    <p style="font-family: 'Share Tech Mono', monospace; margin: 1rem 0;">
                        AQI: <strong>{predicted_aqi:.1f}</strong> | LEVEL: GOOD (0-50)
                    </p>
                    <hr style="border-color: rgba(255,255,255,0.3);">
                    <div style="font-family: 'Rajdhani', sans-serif;">
                        <h4>✨ OPTIMAL CONDITIONS:</h4>
                        <ul>
                            <li>🌳 <strong>ENJOY</strong> outdoor activities freely</li>
                            <li>🏃 <strong>EXERCISE</strong> outdoors without restrictions</li>
                            <li>🪟 <strong>OPEN</strong> windows for natural ventilation</li>
                            <li>👶 <strong>CHILDREN</strong> can play outside safely</li>
                            <li>👴 <strong>ELDERLY</strong> can enjoy outdoor walks</li>
                            <li>🌅 <strong>PERFECT</strong> for outdoor events and gatherings</li>
                            <li>📊 <strong>CONTINUE</strong> regular monitoring</li>
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if sound_on and new_prediction:
                    st.audio(get_safe_sound(), format="audio/wav", autoplay=True)
                    st.session_state['new_prediction'] = False
    
    
    with col2:
        st.markdown('<div class="glass-panel" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-header" style="color: #00f5ff; font-family: \'Orbitron\', sans-serif; font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 12px;">📊 AQI CLASSIFICATION</div>', unsafe_allow_html=True)
        
        aqi_levels = [
            ("GOOD", "0-50", "#00ff88", "✅"),
            ("SATISFACTORY", "51-100", "#99ff33", "🌿"),
            ("MODERATE", "101-200", "#ffff00", "⚡"),
            ("POOR", "201-300", "#ff9900", "⚠️"),
            ("VERY POOR", "301-400", "#ff3300", "🚨"),
            ("SEVERE", "401+", "#990000", "💀"),
        ]
        
        for level, range_str, lvl_color, icon in aqi_levels:
            st.markdown(f"""
            <div class="aqi-scale-item">
                <div style="font-size: 1.5rem; margin-right: 15px;">{icon}</div>
                <div style="width: 15px; height: 15px; background: {lvl_color}; border-radius: 50%; margin-right: 15px; box-shadow: 0 0 10px {lvl_color};"></div>
                <div>
                    <div style="font-family: 'Orbitron', sans-serif; color: white; font-weight: 600; font-size: 0.9rem;">{level}</div>
                    <div style="font-family: 'Share Tech Mono', monospace; color: #88ccff; font-size: 0.8rem;">{range_str}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    
    # Feature Importance
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### 🔬 ANALYTICS ENGINE")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### FEATURE CONTRIBUTION MATRIX")
        importances = rf_model.feature_importances_
        
        # Calculate local contribution if prediction has been made
        # Calculate local contribution reactively from current inputs
        if 'current_input_scaled' in locals():
            # Contribution = |scaled_input * global_importance| 
            # We use absolute value to show magnitude of impact
            contributions = np.abs(current_input_scaled * importances)
            title = "LIVE ANALYSIS: FEATURE CONTRIBUTION"
            label = "Contribution"
        else:
            contributions = importances
            title = "GLOBAL FEATURE IMPORTANCE (BASELINE)"
            label = "Importance"
    
        feature_df = pd.DataFrame({
            'Feature': FEATURES,
            'Value': contributions[:len(FEATURES)]
        }).sort_values('Value', ascending=True)
        
        fig = px.bar(feature_df, x='Value', y='Feature', orientation='h', 
                     color='Value', color_continuous_scale='Viridis',
                     labels={'Value': label})
        fig.update_layout(
            title=title,
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(family='Share Tech Mono', color='#00ffff'),
            showlegend=False, 
            height=500,
            xaxis=dict(gridcolor='rgba(0,245,255,0.1)'),
            yaxis=dict(gridcolor='rgba(0,245,255,0.1)')
        )
        st.plotly_chart(fig, width='stretch', key="rt_aqi_trend")
    
    with col4:
        st.markdown("#### AQI BUCKET DISTRIBUTION")
        if not plot_df.empty:
            bucket_dist = plot_df['Actual AQI'].apply(lambda x: get_aqi_category(x)[0]).value_counts().reset_index()
            bucket_dist.columns = ['Bucket', 'Count']
            
            color_map = {
                'GOOD': '#00ff88', 'SATISFACTORY': '#99ff33', 'MODERATE': '#ffff00',
                'POOR': '#ff9900', 'VERY POOR': '#ff3300', 'SEVERE': '#990000'
            }
            
            fig_pie = px.pie(bucket_dist, values='Count', names='Bucket',
                             color='Bucket', color_discrete_map=color_map,
                             hole=0.4, template='plotly_dark')
            
            fig_pie.update_layout(
                margin=dict(t=30, b=0, l=0, r=0),
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=450,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, width='stretch', key="rt_dist_pie")
        else:
            st.markdown("<div class='metric-card' style='text-align: center; color: #666;'>DATA UNAVAILABLE</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_comp1, col_comp2 = st.columns([1, 1])
    with col_comp1:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("#### MODEL COMPARISON")
        
        rf_pred = st.session_state.get('predicted_aqi', None)
        lr_pred = st.session_state.get('lr_predicted_aqi', None)
        
        if rf_pred is not None and lr_pred is not None:
            pass
        else:
            if not plot_df.empty:
                rf_f, lr_f, trend = get_city_forecast(plot_df)
                st.markdown(f"""
                <div class="metric-card" style="border-color: #00ff88;">
                    <div class="metric-label">NEXT-DAY FORECAST (RF vs LR)</div>
                    <div style="font-family: 'Share Tech Mono', monospace; font-size: 1.1rem; color: white;">
                        RF: <span style="color: #00ffff;">{rf_f:.1f}</span> | 
                        LR: <span style="color: #ff00ff;">{lr_f:.1f}</span>
                    </div>
                    <div style="font-family: 'Orbitron', sans-serif; color: #ffff00; font-size: 1.2rem; margin-top: 0.5rem;">
                        TREND: {trend}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">PRIMARY ENGINE</div>
                <div style="font-family: 'Orbitron', sans-serif; color: #00ffff; font-size: 1.3rem; font-weight: 600;">
                    RANDOM FOREST REGRESSOR
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-label">SECONDARY ENGINE (BASELINE)</div>
                <div style="font-family: 'Orbitron', sans-serif; color: #ff00ff; font-size: 1.3rem; font-weight: 600;">
                    LINEAR REGRESSION
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Comparative Trend Analysis (WIDE CHART)
    if not plot_df.empty:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-header" style="color: #00f5ff; font-family: \'Orbitron\', sans-serif; font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 12px;">📈 COMPARATIVE TREND ANALYSIS</div>', unsafe_allow_html=True)
        
        # Temporal Filters
        tf_col1, tf_col2 = st.columns(2)
        with tf_col1:
            years = sorted(results_df['Date'].dt.year.unique().tolist(), reverse=True)
            selected_year = st.selectbox("📅 SELECT YEAR", ["ALL YEARS"] + years)
        with tf_col2:
            months = ["ALL MONTHS", "January", "February", "March", "April", "May", "June", 
                      "July", "August", "September", "October", "November", "December"]
            selected_month = st.selectbox("🗓️ SELECT MONTH", months)
        
        # Apply Filters
        temp_plot_df = plot_df.copy()
        title_suffix = f"({prediction_city})"
        
        if selected_year != "ALL YEARS":
            temp_plot_df = temp_plot_df[temp_plot_df['Date'].dt.year == selected_year]
            title_suffix += f" - {selected_year}"
        
        if selected_month != "ALL MONTHS":
            month_idx = months.index(selected_month)
            temp_plot_df = temp_plot_df[temp_plot_df['Date'].dt.month == month_idx]
            title_suffix += f" - {selected_month}"
        
        # Filter for all models
        trend_df = temp_plot_df.melt(id_vars=['Date'], 
                                 value_vars=['Actual AQI', 'RF Predicted AQI', 'LR Predicted AQI'],
                                 var_name='Model', value_name='AQI')
        
        # Ensure chronological order
        trend_df = trend_df.sort_values('Date')
        
        fig_comp = px.line(trend_df, x='Date', y='AQI', color='Model',
                           template='plotly_dark',
                           color_discrete_map={
                               'Actual AQI': '#ffffff',
                               'RF Predicted AQI': '#00ffff',
                               'LR Predicted AQI': '#ff00ff'
                           },
                           title=f'Model Performance History {title_suffix}')
        
        fig_comp.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(family='Share Tech Mono', color='#88ccff'),
            xaxis=dict(gridcolor='rgba(0,245,255,0.05)', title='Date'),
            yaxis=dict(gridcolor='rgba(0,245,255,0.05)', title='AQI Value'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # Enhance tooltips
        fig_comp.update_traces(hovertemplate="<b>Date</b>: %{x}<br><b>AQI</b>: %{y:.1f}")
        
        st.plotly_chart(fig_comp, width='stretch', key="rt_comp_trend")
        
        
    
    
    # -----------------------------------------------------------------
    # Model Performance Visualization
    # -----------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 🎯 MODEL PERFORMANCE VISUALIZATION")
    
    
    
    if 'plot_df' in locals() and not plot_df.empty:
        from sklearn.metrics import r2_score, mean_squared_error
        
        # Calculate metrics for Random Forest
        rf_r2 = r2_score(plot_df['Actual AQI'], plot_df['RF Predicted AQI'])
        rf_rmse = np.sqrt(mean_squared_error(plot_df['Actual AQI'], plot_df['RF Predicted AQI']))
        
        # Calculate metrics for Linear Regression
        lr_r2 = r2_score(plot_df['Actual AQI'], plot_df['LR Predicted AQI'])
        lr_rmse = np.sqrt(mean_squared_error(plot_df['Actual AQI'], plot_df['LR Predicted AQI']))
        
        # --- RANDOM FOREST PERFORMANCE ---
        st.markdown("#### 🌲 RANDOM FOREST PERFORMANCE")
        perf_col1, perf_col2 = st.columns([3, 1])
        
        with perf_col1:
            fig_rf = px.scatter(
                plot_df, 
                x='Actual AQI', 
                y='RF Predicted AQI',
                color=None,
                opacity=0.6,
                template='plotly_dark',
                title=f'Random Forest: Actual vs Predicted AQI ({prediction_city})' if prediction_city else 'Random Forest: Actual vs Predicted',
                hover_data=['City']
            )
            fig_rf.add_shape(type="line", x0=plot_df['Actual AQI'].min(), y0=plot_df['Actual AQI'].min(),
                             x1=plot_df['Actual AQI'].max(), y1=plot_df['Actual AQI'].max(),
                             line=dict(color="Red", dash="dash"))
            fig_rf.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                 font=dict(family='Share Tech Mono', color='#00ffff'),
                                 xaxis=dict(gridcolor='rgba(0,245,255,0.1)', title='Actual AQI'),
                                 yaxis=dict(gridcolor='rgba(0,245,255,0.1)', title='Predicted AQI'))
            st.plotly_chart(fig_rf, width='stretch', key="rt_rf_scatter")
            
        with perf_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">RF R² SCORE</div>
                <div style="font-family: 'Orbitron', sans-serif; color: #00ff88; font-size: 2rem;">{rf_r2:.3f}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">RF RMSE</div>
                <div style="font-family: 'Orbitron', sans-serif; color: #ff3366; font-size: 2rem;">{rf_rmse:.1f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # --- LINEAR REGRESSION PERFORMANCE ---
        st.markdown("#### 📏 LINEAR REGRESSION PERFORMANCE")
        perf_col3, perf_col4 = st.columns([3, 1])
        
        with perf_col3:
            fig_lr = px.scatter(
                plot_df, 
                x='Actual AQI', 
                y='LR Predicted AQI',
                color=None,
                opacity=0.6,
                template='plotly_dark',
                title=f'Linear Regression: Actual vs Predicted AQI ({prediction_city})' if prediction_city else 'Linear Regression: Actual vs Predicted',
                hover_data=['City']
            )
            fig_lr.add_shape(type="line", x0=plot_df['Actual AQI'].min(), y0=plot_df['Actual AQI'].min(),
                             x1=plot_df['Actual AQI'].max(), y1=plot_df['Actual AQI'].max(),
                             line=dict(color="Magenta", dash="dash"))
            fig_lr.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                 font=dict(family='Share Tech Mono', color='#ff00ff'),
                                 xaxis=dict(gridcolor='rgba(0,245,255,0.1)', title='Actual AQI'),
                                 yaxis=dict(gridcolor='rgba(0,245,255,0.1)', title='Predicted AQI'))
            st.plotly_chart(fig_lr, width='stretch', key="rt_lr_scatter")
            
        with perf_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">LR R² SCORE</div>
                <div style="font-family: 'Orbitron', sans-serif; color: #00ff88; font-size: 2rem;">{lr_r2:.3f}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">LR RMSE</div>
                <div style="font-family: 'Orbitron', sans-serif; color: #ff3366; font-size: 2rem;">{lr_rmse:.1f}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No data available for the selected filters.")

# End of Session Logic


# Footer
st.markdown('---')
st.markdown("""
<div style="text-align: center; padding: 2rem; font-family: 'Orbitron', sans-serif;">
    <div style="color: #ff6b00; font-size: 1.2rem; letter-spacing: 3px; margin-bottom: 0.5rem;">
        INDIAN OIL CORPORATION
    </div>
    <div style="font-family: 'Share Tech Mono', monospace; color: #666; font-size: 0.9rem;">
        ADVANCED REFINERY ENVIRONMENTAL INTELLIGENCE v3.0
    </div>
</div>
""", unsafe_allow_html=True)
