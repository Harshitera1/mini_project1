# app.py

import streamlit as st
import pandas as pd
from db import get_mechanics, seed_mechanics
from helpers import estimate_repair_time

st.set_page_config(page_title="🛣️ Road Guardian", layout="centered")

# Initialize database
seed_mechanics()

# App header
st.title("🛠️ Road Guardian")
st.subheader("Your Personal Roadside Help Companion")

# Service options
services = [
    "Flat Tire Support",
    "Engine Trouble",
    "Battery Jump",
    "Vehicle Towing",
    "Condition Analysis",
    "Emergency (Call Police)"
]

selected_service = st.selectbox("Choose a service you need:", services)

# Emergency handling
if selected_service == "Emergency (Call Police)":
    st.error("🚨 Emergency Mode Activated!")
    st.markdown("#### 📞 Call Emergency Contacts:")
    st.write("👮 Mumbai Police: 100")
    st.write("🚑 Ambulance: 102")
    st.write("🔥 Fire Brigade: 101")

    st.markdown("### 📍 Nearest Police Station")
    st.map(pd.DataFrame([{
        "latitude": 19.1140,
        "longitude": 72.8470
    }]))

    st.warning("Please stay calm. Authorities have been alerted.")
    st.balloons()
    st.stop()

# Location Input
user_location = st.text_input("📍 Enter your location (e.g., Andheri West, Bandra East):")

if not user_location:
    st.warning("Please enter your location to view nearby mechanics.")
    st.stop()

# Load mechanics and filter by service
mechanics = get_mechanics()
filtered_mechanics = [m for m in mechanics if selected_service in m.get("services", [])]

if filtered_mechanics:
    st.success(f"Mechanics available for {selected_service} near {user_location}:")

    for m in filtered_mechanics:
        st.write(f"🔧 **{m['name']}**")
        st.write(f"📍 Location: {m['location']}")
        st.write(f"💸 Cost: ₹{m['cost']}")
        st.write(f"⏱️ ETA: {m['eta_min']} min")
        repair_time = estimate_repair_time(selected_service)
        st.write(f"🛠️ Estimated Repair Time: {repair_time} minutes")

        if st.button(f"📞 Request {m['name']}", key=m['name']):
            st.success(f"✅ Help requested from {m['name']}! They'll reach you in approx {m['eta_min']} minutes.")
        st.markdown("---")

    # Show on map
    df = pd.DataFrame(filtered_mechanics)
    df = df.rename(columns={"lat": "latitude", "lon": "longitude"})
    st.map(df)
else:
    st.warning(f"No mechanics found for '{selected_service}' near {user_location}.")

st.caption("Built with ❤️ using Streamlit")
