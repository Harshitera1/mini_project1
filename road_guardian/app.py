import streamlit as st

# Set page config
st.set_page_config(page_title="🛣️ Road Guardian", layout="centered")

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

# Fake mechanic info
if selected_service and selected_service != "Emergency (Call Police)":
    st.success(f"Mechanic found nearby for {selected_service}!")
    st.write("👨‍🔧 Name: Rahul Auto Services")
    st.write("📍 Distance: 1.2 km away")
    st.write("💸 Estimated Cost: ₹300")
    st.write("⏱️ Estimated Time of Arrival: 15 minutes")
    st.map()  # Optional map

elif selected_service == "Emergency (Call Police)":
    st.error("🚨 Alert: Notifying local police...")
    st.balloons()

# Footer
st.caption("Built with ❤️ using Streamlit")
