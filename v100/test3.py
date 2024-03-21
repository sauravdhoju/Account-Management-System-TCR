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
            # Create table for executive members
            cursor.execute('''CREATE TABLE IF NOT EXISTS executive_members (
                                name TEXT PRIMARY KEY,
                                position TEXT NOT NULL,
                                email TEXT NOT NULL,
                                phone_number TEXT NOT NULL,
                                amount_spent REAL NOT NULL
                            )''')
            # Create trigger to update amount_spent in executive_members table
            cursor.execute('''CREATE TRIGGER IF NOT EXISTS update_amount_spent
                              AFTER INSERT ON monthly_transactions
                              FOR EACH ROW
                              BEGIN
                                  UPDATE executive_members
                                  SET amount_spent = amount_spent + NEW.debit
                                  WHERE name = 'Saurav Dhoju';
                              END''')
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

# Main function
def main():
    conn = create_connection('accounting.db')
    if conn:
        create_tables(conn)
        
        # Streamlit interface for recording monthly transactions
        st.subheader("Record Monthly Transactions")
        transaction_date = st.date_input("Transaction Date", key="transaction_date")  # Unique key for date input
        transaction_description = st.text_input("Description")
        transaction_debit = st.number_input("Debit", min_value=0.0, step=0.01)
        transaction_credit = st.number_input("Credit", min_value=0.0, step=0.01)
        transaction_balance = st.number_input("Balance", min_value=0.0, step=0.01)
        if st.button("Record Transaction"):
            if insert_monthly_transaction(conn, transaction_date, transaction_description, transaction_debit, transaction_credit, transaction_balance):
                st.success("Transaction recorded successfully!")
            else:
                st.error("Failed to record transaction.")

        # Streamlit interface for adding executive members
        st.subheader("Add Executive Member")
        exec_name = st.text_input("Name")
        exec_position = st.text_input("Position")
        exec_email = st.text_input("Email")
        exec_phone = st.text_input("Phone Number")
        exec_amount_spent = st.number_input("Amount Spent", min_value=0.0, step=0.01)
        if st.button("Add Executive Member"):
            if insert_executive_member(conn, exec_name, exec_position, exec_email, exec_phone, exec_amount_spent):
                st.success("Executive member added successfully!")
            else:
                st.error("Failed to add executive member.")

if __name__ == "__main__":
    main()
