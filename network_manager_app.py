import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config(page_title='Network Manager', page_icon=':globe_with_meridians:', layout='centered')
st.title('Network Manager')

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    
if 'user' not in st.session_state:
    st.session_state['user'] = None

if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

if 'role' not in st.session_state:
    st.session_state['role'] = None

users = [
        {
        'id': '1',
        'email': 'emdesmo@udel.edu',
        'full_name': 'Emily Desmond',
        'password': 'testing123',
        'role': 'Student',
    }
]

advisors = [
    {
        'full_name' : 'Joe Doe',
        'email' : 'joedoe@udel.edu',
        'company' : 'Tech Solutions',
        'position' : 'Senior Software Engineer'
    },
]

students = [
    {
        'id' : '1',
        'full_name' : 'Emily Desmond',
        'email' : 'emdesmo@udel.edu',
        'school' : 'University of Delaware',
        'major' : 'Management Information Systems'
    },
]

json_users = Path("users.json")
if json_users.exists() and json_users.stat().st_size > 0:
    with open(json_users, "r") as f:
        users = json.load(f)

json_advisors = Path("advisors.json")
if json_advisors.exists() and json_advisors.stat().st_size > 0:
    with json_advisors.open("r", encoding= "utf-8") as f:
        advisors = json.load(f)

json_students = Path("students.json")
if json_students.exists() and json_students.stat().st_size > 0:
    with json_students.open("r", encoding= "utf-8") as f:
        students = json.load(f)

#============ Advisor Dashboard ============
if st.session_state["role"] == "Advisor":
    st.markdown("This is the Advisor Dashboard")
    if st.session_state["page"] == "advisor_home_page":
        st.markdown(f'### Welcome, {st.session_state["user"]["full_name"]}!')
        if st.button("Go to Dashboard", type="primary", key='dash_btn'):
            st.session_state['page'] = 'advisor_dashboard'
            st.rerun()




    elif st.session_state["page"] == "advisor_dashboard":
        st.markdown('### Network!')

    tab1, tab2, tab3 = st.tabs(['Students', 'Events', 'option'])
    with tab1:
        st.subheader("Students")
        st.markdown("This is where the student connections will be displayed!")

        st.dataframe(students)

        if st.button("Add Student", type="primary", use_container_width=True):
            st.text_input("Full Name", key = "student_name")
            st.text_input("Email", key = "student_email")
            st.text_input("School", key = "student_school")
            st.text_input("Major", key = "student_major")
            if st.button("Save Connection", type="primary", use_container_width=True):
                new_student = {
                    "id" : str(uuid.uuid4()),
                    "full_name" : st.session_state["student_name"],
                    "email" : st.session_state["student_email"],
                    "school" : st.session_state["student_school"],
                    "major" : st.session_state["student_major"]
                }
                students.append(new_student)
                with open(json_students, "w", encoding="utf-8") as f:
                    json.dump(students, f, indent=4)
                st.success("Connection saved successfully!")
                st.time.sleep(4)
                st.rerun()

    with tab2:
        st.subheader("Manage Connections")
    with tab3:
        st.subheader("Option")
        st.markdown("Under Construction")

#============ Student Dashboard ============
elif st.session_state["role"] == "Student":
    st.markdown("This is the Student Dashboard")
    if st.session_state["page"] == "student_home_page":
        st.markdown(f'### Welcome, {st.session_state["user"]["full_name"]}!')
        if st.button("Go to Dashboard", type="primary", key='dash_btn'):
            st.session_state['page'] = 'student_dashboard'
            st.rerun()
            with st.container():
                st.markdown("This is where the student dashboard content will go!")




    elif st.session_state["page"] == 'student_dashboard':
        st.markdown('### Here is your Network!')

    tab1, tab2, tab3 = st.tabs(['Add Connections', 'Manage Connections', 'AI Email Helper'])
    with tab1:
        st.subheader("Add Connections")

        st.dataframe(advisors)
                         
        with st.expander("Add New Connection"):
            st.text_input("Full Name", key="connection_name")
            st.text_input("Email", key="connection_email")
            st.text_input("Company", key="connection_company")
            st.text_input("Position", key="connection_position")
        if st.button("Save Connection", type="primary", use_container_width=True):
            new_advisor = {
                "full_name": st.session_state["connection_name"],
                "email": st.session_state["connection_email"],
                "company": st.session_state["connection_company"],
                "position": st.session_state["connection_position"]
            }

            advisors.append(new_advisor)

            with open(json_advisors, "w", encoding="utf-8") as f:
                json.dump(advisors, f, indent=4)

            st.success("Connection saved successfully!")
            st.rerun()
    with tab2:
        st.subheader("Manage Connections")

        edited_connections = []
        for person in advisors:
            edited_connections.append(person["full_name"])

        with st.container(border=True):
            selected_item = st.selectbox(
            "Select an item",
            edited_connections,
            label_visibility="collapsed"
        )

        advisor_tochange = {}
        for person in advisors:
            if person["full_name"] == selected_item:
                advisor_tochange = person
                break

        if advisor_tochange:
            edit_name = st.text_input(
            "Full Name",
            value=advisor_tochange["full_name"],
            key=f"edit_name_{advisor_tochange['full_name']}"
        )
        edit_email = st.text_input(
            "Email",
            value=advisor_tochange["email"],
            key=f"edit_email_{advisor_tochange['full_name']}"
        )
        edit_company = st.text_input(
            "Company",
            value=advisor_tochange["company"],
            key=f"edit_company_{advisor_tochange['full_name']}"
        )
        edit_position = st.text_input(
            "Position",
            value=advisor_tochange["position"],
            key=f"edit_position_{advisor_tochange['full_name']}"
        )

        update_btn = st.button(
            "Update Connection",
            key=f"btn_update_{advisor_tochange['full_name']}",
            use_container_width=True,
            type="primary"
        )

        if update_btn:
            with st.spinner("Updating the connection..."):
                time.sleep(2)
                advisor_tochange["full_name"] = edit_name
                advisor_tochange["email"] = edit_email
                advisor_tochange["company"] = edit_company
                advisor_tochange["position"] = edit_position

            with json_advisors.open("w", encoding="utf-8") as f:
                json.dump(advisors, f, indent=4)

            st.success("Connection is updated!")
            time.sleep(2)
            st.rerun()

        elif st.session_state["page"] == 'student_dashboard':
            st.markdown('### Here is your Network!')
    with tab3:
        st.subheader("AI Email Helper")
        st.markdown("This is where the AI Email Helper will go!")

else:
    st.subheader("Log In")
    with st.container(border=True):
        email_input = st.text_input("Email Address", key = "email_login")
        password_input = st.text_input("Password", type="password", key = "password")
        
        if st.button("Log In", type="primary",use_container_width=True):
            with st.spinner("Logging in..."):
                time.sleep(2)
                
                
                found_user = None
                for user in users:
                    if user["email"].strip().lower() == email_input.strip().lower() and user["password"] == password_input:
                        found_user = user
                        break
                
                if found_user:
                    st.success(f"Welcome back, {found_user['email']}!")
                    st.session_state["logged_in"]= True
                    st.session_state["user"] = found_user
                    st.session_state["role"] = found_user['role']
                    st.session_state["page"] = "home"
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Invalid email or password. Please try again.")






#============ Log Out ============
    if st.button("Log Out"):
        with st.spinner("logging out..."):
            time.sleep(4)
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.rerun()