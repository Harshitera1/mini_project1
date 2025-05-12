import streamlit as st
import pandas as pd
from db import get_mechanics, seed_mechanics

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

if selected_service and selected_service != "Emergency (Call Police)":
    mechanics = get_mechanics()
    if mechanics:
        st.success(f"Mechanics available for {selected_service}:")

        for m in mechanics:
            st.write(f"🔧 **{m['name']}**")
            st.write(f"📍 Location: {m['location']}")
            st.write(f"💸 Cost: ₹{m['cost']}")
            st.write(f"⏱️ ETA: {m['eta_min']} min")
            st.markdown("---")

        # Map
        df = pd.DataFrame(mechanics)
        df = df.rename(columns={"lat": "latitude", "lon": "longitude"})
        st.map(df)
    else:
        st.warning("No mechanics found.")
elif selected_service == "Emergency (Call Police)":
    st.error("🚨 Alert: Notifying local police...")
    st.balloons()

st.caption("Built with ❤️ using Streamlit")
