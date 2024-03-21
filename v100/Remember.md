🚀 TCR Dashboard
📊 Financial Overview
Monthly Transactions
Member Payments
Contributions Summary
Revenue & Expenses
Financial Status
👤 Executive Members
Add Executive Members
View Members
View Profile
Payment History
Contributions
🔒 Logout



#bakcup code
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
                                address TEXT NOT NULL
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
            # Create table for executive member payments
            cursor.execute('''CREATE TABLE IF NOT EXISTS member_payments (
                                id INTEGER PRIMARY KEY,
                                executive_id INTEGER NOT NULL,
                                date TEXT NOT NULL,
                                description TEXT NOT NULL,
                                amount REAL NOT NULL,
                                payment_method TEXT NOT NULL,
                                portal TEXT,
                                FOREIGN KEY (executive_id) REFERENCES users (id)
                            )''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

# Function to insert a new user into the database
def insert_user(conn, username, password, email, phone_number, address):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO users (username, password, email, phone_number, address) VALUES (?, ?, ?, ?, ?)''', (username, password, email, phone_number, address))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False

# Function to retrieve all monthly transactions from the database
def get_monthly_transactions(conn):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM monthly_transactions''')
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    return None

# Function to insert a new monthly transaction into the database
def insert_monthly_transaction(conn, date, description, debit, credit, balance):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO monthly_transactions (date, description, debit, credit, balance) VALUES (?, ?, ?, ?, ?)''', (date, description, debit, credit, balance))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False

# Function to insert a new member payment into the database
def insert_member_payment(conn, executive_id, date, description, amount, payment_method, portal=None):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO member_payments (executive_id, date, description, amount, payment_method, portal) VALUES (?, ?, ?, ?, ?, ?)''', (executive_id, date, description, amount, payment_method, portal))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False

# Function to retrieve all member payments from the database
def get_member_payments(conn):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM member_payments''')
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    return None

def main():
    conn = create_connection('accounting.db')
    if conn:
        create_tables(conn)
        
        # Streamlit interface for recording member payments
        st.subheader("Record Member Payments")
        executive_id = st.selectbox("Select Executive Member", [1, 2, 3])  # Placeholder for executive member IDs
        payment_date = st.date_input("Payment Date", key="payment_date")  # Unique key for date input
        payment_description = st.text_input("Description")
        payment_amount = st.number_input("Amount", min_value=0.0, step=0.01)
        payment_method = st.selectbox("Payment Method", ["Cash", "Online"])
        if payment_method == "Online":
            payment_portal = st.selectbox("Select Payment Portal", ["ESewa", "Khalti", "IME Pay", "ConnectIPS", "Mobile Banking"])
        else:
            payment_portal = None
        if st.button("Record Payment"):
            if insert_member_payment(conn, executive_id, payment_date, payment_description, payment_amount, payment_method, payment_portal):
                st.success("Payment recorded successfully!")
            else:
                st.error("Failed to record payment.")
        
        # Displaying existing member payment records
        st.subheader("Existing Member Payments")
        payments = get_member_payments(conn)
        if payments:
            df_payments = pd.DataFrame(payments, columns=["ID", "Executive ID", "Date", "Description", "Amount", "Payment Method", "Portal"])
            st.dataframe(df_payments)
        else:
            st.info("No member payment records found.")

if __name__ == "__main__":
    main()