import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import joblib
import os
from pmdarima import auto_arima
import warnings

warnings.filterwarnings('ignore')

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

class HybridAQIForecaster:
    def __init__(self, city_name, refinery_name="IOCL Refinery"):
        self.city_name = city_name
        self.refinery_name = refinery_name
        self.scaler = MinMaxScaler()
        self.model_lstm = None
        self.arima_order = None
        self.decomposition = None
        self.data = None
        self.aqi_series = None
        
    def load_and_preprocess(self, file_path="data/preprocessed_city_day.csv"):
        df = pd.read_csv(file_path)
        city_df = df[df['City'] == self.city_name].copy()
        city_df['Date'] = pd.to_datetime(city_df['Date'])
        city_df = city_df.sort_values('Date')
        
        # Interpolate requires DatetimeIndex for method='time'
        city_df = city_df.set_index('Date')
        
        city_df['AQI'] = city_df['AQI'].interpolate(method='time').ffill().bfill()
        
        # 5. Synthesis of missing environmental vectors (Temperature/Humidity)
        # Required for the 14-feature model compatibility
        if 'Temperature' not in city_df.columns:
            day_of_year = city_df.index.dayofyear
            # Basic seasonal synthesis (Peak temp around day 150-200)
            city_df['Temperature'] = 25 + 12 * np.sin(2 * np.pi * (day_of_year - 100) / 365) + np.random.normal(0, 1, len(city_df))
        
        if 'Humidity' not in city_df.columns:
            day_of_year = city_df.index.dayofyear
            # Humid peaks in monsoon (around day 200-250)
            city_df['Humidity'] = 65 + 25 * np.sin(2 * np.pi * (day_of_year - 150) / 365) + np.random.normal(0, 2, len(city_df))

        # Keep a version with standard index for some features if needed, 
        # but the class logic mostly uses the index-based data now.
        self.data = city_df.reset_index()
        self.aqi_series = city_df['AQI']
        return self.data

    def perform_seasonal_decomposition(self):
        series_resampled = self.aqi_series.asfreq('D').ffill()
        self.decomposition = STL(series_resampled, period=365).fit()
        return self.decomposition

    def train_arima(self):
        print(f"Optimizing ARIMA for {self.city_name}...")
        stepwise_fit = auto_arima(self.aqi_series, start_p=1, start_q=1,
                                 max_p=3, max_q=3, m=12,
                                 start_P=0, seasonal=True,
                                 d=None, D=1, trace=False,
                                 error_action='ignore',  
                                 suppress_warnings=True, 
                                 stepwise=True)
        
        self.arima_order = stepwise_fit.order
        self.arima_seasonal_order = stepwise_fit.seasonal_order
        self.model_arima = ARIMA(self.aqi_series, order=self.arima_order, seasonal_order=self.arima_seasonal_order).fit()
        return self.model_arima

    def prepare_lstm_data(self, look_back=30):
        arima_preds = self.model_arima.fittedvalues
        residuals = self.aqi_series - arima_preds
        
        features = ['PM2.5', 'PM10', 'NO2', 'CO', 'SO2', 'O3']
        feature_data = self.data[features].values
        
        combined_data = np.column_stack((residuals.values, feature_data))
        scaled_data = self.scaler.fit_transform(combined_data)
        
        X, y = [], []
        for i in range(len(scaled_data) - look_back):
            X.append(scaled_data[i:(i + look_back), :])
            y.append(scaled_data[i + look_back, 0])
            
        return np.array(X), np.array(y)

    def train_lstm(self, X, y, epochs=10, batch_size=32):
        print(f"Training PyTorch LSTM for {self.city_name} residuals...")
        X_tensor = torch.from_numpy(X).float().to(device)
        y_tensor = torch.from_numpy(y).float().to(device).view(-1, 1)
        
        dataset = TensorDataset(X_tensor, y_tensor)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        model = LSTMModel(input_size=X.shape[2], hidden_size=64, num_layers=2, output_size=1).to(device)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        criterion = nn.MSELoss()
        
        model.train()
        for epoch in range(epochs):
            for batch_X, batch_y in dataloader:
                optimizer.zero_grad()
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                
        self.model_lstm = model
        return model

    def forecast_7_days(self):
        arima_forecast = self.model_arima.forecast(steps=7)
        
        look_back = 30
        last_X, _ = self.prepare_lstm_data(look_back=look_back)
        curr_X = torch.from_numpy(last_X[-1:]).float().to(device)
        
        self.model_lstm.eval()
        lstm_residuals = []
        with torch.no_grad():
            for _ in range(7):
                pred_res = self.model_lstm(curr_X)
                lstm_residuals.append(pred_res.item())
                
                # Update curr_X
                new_row = curr_X[0, -1, :].clone()
                new_row[0] = pred_res.item()
                # Slide window
                curr_X = torch.cat((curr_X[:, 1:, :], new_row.unsqueeze(0).unsqueeze(0)), dim=1)
                
        dummy = np.zeros((7, 7))
        dummy[:, 0] = lstm_residuals
        final_residuals = self.scaler.inverse_transform(dummy)[:, 0]
        
        hybrid_forecast = arima_forecast + final_residuals
        return hybrid_forecast, arima_forecast

if __name__ == "__main__":
    forecaster = HybridAQIForecaster("Guwahati")
    forecaster.load_and_preprocess()
    forecaster.perform_seasonal_decomposition()
    forecaster.train_arima()
    X, y = forecaster.prepare_lstm_data()
    forecaster.train_lstm(X, y, epochs=2)
    hybrid, arima = forecaster.forecast_7_days()
    print("7-Day Hybrid Forecast (PyTorch):", hybrid.values)
