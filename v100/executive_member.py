# app.py

import streamlit as st
from passlib.hash import pbkdf2_sha256
from database import create_connection, add_executive_member, search_executive_members, get_all_executive_members

conn = create_connection()

def add_executive_members_ui(conn):
    st.subheader("Add Executive Members")
    exec_name = st.text_input("Full Name")
    exec_position = st.selectbox('Position', ['President', 'Vice President', 'Secretary', 'IT Coordinator'])
    exec_email = st.text_input("Email Address")
    exec_phone = st.text_input("Contact Number")
    exec_username = st.text_input("Username")
    exec_password = st.text_input("Password", type="password")
    exec_balance = st.number_input("Account Balance", value=0.0, step=0.01)
    exec_joined_date = st.date_input("Joined Date")
    exec_performance_metrics = st.number_input("Performance Metrics (Stars)", min_value=0, max_value=3, step=1)
    exec_active_status = st.checkbox("Active Status")
    access_level = st.selectbox("Access Level", ["Treasurer", "Secretary", "President", "Vice President"])

    if st.button("Add Executive Member"):
        hashed_password = pbkdf2_sha256.hash(exec_password)
        add_executive_member(conn, exec_name, exec_position, exec_email, exec_phone, exec_username, hashed_password, exec_balance, exec_joined_date, exec_performance_metrics, exec_active_status, access_level)

def display_executive_members_ui(conn):
    st.subheader("Executive Members")
    search_query = st.text_input("Search by name or email")
    if st.button("Search"):
        search_results = search_executive_members(conn, search_query)
        if search_results:
            st.write("Search Results:")
            for result in search_results:
                display_member_info(result)
        else:
            st.write("No matching executive members found.")
    else:
        # If search button is not clicked, display all executive members
        all_executive_members = get_all_executive_members(conn)
        if all_executive_members:
            st.write("All Executive Members:")
            for member in all_executive_members:
                display_member_info(member)
        else:
            st.write("No executive members found.")

def display_member_info(member):
    st.write("Full Name:", member[3])
    st.write("Position:", member[6])
    st.write("Email:", member[4])
    st.write("Phone:", member[5])
    st.write("Username:", member[1])
    st.write("Account Balance:", member[7])
    st.write("Joined Date:", member[8])
    st.write("Performance Metrics:", member[9])
    st.write("Active Status:", "Active" if member[10] else "Inactive")
    st.write("Access Level:", member[11])
    st.write("---")

# display_executive_members(conn)
# add_executive_members_ui(conn)
