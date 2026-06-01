import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Load the preprocessed data
data = pd.read_csv("data/preprocessed_city_day.csv")

# Identify target and features
# The dataset still contains City and Date, we drop them for training
# We also drop AQI_Bucket as it is a classification target
FEATURES = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene']
X = data[FEATURES]
y = data['AQI']

# print(data.info())
# print(data.isnull().sum())

# print(X,y)

# CO-RELATION MATRIX(Optional)
# plt.figure(figsize=(10,8))
# sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
# plt.title("Correlation Matrix")
# plt.show()


#20% will be the test data
#80% will be the trained data

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#In order to prevent larger values getting higher importance, we use a scaling method.
#Standardization is the method used. Linear Regressing requires scaling





scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print(X_train)
# -------------------------------------------------
# Random Forest Regressor
# -------------------------------------------------
rf = RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

# Evaluation
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
print("\nRandom Forest Evaluation")
print(f"RMSE: {rmse:.3f}")
print(f"R^2: {r2:.3f}")

# Save the model and scaler
joblib.dump(rf, "rf_model.joblib")
joblib.dump(scaler, "scaler.joblib")
print("Model saved to rf_model.joblib")
print("Scaler saved to scaler.joblib")

# -------------------------------------------------
# Early Warning & Helper Functions
# -------------------------------------------------

# Define an AQI threshold for an early warning (e.g., 150 = Unhealthy)
AQI_WARNING_THRESHOLD = 150

# Function to check predictions and emit warnings
def check_early_warning(predictions, threshold=AQI_WARNING_THRESHOLD):
    """Print a warning for any predicted AQI values above the threshold.

    Args:
        predictions (array‑like): Predicted AQI values.
        threshold (float): AQI value above which a warning is issued.
    """
    high_indices = [i for i, val in enumerate(predictions) if val > threshold]
    if high_indices:
        print(f"\n⚠️  Early Warning: {len(high_indices)} prediction(s) exceed the AQI threshold of {threshold}.")
        for i in high_indices:
            print(f"  - Sample {i}: predicted AQI = {predictions[i]:.2f}")
    else:
        print("\n✅  All predicted AQI values are below the warning threshold.")

# Run the early‑warning check on the current test predictions
check_early_warning(y_pred)

# -----------------------------------------------------------------
# Utility to predict AQI on a new dataset using the saved model & scaler
# -----------------------------------------------------------------
import os
from pathlib import Path

def predict_aqi(new_csv_path: str, model_path: str = "rf_model.joblib", scaler_path: str = "scaler.joblib"):
    """Load a saved Random Forest model and scaler, predict AQI for a new CSV.

    Parameters
    ----------
    new_csv_path : str
        Path to a CSV file with the same feature columns as the training data (excluding AQI).
    model_path : str, optional
        Path to the saved Random Forest model (default: "rf_model.joblib").
    scaler_path : str, optional
        Path to the saved StandardScaler (default: "scaler.joblib").
    """
    # Verify files exist
    if not Path(new_csv_path).is_file():
        raise FileNotFoundError(f"Input CSV not found: {new_csv_path}")
    if not Path(model_path).is_file() or not Path(scaler_path).is_file():
        raise FileNotFoundError("Saved model or scaler not found. Ensure you have run the training script first.")

    # Load data
    new_data = pd.read_csv(new_csv_path)
    # Drop columns that were removed during training
    for col in ["City", "Date", "AQI_Bucket"]:
        if col in new_data.columns:
            new_data = new_data.drop(columns=[col])
    # Fill missing values: Since this is for new predictions, we could use mean from training 
    # but for simplicity if we must fill, we'll follow a similar random logic if possible, 
    # or just use 0 if sampling isn't feasible without training-time stats.
    # However, for prediction, usually mean is safer. But let's round the input data.
    new_data = new_data.round(2)
    # Filter columns to only those the model expects
    X_new = new_data.drop(columns=["AQI"], errors="ignore")
    # Handle any remaining NaNs with 0 for robustness in prediction
    X_new = X_new.fillna(0)
    # Load scaler and model
    loaded_scaler = joblib.load(scaler_path)
    loaded_model = joblib.load(model_path)
    # Scale and predict
    X_new_scaled = loaded_scaler.transform(X_new)
    predictions = loaded_model.predict(X_new_scaled)
    # Output results
    print(f"\nPredictions for {len(predictions)} samples from {new_csv_path}:")
    for i, pred in enumerate(predictions[:10]):  # show first 10 predictions
        print(f"  Sample {i}: AQI = {pred:.2f}")
    if len(predictions) > 10:
        print(f"  ... (and {len(predictions)-10} more)")
    # Run early‑warning check on the new predictions
    check_early_warning(predictions)
    return predictions

# Example usage (uncomment to run with a new file)
# predict_aqi("data/new_city_day.csv")
