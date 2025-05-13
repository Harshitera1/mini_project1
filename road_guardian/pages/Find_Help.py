import streamlit as st
import pandas as pd
from db import get_mechanics, get_average_rating
from helpers import estimate_repair_time, calculate_distance, estimate_eta_and_cost
from geopy.geocoders import Nominatim

st.set_page_config(page_title="🔧 Find Help - Road Guardian")

st.title("🛠️ Find Nearby Help")
st.subheader("Describe your problem and location to find mechanics near you.")

# User inputs
problem_description = st.text_input("Describe your problem (e.g., flat tire, engine trouble):")
user_location = st.text_input("📍 Enter your location (e.g., Connaught Place, Delhi):")

if not (problem_description and user_location):
    st.warning("Please enter both your problem and location to continue.")
    st.stop()

# Geocode user location
geolocator = Nominatim(user_agent="road_guardian")
try:
    location = geolocator.geocode(user_location)
    if location:
        user_lat, user_lon = location.latitude, location.longitude
    else:
        st.error("Location not found. Please try a different location.")
        st.stop()
except Exception as e:
    st.error(f"Geocoding error: {e}")
    st.stop()

# Service keyword mapping for partial matching
service_keywords = {
    "Flat Tire Support": ["flat", "tire", "tyre", "puncture"],
    "Engine Trouble": ["engine", "start", "stall", "overheat"],
    "Battery Jump": ["battery", "jump", "dead", "charge"],
    "Vehicle Towing": ["tow", "stuck", "accident", "breakdown"],
    "Condition Analysis": ["check", "analysis", "inspection", "diagnosis"]
}
all_services = list(service_keywords.keys())

# Match services based on problem description
desc_words = problem_description.lower().split()
matched_services = []
for service, keywords in service_keywords.items():
    if any(word in keywords for word in desc_words):
        matched_services.append(service)

if not matched_services:
    st.warning("No matching services found. Try rephrasing your problem.")
    st.stop()

# Load and filter mechanics
mechanics = get_mechanics()
filtered = [m for m in mechanics if any(s in m.get("services", []) for s in matched_services)]

# Calculate distances and sort
for m in filtered:
    m["distance_km"] = calculate_distance(user_lat, user_lon, m["lat"], m["lon"])
filtered.sort(key=lambda x: x["distance_km"])

# Display mechanics
if filtered:
    st.success(f"Mechanics available near **{user_location}** for your problem:")

    for m in filtered:
        st.write(f"🔧 **{m['name']}**")
        st.write(f"📍 Location: {m['location']}")
        st.write(f"📶 Distance: {m['distance_km']:.2f} km")
        
        # Find matching service for ETA/cost (use first match)
        matched_service = next((s for s in matched_services if s in m["services"]), None)
        eta, cost = estimate_eta_and_cost(m["distance_km"], matched_service)
        st.write(f"⏱ ETA: {eta} minutes")
        st.write(f"💸 Cost: ₹{cost}")
        
        repair_time = estimate_repair_time(matched_service)
        st.write(f"🛠️ Estimated Repair Time: {repair_time} minutes")
        
        avg_rating = get_average_rating(m)
        st.write(f"⭐ Average Rating: {avg_rating}")
        
        with st.expander("View Reviews"):
            reviews = m.get("reviews", [])
            if reviews:
                for r in reviews:
                    st.write(f"Rating: {r['rating']}/5")
                    if "comment" in r:
                        st.write(f"Comment: {r['comment']}")
            else:
                st.write("No reviews yet.")
        
        if st.button(f"📞 Request {m['name']}", key=m["name"]):
            st.success(f"✅ Help requested from {m['name']}! ETA: {eta} minutes.")
        
        st.markdown("---")

    # Show map
    df = pd.DataFrame(filtered).rename(columns={"lat": "latitude", "lon": "longitude"})
    st.map(df)
else:
    st.warning(f"No mechanics found near **{user_location}** for your problem.")