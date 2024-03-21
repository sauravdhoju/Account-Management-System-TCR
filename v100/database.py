import sqlite3
from passlib.hash import pbkdf2_sha256

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


# Function to insert a new user into the database
def insert_user(conn, username, password, email, phone_number, address):
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Hash the password before inserting it into the database
            hashed_password = pbkdf2_sha256.hash(password)
            cursor.execute('''INSERT INTO users (username, password, email, phone_number, address) VALUES (?, ?, ?, ?, ?)''', (username, hashed_password, email, phone_number, address))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False

def delete_user(conn, username):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM users WHERE username = ?''', (username,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    return False
    
def authenticate_user(conn, username, password):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM users WHERE username = ?''', (username,))
            user = cursor.fetchone()
            if user:
                stored_password = user[2]  # Password is stored at index 2
                if pbkdf2_sha256.verify(password, stored_password):
                    return True
            return False
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    return False

#Function to insert a new monthly transaction into the database
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


