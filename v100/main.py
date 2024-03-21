import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import database
from financial_overview import monthly_transaction 

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
            st.markdown(
                """
                <div style="text-align:center">
                    <h3>FInancial Overview</h3>
                </div>
                """,
                unsafe_allow_html=True
            )   
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





if __name__ == "__main__":
    main()
