import streamlit as st
import pandas as pd
from db import get_mechanics, seed_mechanics, add_booking, get_user_bookings, rate_mechanic, get_average_rating
from helpers import estimate_repair_time, get_youtube_link, calculate_distance, estimate_eta_and_cost

st.set_page_config(page_title="🛣️ Road Guardian", layout="centered")

# Seed mechanics if needed
seed_mechanics()

# Session for user login
if "user_mobile" not in st.session_state:
    st.session_state.user_mobile = ""

# User login/registration
st.markdown("### 📱 User Login / Register")
st.session_state.user_mobile = st.text_input("Enter your mobile number to continue")

if not st.session_state.user_mobile:
    st.warning("Please enter your mobile number to proceed.")
    st.stop()

# App Header
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

# Emergency Handling
if selected_service == "Emergency (Call Police)":
    st.error("🚨 Emergency Mode Activated!")
    st.markdown("#### 📞 Call Emergency Contacts:")
    st.write("👮 Police: 100")
    st.write("🚑 Ambulance: 102")
    st.write("🔥 Fire Brigade: 101")
    st.map(pd.DataFrame([{"latitude": 28.6139, "longitude": 77.2090}]))  # Delhi Police HQ
    st.warning("Stay calm. Help is on the way.")
    st.stop()

# User Location Input
st.markdown("## 📍 Your Location")
region = st.selectbox("Select Region", ["North", "South", "East", "West", "Central", "North-East"])
state = st.text_input("Enter State")
city = st.text_input("Enter City")

# GPS input
user_lat = st.number_input("Enter your Latitude", format="%.6f")
user_lon = st.number_input("Enter your Longitude", format="%.6f")

if not (state and city):
    st.warning("Please enter your state and city to continue.")
    st.stop()

# Fetch and filter mechanics
mechanics = get_mechanics()
filtered_mechanics = [
    m for m in mechanics
    if selected_service in m.get("services", []) and
       m.get("region") == region and
       state.lower() in m.get("state", "").lower() and
       city.lower() in m.get("city", "").lower()
]

# Show mechanics
if filtered_mechanics:
    st.success(f"🔍 Found {len(filtered_mechanics)} mechanics in {city}, {state} for {selected_service}:")

    for m in filtered_mechanics:
        m["distance_km"] = round(calculate_distance(user_lat, user_lon, m["lat"], m["lon"]), 2)
        m["eta_min"], m["cost"] = estimate_eta_and_cost(m["distance_km"], selected_service)

        st.write(f"🔧 **{m['name']}**")
        st.write(f"📍 Location: {m['location']}")
        st.write(f"📶 Distance: {m['distance_km']} km")
        st.write(f"💸 Cost: ₹{m['cost']}")
        st.write(f"⏱️ ETA: {m['eta_min']} min")

        repair_time = estimate_repair_time(selected_service)
        st.write(f"🛠️ Estimated Repair Time: {repair_time} minutes")
        yt_link = get_youtube_link(selected_service)
        st.markdown(f"[🎥 How to deal with this issue]({yt_link})", unsafe_allow_html=True)

        avg_rating = get_average_rating(m)
        st.write(f"⭐ Average Rating: {avg_rating}")

        with st.expander("Rate this mechanic"):
            user_rating = st.slider("Rate from 1 (worst) to 5 (best)", 1, 5, key=f"rating_{m['name']}")
            if st.button(f"Submit Rating for {m['name']}", key=f"submit_{m['name']}"):
                rate_mechanic(m['name'], user_rating)
                st.success("Thank you! Your rating has been submitted.")

        if st.button(f"📞 Request {m['name']}", key=m['name']):
            booking = {
                "user_name": st.session_state.user_mobile,
                "mechanic": m['name'],
                "location": m['location'],
                "service": selected_service,
                "cost": m['cost'],
                "eta": m['eta_min']
            }
            add_booking(booking)
            st.success(f"✅ Help requested from {m['name']}! ETA: {m['eta_min']} minutes.")

        st.markdown("---")

    # Show map
    df = pd.DataFrame(filtered_mechanics).rename(columns={"lat": "latitude", "lon": "longitude"})
    st.map(df)
else:
    st.warning(f"No mechanics found in {city}, {state} for '{selected_service}'.")

# Booking history
st.markdown("## 📋 Your Booking History")
bookings = get_user_bookings(st.session_state.user_mobile)
if bookings:
    for i, b in enumerate(bookings):
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
