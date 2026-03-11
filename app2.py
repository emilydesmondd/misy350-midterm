import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

json_file = Path("users.json")
with st.sidebar:
    st.title("Budget-Friendly Map Login")
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


st.title("Budget-Friendly Map Login")

page = st.sidebar.radio("Choose a page", ["Register", "Login"])

if page == "Register":
    st.subheader("Create an Account!")

    with st.container():
        email = st.text_input("Email Address")
        user_name = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["College Student", "High-School Student", "Other"])

        if st.button("Create Account"):
            if not email or not user_name or not password:
                st.error("Please fill out all fields.")
            else:
                email_exists = any(user["email"].strip().lower() == email.strip().lower() for user in users)

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

elif page == "Login":
    st.subheader("Login")

    with st.container():
        login_email = st.text_input("Email")
        login_password = st.text_input("Password", type="password")

        if st.button("Log In"):
            with st.spinner("Verifying credentials..."):
                time.sleep(2)

                matched_user = None
                for user in users:
                    if user["email"].strip().lower() == login_email.strip().lower() and user["password"] == login_password:
                        matched_user = user
                        break

                if matched_user:
                    st.session_state['logged_in'] = True
                    st.session_state['user'] = matched_user
                    st.session_state['role'] = matched_user['role']
                    st.success(f"Welcome back, {matched_user['username']}!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")



geolocator = Nominatim(user_agent="fun_map")

st.title("Budget-friendly College Life Map!")

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