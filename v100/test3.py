import streamlit as st
import sqlite3

# Function to create a database connection
def create_connection():
    conn = sqlite3.connect('your_database.db')
    return conn

# Function to check if a username exists in the ExecutiveMembers table
def check_username(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ExecutiveMembers WHERE username = ?", (username,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

# Function to insert a new user into the Members table
def insert_user(username, hashed_password, full_name, email, phone, position):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Members (username, hashed_password, full_name, email, phone, position) VALUES (?, ?, ?, ?, ?, ?)",
                   (username, hashed_password, full_name, email, phone, position))
    conn.commit()
    conn.close()

# Streamlit app
def main():
    st.title("Executive Member Registration")

    # Registration form
    st.header("Register as an Executive Member")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    position = st.text_input("Position")

    if st.button("Register"):
        if check_username(username):
            # If the username exists in the ExecutiveMembers table, insert the user into the Members table
            insert_user(username, password, full_name, email, phone, position)
            st.success("Registration successful!")
        else:
            st.error("You are not authorized to register as an executive member.")

if __name__ == "__main__":
    main()
