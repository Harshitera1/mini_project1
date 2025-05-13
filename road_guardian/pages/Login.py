import streamlit as st
from db import verify_user

st.set_page_config(page_title="🔐 Login - Road Guardian")

st.title("🔐 Login to Road Guardian")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_mobile" not in st.session_state:
    st.session_state.user_mobile = ""

with st.form("login_form"):
    mobile = st.text_input("Enter your mobile number")
    password = st.text_input("Enter your password", type="password")
    submit_btn = st.form_submit_button("Login")

    if submit_btn:
        if mobile and password:
            if verify_user(mobile, password):
                st.session_state.user_mobile = mobile
                st.session_state.logged_in = True
                st.success(f"✅ Logged in as {mobile}")
                st.rerun()
            else:
                st.error("❌ Invalid mobile number or password.")
        else:
            st.error("❌ Please enter both mobile number and password.")

if st.session_state.logged_in:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_mobile = ""
        st.success("✅ Logged out successfully")
        st.experimental_rerun()