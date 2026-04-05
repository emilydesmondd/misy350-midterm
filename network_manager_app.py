import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time
import re

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
        "advisor_email": "joedoe@udel.edu",
        "advisor_name": "Joe Doe",
        "student_email": "emdesmo@udel.edu",
        "student_name": "Emily Desmond",
        "student_school": "University of Delaware",
        "student_major": "Management Information Systems",
        "notes": "I would love to hear about your experience in the tech industry and any advice you have for someone starting out.",
        "advisor_note": ""
    }
]

profile = []

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

json_profile = Path("profile.json")
if json_profile.exists() and json_profile.stat().st_size > 0:
    with json_profile.open("r", encoding= "utf-8") as f:
        profile = json.load(f)

#============ Advisor Home Page ============
if st.session_state["role"] == "Advisor":

    if st.session_state["page"] == "advisor_home_page":
        st.markdown("This is the Advisor Home Page")
        st.markdown(f'### Welcome, {st.session_state["user"]["full_name"]}!')


    elif st.session_state["page"] == "advisor_dashboard":
        st.markdown('### Network!')

        view_connections = []


        tab1, tab2, tab3 = st.tabs(['Students', 'Events', 'Option'])

        with tab1:
            st.header("Student Connection Requests")
            st.markdown("This is where advisors can review student connection requests.")

            view_connections = [
                request for request in connection_requests
                if request.get("advisor_email", "").strip().lower()
                == st.session_state["user"]["email"].strip().lower()
            ]

            col1, col2, col3 = st.columns([3, 1.5, 1.5])

            with col1:
                st.markdown("## Submitted Requests")

            with col2:
                with st.container(border=True):
                    st.markdown("Count")
                    st.markdown(f"### {len(view_connections)}")

            with col3:
                with st.container(border=True):
                    pending_count = sum(
                        1 for request in view_connections
                        if request.get("status", "").strip().lower() == "pending"
                    )
                    st.markdown("Pending")
                    st.markdown(f"### {pending_count}")

            st.divider()

            with st.container(border=True):
                filter_col1, filter_col2 = st.columns([4, 2])

                with filter_col1:
                    search_item = st.text_input(
                        "Search by Student Email",
                        key="search_txt_by_email"
                    )

                with filter_col2:
                    selected_status = st.selectbox(
                        "Status",
                        ["All", "Pending", "Approved", "Rejected"],
                        key="selected_status_filter"
                    )

            filtered_requests = view_connections.copy()

            if search_item:
                filtered_requests = [
                    request for request in filtered_requests
                    if search_item.lower() in request.get("student_email", "").lower()
                ]

            if selected_status != "All":
                filtered_requests = [
                    request for request in filtered_requests
                    if request.get("status", "").strip().lower() == selected_status.lower()
                ]

            display_requests = [
                {
                    "Status": request.get("status", ""),
                    "Student Name": request.get("student_name", ""),
                    "Student Email": request.get("student_email", ""),
                    "School": request.get("student_school", ""),
                    "Major": request.get("student_major", "")
                }
                for request in filtered_requests
            ]

            table_col, details_col = st.columns([4, 2])
            selected_request = None

            with table_col:
                event = st.dataframe(
                    display_requests,
                    on_select="rerun",
                    selection_mode="single-row",
                    use_container_width=True,
                    key="advisor_requests_table"
                )

                if event.selection.rows:
                    selected_index = event.selection.rows[0]
                    selected_request = filtered_requests[selected_index]

            with details_col:
                with st.container(border=True):
                    st.markdown("### Request Details")

                    if selected_request is not None:
                        st.markdown(f"**Status:** {selected_request.get('status', '')}")
                        st.markdown(f"**Student Name:** {selected_request.get('student_name', '')}")
                        st.markdown(f"**Student Email:** {selected_request.get('student_email', '')}")
                        st.markdown(f"**School:** {selected_request.get('student_school', '')}")
                        st.markdown(f"**Major:** {selected_request.get('student_major', '')}")
                        st.markdown(f"**Notes:** {selected_request.get('notes', '')}")

                        if selected_request.get("status", "").strip().lower() == "pending":
                            st.divider()

                            advisor_note = st.text_area(
                                "Advisor Note (optional)",
                                key=f"advisor_note_{selected_request['request_id']}",
                                height=100
                            )

                            decision = st.radio(
                                "Decision",
                                ["Approved", "Rejected"],
                                key=f"decision_{selected_request['request_id']}"
                            )

                            if st.button(
                                "Record Decision",
                                key=f"record_decision_{selected_request['request_id']}",
                                type="primary",
                                use_container_width=True
                            ):
                                for request in connection_requests:
                                    if request["request_id"] == selected_request["request_id"]:
                                        request["status"] = decision
                                        request["advisor_note"] = advisor_note
                                        break

                                with open(json_connections, "w", encoding="utf-8") as f:
                                    json.dump(connection_requests, f, indent=4)

                                st.success("Decision recorded.")
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

        st.header(f'Welcome, {st.session_state["user"]["full_name"]}!')
        st.subheader("Your Network")
        st.divider()

        pending = []
    
        for request in connection_requests:

            if request["status"].strip().lower() == "pending" and request["student_email"].strip().lower() == st.session_state["user"]["email"].strip().lower():

                pending.append = [
                    {"Status": request["status"],
                    "Advisor": request.get("advisor_name", ""),
                    "Company": request.get("advisor_company", ""),}]
        for prof in profile:
            if prof["profile_email"].strip().lower() == st.session_state["user"]["email"].strip().lower():
                col1, col2 = st.columns([3, 2])
                with col1:
                    st.markdown("## Pending Requests")
                    st.dataframe(pending, use_container_width=True)
                with col2:
                    with st.container(border=True, horizontal=False):
                        st.markdown(f"**Name:** {prof.get('profile_full_name','')}")
                        st.markdown(f"**Email:** {prof.get('profile_email','')}")
                        st.markdown(f"**Major:** {prof.get('profile_major','')}")
                        st.markdown(f"**School:** {prof.get('profile_school','')}")
                        st.markdown(f"**Grad Year:** {prof.get('profile_grad_year','')}")

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
                    if not full_name_signup or not email_signup or not password_signup:
                        st.warning("Please fill out all fields.")
                    else:
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

                        st.session_state["page"] = "profile_setup"
                        st.rerun()

                if st.button("Have an Account? Log In", type="secondary", use_container_width=True):
                    st.session_state["page"] = "login"
                    st.rerun()


