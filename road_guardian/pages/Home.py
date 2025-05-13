import streamlit as st

st.set_page_config(page_title="🏠 Home - Road Guardian")

st.title("🏠 Welcome to Road Guardian")
st.write("""
Road Guardian is your trusted companion on the road.

Whether you’re stuck with a flat tire, engine trouble, or need emergency help, we’ve got you covered!

👉 Use the sidebar to navigate through the app:
- **Find Help** to get nearby mechanics
- **About** to learn more about this project
- **Admin Panel** for management tools
""")
st.image("assets/home_banner.png", use_column_width=True)  # Optional if you have an image
