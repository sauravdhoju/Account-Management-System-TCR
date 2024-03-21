import streamlit as st
import re  # Import the regular expression module
from database import create_connection, create_tables, insert_user, authenticate_user
from main import display_dashboard

def main():
    session_state = st.session_state

    if 'authenticated' not in session_state:
        session_state.authenticated = False

    conn = create_connection()
    create_tables(conn)

    if session_state.authenticated:
        display_dashboard()
    else:
        # Use st.tabs to create tabs for Login and Register
        tabs = st.tabs(["Login", "Register"])

        # Initially, hide the Register tab
        tabs[1].visible = False

        # Login tab content
        with tabs[0]:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.button("Login")
            if login_button:
                if authenticate_user(conn, username, password):
                    session_state.authenticated = True
                    st.success("Login successful!")
                else:
                    st.error("Invalid username or password")

        # Register tab content
        with tabs[1]:
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            email = st.text_input("Email")
            phone_number = st.text_input("Phone Number")
            address = st.text_input("Address")
            
            if st.button("Register"):
                # Check if the username is already taken
                if is_username_taken(conn, new_username):
                    st.error("Username already exists. Please choose a different username.")
                else:
                    # Validate email if it's not empty
                    if email.strip() != "":
                        if not is_valid_email(email):
                            st.error("Invalid email address. Please enter a valid email.")
                            st.stop()

                    # Validate phone number
                    if not is_valid_phone_number(phone_number):
                        st.error("Invalid phone number. Please enter a valid phone number in the format +977-XXXXXXXXXX.")
                        st.stop()

                    # Check if passwords match
                    if new_password == confirm_password:
                        insert_user(conn, new_username, new_password, email, phone_number, address)
                        st.success("Registration successful!")
                        tabs[0].visible = True
                        tabs[1].visible = False
                    else:
                        st.error("Passwords do not match")

def is_valid_email(email):
    """Check if the email is valid using regular expression."""
    # Regular expression pattern for validating email
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def is_valid_phone_number(phone_number):
    """Check if the phone number is valid."""
    # Regular expression pattern for validating phone number
    pattern = r"^\+977-[0-9]{10}$"
    return re.match(pattern, phone_number) is not None

def is_username_taken(conn, username):
    """Check if the username is already taken."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone() is not None

if __name__ == "__main__":
    main()
