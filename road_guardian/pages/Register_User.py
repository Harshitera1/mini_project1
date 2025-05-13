import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="🧍 User Registration")

st.title("🧍 Register as a Road Guardian User")

st.markdown("Create your account to access roadside services instantly.")

with st.form("user_registration_form"):
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")
    region = st.selectbox("Region", ["North", "South", "East", "West", "Central", "North-East"])
    state = st.text_input("State")
    city = st.text_input("City")
    otp = st.text_input("Enter OTP (simulated)", max_chars=6)

    if st.form_submit_button("Send OTP"):
        otp_code = str(random.randint(100000, 999999))
        st.session_state.otp_code = otp_code
        st.info(f"(Simulated) OTP sent: {otp_code}")

    if st.form_submit_button("Register"):
        if not (name and phone and email and state and city):
            st.error("❌ All fields are required.")
        elif otp != st.session_state.get("otp_code"):
            st.error("❌ Incorrect OTP.")
        else:
            user_data = {
                "name": name,
                "phone": phone,
                "email": email,
                "region": region,
                "state": state,
                "city": city,
                "registered_at": datetime.now().isoformat()
            }
            if "users" not in st.session_state:
                st.session_state.users = []
            st.session_state.users.append(user_data)
            st.success(f"✅ Welcome, {name}! You’ve been registered.")
            st.info(f"🗺️ You’re located in {city}, {state} — Region: {region}")
