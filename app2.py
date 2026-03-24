import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config(page_title="Hangout Map", layout="centered")

json_file = Path("users.json")
json_location = Path("location.json")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'user' not in st.session_state:
    st.session_state['user'] = None

if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

if 'role' not in st.session_state:
    st.session_state['role'] = None

if json_file.exists():
    with open(json_file, "r") as f:
        users = json.load(f)
else:
    users = [
        {
            "id": "1",
            "email": "emdesmo@udel.edu",
            "username": "System Admin",
            "password": "testing123",
            "role": "Admin"
        }
    ]
    with open(json_file, "w") as f:
        json.dump(users, f, indent=4)

if json_location.exists():
    with open(json_location, "r") as f:
        saved_locations = json.load(f)
else:
    saved_locations = []
    with open(json_location, "w") as f:
        json.dump(saved_locations, f, indent=4)

st.markdown("<h1 style='text-align: center;'>Budget-Friendly Map</h1>", unsafe_allow_html=True)

# top buttons before login
if not st.session_state["logged_in"]:
    left_space, center_area, right_space = st.columns([1, 2, 1])

    with center_area:
        st.write("")
        button_col1, button_col2 = st.columns(2)

        with button_col1:
            if st.button("Login", use_container_width=True):
                st.session_state["page"] = "login"
                st.rerun()

        with button_col2:
            if st.button("Register", use_container_width=True):
                st.session_state["page"] = "register"
                st.rerun()

# sidebar only after login
if st.session_state["logged_in"]:
    st.sidebar.title("Navigation")

    if st.sidebar.button("Map"):
        st.session_state["page"] = "map"
        st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.session_state["role"] = None
        st.session_state["page"] = "login"
        st.rerun()

# register page
if st.session_state["page"] == "register" and not st.session_state["logged_in"]:
    left_space, center_area, right_space = st.columns([1, 2, 1])

    with center_area:
        st.header("Create an Account")

        email = st.text_input("Email Address", key="register_email")
        user_name = st.text_input("Username", key="register_username")
        password = st.text_input("Password", type="password", key="register_password")
        role = st.selectbox(
            "Role",
            ["College Student", "High-School Student", "Other"],
            key="register_role"
        )

        if st.button("Create Account"):
            if not email or not user_name or not password:
                st.error("Please fill out all fields.")
            else:
                email_exists = any(
                    user["email"].strip().lower() == email.strip().lower()
                    for user in users
                )

                if email_exists:
                    st.error("An account with this email already exists.")
                else:
                    with st.spinner("Creating your account..."):
                        time.sleep(2)

                        new_user = {
                            "id": str(uuid.uuid4()),
                            "email": email,
                            "username": user_name,
                            "password": password,
                            "role": role,
                            "registered_at": str(datetime.now())
                        }

                        users.append(new_user)

                        with open(json_file, "w") as f:
                            json.dump(users, f, indent=4)

                    st.success("Account created successfully!")
                    st.session_state["page"] = "login"
                    st.rerun()

# login page
elif st.session_state["page"] == "login" and not st.session_state["logged_in"]:
    left_space, center_area, right_space = st.columns([1, 2, 1])

    with center_area:
        st.header("Login")

        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Log In"):
            with st.spinner("Verifying credentials..."):
                time.sleep(2)

                matched_user = None
                for user in users:
                    if user["email"].strip().lower() == login_email.strip().lower() and user["password"] == login_password:
                        matched_user = user
                        break

                if matched_user:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = matched_user
                    st.session_state["role"] = matched_user["role"]
                    st.session_state["page"] = "map"
                    st.success(f"Welcome back, {matched_user['username']}!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

# map page
elif st.session_state["page"] == "map" and st.session_state["logged_in"]:
    st.header("Hangout Map")

    geolocator = Nominatim(user_agent="my_app")

    place = st.text_input("Enter a location", key="map_place")

    if place:
        geo_location = geolocator.geocode(place)
        marker_name = st.text_input("Enter a saved marker name", key="map_marker_name")

        if geo_location:
            m = folium.Map(location=[geo_location.latitude, geo_location.longitude], zoom_start=13)

            folium.Marker(
                [geo_location.latitude, geo_location.longitude],
                popup=place,
                tooltip="Search Location"
            ).add_to(m)

            for loc in saved_locations:
                if "lat" in loc and "lon" in loc:
                    folium.Marker(
                    [loc["lat"], loc["lon"]],
                    popup=loc["name"],
                    tooltip=loc["name"]
                    ).add_to(m)

            st_folium(m, width=700, height=500)

            if st.button("Save Location"):
                new_location = {
                    "name": marker_name if marker_name else place,
                    "lat": geo_location.latitude,
                    "lon": geo_location.longitude
                }

                saved_locations.append(new_location)

                with open(json_location, "w") as f:
                    json.dump(saved_locations, f, indent=4)

                st.success("Location saved!")
                st.rerun()

        else:
            st.error("Location not found")

    if saved_locations:
        st.subheader("Saved Locations")
        st.dataframe(saved_locations)
    else:
        st.write("No saved locations yet.")