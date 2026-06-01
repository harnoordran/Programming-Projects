import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Load the preprocessed data
data = pd.read_csv("data/preprocessed_city_day.csv")

# Identify target and features
FEATURES = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene']
X = data[FEATURES]
y = data['AQI']

# Load the existing scaler
scaler = joblib.load("scaler.joblib")

# Scale the data
X_scaled = scaler.transform(X)

# -------------------------------------------------
# Linear Regression Model
# -------------------------------------------------
lr = LinearRegression()
lr.fit(X_scaled, y)

# Predictions on the same data for quick check
y_pred = lr.predict(X_scaled)

# Evaluation
rmse = np.sqrt(mean_squared_error(y, y_pred))
r2 = r2_score(y, y_pred)
print("\nLinear Regression Evaluation (on whole training set)")
print(f"RMSE: {rmse:.3f}")
print(f"R^2: {r2:.3f}")

# Save the model
joblib.dump(lr, "lr_model.joblib")
print("Model saved to lr_model.joblib")
