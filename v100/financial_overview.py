import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import database

debit = 0
credit = 0

def monthly_transaction(conn):
    conn = database.create_connection()
    if conn:
        database.create_tables(conn)
        st.markdown(
            """
            <div style="text-align:center">
                <h3>Monthly Transaction</h3>
            </div>
            """,
            unsafe_allow_html=True
        )   

        # Initialize debit variable
        debit = 0
        balance = 0
        # Form for adding a new transaction
        st.subheader("Add New Transaction")
        date = st.date_input("Date")
        description = st.text_input("Description")
        type = st.selectbox("Transaction Type", options = ["Debit", "Credit"])
        if type == 'Debit':
            debit = st.number_input("Debit", min_value=0.0, step=0.01)
        elif type == 'Credit':
            credit = st.number_input("Credit", min_value=0.0, step=0.01)
            
        if st.button("Add Transaction"):
            if type == 'Debit':
                if database.insert_monthly_transaction(conn, date, description, debit, 0, balance):
                    st.success("Transaction added successfully!")
                    database.update_balance(conn)
                else:
                    st.error("Failed to add transaction.")
            elif type == 'Credit':
                if database.insert_monthly_transaction(conn, date, description, 0, credit, balance):
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