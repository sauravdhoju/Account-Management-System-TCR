import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import database


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