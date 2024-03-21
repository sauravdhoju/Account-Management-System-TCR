import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import database

debit = 0
credit = 0
# Main function
def display_dashboard():
    conn = database.create_connection()
    if conn:
        database.create_tables(conn)

        # Streamlit interface
        st.sidebar.image("background.png")
        with st.sidebar:
            selected_option = option_menu(
                menu_title=None,  # Title of the menu
                options=["Financial Overview", "Executive Members", "Logout"],  # Options in the menu
                icons=["bank", "people-fill", "power"],  # Icons corresponding to each option
                menu_icon="th-large",  # Icon for the menu itself
                default_index=0,  # Index of the default selected option
                orientation="vertical",  # Orientation of the menu (vertical or horizontal)
                styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "green", "font-size": "20px"},  # Customize icon appearance
                    "nav-link": {
                        "font-size": "15px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "#eee",
                    },
                    "nav-link-selected": {"background-color": "grey"},
                },
            )

        if selected_option == "Financial Overview":
            st.title("Financial")
            selected_suboption = st.selectbox("Select Suboption", ["Monthly Transactions", "Member Payments", "Contributions", "Revenue"])
            if selected_suboption == "Monthly Transactions":
                monthly_transaction(conn)
            elif selected_suboption == "Member Payments":
                st.subheader("Member Payments")
                # Insert content for member payments here
            elif selected_suboption == "Contributions":
                st.subheader("Contributions")
                # Insert content for contributions here
            elif selected_suboption == "Revenue":
                st.subheader("Revenue")
                # Insert content for revenue here
        elif selected_option == "Executive Members":
            st.title("Executive")
            selected_suboption = st.selectbox("Select Suboption", ["Add Executive Members", "View Executive Members", "View Profile", "Payment History", "Contributions"])
            if selected_suboption == "Add Executive Members":
                st.subheader("Add Executive Members")
                #add executive members
            elif selected_suboption == "View Executive Members":
                st.subheader("View Executive Members")
                # Insert content for member payments here
            elif selected_suboption == "View Profile":
                st.subheader("View Profile")
                # Insert content for contributions here
            elif selected_suboption == "Payment History":
                st.subheader("Payment History")
            elif selected_suboption == "Contributions":
                st.subheader("Contributions")
                # Insert content for revenue here
            # Insert content for executive members here
        elif selected_option == "Logout":
            st.success("Logout Successful")
def monthly_transaction(conn):
    # Streamlit interface
    st.title("Monthly Transactions")

    # Initialize debit and credit
    debit = 0
    credit = 0

    # Form for adding a new transaction
    st.subheader("Add New Transaction")
    date = st.date_input("Date")
    description = st.text_input("Description")
    type = st.selectbox("Transaction Type", options=["Debit", "Credit"])
    if type == 'Debit':
        debit = st.number_input("Debit", min_value=0.0, step=0.01)
    if type == 'Credit':
        credit = st.number_input("Credit", min_value=0.0, step=0.01)
        
    if st.button("Add Transaction"):
        if database.insert_monthly_transaction(conn, date, description, debit, credit):
            st.success("Transaction added successfully!")
            database.update_balance(conn)
        else:
            st.error("Failed to add transaction.")

    # Displaying existing transactions
    st.subheader("Existing Transactions")
    transactions = database.get_monthly_transactions(conn)
    if transactions:
        df = pd.DataFrame(transactions, columns=["ID", "Date", "Description", "Debit", "Credit", "Balance"])
        st.dataframe(df)
    else:
        st.info("No transactions found.")

'''
def executive_members():
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
'''
if __name__ == "__main__":
    main()
