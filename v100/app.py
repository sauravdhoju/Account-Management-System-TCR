import streamlit as st
from login_register import main as login_register_main
# from main import main as main_page_main

# st.set_page_config(page_title = "TROJAN", page_icon = ":NOTE:", layout = "centered")

def display_app_interface():
    st.markdown(
        """
        <div style="text-align:center">
            <h1>Account Management System</h1>
            <h3>Trojan Club of Robotics-TCR</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    show_login = st.toggle("Show Login", False)

    if show_login:
        login_register_main()
    else:
        image = "background.png"
        st.image(image, use_column_width=True)

if __name__ == "__main__":
    display_app_interface()
