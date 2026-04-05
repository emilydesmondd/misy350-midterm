import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config(page_title='Network Manager', page_icon=':globe_with_meridians:', layout='centered')

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

connection_requests = [
    {
        "request_id": "011101",
        "status": "Pending",
        "student_email": "emdesmo@udel.edu",
        "student_name": "Emily Desmond",
        "student_school": "University of Delaware",
        "student_major": "Management Information Systems",
        "notes": "I would love to hear about your experience in the tech industry and any advice you have for someone starting out.",
    }
]

json_users = Path("users.json")
if json_users.exists() and json_users.stat().st_size > 0:
    with open(json_users, "r") as f:
        users = json.load(f)

json_advisors = Path("advisors.json")
if json_advisors.exists() and json_advisors.stat().st_size > 0:
    with json_advisors.open("r", encoding= "utf-8") as f:
        advisors = json.load(f)

json_connections = Path("connection_request.json")
if json_connections.exists() and json_connections.stat().st_size > 0:
    with json_connections.open("r", encoding= "utf-8") as f:
        connection_requests = json.load(f)



#============ Advisor Home Page ============
if st.session_state["role"] == "Advisor":

    if st.session_state["page"] == "advisor_home_page":
        st.markdown("This is the Advisor Home Page")
        st.markdown(f'### Welcome, {st.session_state["user"]["full_name"]}!')


    elif st.session_state["page"] == "advisor_dashboard":
        st.markdown('### Network!')

        tab1, tab2, tab3 = st.tabs(['Students', 'Events', 'option'])
        with tab1:
            st.header("Student Connection Requests")
            st.markdown("This is where advisors can review student connection requests.")
            col1, col2, col3 = st.columns([3, 2, 2])

            with col1:
                st.markdown("## Submitted Requests")

            with col2:
                with st.container(border=True):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("Count")
                    with c2:
                        st.markdown(f"## {len(connection_requests)}")

            with col3:
                with st.container(border=True):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"Pending")
                    with c2:
                        pending = 0
                        for request in connection_requests:
                            if request["status"].strip().lower() == "pending":
                                pending += 1
                        st.markdown(f"## {pending}")

            with st.container(border=True):
                col1, col2 = st.columns([4, 2])

                with col1:
                    search_item = st.text_input("Search by Student Email", key="search_txt_by_email")

                with col2:
                    status_options = ["All", "Pending", "Approved", "Rejected"]
                    selected_status = st.selectbox("Status", status_options, key="selected_status_filter")

            filtered_requests = connection_requests

            if search_item:
                filtered_requests = [
                    request for request in filtered_requests
                    if search_item.lower() in request["student_email"].lower()
                ]
            if selected_status != "All":
                filtered_requests = [
                    request for request in filtered_requests
                    if request["status"].strip().lower() == selected_status.lower()
                ]
            col1, col2 = st.columns([4, 2])
            selected_request = None

            with col1:
                event = st.dataframe(
                filtered_requests,
                on_select="rerun",
                selection_mode="single-row",
                use_container_width=True
                )

                if event.selection.rows:
                    selected_index = event.selection.rows[0]
                    selected_request = filtered_requests[selected_index]

            with col2:
                with st.container(border=True):
                    st.markdown("### Request Details")

                    if selected_request:
                        with st.container(border=True):
                            st.markdown(f"**Status:** {selected_request['status']}")
                            st.markdown(f"**Student Name:** {selected_request['student_name']}")
                            st.markdown(f"**Student Email:** {selected_request['student_email']}")
                            st.markdown(f"**School:** {selected_request['student_school']}")
                            st.markdown(f"**Major:** {selected_request['student_major']}")
                            st.markdown(f"**Notes:** {selected_request['notes']}")

                        if selected_request["status"].strip().lower() == "pending":
                            advisor_note = st.text_area(
                            "Advisor Note (optional)",
                            key="advisor_note_textbox",
                            height=100
                        )

                            decision = st.radio(
                            "Decision",
                            ["Approved", "Rejected"],
                            key="decision_radio"
                        )

                            if st.button(
                            "Record Decision",
                            key="record_decision_btn",
                            type="primary",
                            use_container_width=True
                        ):
                                for request in connection_requests:
                                    if request["request_id"] == selected_request["request_id"]:
                                        request["status"] = decision
                                        request["advisor_note"] = advisor_note
                                        break

                            with open(json_connections, "w") as f:
                                json.dump(connection_requests, f, indent=4)

                                st.success("Decision recorded.")
                                time.sleep(2)
                                st.rerun()
                    else:
                        st.info("Select a request to view details.")
        with tab2:
            st.subheader("Manage Connections")
        with tab3:
            st.subheader("Option")
            st.markdown("Under Construction")


