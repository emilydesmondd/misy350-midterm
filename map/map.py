import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import json
from pathlib import Path
from datetime import datetime
import uuid
import time


geolocator = Nominatim(user_agent="fun_map")

st.title(f'Budget-friendly College Life Map!')

user_location = st.text_input("Enter city or town (e.g., 'Newark, DE') to find nearby fun spots:")

default_center = [39.7392, -104.9903]
m = folium.Map(location=default_center, zoom_start=5)

if user_location:
    location = geolocator.geocode(user_location)

    if location:
        lat = location.latitude
        lon = location.longitude

        m = folium.Map(location=[lat, lon], zoom_start=10)

        folium.Marker(
            [lat, lon],
            popup=f"You searched: {user_location}",
            tooltip="Your location"
        ).add_to(m)
    else:
        st.warning("Couldn't find that location. Try adding state (e.g., 'Hockessin, DE').")

folium.Marker(
    [39.7392, -104.9903],
    popup="Night Life Spot",
    tooltip="Click for more info"
).add_to(m)

st_folium(m, width=700)

with st.sidebar:
    st.title("Your Favorites")
    if st.session_state["logged_in"] and st.session_state["user"] is not None:
        st.write(f"Logged in as: {st.session_state['user']['username']}")
    else:
        st.write("Not logged in.")

if st.session_state['role'] == "Admin":
    st.sidebar.title("Admin Panel")
    st.sidebar.write("Here you can manage users and content.")

if st.session_state['role'] == "College Student":
    st.sidebar.title("College Student Resources")
    st.sidebar.write("Check out these budget-friendly spots near you!")

if st.session_state['role'] == "Other":
    st.sidebar.title("Area Resources")
    st.sidebar.write("Explore fun and affordable activities for all ages!")


if st.button('Log Out'):
    with st.spinner("Logging out..."):
        time.sleep(5)
    st.session_state['logged_in'] = False
    st.session_state['user'] = None
    st.session_state['role'] = None
    st.success("Logged out successfully!")
    st.rerun()