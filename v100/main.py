import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import database
from financial_overview import monthly_transaction 
from executive_member import add_excutive_members

# debit = 0
# credit = 0
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
                options=["Financial Management", "Executive Members", "Club Members", "Logout"],  # Options in the menu
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
#Financial Management
        if selected_option == "Financial Management":
            st.markdown(
                """
                <div style="text-align:center">
                    <h3>Financial Management</h3>
                </div>
                """,
                unsafe_allow_html=True
            )   
            selected_suboption = st.selectbox("Select Suboption", ["View Financial Status", "Generate Financial Reports", "Manage Club Expenses", "Manage bank Transactions"])
            if selected_suboption == "View Financial Status":
                st.subheader("View Financial Status")
            elif selected_suboption == "Generate Financial Reports":
                st.subheader("Generate Financial Reports")
            elif selected_suboption == "Manage Club Expenses":
                st.subheader("Manage Club Expenses")
            elif selected_suboption =="Manage bank Transactions":
                st.subheader("Manage bank Transactions")
#Executive Members
        elif selected_option == "Executive Members":
            st.markdown(
                """
                <div style="text-align:center">
                    <h3>Executive Members</h3>
                </div>
                """,
                unsafe_allow_html=True
            )   
            selected_suboption = st.selectbox("Select Suboption", ["Add Executive Members", "View Executive Members", "View Executive Member Profile", "Edit Executive Member Profile", "Remove Executive Member"])
            if selected_suboption == "Add Executive Members":
                st.subheader("Add Executive Members")
                add_excutive_members()
                #add executive members
            elif selected_suboption == "View Executive Members":
                st.subheader("View Executive Members")
                # Insert content for member payments here
            elif selected_suboption == "View Executive Profile":
                st.subheader("View Executive Profile")
                # Insert content for contributions here
            elif selected_suboption == "Edit Members Profile":
                st.subheader("Edit Members Profile")
            elif selected_suboption == "Remove Executive Members":
                st.subheader("Remove Executive Members")
                # Insert content for revenue here
#Club Members       
        elif selected_option == "Club Members":
            st.markdown(
                """
                <div style="text-align:center">
                    <h3>Club Members</h3>
                </div>
                """,
                unsafe_allow_html=True
            )   
            selected_suboption = st.selectbox("Select Suboption", ["View Members", "View Member Profile", "Edit Member Profile", "Remove Member"])
            if selected_suboption == "View Members":
                st.subheader("Memebers")
            elif selected_suboption == "View Member Profile":
                st.subheader("View Member Profile")
            elif selected_suboption == "Edit Member Profile":
                st.subheader("Edit Member Profile")
            elif selected_suboption =="Remove Member":
                st.subheader("Remove Member")

#Logout
        elif selected_option == "Logout":
            st.success("Logout Successful")
            st.rerun()

if __name__ == "__main__":
    main()