#============ Student Home Page ============
elif st.session_state["role"] == "Student":

    if st.session_state["page"] == "student_home_page":

        st.markdown(f'### Welcome, {st.session_state["user"]["full_name"]}!')

        #profile page view ur major, school, name, email, etc. and then button to go to dashboard where they can see their network and add connections




#============ Student Dashboard ============
    elif st.session_state["page"] == 'student_dashboard':
        st.markdown('### Here is your Network!')

        tab1, tab2 = st.tabs(['Add Connections', 'Manage Connections'])
        with tab1:
            st.subheader("Request a Connection")
            st.markdown("Send a networking request to an advisor.")

            advisor_options = [f"{advisor['full_name']} - {advisor['company']}" for advisor in advisors]
            selected_advisor = st.selectbox("Choose an Advisor", advisor_options)

            student_name = st.text_input("Your Name")
            student_email = st.text_input("Your Email")
            student_school = st.text_input("School")
            student_major = st.text_input("Major")
            notes = st.text_area("Message to Advisor", height=120)

            if st.button("Submit Request", type="primary", use_container_width=True):
                if not student_name or not student_email or not notes:
                    st.warning("Please fill out all required fields.")
                else:
                    advisor_name = selected_advisor.split(" - ")[0]
                    advisor_company = selected_advisor.split(" - ")[1]
                new_request = {
                "request_id": str(uuid.uuid4()),
                "status": "Pending",
                "advisor_name": advisor_name,
                "advisor_company": advisor_company,
                "student_email": student_email,
                "student_name": student_name,
                "student_school": student_school,
                "student_major": student_major,
                "notes": notes,
                "advisor_note": ""
            }

                connection_requests.append(new_request)

                with open(json_connections, "w") as f:
                    json.dump(connection_requests, f, indent=4)

                st.success("Request sent!")
                time.sleep(2)
                st.rerun()


        with tab2:
            st.subheader("Manage Connections")
            st.subheader("Manage Connections")

            advisor_tochange = None
            selected_index = None

            event = st.dataframe(advisors,
            on_select="rerun",
            selection_mode="single-row",
            use_container_width=True,
            key="manage_connections_table"
            )

            if event.selection.rows:
                selected_index = event.selection.rows[0]
                advisor_tochange = advisors[selected_index]

            if advisor_tochange is not None:
                edit_name = st.text_input("Full Name", value=advisor_tochange.get("full_name", ""),
                key="edit_full_name")
                edit_email = st.text_input("Email", value=advisor_tochange.get("email", ""),
                key="edit_email")
                edit_company = st.text_input("Company", value=advisor_tochange.get("company", ""),
                key="edit_company")
                edit_position = st.text_input("Position", value=advisor_tochange.get("position", ""),
                key="edit_position")

                update_btn = st.button("Update Connection",
                key=f"btn_update_{selected_index}",
                use_container_width=True,
                type="primary")

                if update_btn:
                    advisor_tochange["full_name"] = edit_name
                    advisor_tochange["email"] = edit_email
                    advisor_tochange["company"] = edit_company
                    advisor_tochange["position"] = edit_position

                    with json_advisors.open("w", encoding="utf-8") as f:
                        json.dump(advisors, f, indent=4)

                    st.success("Connection is updated!")
                    st.rerun()

            else:
                st.info("Select a connection to edit.")

#============ Student AI Email Helper ============
    elif st.session_state["page"] == "AI_email_helper":
        st.markdown("### AI Email Helper")
        st.markdown("This is where students can get help drafting emails to advisors.")
        st.markdown("Under Construction")


