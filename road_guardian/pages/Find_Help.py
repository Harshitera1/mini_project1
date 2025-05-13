import streamlit as st
import pandas as pd
from db import get_mechanics
from helpers import estimate_repair_time

st.set_page_config(page_title="🔧 Find Help - Road Guardian")

st.title("🛠️ Find Nearby Help")
st.subheader("Select a service and your location to find the best mechanic near you.")

# Service options
services = [
    "Flat Tire Support",
    "Engine Trouble",
    "Battery Jump",
    "Vehicle Towing",
    "Condition Analysis",
    "Emergency (Call Police)"
]

selected_service = st.selectbox("Choose a service:", services)

# User location input
user_location = st.text_input("📍 Enter your location (e.g., Andheri West, Bandra East):")

if selected_service == "Emergency (Call Police)":
    st.error("🚨 Emergency triggered. Notifying local authorities...")
    st.balloons()
    st.stop()

if not user_location:
    st.warning("Please enter your location to continue.")
    st.stop()

# Load mechanics and filter
mechanics = get_mechanics()
filtered = [m for m in mechanics if selected_service in m.get("services", [])]

if filtered:
    st.success(f"Mechanics available for **{selected_service}** near **{user_location}**:")
    for m in filtered:
        st.write(f"🔧 **{m['name']}**")
        st.write(f"📍 Location: {m['location']}")
        st.write(f"💸 Cost: ₹{m['cost']}")
        st.write(f"⏱️ ETA: {m['eta_min']} minutes")
        repair_time = estimate_repair_time(selected_service)
        st.write(f"🛠️ Estimated Repair Time: {repair_time} minutes")

        if st.button(f"📞 Request {m['name']}", key=m['name']):
            st.success(f"✅ Help requested from {m['name']}! ETA: {m['eta_min']} minutes.")

        st.markdown("---")

    # Show mechanic locations on map
    df = pd.DataFrame(filtered)
    df = df.rename(columns={"lat": "latitude", "lon": "longitude"})
    st.map(df)
else:
    st.warning(f"No available mechanics found for **{selected_service}** near **{user_location}**.")
