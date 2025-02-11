# -*- coding: utf-8 -*-
"""Data cleaning (step 1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/153mAdfPNOmxfyHBunAgj2M2NC_Lka_E3
"""

import pandas as pd

import re


df = pd.read_csv(r"C:\Users\GANGAVARAM MAHAMMAD .LAPTOP-KRMM4FVO\Downloads\goibibo_flights_data.csv)

df

import pandas as pd
import re

# Step 1: Drop unnecessary columns
columns_to_drop = ["Unnamed: 11", "Unnamed: 12"]
df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

# Step 2: Convert 'flight date' to datetime format and extract features
df.rename(columns={"flight date": "flight_date"}, inplace=True)
df["flight_date"] = pd.to_datetime(df["flight_date"], format="%d-%m-%Y")

# Extract date, month, and year
df["date"] = df["flight_date"].dt.day
df["month"] = df["flight_date"].dt.month
df["year"] = df["flight_date"].dt.year

# Step 3: Convert price column to numeric format if necessary
if df["price"].dtype == "object":
    df["price"] = df["price"].str.replace(",", "").astype(int)

# Step 4: Clean and convert 'duration' to total minutes
def clean_duration(duration):
    match = re.search(r"(\d{1,2})\.?\d{0,2}?h?\s?(\d{1,2})?m?", duration)
    if match:
        h = int(match.group(1)) if match.group(1) else 0
        m = int(match.group(2)) if match.group(2) else 0
        return h * 60 + m
    return None  # Return None if format is invalid

if "duration" in df.columns:
    df["duration_minutes"] = df["duration"].apply(clean_duration)
    df.drop(columns=["duration"], inplace=True)

# Step 5: Convert 'stops' to numerical format
import pandas as pd
import re

# Function to clean the 'stops' column
def clean_stops(value):
    value = str(value).strip()  # Remove leading/trailing spaces
    value = re.sub(r"\s*Via.*", "", value)  # Remove 'Via' and extra text
    return value

# Apply cleaning function
df["stops"] = df["stops"].apply(clean_stops)

# Convert 'stops' to numerical format
df["stops"] = df["stops"].replace({"non-stop": 0, "1-stop": 1, "2+-stop": 2}).fillna(1).astype(int)


# Step 6: Rename columns for clarity
new_column_names = {
    "flight_date": "Flight Date",
    "airline": "Airline",
    "flight_num": "Flight Number",
    "class": "Class",
    "origin": "Origin",
    "destination": "Destination",
    "dep_time": "Departure Time",
    "arr_time": "Arrival Time",
    "price": "Price (₹)",
    "stops": "Number of Stops",
    "date": "Date",
    "month": "Month",
    "year": "Year",
    "duration_minutes": "Duration (Minutes)",
    "day_of_week": "Day"
}
df.rename(columns=new_column_names, inplace=True)

# Display cleaned dataset
print(df.head())  # Display the first few rows of the cleaned dataset

# Save the updated CSV file
df.to_csv("updated_flight_data.csv", index=False)

print("CSV file with renamed columns has been saved as 'updated_flight_data.csv'.")

df.columns

d = pd.read_csv(r"C:\Users\GANGAVARAM MAHAMMAD .LAPTOP-KRMM4FVO\Downloads\Flights123\updated_flight_dataset.csv")

d.columns
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# Load cleaned dataset
df = pd.read_csv(r"C:\Users\GANGAVARAM MAHAMMAD .LAPTOP-KRMM4FVO\Downloads\Flights123\updated_flight_dataset.csv")

# Select features (independent variables)
features = ["Airline", "Origin", "Destination", "Number of Stops", "Class", "Duration (Minutes)"]
target = "Price (₹)"  # Dependent variable

# One-Hot Encoding for categorical variables
df_encoded = pd.get_dummies(df[features], drop_first=True)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(df_encoded, df[target], test_size=0.2, random_state=42)

print("✅ Data Preprocessing Complete! Ready for Model Training.")
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Initialize models
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
}

# Train and evaluate models
results = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Compute evaluation metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    results[name] = {"MAE": mae, "RMSE": rmse, "R² Score": r2}

# Display model results
results_df = pd.DataFrame(results).T
print("✅ Model Training Complete! Results:")
print(results_df)
from sklearn.model_selection import GridSearchCV

# Define parameter grid for Random Forest
param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [None, 10, 20],
    "min_samples_split": [2, 5, 10]
}

# Perform GridSearchCV
grid_search = GridSearchCV(RandomForestRegressor(random_state=42), param_grid, cv=5, scoring="neg_mean_absolute_error", n_jobs=-1)
grid_search.fit(X_train, y_train)

# Best parameters
print("✅ Best Hyperparameters:", grid_search.best_params_)

# Train the best model
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

# Final Evaluation
final_mae = mean_absolute_error(y_test, y_pred)
final_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
final_r2 = r2_score(y_test, y_pred)

print(f"🎯 Final Model Performance: MAE = {final_mae:.2f}, RMSE = {final_rmse:.2f}, R² Score = {final_r2:.2f}")
import joblib

# Save the best model found by GridSearchCV
joblib.dump(best_model, 'flight_price_model.pkl')

print("✅ Model saved successfully as flight_price_model.pkl")