#================Sign Up Screen =================
elif st.session_state["page"] == "signup":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2: 
        st.header("Network Manager :globe_with_meridians:")
    st.divider()
        
    st.subheader("Create an Account")

    with st.container(border=True):

                full_name_signup = st.text_input("Full Name", key = "full_name_signup")

                email_signup = st.text_input("Email Address", key = "email_signup")

                password_signup = st.text_input("Password", type="password", key = "password_signup")

                role_signup = st.selectbox("Role", ["Student", "Advisor"], key="role_signup")
        
                if st.button("Create Account", type="primary",use_container_width=True):
                    st.session_state["logged_in"]= True
                    st.session_state["user"] = {
                        "id": str(uuid.uuid4()),
                        "email": email_signup,
                        "full_name": full_name_signup,
                        "password": password_signup,
                        "role": role_signup 
                    }
                    st.session_state["role"] = role_signup
                    users.append(st.session_state["user"])  
                    with open(json_users, "w") as f:
                        json.dump(users, f, indent=4)
                    with st.spinner("Creating account..."):
                        time.sleep(2)
                    st.success(f"Account created! Welcome, {full_name_signup}!")

                    st.session_state["page"] = "student_home_page" if role_signup == "Student" else "advisor_home_page"
                    st.rerun()


                if st.button("Have an Account? Log In", type="secondary", use_container_width=True):
                    st.session_state["page"] = "login"
                    st.rerun()


#================Log In Screen =================
else:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2: st.header("Network Manager :globe_with_meridians:")

    st.divider()

    left_spacer, center_column, right_spacer = st.columns([1, 2, 1])
    with center_column:
            st.subheader("Log In")
            with st.container(border=True, width=600):
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
                
                        if found_user and found_user["role"] == "Student":
                            st.success(f"Welcome back, {found_user['email']}!")
                            st.session_state["logged_in"]= True
                            st.session_state["user"] = found_user
                            st.session_state["role"] = found_user['role']
                            st.session_state["page"] = "student_home_page"
                            time.sleep(2)
                            st.rerun()

                        elif found_user and found_user["role"] == "Advisor":
                            st.success(f"Welcome back, {found_user['email']}!")
                            st.session_state["logged_in"]= True
                            st.session_state["user"] = found_user
                            st.session_state["role"] = found_user['role']
                            st.session_state["page"] = "advisor_home_page"
                            time.sleep(2)
                            st.rerun()

                        else:
                            st.error("Invalid email or password. Please try again.")

                if st.button("Don't have an account? Sign Up", type="secondary", use_container_width=True):
                    st.session_state["page"] = "signup"
                    st.rerun()


#================Page Navigation in Sidebar =================
if st.session_state["logged_in"]:
    with st.sidebar:
        st.markdown("### Move From Page to Page")
        if st.session_state["role"] == "Student":

            if st.button("Home", key="home_btn"):
                st.session_state["page"] = "student_home_page"
                st.rerun()

            if st.button("Dashboard", key="dash_btn"):
                st.session_state["page"] = "student_dashboard"
                st.rerun()

            if st.button("AI Email Helper", key="ai_btn"):
                st.session_state["page"] = "AI_email_helper"
                st.rerun()

            if st.button("Log Out", key="logout_btn"):
                with st.spinner("logging out..."):
                    time.sleep(4)
                    st.session_state["logged_in"] = False
                    st.session_state["user"] = None
                    st.session_state["role"] = None
                    st.rerun()


        if st.session_state["role"] == "Advisor":

            if st.button("Home", key="home_btn_2"):
                st.session_state["page"] = "advisor_home_page"
                st.rerun()

            if st.button("Dashboard", key="dash_btn_2"):
                st.session_state["page"] = "advisor_dashboard"
                st.rerun()

            if st.button("Log Out", key="logout_btn_2"):
                with st.spinner("logging out..."):
                    time.sleep(4)
                    st.session_state["logged_in"] = False
                    st.session_state["user"] = None
                    st.session_state["role"] = None
                    st.rerun()