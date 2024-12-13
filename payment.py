import streamlit as st
from dotenv import load_dotenv
import os
import datetime
from pymongo import MongoClient

# Load environment variables
load_dotenv()
PHONEPE_UPI = os.getenv("PHONEPE_UPI")

# MongoDB connection
client = MongoClient("mongodb+srv://<username>:<password>@cluster0.mongodb.net/test")
db = client["loan_application"]
loan_agents_collection = db["loan_agents"]
loan_receivers_collection = db["loan_receivers"]

# Function to handle payment
def process_payment(amount, payment_method):
    if payment_method == "PhonePe":
        st.write(f"Pay ₹{amount} to `{PHONEPE_UPI}` and click 'Confirm'.")
        if st.button("Confirm Payment"):
            st.success("Payment confirmed!")
            return True
    elif payment_method == "Razorpay":
        st.write("Redirecting to Razorpay...")
        # Placeholder for Razorpay integration
        st.success("Payment successful via Razorpay!")
        return True
    return False

# Registration page
def registration_page():
    st.title("User Registration")

    # Form inputs
    name = st.text_input("Name")
    mobile = st.text_input("Mobile")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    user_type = st.selectbox("User Type", ["Loan Agent", "Loan Receiver"])

    # Validate inputs
    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        # Check username uniqueness
        if loan_agents_collection.find_one({"username": username}) or loan_receivers_collection.find_one({"username": username}):
            st.error("Username already exists.")
            return

        # Determine payment amount
        payment_amount = 1000 if user_type == "Loan Agent" else 100

        # Process payment
        payment_method = st.radio("Select Payment Method", ["PhonePe", "Razorpay"])
        if process_payment(payment_amount, payment_method):
            # Add user to the appropriate collection
            user_data = {
                "name": name,
                "mobile": mobile,
                "email": email,
                "username": username,
                "password": password,  # In production, hash passwords before storing them
                "user_type": user_type,
                "registered_at": datetime.datetime.now()
            }

            if user_type == "Loan Agent":
                loan_agents_collection.insert_one(user_data)
            else:
                loan_receivers_collection.insert_one(user_data)

            st.success(f"Registration successful! Welcome, {user_type}.")

# Run the registration page
if __name__ == "__main__":
    registration_page()
