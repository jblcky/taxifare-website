import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# --- Streamlit App ---
st.set_page_config(page_title="Taxi Fare Predictor", layout="centered")

st.title("🚖 Taxi Fare Predictor")
st.write("Enter the ride details below to predict fare:")

# --- Input Fields ---
pickup_datetime = st.date_input(
    "Pickup Date",
    value=datetime.now().date()
)
pickup_time = st.time_input(
    "Pickup Time",
    value=datetime.now().time()
)
pickup_datetime_str = f"{pickup_datetime} {pickup_time}"

pickup_longitude = st.number_input(
    "Pickup Longitude",
    value=-73.985428,
    format="%.6f"
)
pickup_latitude = st.number_input(
    "Pickup Latitude",
    value=40.748817,
    format="%.6f"
)
dropoff_longitude = st.number_input(
    "Dropoff Longitude",
    value=-73.985428,
    format="%.6f"
)
dropoff_latitude = st.number_input(
    "Dropoff Latitude",
    value=40.748817,
    format="%.6f"
)
passenger_count = st.number_input(
    "Passenger Count",
    min_value=1, max_value=10, value=1
)

# --- Display Inputs ---
st.subheader("Your Ride Details")

params={
    "pickup_datetime": pickup_datetime_str,
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}

# --- Show Map ---
st.subheader("Pickup & Dropoff Locations")
map_data = pd.DataFrame([
    {"lat": pickup_latitude, "lon": pickup_longitude, "type": "Pickup"},
    {"lat": dropoff_latitude, "lon": dropoff_longitude, "type": "Dropoff"}
])
st.map(map_data[['lat', 'lon']])

# Optional: show markers with more info
st.write("Pickup is the first point (blue), Dropoff is the second point (red).")

# --- Predict Button ---
if st.button("Predict Fare"):
    try:
        url = 'https://newtaxifare-1096775302336.europe-west1.run.app/predict'
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an error if the request failed
        prediction = response.json()
        st.success(f"Predicted Fare: ${prediction['fare']:.2f}")
    except Exception as e:
        st.error(f"Error calling prediction API: {e}")
