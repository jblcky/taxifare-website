import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
from datetime import datetime
import requests


# --- Streamlit App ---
st.set_page_config(page_title="Taxi Fare Predictor", layout="centered")

st.title("🚖 Taxi Fare Predictor")
# st.write("Enter the ride details below to predict fare:")

# --- Initialize session state for pickup/dropoff ---
if "pickup" not in st.session_state:
    st.session_state.pickup = {"lat": 40.748817, "lon": -73.985428}
if "dropoff" not in st.session_state:
    st.session_state.dropoff = {"lat": 40.748817, "lon": -73.985428}
if "selecting" not in st.session_state:
    st.session_state.selecting = "pickup"  # toggle between pickup and dropoff

# --- Map for selecting points ---
m = folium.Map(location=[40.748817, -73.985428], zoom_start=12)
folium.Marker([st.session_state.pickup["lat"], st.session_state.pickup["lon"]],
              tooltip="Pickup", icon=folium.Icon(color="green")).add_to(m)
folium.Marker([st.session_state.dropoff["lat"], st.session_state.dropoff["lon"]],
              tooltip="Dropoff", icon=folium.Icon(color="red")).add_to(m)


st.write("Select point type:")
point_type = st.radio("Choose point to set on map:", ["Pickup", "Dropoff"])

st.write("Click on the map to set the location:")


# Render map with click
map_data = st_folium(m, width=700, height=500, returned_objects=["last_clicked"])

if map_data["last_clicked"]:
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    if point_type == "Pickup":
        st.session_state.pickup = {"lat": lat, "lon": lon}
    else:
        st.session_state.dropoff = {"lat": lat, "lon": lon}

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

pickup_latitude = st.session_state.pickup["lat"]
pickup_longitude = st.session_state.pickup["lon"]
dropoff_latitude = st.session_state.dropoff["lat"]
dropoff_longitude = st.session_state.dropoff["lon"]

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
# st.subheader("Pickup & Dropoff Locations")
# map_data = pd.DataFrame([
#     {"lat": pickup_latitude, "lon": pickup_longitude, "type": "Pickup"},
#     {"lat": dropoff_latitude, "lon": dropoff_longitude, "type": "Dropoff"}
# ])
# st.map(map_data[['lat', 'lon']])

# Optional: show markers with more info
# st.write("Pickup is the first point (blue), Dropoff is the second point (red).")

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
