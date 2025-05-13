import os
from pymongo import MongoClient, errors
from dotenv import load_dotenv

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

# -----------------------------
# MOCK DATA (Fallback Mode)
# -----------------------------

_mock_mechanics = [
    {
        "name": "Delhi AutoHelp",
        "region": "North",
        "state": "Delhi",
        "city": "Connaught Place",
        "location": "Connaught Place, Delhi",
        "services": ["Flat Tire Support", "Battery Jump", "Towing"],
        "cost": 350,
        "distance_km": 1.2,
        "eta_min": 15,
        "lat": 28.6315,
        "lon": 77.2167
    },
    {
        "name": "Noida FixHub",
        "region": "North",
        "state": "Uttar Pradesh",
        "city": "Sector 18",
        "location": "Sector 18, Noida",
        "services": ["Engine Trouble", "Towing"],
        "cost": 400,
        "distance_km": 1.6,
        "eta_min": 18,
        "lat": 28.5708,
        "lon": 77.3260
    },
    {
        "name": "Gurgaon Speed Garage",
        "region": "North",
        "state": "Haryana",
        "city": "Cyber Hub",
        "location": "Cyber Hub, Gurgaon",
        "services": ["Flat Tire Support", "Condition Analysis"],
        "cost": 300,
        "distance_km": 1.0,
        "eta_min": 12,
        "lat": 28.4986,
        "lon": 77.0884
    },
    {
        "name": "Mumbai Mechanic Mart",
        "region": "West",
        "state": "Maharashtra",
        "city": "Dadar",
        "location": "Dadar, Mumbai",
        "services": ["Engine Trouble", "Flat Tire Support"],
        "cost": 400,
        "distance_km": 2.0,
        "eta_min": 20,
        "lat": 19.0176,
        "lon": 72.8562
    },
    {
        "name": "Bangalore Pit Stop",
        "region": "South",
        "state": "Karnataka",
        "city": "Koramangala",
        "location": "Koramangala, Bangalore",
        "services": ["Battery Jump", "Towing"],
        "cost": 300,
        "distance_km": 1.8,
        "eta_min": 12,
        "lat": 12.9352,
        "lon": 77.6140
    },
    {
        "name": "Chennai Car Doctor",
        "region": "South",
        "state": "Tamil Nadu",
        "city": "T Nagar",
        "location": "T Nagar, Chennai",
        "services": ["Engine Trouble", "Condition Analysis"],
        "cost": 500,
        "distance_km": 2.1,
        "eta_min": 18,
        "lat": 13.0418,
        "lon": 80.2337
    },
    {
        "name": "Kolkata TyreCare",
        "region": "East",
        "state": "West Bengal",
        "city": "Salt Lake",
        "location": "Salt Lake, Kolkata",
        "services": ["Flat Tire Support"],
        "cost": 250,
        "distance_km": 1.4,
        "eta_min": 10,
        "lat": 22.5793,
        "lon": 88.4310
    },
    {
        "name": "Hyderabad GarageGo",
        "region": "South",
        "state": "Telangana",
        "city": "Hitech City",
        "location": "Hitech City, Hyderabad",
        "services": ["Flat Tire Support", "Battery Jump"],
        "cost": 320,
        "distance_km": 1.6,
        "eta_min": 14,
        "lat": 17.4435,
        "lon": 78.3772
    }
]

_mock_bookings = []

# -----------------------------
# MECHANIC FUNCTIONS
# -----------------------------

def seed_mechanics():
    """Seed MongoDB or mock with pan-India mechanic data"""
    if _use_mock:
        print("ℹ️ Running in MOCK mode — skipping seeding.")
        return

    if mechanics_collection.count_documents({}) > 0:
        print("ℹ️ Mechanics already exist — skipping seeding.")
        return

    mechanics_collection.insert_many(_mock_mechanics)
    print("✅ Seeded pan-India mechanics into MongoDB.")

def get_mechanics():
    """Fetch all mechanics from database"""
    if _use_mock:
        return list(_mock_mechanics)
    return list(mechanics_collection.find({}, {"_id": 0}))

def add_mechanic(mechanic_data):
    """Add a new mechanic (from admin or registration form)"""
    if _use_mock:
        _mock_mechanics.append(mechanic_data)
        print(f"ℹ️ (MOCK) Added mechanic: {mechanic_data['name']}")
    else:
        mechanics_collection.insert_one(mechanic_data)
        print(f"✅ Added mechanic to MongoDB: {mechanic_data['name']}")

# -----------------------------
# BOOKING FUNCTIONS
# -----------------------------

def add_booking(booking_data):
    """Add a booking record to DB or mock"""
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
