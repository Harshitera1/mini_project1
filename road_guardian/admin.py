import streamlit as st
from db import get_mechanics, add_mechanic

st.set_page_config(page_title="Admin Panel", layout="centered")

st.title("🔐 Admin Panel - Road Guardian")

st.header("📋 Current Mechanics List")
mechanics = get_mechanics()

if mechanics:
    for m in mechanics:
        st.write(f"**Name**: {m['name']}")
        st.write(f"📍 Location: {m['location']}")
        st.write(f"🛠 Services: {', '.join(m['services'])}")
        st.write(f"💸 Cost: ₹{m['cost']}")
        st.write(f"📍 Lat/Lon: ({m['lat']}, {m['lon']})")
        st.markdown("---")
else:
    st.warning("No mechanics found.")

st.header("➕ Add New Mechanic")
with st.form("add_mechanic_form"):
    name = st.text_input("Name")
    location = st.text_input("Location")
    services_input = st.text_input("Services (comma-separated)")
    cost = st.number_input("Cost (₹)", min_value=100, step=50)
    eta = st.number_input("ETA (in minutes)", min_value=5, step=1)
    lat = st.number_input("Latitude", format="%.6f")
    lon = st.number_input("Longitude", format="%.6f")
    submit_btn = st.form_submit_button("Add Mechanic")

    if submit_btn:
        if not name or not location or not services_input:
            st.error("Please fill all required fields.")
        else:
            services = [s.strip() for s in services_input.split(",")]
            new_mechanic = {
                "name": name,
                "location": location,
                "services": services,
                "cost": cost,
                "distance_km": 1.0,
                "eta_min": eta,
                "lat": lat,
                "lon": lon
            }
            add_mechanic(new_mechanic)
            st.success(f"✅ Mechanic '{name}' added successfully!")
            st.experimental_rerun()
