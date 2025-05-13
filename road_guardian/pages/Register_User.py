# road_guardian/pages/Register_User.py

import streamlit as st
from datetime import datetime

st.set_page_config(page_title="🧍 User Registration")

st.title("🧍 Register as a Road Guardian User")

st.markdown("Create your account to access nationwide roadside services instantly.")

with st.form("user_registration_form"):
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")
    region = st.selectbox("Region", ["North", "South", "East", "West", "Central", "North-East"])
    state = st.text_input("State")
    city = st.text_input("City")

    submit = st.form_submit_button("Register")

    if submit:
        if not (name and phone and email and state and city):
            st.error("❌ All fields are required.")
        else:
            # Simulate storing user (expand later to MongoDB)
            user_data = {
                "name": name,
                "phone": phone,
                "email": email,
                "region": region,
                "state": state,
                "city": city,
                "role": "user",
                "registered_at": datetime.now().isoformat()
            }

            # Save in session or send to MongoDB (future)
            if "users" not in st.session_state:
                st.session_state.users = []

            st.session_state.users.append(user_data)

            st.success(f"✅ Welcome, {name}! You’ve been registered as a user.")
            st.info(f"🗺️ You’re located in {city}, {state} — Region: {region}")
