import streamlit as st
from database import add_transaction, get_transactions_by_user

def show_loan_agent_dashboard():
    st.sidebar.title("Loan Agent Dashboard")
    page = st.sidebar.selectbox("Choose a page", ["Transaction", "Amount Loan Given", "Update", "Print Transactions"])

    if page == "Transaction":
        st.subheader("Add Loan Transaction")
        receiver = st.text_input("Loan Receiver Username")
        amount = st.number_input("Loan Amount", min_value=0)
        interest = st.number_input("Interest (%)", min_value=0.0)
        duration = st.number_input("Duration (days)", min_value=1)
        if st.button("Submit"):
            add_transaction({"receiver": receiver, "amount": amount, "interest": interest, "duration": duration})
            st.success("Transaction added successfully!")
