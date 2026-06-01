import sys
import os
import pandas as pd
import numpy as np
import warnings
import torch

# Disable warnings
warnings.filterwarnings('ignore')

# Add current directory to path
sys.path.append(os.getcwd())

from forecasting_engine import HybridAQIForecaster

def test_engine():
    city = "Guwahati"
    print(f"--- INITIALIZING DIAGNOSTIC FOR {city} ---")
    
    try:
        # 1. Initialization
        forecaster = HybridAQIForecaster(city)
        print("[1/5] Forecaster Object Created.")
        
        # 2. Data Loading
        df = forecaster.load_and_preprocess()
        print(f"[2/5] Data Loaded. Shape: {df.shape}")
        
        # 3. Seasonal Decomposition
        decomp = forecaster.perform_seasonal_decomposition()
        print("[3/5] STL Decomposition Successful.")
        
        # 4. Training Sample (Very small epochs for speed)
        # Note: We simulate a very small subset of data if needed, 
        # but here we'll just run 1 epoch on the whole set if possible.
        print("[4/5] Testing Model Pipeline (ARIMA + LSTM)...")
        forecaster.train_arima()
        X, y = forecaster.prepare_lstm_data()
        
        # Check if torch can run
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"      - PyTorch Device: {device}")
        
        forecaster.train_lstm(X, y, epochs=1) # 1 epoch for verification
        print("      - Training cycle complete.")
        
        # 5. Forecasting
        hybrid, arima = forecaster.forecast_7_days()
        print(f"[5/5] 7-Day Horizon Generated. Mean Hybrid AQI: {hybrid.mean():.2f}")
        
        print("\n✅ DIAGNOSTIC RESULT: ALL SYSTEMS NOMINAL")
        return True
    except Exception as e:
        print(f"\n❌ DIAGNOSTIC FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_engine()
    sys.exit(0 if success else 1)
