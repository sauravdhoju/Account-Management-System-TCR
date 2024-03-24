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
            cursor.execute('''CREATE TABLE IF NOT EXISTS Members (
                                member_id INTEGER PRIMARY KEY,
                                username TEXT UNIQUE NOT NULL,
                                hashed_password TEXT NOT NULL,
                                full_name TEXT NOT NULL,
                                email TEXT UNIQUE,
                                phone INTEGER,
                                position TEXT NOT NULL,
                                account_balance REAL DEFAULT 0 CHECK (account_balance >= 0)
                            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS Transactions (
                                transaction_id INTEGER PRIMARY KEY,
                                member_id INTEGER NOT NULL,
                                amount REAL NOT NULL,
                                purpose TEXT NOT NULL,
                                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                transaction_type TEXT CHECK (transaction_type IN ('Club Payment', 'Member Contribution')) NOT NULL,
                                payment_gateway TEXT,
                                FOREIGN KEY (member_id) REFERENCES Members(member_id)
                            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS ClubExpenses(
                                expense_id INTEGER PRIMARY KEY,
                                descriptions TEXT NOT NULL,
                                amount REAL NOT NULL,
                                category TEXT NOT NULL,
                                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                payer_member_id INTEGER,
                                FOREIGN KEY (payer_member_id) REFERENCES Members(member_id)
                            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS BankTransactions (
                                transaction_id INTEGER PRIMARY KEY,
                                member_id INTEGER NOT NULL,
                                debit_amount REAL NOT NULL,
                                credit_amount REAL NOT NULL,
                                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (member_id) REFERENCES Members(member_id) 
                            )''')
            cursor.execute('''CREATE INDEX IF NOT EXISTS idx_member_id ON Transactions(member_id)
                            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

#MEMBER MANAGEMENT FUNCTIONS
def add_member(conn, username, hashed_password, full_name, email, phone, position, account_balance = 0):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Members (username, hashed_password, full_name, email, phone, position, account_balance)
                              VALUES (?,?,?,?,?,?,?)''', (username, hashed_password, full_name, email, phone, position, account_balance))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    return None

def get_member_by_username(conn, username):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Members WHERE username = ?''', (username))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

def get_member_by_email(conn, email):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * from Members WHERE email = ?''', (email))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    return None
        
def update_member_details(conn, member_id, new_details):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''UPDATE Members SET username = ?, hashed_password = ?, full_name = ?, email = ?, phone = ?, account_balance = ?
            WHERE member_id = ?''', (new_details['username'], new_details['hashed_password'], new_details['full_name'], new_details['email'], 
                                                       new_details['phone'], new_details['account_balance'], member_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    return False

def delete_member(conn, member_id):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM Members WHERE member_id = ?''', (member_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    return False

#TRANSACTION MANAGEMENT FUNCTIONS
def record_transaction(conn, member_id, amount, purpose, transaction_type,payment_gateway = None):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Transactions(member_id, amount, purpose, transaction_type, payment_gateway) 
                              VALUES (?,?,?,?,?)''', (member_id, amount, purpose,transaction_type,payment_gateway))
            conn.commit()
            print("Transaction recorded successfully.")
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    else:
        print("Error: Connection to SQLite database is not established.")

def get_member_transaction_history(conn, member_id):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Transactions WHERE member_id = ?''', (member_id))
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    return None
        
def calculate_member_balance(conn, member_id):
    if conn is not None:
        try: 
            cursor = conn.cursor()
            cursor.execute('''SELECT SUM(amount) FROM Transactions Where member_id = ?''', (member_id))
            balance = cursor.fetchone()[0]
            return balance
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    return None

def categorize_transaction(conn, transaction_id, category):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''UPDATE Transactions SET category = ? WHERE transaction_id = ?''', (category, transaction_id))
            conn.commit()
            print("Transaction categorized successfully.")
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    else:
        print("Error: Connection to SQLite database is not established.")

def delete_transaction(conn, transaction_id):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM Transactions WHERE transaction_id = ?''', (transaction_id))
            conn.commit()
            print("Transaction deleted successfully.")
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    else:
        print("Error: Connection to SQLite database is not established.")

#EXPENSE MANAGEMENT FUNCTIONS
def add_club_expense(conn, description, amount, category, payer_member_id = None):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO ClubExpenses (description, amount, category, payer_member_id)
                              Values (?,?,?,?)''', (description, amount, category, payer_member_id))
            conn.commit()
            print("Club expense added successfully.")
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    else:
        print("Error: Connection to SQLite database is not established.")

def get_expense_details(conn, expense_id):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM ClubExpenses WHERE expense_id = ?''', (expense_id))
            expense = cursor.fetchone()
            return expense
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    return None

def generate_expense_report(conn):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM ClubExpenses''')
            expenses = cursor.fetchall()
            return expenses
        except sqlite3.Error as e:
            print(f"Error generating expense report: {e}")
    return None

def categorize_expense(conn, expense_id, category):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''UPDATE ClubExpenses SET category = ? WHERE expense_id = ?''', (category, expense_id))
            conn.commit()
            print("Expense categorized successfully.")
        except sqlite3.Error as e:
            print(f"Error categorizing expense: {e}")
    else:
        print("Error: Connection to SQLite database is not established.")

def delete_expense(conn, expense_id):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM ClubExpenses WHERE expense_id = ?''', (expense_id,))
            conn.commit()
            print("Expense deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting expense: {e}")
    else:
        print("Error: Connection to SQLite database is not established.")

#BANK TRANSACTION FUNCTIONS
def record_bank_transaction(conn, member_id, debit_amount, credit_amount):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO BankTransactions (member_id, debit_amount, credit_amount) 
                              VALUES (?, ?, ?)''', (member_id, debit_amount, credit_amount))
            conn.commit()
            print("Bank transaction recorded successfully.")
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

def get_member_bank_transactions(conn, member_id):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM BankTransactions WHERE member_id = ?''', (member_id,))
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    return None

'''def reconcile_bank_transactions(conn):
    if conn is not None:
        try:
            # Your reconciliation logic goes here
            print("Bank transactions reconciled successfully.")
        except Exception as e:
            print(f"Error during reconciliation: {e}")'''

def get_bank_transactions_by_type(conn, transaction_type):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM BankTransactions WHERE transaction_type = ?''', (transaction_type,))
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    return None

    
#USER AUTHENTICATION AND AUTHRIZATION FUNCTIONS
def insert_user(conn, username, password, full_name, email, phone, position, account_balance=0):
    if conn is not None:
        try:
            cursor = conn.cursor()
            hashed_password = pbkdf2_sha256.hash(password)
            cursor.execute('''INSERT INTO Members (username, hashed_password, full_name, email, phone, position, account_balance)
                              VALUES (?, ?, ?, ?, ?,?, ?)''', (username, hashed_password, full_name, email, phone, position, account_balance))
            conn.commit()
            print("User inserted successfully.")
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    else:
        print("Error: Connection to SQLite database is not established.")

def delete_user(conn, username):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM Members WHERE username = ?''', (username))
            conn.commit()
            print("User deleted successfully.")
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    else:
        print("Error: Connection to SQLite database is not established.")

def authenticate_user(conn, username, password):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Members WHERE username = ?''', (username,))
            user = cursor.fetchone()
            if user:
                stored_password = user[2]   #password stored in index 2
                if pbkdf2_sha256.verify(password, stored_password):
                    print("Authentication successful.")
                    return True
            print("Authentication Failed.")
            return False
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    return False



