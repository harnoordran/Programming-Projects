# Indian Oil Corporation - AQI Prediction & Forecasting System

An advanced Mission Control UI designed for proactive environmental monitoring and emission management at Indian Oil Corporation (IOCL) refinery zones.

## 🧠 Advanced Architecture: The 9-Stage Intelligence Pipeline

The system operates on a rigorous 9-stage data processing and predictive pipeline, ensuring maximum accuracy for refinery-grade environmental monitoring:

1.  **Sensor Data Ingestion**: Aggregating real-time pollutant vectors (PM2.5, NO2, SO2, etc.).
2.  **Multivariate Preprocessing**: Robust data cleaning and city-wise random imputation for missing telemetry.
3.  **Environmental Sensor Synthesis**: Fusing raw pollutant data with meteorological variables (Temperature, Humidity).
4.  **STL Decomposition**: Deep-dive statistical breakdown separating complex timelines into **Long-Term Trends**, **Seasonal Periodicity**, and **Residual Noise**.
5.  **Diagnostic Modeling**: Dual-path analysis using **Random Forest** and **Linear Regression** for instant AQI validation.
6.  **Quantum Forecast Matrix**: 7-day temporal projection using the **Hybrid ARIMA-LSTM** trajectory.
7.  **Neural Residual Learning**: Utilizing deep learning to capture non-linear residuals missed by traditional statistical methods.
8.  **Strategic Intelligence Matrix**: Generating actionable emission advisories and 7-day outlooks.
9.  **Mission Control Visualization**: Real-time HUD with chemical radar charts, temporal heatmaps, and audio telemetry.

## 🚀 Key Features
- **Mission Cockpit UI**: A premium glassmorphism dashboard with dynamic strategic sky backgrounds and neural data sparks.
- **Quantum Forecast Engine**: A state-of-the-art Hybrid ARIMA-LSTM engine providing high-precision 7-day AQI forecasts.
- **STL Analytics**: Advanced Seasonal-Trend decomposition using LOESS for deep atmospheric insight.
- **Audio Telemetry**: Real-time holographic audio alerts (Safe, Warning, Critical) for immediate situational awareness.
- **Geospatial Monitoring**: Integrated monitoring for all major IOCL refinery zones and cities across India.
- **Strategic Decision Support**: Automated emission advisories and strategic outlooks for proactive management.

## 🛠️ Tech Stack
- **Frontend**: Streamlit (Advanced Glassmorphism UI)
- **Deep Learning**: PyTorch (LSTM Residual Learning)
- **Statistical Modeling**: Statsmodels (ARIMA, STL Decomposition), Pmdarima
- **Machine Learning**: Scikit-learn (Random Forest, Linear Regression, Scalers)
- **Visualization**: Plotly (Radar Charts, Heatmaps, Overlay Trends)
- **Data Engine**: Pandas, NumPy, Joblib

## 📦 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/dsingla3be24/Indian-Oil-Corporation-AQI-Prediction-Forecasting-System.git
   cd Indian-Oil-Corporation-AQI-Prediction-Forecasting-System
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage
To launch the Mission Control dashboard:
```bash
streamlit run app.py
```

---
*Developed for Indian Oil Corporation — Advancing Environmental Excellence through AI.*
