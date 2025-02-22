# -*- coding: utf-8 -*-
"""model training.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19Y8tUJf_BASBUYLqBMaZE56jQQC_H4Al
"""

# Reload necessary libraries
import pandas as pd

# Load the dataset
file_path = r"C:\Users\GANGAVARAM MAHAMMAD .LAPTOP-KRMM4FVO\Downloads\newupdated_flight_data.csv"
df = pd.read_csv(file_path)

# Display basic information and first few rows
df.info(), df.head()



import pandas as pd
import joblib
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load the dataset
df = pd.read_csv(r"C:\Users\GANGAVARAM MAHAMMAD .LAPTOP-KRMM4FVO\Downloads\Flights123\updated_flight_dataset.csv")

# Feature selection
features = ["Airline", "Class", "Origin", "Destination", "Number of Stops", "Date", "Month", "Year", "Duration (Minutes)"]
target = "Price (₹)"

# Encoding categorical variables
categorical_cols = ["Airline", "Class", "Origin", "Destination"]
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Store encoders

# Splitting dataset
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and encoders
joblib.dump(model, "flight_price_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")

# Evaluate model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Model Performance: MAE={mae}, MSE={mse}, R2={r2}")

# Streamlit App for Deployment
st.title("Flight Price Prediction")

# User input
airline = st.selectbox("Airline", df["Airline"].unique())
flight_class = st.selectbox("Class", df["Class"].unique())
origin = st.selectbox("Origin", df["Origin"].unique())
destination = st.selectbox("Destination", df["Destination"].unique())
stops = st.number_input("Number of Stops", min_value=0, max_value=5, step=1)
date = st.number_input("Date", min_value=1, max_value=31, step=1)
month = st.number_input("Month", min_value=1, max_value=12, step=1)
year = st.number_input("Year", min_value=2023, max_value=2030, step=1)
duration = st.number_input("Duration (Minutes)", min_value=0, step=1)

# Handle unseen labels
def encode_label(encoder, value):
    return encoder.transform([value])[0] if value in encoder.classes_ else 0

input_data = pd.DataFrame({
    "Airline": [encode_label(label_encoders["Airline"], airline)],
    "Class": [encode_label(label_encoders["Class"], flight_class)],
    "Origin": [encode_label(label_encoders["Origin"], origin)],
    "Destination": [encode_label(label_encoders["Destination"], destination)],
    "Number of Stops": [stops],
    "Date": [date],
    "Month": [month],
    "Year": [year],
    "Duration (Minutes)": [duration]
})

if st.button("Predict Price"):
    model = joblib.load("flight_price_model.pkl")
    predicted_price = model.predict(input_data)[0]
    st.success(f"Predicted Flight Price: ₹{predicted_price:.2f}")

