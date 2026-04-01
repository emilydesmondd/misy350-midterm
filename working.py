import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config(page_title="Network Manager", layout="centered")
st.title("Network Manager Application")


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    
if "user" not in st.session_state:
    st.session_state["user"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"

if "role" not in st.session_state:
    st.session_state["role"] = None

users = [
        {
        "id": "1",
        "email": "admin@school.edu",
        "full_name": "System Admin",
        "password": "123ssag@43AE",
        "role": "Admin",
    }
]

connections = [
    {
        "id" : "1",
        "full_name" : "John Doe",
        "company" : "Tech Corp",
        "position" : "Software Engineer"
    },

]


json_file = Path("users.json")
if json_file.exists():
    with open(json_file, "r") as f:
        users = json.load(f)

json_path = Path("connections.json")
if json_path.exists():
    with json_path.open("r", encoding= "utf-8") as f:
        connections = json.load(f)

if st.session_state["role"] == "Admin":
    st.markdown("This is the Admin UI- Dashboard")

    if st.button("Log Out"):
        with st.spinner("logging out..."):
            time.sleep(4)
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.rerun()


elif st.session_state["role"] =="Professional":
    st.markdown("This is the Professional Dashboard")
    if st.session_state['page'] == 'home':
        st.markdown(f'Welcome {st.session_state["user"]["email"]}!')
        if st.button("Go to Dashboard", type="primary", key='view_dash_btn'):
            st.session_state['page'] = 'dashboard'
            st.rerun()
    elif st.session_state['page'] == 'dashboard':
        tab1, tab2, tab3 = st.tabs(["View Assignments", "Add New Assignment", "Update An Assignment"])        
        with tab1:
            #st.info("This tab is under development!")
            option = st.radio("View/Search", ["View" , "Search"], horizontal= True)

            if option == "View":
                st.dataframe(connections)

            else:
                titles = []
                for people in connections:
                    titles.append(people["first_name"])

                if not titles:
                    st.warning("No Connections found")
                else:
                    selected_title = st.selectbox("Assignmnet Title", titles)

            for people in connections:
                if people["first_name"] == selected_title:
                    with st.expander( 'Assignment Details', expanded=True):
                        st.markdown(f"### Ttitle: {people['first_name']}")
                        st.markdown(f"Description: {people['last_name']}")
                        st.markdown(f"Type: **{people['company']}**")
                    break
            
            selected_assignment = st.selectbox('Assignment Title',
                                          options=connections,
                                          format_func=lambda x: f"{x['first_name']}",
                                          key= 'new_assignment')
            
            with st.expander( 'Assignment Details', expanded=True):
                st.markdown(f"### Ttitle: {selected_assignment['first_name']}")
                st.markdown(f"Description: {selected_assignment['last_name']}")
                st.markdown(f"Type: **{selected_assignment['company']}**")
        
        with tab2:
            # Add New Assignment
            st.markdown("# Add New Connection")

        #input

            name = st.text_input("Name",placeholder="ex. John Doe", 
                            help="This is the name of the connection")

            description = st.text_area("Description",placeholder="ex. database design...")
            due_date = st.date_input("Due Date")
            assignments_type = st.radio("Type",["Homework", "Lab"])


            assignments_type2 = st.selectbox("Type", ["Homework", "Lab","Other"])
            if assignments_type2 == "Other":
                assignments_type2 = st.text_input("Assingment Type")

            lab = st.checkbox("Lab")

            with st.expander("Assignment Preview",expanded= True):
                st.markdown("## Live Preview")
                st.markdown(f"Title: {title}")
st.title
            btn_save = st.button("Save",use_container_width=True, disabled=False,type="")

            if btn_save:
                with st.spinner("Saving the Assignmnet..."):
                    time.sleep(5)
                    if not title:
                        st.warning("Enter Assignmnet Title")
                    else:
                        #Add/Create new Assignmnet
                        new_assignmnet_id = "HW" + str(next_assignment_id_number)
                        next_assignment_id_number += 1

                    assignments.append(
                        {
                        "id" : new_assignmnet_id,
                        "title": title,
                        "description" : description,
                        "points" : points,
                        "type" : assignments_type
                        }
                    )

                    with json_path.open("w",encoding="utf-8") as f:
                        json.dump(assignments,f)

                    time.sleep(4)
                    st.success("Assignment is recorded!")
                    st.rerun()
                    st.dataframe(assignments)

        with tab3:
            st.markdown("# Update an Assignment")

            titles = []
            for assignment in assignments:
                titles.append(assignment["title"])

            selected_item = st.selectbox("Select an item", titles,key="search_titles")
    
            selected_assignment = {}
            for assignment in assignments:
                if assignment["title"] == selected_item:
                    selected_assignment = assignment
                    break

            edit_title = st.text_input("Title", value = selected_assignment['title'], 
                                key=f"edit_title_{selected_assignment['id']}")
            edit_description = st.text_area("Description", value= selected_assignment['description'], 
                                    key = f"edit_description_{selected_assignment['id']}")
    
            type_list = ["Homework", "Lab"]
            selected_assignmnet_type_index = type_list.index(selected_assignment['type'].capitalize())

            edit_type = st.radio("Type", type_list, index=selected_assignmnet_type_index,
                         key= f"edit_type_{selected_assignment['id']}" )


            update_btn = st.button("Update Assignment",key="btn_update",use_container_width=True,type="primary")
            if update_btn:
                with st.spinner("Updating the assignment..."):
                    time.sleep(5)
                    selected_assignment['title'] = edit_title
                    selected_assignment["description"] = edit_description

                with json_path.open("w",encoding="utf-8") as f:
                    json.dump(assignments,f)

                st.success("Assignment is updated!")
                time.sleep(5)
                st.rerun()


            # st.dataframe(assignments)


else:
    st.subheader("Log In")
    with st.container(border=True):
        email_input = st.text_input("Email Address", key = "email_address_login")
        password_input = st.text_input("Password", type="password", key = "password_login")
        
        if st.button("Log In", type="primary",use_container_width=True):
            with st.spinner("Logging in..."):
                time.sleep(2) # Fake backend delay
                
                # Find user
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
                    st.error("Invalid credentials")

    st.subheader("New Instructor Account")
    with st.container(border=True):
        new_email = st.text_input("Email Address", key="email_address_register")
        new_password = st.text_input("Password", type="password" , key = "password_reg")
        
        if st.button("Create Account", type="secondary", use_container_width=True):
            with st.spinner("Creating account..."):
                time.sleep(2) # Fake backend delay
                # ... (Assume validation logic here) ...
                users.append({
                    "id": str(uuid.uuid4()),
                    "email": new_email,
                    "password": new_password,
                    "role": "Instructor"
                })
                with open(json_file, "w") as f:
                    json.dump(users, f, indent=4)
                st.success(f"Account created! {new_email}")
                time.sleep(4)
                st.rerun()

    st.write("---")
    st.dataframe(users)

with st.sidebar:
    if "logged_in" in st.session_state and st.session_state["logged_in"] != False:
        user = st.session_state["user"]
        st.markdown(f"Welcome {user['email']}")
    else:
        st.markdown("Welcome! - Login")

if st.button('Log Out'):
    with st.spinner("Logging out..."):
        time.sleep(5)
    st.session_state['logged_in'] = False
    st.session_state['user'] = None
    st.session_state['role'] = None 
    st.success("Logged out successfully!")
    st.rerun()

