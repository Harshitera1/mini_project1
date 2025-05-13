# road_guardian/pages/Register_Mechanic.py

import streamlit as st
from db import add_mechanic

st.set_page_config(page_title="🔧 Mechanic Registration")

st.title("🔧 Register Yourself as a Mechanic")

st.markdown("Provide your location, services, and contact details. Your profile will be shown to users in need.")

with st.form("mechanic_registration_form"):
    name = st.text_input("Full Name")
    region = st.selectbox("Region", ["North", "South", "East", "West", "Central", "North-East"])
    state = st.text_input("State")
    city = st.text_input("City")
    location = st.text_input("Detailed Location (e.g., Sector 18, Noida)")
    services_input = st.text_input("Services Offered (comma-separated)")
    cost = st.number_input("Service Cost (₹)", min_value=100, step=50)
    eta = st.number_input("ETA to Reach (minutes)", min_value=5, step=1)
    lat = st.number_input("Latitude", format="%.6f")
    lon = st.number_input("Longitude", format="%.6f")

    submit_btn = st.form_submit_button("Submit Registration")

    if submit_btn:
        if not (name and state and city and location and services_input):
            st.error("❌ Please fill all required fields.")
        else:
            services = [s.strip() for s in services_input.split(",")]
            new_mechanic = {
                "name": name,
                "region": region,
                "state": state,
                "city": city,
                "location": location,
                "services": services,
                "cost": cost,
                "distance_km": 1.0,  # Can be dynamically calculated later
                "eta_min": eta,
                "lat": lat,
                "lon": lon
            }
            add_mechanic(new_mechanic)
            st.success(f"✅ Mechanic {name} registered successfully!")
            st.map([{"latitude": lat, "longitude": lon}])
