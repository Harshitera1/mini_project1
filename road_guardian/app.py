# app.py

import streamlit as st
import pandas as pd
from db import get_mechanics, seed_mechanics
from helpers import estimate_repair_time

st.set_page_config(page_title="🛣️ Road Guardian", layout="centered")

# Seed mechanics (if needed)
seed_mechanics()

# Session state for bookings
if "bookings" not in st.session_state:
    st.session_state.bookings = []

# App header
st.title("🛠️ Road Guardian")
st.subheader("Your Nationwide Roadside Help Companion")

# Select service
services = [
    "Flat Tire Support",
    "Engine Trouble",
    "Battery Jump",
    "Vehicle Towing",
    "Condition Analysis",
    "Emergency (Call Police)"
]
selected_service = st.selectbox("🔧 Choose a service you need:", services)

# Emergency trigger
if selected_service == "Emergency (Call Police)":
    st.error("🚨 Emergency Mode Activated!")
    st.markdown("#### 📞 Call Emergency Contacts:")
    st.write("👮 Police: 100")
    st.write("🚑 Ambulance: 102")
    st.write("🔥 Fire Brigade: 101")
    st.map(pd.DataFrame([{"latitude": 28.6139, "longitude": 77.2090}]))  # Delhi Police HQ
    st.warning("Stay calm. Help is on the way.")
    st.stop()

# Location inputs
st.markdown("## 📍 Your Location")
region = st.selectbox("Select Region", ["North", "South", "East", "West", "Central", "North-East"])
state = st.text_input("Enter State")
city = st.text_input("Enter City")

if not (state and city):
    st.warning("Please enter your state and city to continue.")
    st.stop()

# Load mechanics and filter
mechanics = get_mechanics()
filtered_mechanics = [
    m for m in mechanics
    if selected_service in m.get("services", []) and
       m.get("region") == region and
       state.lower() in m.get("state", "").lower() and
       city.lower() in m.get("city", "").lower()
]

# Show results
if filtered_mechanics:
    st.success(f"🔍 Found {len(filtered_mechanics)} mechanics in {city}, {state} for {selected_service}:")

    for m in filtered_mechanics:
        st.write(f"🔧 **{m['name']}**")
        st.write(f"📍 Location: {m['location']}")
        st.write(f"💸 Cost: ₹{m['cost']}")
        st.write(f"⏱️ ETA: {m['eta_min']} min")
        repair_time = estimate_repair_time(selected_service)
        st.write(f"🛠️ Estimated Repair Time: {repair_time} minutes")

        if st.button(f"📞 Request {m['name']}", key=m['name']):
            booking = {
                "mechanic": m['name'],
                "location": m['location'],
                "service": selected_service,
                "cost": m['cost'],
                "eta": m['eta_min']
            }
            st.session_state.bookings.append(booking)
            st.success(f"✅ Help requested from {m['name']}! ETA: {m['eta_min']} minutes.")

        st.markdown("---")

    # Map view
    df = pd.DataFrame(filtered_mechanics)
    df = df.rename(columns={"lat": "latitude", "lon": "longitude"})
    st.map(df)
else:
    st.warning(f"No mechanics found in {city}, {state} for '{selected_service}'.")

# Booking history
st.markdown("## 📋 Your Booking History")
if st.session_state.bookings:
    for i, b in enumerate(st.session_state.bookings):
        st.write(f"### Booking #{i+1}")
        st.write(f"🔧 Mechanic: {b['mechanic']}")
        st.write(f"📍 Location: {b['location']}")
        st.write(f"🛠️ Service: {b['service']}")
        st.write(f"💸 Cost: ₹{b['cost']}")
        st.write(f"⏱️ ETA: {b['eta']} minutes")
        st.markdown("---")
else:
    st.info("No bookings made yet.")

st.caption("Built with ❤️ using Streamlit")
