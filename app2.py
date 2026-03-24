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

st.title("Budget-Friendly Map")
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

st.markdown(f"Budget-Friendly Map Login")

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



