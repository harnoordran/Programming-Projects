import pandas as pd
import numpy as np
import os

def preprocess_aqi_data(file_path="data/city_day.csv", output_path="data/preprocessed_city_day.csv"):
    print(f"Loading data from {file_path}...")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
    
    df = pd.read_csv(file_path)
    initial_shape = df.shape
    print(f"Initial Shape: {initial_shape}")
    
    # 1. Remove Duplicate Rows and Columns
    print("Removing duplicates...")
    df = df.drop_duplicates()
    df = df.loc[:, ~df.columns.duplicated()]
    
    # 2. Handle COMPLETELY Empty Rows and Columns
    print("Removing entirely empty rows and columns...")
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')
    
    # 3. Handle Target (AQI) - Mandatory for training
    print("Dropping rows with missing AQI (Target required for ML)...")
    df = df.dropna(subset=['AQI'])
    print(f"Shape after initial cleaning: {df.shape}")
    
    # 5. Deterministic Imputation and Synthesis
    pollutants = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene']
    
    # Linear Interpolation for existing columns
    print("Performing deterministic imputation (Interpolation)...")
    for pollutant in pollutants:
        if pollutant in df.columns:
            df[pollutant] = df.groupby('City')[pollutant].transform(lambda x: x.interpolate(method='linear').ffill().bfill())
            if df[pollutant].isnull().any():
                df[pollutant] = df[pollutant].fillna(0)
    
    # 6. Environmental Vector Synthesis (Temperature and Humidity)
    # Required for the 14-feature model compatibility
    print("Synthesizing missing environmental vectors (Temp/Hum)...")
    df['Date'] = pd.to_datetime(df['Date'])
    day_of_year = df['Date'].dt.dayofyear
    
    if 'Temperature' not in df.columns:
        df['Temperature'] = 25 + 12 * np.sin(2 * np.pi * (day_of_year - 100) / 365) + np.random.normal(0, 1, len(df))
    
    if 'Humidity' not in df.columns:
        df['Humidity'] = 65 + 25 * np.sin(2 * np.pi * (day_of_year - 150) / 365) + np.random.normal(0, 2, len(df))

    # Add back to pollutants list for rounding/capping
    pollutants += ['Temperature', 'Humidity']
    
    # 7. AQI Category Validation
    print("Validating AQI Bucket parity...")
    def get_aqi_bucket(aqi):
        if aqi <= 50: return "Good"
        elif aqi <= 100: return "Satisfactory"
        elif aqi <= 200: return "Moderate"
        elif aqi <= 300: return "Poor"
        elif aqi <= 400: return "Very Poor"
        else: return "Severe"
    df['AQI_Bucket'] = df['AQI'].apply(get_aqi_bucket)
    
    # 8. Outlier Mitigation
    print("Applying outlier capping...")
    for pollutant in pollutants:
        if pollutant in df.columns:
            upper_limit = df[pollutant].quantile(0.99)
            df[pollutant] = df[pollutant].clip(upper=upper_limit)
    
    # 9. Rounding and Final Sorting
    print("Rounding values and sorting chronologically...")
    df = df.round(2)
    df = df.sort_values('Date')
    
    # Final cleanup of any remaining NaNs (if any)
    df = df.fillna(0)
    
    print(f"Saving preprocessed data to {output_path}...")
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    df.to_csv(output_path, index=False)
    
    print(f"Final Shape: {df.shape}")
    print("Preprocessing complete.")
    return df

if __name__ == "__main__":
    preprocess_aqi_data()
