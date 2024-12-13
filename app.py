import streamlit as st
from utils import check_user_role
from pages import auth, loan_agent, loan_receiver

# Main app navigation
def main():
    st.title("Loan Application System")

    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        role = check_user_role(st.session_state.user)
        if role == "loan_agent":
            loan_agent.show_loan_agent_dashboard()
        elif role == "loan_receiver":
            loan_receiver.show_loan_receiver_dashboard()
    else:
        auth.show_auth_page()

if __name__ == "__main__":
    main()
