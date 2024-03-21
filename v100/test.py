import sqlite3
import streamlit as st
import pandas as pd

# Function to create a SQLite connection
def create_connection():
    try:
        conn = sqlite3.connect('accounting.db')
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
            conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

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

# Function to calculate and update balance for all transactions
def update_balance(conn):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT id, debit, credit FROM monthly_transactions ORDER BY id ASC''')
            rows = cursor.fetchall()
            balance = 0
            for row in rows:
                transaction_id, debit, credit = row
                balance = balance - debit + credit
                cursor.execute('''UPDATE monthly_transactions SET balance = ? WHERE id = ?''', (balance, transaction_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

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

# Main function
def main():
    conn = create_connection()
    if conn:
        create_tables(conn)

        # Streamlit interface
        st.title("Monthly Transactions")

        # Form for adding a new transaction
        st.subheader("Add New Transaction")
        date = st.date_input("Date")
        description = st.text_input("Description")
        debit = st.number_input("Debit", min_value=0.0, step=0.01)
        credit = st.number_input("Credit", min_value=0.0, step=0.01)
        if st.button("Add Transaction"):
            if insert_monthly_transaction(conn, date, description, debit, credit, balance):
                st.success("Transaction added successfully!")
                update_balance(conn)
            else:
                st.error("Failed to add transaction.")

        # Displaying existing transactions
        st.subheader("Existing Transactions")
        transactions = get_monthly_transactions(conn)
        if transactions:
            df = pd.DataFrame(transactions, columns=["ID", "Date", "Description", "Debit", "Credit", "Balance"])
            st.dataframe(df)
        else:
            st.info("No transactions found.")

if __name__ == "__main__":
    main()
