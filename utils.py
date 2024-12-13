import streamlit as st
def validate_password(password, confirm_password):
    return password == confirm_password

def check_user_role(username):
    from database import check_username_exists
    user = check_username_exists(username)
    if user:
        return user.get("type")
    return None

def notify_user(username, message):
    # Simulate notification (can be extended for email/real-time notifications)
    st.write(f"Notification for {username}: {message}")
