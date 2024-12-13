import streamlit as st
from database import add_user, check_username_exists
from payment import process_payment
from utils import validate_password

def show_auth_page():
    st.sidebar.title("Login / Sign Up")
    choice = st.sidebar.selectbox("Choose an option", ["Login", "Sign Up"])

    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            # Logic to validate login
            if check_username_exists(username):
                st.session_state.user = username
                st.success("Login successful!")
            else:
                st.error("Invalid username or password.")
    elif choice == "Sign Up":
        st.subheader("Sign Up")
        name = st.text_input("Name")
        mobile = st.text_input("Mobile")
        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        user_type = st.selectbox("User Type", ["Loan Agent", "Loan Receiver"])

        if st.button("Sign Up"):
            if not validate_password(password, confirm_password):
                st.error("Passwords do not match!")
            elif check_username_exists(username):
                st.error("Username already exists!")
            else:
                if process_payment(user_type):
                    add_user({"name": name, "mobile": mobile, "email": email, 
                              "username": username, "password": password, "type": user_type},
                             "loan_agents" if user_type == "Loan Agent" else "loan_receivers")
                    st.success("Registration successful!")
