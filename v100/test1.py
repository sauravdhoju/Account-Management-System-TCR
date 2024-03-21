import sqlite3
import streamlit as st
import pandas as pd

# Function to create a SQLite connection
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    return None

# Function to create tables if they don't exist
def create_tables(conn):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL,
                                email TEXT NOT NULL,
                                phone_number TEXT NOT NULL,
                                address TEXT NOT NULL,
                                user_type TEXT NOT NULL,
                                image BLOB
                            )''')
            # Create table for monthly transactions
            cursor.execute('''CREATE TABLE IF NOT EXISTS monthly_transactions (
                                id INTEGER PRIMARY KEY,
                                date TEXT NOT NULL,
                                description TEXT NOT NULL,
                                debit REAL NOT NULL,
                                credit REAL NOT NULL,
                                balance REAL NOT NULL
                            )''')
            # Create table for member payments
            cursor.execute('''CREATE TABLE IF NOT EXISTS member_payments (
                                id INTEGER PRIMARY KEY,
                                user_id INTEGER NOT NULL,
                                date TEXT NOT NULL,
                                description TEXT NOT NULL,
                                amount REAL NOT NULL,
                                payment_method TEXT NOT NULL,
                                portal TEXT,
                                FOREIGN KEY (user_id) REFERENCES users (id)
                            )''')
            # Create table for executive members
            cursor.execute('''CREATE TABLE IF NOT EXISTS executive_members (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                position TEXT NOT NULL,
                                email TEXT NOT NULL,
                                phone_number TEXT NOT NULL,
                                amount_spent REAL NOT NULL
                            )''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

# Function to insert a new user into the database
def insert_user(conn, username, password, email, phone_number, address, user_type, image):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO users (username, password, email, phone_number, address, user_type, image) VALUES (?, ?, ?, ?, ?, ?, ?)''', (username, password, email, phone_number, address, user_type, image))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False

# Function to retrieve user information based on username and password
def get_user(conn, username, password):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM users WHERE username = ? AND password = ?''', (username, password))
            row = cursor.fetchone()
            return row
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    return None

# Function to insert a new member payment into the database
def insert_member_payment(conn, user_id, date, description, amount, payment_method, portal=None):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO member_payments (user_id, date, description, amount, payment_method, portal) VALUES (?, ?, ?, ?, ?, ?)''', (user_id, date, description, amount, payment_method, portal))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False

# Function to insert a new executive member into the database
def insert_executive_member(conn, name, position, email, phone_number, amount_spent):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO executive_members (name, position, email, phone_number, amount_spent) VALUES (?, ?, ?, ?, ?)''', (name, position, email, phone_number, amount_spent))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False

# Function to retrieve all executive members from the database
def get_executive_members(conn):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM executive_members''')
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    return None

def main():
    conn = create_connection('accounting.db')
    if conn:
        create_tables(conn)
        
        # Streamlit interface for user registration
        st.subheader("User Registration")
        username_reg = st.text_input("Username")
        password_reg = st.text_input("Password", type="password")
        email_reg = st.text_input("Email")
        phone_number_reg = st.text_input("Phone Number")
        address_reg = st.text_input("Address")
        user_type_reg = "user"  # Regular user
        image_reg = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        if st.button("Register"):
            if insert_user(conn, username_reg, password_reg, email_reg, phone_number_reg, address_reg, user_type_reg, image_reg.read()):
                st.success("Registration successful!")
            else:
                st.error("Failed to register.")
        
        # Streamlit interface for user login
        st.subheader("User Login")
        username_login = st.text_input("Username1")
        password_login = st.text_input("Password1", type="password")
        if st.button("Login"):
            user_info = get_user(conn, username_login, password_login)
            if user_info:
                st.success("Login successful!")
                st.write(f"Welcome, {user_info[1]}!")
                st.image(user_info[-1])
                if user_info[-2] == "user":
                    # Streamlit interface for recording member payments
                    st.subheader("Record Member Payments")
                    payment_date = st.date_input("Payment Date", key="payment_date")  # Unique key for date input
                    payment_description = st.text_input("Description")
                    payment_amount = st.number_input("Amount", min_value=0.0, step=0.01)
                    payment_method = st.selectbox("Payment Method", ["Cash", "Online"])
                    if payment_method == "Online":
                        payment_portal = st.selectbox("Select Payment Portal", ["ESewa", "Khalti", "IME Pay", "ConnectIPS", "Mobile Banking"])
                    else:
                        payment_portal = None
                    if st.button("Record Payment"):
                        if insert_member_payment(conn, user_info[0], payment_date, payment_description, payment_amount, payment_method, payment_portal):
                            st.success("Payment recorded successfully!")
                        else:
                            st.error("Failed to record payment.")
                
                    # Displaying existing member payment records for the logged-in user
                    st.subheader("Your Member Payments")
                    payments = get_member_payments(conn)
                    if payments:
                        user_payments = [payment for payment in payments if payment[1] == user_info[0]]
                        df_payments = pd.DataFrame
                        user_payments, columns=["ID", "User ID", "Date", "Description", "Amount", "Payment Method", "Portal"]
                        st.dataframe(df_payments)
                    else:
                        st.info("No member payment records found.")

            else:
                st.error("Invalid username or password.")

        # Streamlit interface for adding executive members
        st.subheader("Add Executive Members")
        exec_name = st.text_input("Name")
        exec_position = st.text_input("Position")
        exec_email = st.text_input("Email1")
        exec_phone = st.text_input("Phone Number1")
        exec_amount_spent = st.number_input("Amount Spent", min_value=0.0, step=0.01)
        if st.button("Add Executive Member"):
            if insert_executive_member(conn, exec_name, exec_position, exec_email, exec_phone, exec_amount_spent):
                st.success("Executive member added successfully!")
            else:
                st.error("Failed to add executive member.")

        # Displaying existing executive members
        st.subheader("Existing Executive Members")
        exec_members = get_executive_members(conn)
        if exec_members:
            df_exec_members = pd.DataFrame(exec_members, columns=["ID", "Name", "Position", "Email", "Phone Number", "Amount Spent"])
            st.dataframe(df_exec_members)
        else:
            st.info("No executive members found.")

if __name__ == "__main__":
    main()

