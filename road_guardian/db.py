import os
from pymongo import MongoClient, errors
from dotenv import load_dotenv
import random

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "").strip()
_use_mock = False

# Attempt MongoDB connection
if MONGO_URI:
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        db = client["road_guardian"]
        mechanics_collection = db["mechanics"]
        bookings_collection = db["bookings"]
        print("✅ Connected to MongoDB Atlas.")
    except errors.PyMongoError as e:
        print(f"⚠️ MongoDB connection failed: {e}")
        _use_mock = True
else:
    print("⚠️ No MONGO_URI found in .env; using mock mode.")
    _use_mock = True

# Sample mechanics for demonstration (Delhi and Uttar Pradesh)
_mock_mechanics = [
    # Delhi
    {
        "name": "Raj Sharma Mechanics",
        "region": "North",
        "state": "Delhi",
        "city": "Connaught Place",
        "location": "Connaught Place, Delhi",
        "services": ["Flat Tire Support", "Battery Jump", "Vehicle Towing"],
        "lat": 28.6315,
        "lon": 77.2167,
        "reviews": []
    },
    {
        "name": "Amit Verma Mechanics",
        "region": "North",
        "state": "Delhi",
        "city": "Karol Bagh",
        "location": "Karol Bagh, Delhi",
        "services": ["Engine Trouble", "Vehicle Towing"],
        "lat": 28.6514,
        "lon": 77.1907,
        "reviews": []
    },
    {
        "name": "Suresh Gupta Mechanics",
        "region": "North",
        "state": "Delhi",
        "city": "Dwarka",
        "location": "Dwarka, Delhi",
        "services": ["Condition Analysis", "Battery Jump"],
        "lat": 28.5921,
        "lon": 77.0460,
        "reviews": []
    },
    # Uttar Pradesh
    {
        "name": "Vikram Singh Mechanics",
        "region": "North",
        "state": "Uttar Pradesh",
        "city": "Noida",
        "location": "Noida, Uttar Pradesh",
        "services": ["Flat Tire Support", "Engine Trouble"],
        "lat": 28.5708,
        "lon": 77.3260,
        "reviews": []
    },
    {
        "name": "Priya Kumar Mechanics",
        "region": "North",
        "state": "Uttar Pradesh",
        "city": "Lucknow",
        "location": "Lucknow, Uttar Pradesh",
        "services": ["Battery Jump", "Vehicle Towing"],
        "lat": 26.8467,
        "lon": 80.9462,
        "reviews": []
    },
    {
        "name": "Neha Patel Mechanics",
        "region": "North",
        "state": "Uttar Pradesh",
        "city": "Agra",
        "location": "Agra, Uttar Pradesh",
        "services": ["Condition Analysis", "Flat Tire Support"],
        "lat": 27.1767,
        "lon": 78.0081,
        "reviews": []
    },
    # Extend with 3 mechanics per state using a dataset
]

_mock_bookings = []

def seed_mechanics(force=False):
    """Seed MongoDB with mechanics data, clearing existing if forced"""
    if _use_mock:
        print("ℹ️ Running in MOCK mode — skipping seeding.")
        return

    if force or mechanics_collection.count_documents({}) == 0:
        if force:
            mechanics_collection.delete_many({})
            print("🗑️ Cleared all existing mechanics.")
        
        mechanics_collection.insert_many(_mock_mechanics)
        print("✅ Seeded mechanics into MongoDB.")

def get_mechanics():
    """Fetch all mechanics from database"""
    if _use_mock:
        print("🔁 Returning mechanics from MOCK data.")
        return list(_mock_mechanics)

    if mechanics_collection.count_documents({}) == 0:
        print("📦 MongoDB empty — seeding with mechanics.")
        seed_mechanics()
    
    return list(mechanics_collection.find({}, {"_id": 0}))

def add_mechanic(mechanic_data):
    """Add a new mechanic"""
    if _use_mock:
        _mock_mechanics.append(mechanic_data)
        print(f"ℹ️ (MOCK) Added mechanic: {mechanic_data['name']}")
    else:
        mechanics_collection.insert_one(mechanic_data)
        print(f"✅ Added mechanic to MongoDB: {mechanic_data['name']}")

def add_booking(booking_data):
    """Add a booking record"""
    if _use_mock:
        _mock_bookings.append(booking_data)
        print(f"📝 (MOCK) Booking added: {booking_data['user_name']} -> {booking_data['mechanic']}")
    else:
        bookings_collection.insert_one(booking_data)
        print(f"📝 Booking added to MongoDB for user: {booking_data['user_name']}")

def get_user_bookings(user_name):
    """Retrieve bookings made by a specific user"""
    if _use_mock:
        return [b for b in _mock_bookings if b["user_name"] == user_name]
    return list(bookings_collection.find({"user_name": user_name}, {"_id": 0}))

def rate_mechanic(name, review):
    """Store review (rating and optional comment) for a mechanic"""
    if _use_mock:
        for mech in _mock_mechanics:
            if mech["name"] == name:
                mech.setdefault("reviews", []).append(review)
                return
    else:
        mechanics_collection.update_one(
            {"name": name},
            {"$push": {"reviews": review}}
        )

def get_average_rating(mechanic):
    """Calculate average rating from reviews"""
    reviews = mechanic.get("reviews", [])
    ratings = [r["rating"] for r in reviews if "rating" in r]
    return round(sum(ratings) / len(ratings), 1) if ratings else "No ratings"