import streamlit as st
from database import get_transactions_by_user, update_transaction_status
from utils import notify_user
import pandas as pd

def show_loan_receiver_dashboard():
    st.sidebar.title("Loan Receiver Dashboard")
    page = st.sidebar.selectbox("Choose a page", ["Acceptance", "Print Transactions"])

    if page == "Acceptance":
        st.subheader("Loan Offers")
        # Fetch loan offers for the logged-in user
        username = st.session_state.user
        loan_offers = get_transactions_by_user(username, role="loan_receiver")

        for offer in loan_offers:
            st.write(f"**Loan Agent:** {offer['loan_agent']}")
            st.write(f"**Amount:** ₹{offer['amount']}")
            st.write(f"**Interest:** {offer['interest']}%")
            st.write(f"**Duration:** {offer['duration']} days")
            if st.button(f"Accept Offer from {offer['loan_agent']}", key=offer['_id']):
                update_transaction_status(offer["_id"], status="accepted")
                notify_user(offer["loan_agent"], f"{username} accepted your loan offer.")
                st.success("Offer accepted successfully!")

    elif page == "Print Transactions":
        st.subheader("Transaction History")
        username = st.session_state.user
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        transactions = get_transactions_by_user(username, role="loan_receiver", start_date=start_date, end_date=end_date)

        # Display transactions
        if transactions:
            df = pd.DataFrame(transactions)
            st.dataframe(df)
            if st.button("Download as Excel"):
                df.to_excel("loan_receiver_transactions.xlsx", index=False)
                st.success("Transactions exported to Excel!")
        else:
            st.write("No transactions found for the selected date range.")
