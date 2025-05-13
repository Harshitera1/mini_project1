import streamlit as st
import pandas as pd
from db import get_mechanics, add_booking, get_user_bookings, rate_mechanic, get_average_rating
from helpers import estimate_repair_time, calculate_distance, estimate_eta_and_cost, get_youtube_link
from geopy.geocoders import Nominatim

st.set_page_config(page_title="🛣️ Road Guardian", layout="centered")

if not st.session_state.get("logged_in", False):
    st.error("Please log in to access this page.")
    st.markdown("[Login](/Login)", unsafe_allow_html=True)
    st.stop()

st.title("🛠️ Road Guardian - Get Help")
st.subheader("Describe your problem and location to find nearby mechanics.")

with st.form("help_form"):
    problem_description = st.text_area("Describe your problem (e.g., flat tire, engine trouble):")
    user_location = st.text_input("Enter your location (e.g., Connaught Place, Delhi):")
    submitted = st.form_submit_button("Find Help")

if submitted:
    if not (problem_description and user_location):
        st.warning("Please enter both your problem and location.")
        st.stop()

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

    service_keywords = {
        "Flat Tire Support": ["flat", "tire", "tyre", "puncture"],
        "Engine Trouble": ["engine", "start", "stall", "overheat"],
        "Battery Jump": ["battery", "jump", "dead", "charge"],
        "Vehicle Towing": ["tow", "stuck", "accident", "breakdown"],
        "Condition Analysis": ["check", "analysis", "inspection", "diagnosis"],
        "Emergency (Call Police)": ["emergency", "police", "help"]
    }

    desc_words = problem_description.lower().split()
    matched_services = [service for service, keywords in service_keywords.items() if any(word in keywords for word in desc_words)]

    if not matched_services:
        st.warning("No matching services found. Try rephrasing your problem.")
    else:
        mechanics = get_mechanics()
        filtered_mechanics = []
        for m in mechanics:
            for service in matched_services:
                if service in m.get("services", []):
                    distance_km = calculate_distance(user_lat, user_lon, m["lat"], m["lon"])
                    eta, cost = estimate_eta_and_cost(distance_km, service)
                    m["distance_km"] = round(distance_km, 2)
                    m["eta_min"] = eta
                    m["cost"] = cost
                    filtered_mechanics.append(m)
                    break

        filtered_mechanics.sort(key=lambda x: x["distance_km"])
        top_10_mechanics = filtered_mechanics[:10]

        if top_10_mechanics:
            st.success(f"Found {len(top_10_mechanics)} mechanics near {user_location}:")
            for m in top_10_mechanics:
                st.write(f"🔧 **{m['name']}**")
                st.write(f"📍 Location: {m['location']} ({m['distance_km']} km away)")
                st.write(f"💸 Cost: ₹{m['cost']}")
                st.write(f"⏱️ ETA: {m['eta_min']} min")
                repair_time = estimate_repair_time(next(s for s in matched_services if s in m["services"]))
                st.write(f"🛠️ Estimated Repair Time: {repair_time} minutes")
                yt_link = get_youtube_link(next(s for s in matched_services if s in m["services"]))
                st.markdown(f"[🎥 How to deal with this issue]({yt_link})", unsafe_allow_html=True)
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

                with st.expander("Rate this mechanic"):
                    user_rating = st.slider("Rate from 1 to 5", 1, 5, key=f"rating_{m['name']}")
                    user_comment = st.text_area("Optional comment", key=f"comment_{m['name']}")
                    if st.button(f"Submit Rating for {m['name']}", key=f"submit_{m['name']}"):
                        review = {"rating": user_rating}
                        if user_comment:
                            review["comment"] = user_comment
                        rate_mechanic(m['name'], review)
                        st.success("Thank you! Your rating has been submitted.")

                if st.button(f"📞 Request {m['name']}", key=m['name']):
                    booking = {
                        "user_name": st.session_state.user_mobile,
                        "mechanic": m['name'],
                        "location": m['location'],
                        "service": next(s for s in matched_services if s in m["services"]),
                        "cost": m['cost'],
                        "eta": m['eta_min'],
                        "mechanic_lat": m['lat'],
                        "mechanic_lon": m['lon']
                    }
                    add_booking(booking)
                    st.success(f"✅ Help requested from {m['name']}! ETA: {m['eta_min']} min.")
                    st.write(f"📍 Mechanic Location: {m['location']}")
                    st.write(f"⏱️ ETA: {m['eta_min']} min")
                    st.write(f"⭐ Rating: {avg_rating}")
                    st.map(pd.DataFrame([{"latitude": m['lat'], "longitude": m['lon']}]))
                st.markdown("---")

            df = pd.DataFrame(top_10_mechanics).rename(columns={"lat": "latitude", "lon": "longitude"})
            st.map(df)
        else:
            st.warning(f"No mechanics found near {user_location} for your problem.")

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
        if 'mechanic_lat' in b and 'mechanic_lon' in b:
            st.map(pd.DataFrame([{"latitude": b['mechanic_lat'], "longitude": b['mechanic_lon']}]))
        st.markdown("---")
else:
    st.info("No bookings made yet.")

st.caption("Built with ❤️ using Streamlit")