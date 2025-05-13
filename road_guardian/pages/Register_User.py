import streamlit as st
from datetime import datetime
import random
import re
from db import register_user

st.set_page_config(page_title="🧍 User Registration")

st.title("🧍 Register as a Road Guardian User")

st.markdown("Create your account to access roadside services instantly.")

with st.form("user_registration_form"):
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")
    region = st.selectbox("Region", ["North", "South", "East", "West", "Central", "North-East"])
    state = st.text_input("State")
    city = st.text_input("City")
    otp = st.text_input("Enter OTP (simulated)", max_chars=6)

    if st.form_submit_button("Send OTP"):
        otp_code = str(random.randint(100000, 999999))
        st.session_state.otp_code = otp_code
        st.info(f"(Simulated) OTP sent: {otp_code}")

    if st.form_submit_button("Register"):
        # Debug: Log raw form inputs
        st.write("Debug: Raw form inputs:", {
            "name": name,
            "phone": phone,
            "email": email,
            "password": password,
            "region": region,
            "state": state,
            "city": city,
            "otp": otp
        })

        if not (name and phone and email and password and state and city):
            st.error("❌ All fields are required.")
        else:
            # Strip whitespace from inputs
            user_data = {
                "name": name.strip(),
                "phone": phone.strip(),
                "email": email.strip(),
                "password": password,
                "region": region,
                "state": state.strip(),
                "city": city.strip(),
                "registered_at": datetime.now().isoformat()
            }

            # Debug: Log user_data after stripping
            st.write("Debug: User data after stripping:", user_data)

            # Validate phone number format (at least 10 digits)
            phone_pattern = re.compile(r'^\d{10,}$')
            if not user_data["phone"]:
                st.error("❌ Phone number cannot be empty.")
            elif not phone_pattern.match(user_data["phone"]):
                st.error("❌ Phone number must be at least 10 digits.")
            elif otp != st.session_state.get("otp_code"):
                st.error("❌ Incorrect OTP.")
            else:
                # Debug: Final user_data before registration
                st.write("Debug: Final user_data being sent to register_user:", user_data)
                try:
                    if register_user(user_data):
                        st.success(f"✅ Welcome, {name}! You’ve been registered.")
                        st.info(f"🗺️ You’re located in {city}, {state} — Region: {region}")
                        # Clear form state and refresh the page
                        st.session_state.otp_code = None
                        st.rerun()  # Updated from st.experimental_rerun() to st.rerun()
                    else:
                        st.error("❌ Phone number already registered.")
                except Exception as e:
                    st.error(f"❌ Registration failed: {str(e)}")