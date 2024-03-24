# Function to create tables if they don't exist
def create_tables(conn):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL UNIQUE,
                                password TEXT NOT NULL,
                                email TEXT NOT NULL,
                                phone_number TEXT NOT NULL,
                                address TEXT NOT NULL,
                                user_type TEXT NOT NULL,
                                image BLOB
                            )''')
            # Create table for executive members
            cursor.execute('''CREATE TABLE IF NOT EXISTS executive_members (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL UNIQUE,
                                name TEXT NOT NULL,
                                position TEXT NOT NULL,
                                email TEXT NOT NULL,
                                phone_number TEXT NOT NULL,
                                amount_spent REAL NOT NULL,
                                image BLOB
                            )''')
            # Create table for transactions
            cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                amount REAL NOT NULL,
                                FOREIGN KEY (username) REFERENCES executive_members(username)
                            )''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

# Function to insert a new executive member into the database
def insert_executive_member(conn, username, name, position, email, phone_number, amount_spent, image):
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Check if the executive member with the same username already exists
            cursor.execute('''SELECT * FROM executive_members WHERE username = ?''', (username,))
            existing_member = cursor.fetchone()
            if existing_member:
                print("Executive member with the same username already exists.")
                return False
            else:
                # Insert the new executive member
                cursor.execute('''INSERT INTO executive_members (username, name, position, email, phone_number, amount_spent, image) VALUES (?, ?, ?, ?, ?, ?, ?)''', (username, name, position, email, phone_number, amount_spent, image))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False

# Function to manage accounting transactions
def manage_transaction(conn, username, amount):
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Insert the transaction
            cursor.execute('''INSERT INTO transactions (username, amount) VALUES (?, ?)''', (username, amount))
            # Update the amount spent for the executive member
            cursor.execute('''UPDATE executive_members SET amount_spent = amount_spent + ? WHERE username = ?''', (amount, username))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False

# Streamlit interface
def main():
    conn = create_connection('accounting.db')
    if conn:
        create_tables(conn)
        st.title("Executive Members Management")
        
        # Sidebar options
        st.sidebar.title("Menu")
        option = st.sidebar.selectbox("Select Option", ["Add Executive Member", "Manage Transactions", "View Executive Members"])
        
        if option == "Add Executive Member":
            # Add executive member functionality

        elif option == "Manage Transactions":
            st.subheader("Manage Transactions")
            transaction_username = st.selectbox("Select Executive Member", get_executive_member_usernames(conn))
            transaction_amount = st.number_input("Transaction Amount", min_value=0.0, step=0.01)
            if st.button("Submit Transaction"):
                if manage_transaction(conn, transaction_username, transaction_amount):
                    st.success("Transaction successful!")
                else:
                    st.error("Failed to process transaction.")
        
        elif option == "View Executive Members":
            # View executive members functionality

if __name__ == "__main__":
    main()