#================Log In Screen =================
elif st.session_state["page"] == "login":
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

elif st.session_state["page"] == "profile_setup":
    st.markdown("### Profile Setup")

    profile_full_name = st.text_input(
        "Student Name",
        value=st.session_state["user"]["full_name"],
        key="profile_full_name"
    )
    profile_email = st.text_input(
        "Student Email",
        value=st.session_state["user"]["email"],
        key="profile_email"
    )
    profile_school = st.text_input("School", key="profile_school")
    profile_major = st.text_input("Major", key="profile_major")
    profile_grad_year = st.text_input("Graduation Year", key="profile_grad_year")

    if st.button("Complete Profile", type="primary", use_container_width=True):
        new_profile = {
            "profile_full_name": profile_full_name,
            "profile_email": profile_email,
            "profile_school": profile_school,
            "profile_major": profile_major,
            "profile_grad_year": profile_grad_year
        }

        found_profile = False
        for i, prof in enumerate(profile):
            if prof.get("profile_email", "").strip().lower() == profile_email.strip().lower():
                profile[i] = new_profile
                found_profile = True
                break

        if not found_profile:
            profile.append(new_profile)

        with open(json_profile, "w") as f:
            json.dump(profile, f, indent=4)

        st.success("Profile setup complete!")

        if st.session_state["role"] == "Student":
            st.session_state["page"] = "student_home_page"
        else:
            st.session_state["page"] = "advisor_home_page"

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

            if st.button("Profile", key="profile_btn"):
                st.session_state["page"] = "profile"
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

            if st.button("Profile", key="profile_btn"):
                st.session_state["page"] = "profile"
                st.rerun()

            if st.button("Log Out", key="logout_btn_2"):
                with st.spinner("logging out..."):
                    time.sleep(4)
                    st.session_state["logged_in"] = False
                    st.session_state["user"] = None
                    st.session_state["role"] = None
                    st.rerun()
