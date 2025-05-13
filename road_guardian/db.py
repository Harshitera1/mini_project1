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
    },
    # 20 additional mechanics
    {
        "name": "Pune AutoCare",
        "region": "West",
        "state": "Maharashtra",
        "city": "Viman Nagar",
        "location": "Viman Nagar, Pune",
        "services": ["Battery Jump", "Towing"],
        "cost": 350,
        "distance_km": 1.2,
        "eta_min": 15,
        "lat": 18.5537,
        "lon": 73.9261
    },
    {
        "name": "Surat SpeedFix",
        "region": "West",
        "state": "Gujarat",
        "city": "Surat City",
        "location": "Surat City, Surat",
        "services": ["Engine Trouble", "Condition Analysis"],
        "cost": 400,
        "distance_km": 1.3,
        "eta_min": 18,
        "lat": 21.1702,
        "lon": 72.8311
    },
    {
        "name": "Indore Car Fix",
        "region": "Central",
        "state": "Madhya Pradesh",
        "city": "Indore City",
        "location": "Indore City, Indore",
        "services": ["Flat Tire Support", "Battery Jump"],
        "cost": 330,
        "distance_km": 1.0,
        "eta_min": 16,
        "lat": 22.7196,
        "lon": 75.8577
    },
    {
        "name": "Ahmedabad Auto Assist",
        "region": "West",
        "state": "Gujarat",
        "city": "Ghatlodia",
        "location": "Ghatlodia, Ahmedabad",
        "services": ["Engine Trouble", "Towing"],
        "cost": 450,
        "distance_km": 1.8,
        "eta_min": 19,
        "lat": 23.0675,
        "lon": 72.5386
    },
    {
        "name": "Lucknow QuickFix",
        "region": "North",
        "state": "Uttar Pradesh",
        "city": "Hazratganj",
        "location": "Hazratganj, Lucknow",
        "services": ["Flat Tire Support", "Engine Trouble"],
        "cost": 375,
        "distance_km": 1.4,
        "eta_min": 14,
        "lat": 26.8467,
        "lon": 80.9462
    },
    {
        "name": "Jaipur Pit Crew",
        "region": "North",
        "state": "Rajasthan",
        "city": "C-Scheme",
        "location": "C-Scheme, Jaipur",
        "services": ["Flat Tire Support", "Condition Analysis"],
        "cost": 300,
        "distance_km": 1.7,
        "eta_min": 12,
        "lat": 26.9124,
        "lon": 75.7873
    },
    {
        "name": "Bhopal Car Fixers",
        "region": "Central",
        "state": "Madhya Pradesh",
        "city": "TT Nagar",
        "location": "TT Nagar, Bhopal",
        "services": ["Towing", "Battery Jump"],
        "cost": 380,
        "distance_km": 1.6,
        "eta_min": 15,
        "lat": 23.2599,
        "lon": 77.4126
    },
    {
        "name": "Vijayawada Auto Rescue",
        "region": "South",
        "state": "Andhra Pradesh",
        "city": "Benz Circle",
        "location": "Benz Circle, Vijayawada",
        "services": ["Flat Tire Support", "Engine Trouble"],
        "cost": 350,
        "distance_km": 1.3,
        "eta_min": 14,
        "lat": 16.5061,
        "lon": 80.6480
    },
    {
        "name": "Patna Mechanic Hub",
        "region": "East",
        "state": "Bihar",
        "city": "Boring Road",
        "location": "Boring Road, Patna",
        "services": ["Battery Jump", "Engine Trouble"],
        "cost": 325,
        "distance_km": 1.4,
        "eta_min": 13,
        "lat": 25.5941,
        "lon": 85.1376
    },
    {
        "name": "Agra Quick Auto",
        "region": "North",
        "state": "Uttar Pradesh",
        "city": "Sadar Bazar",
        "location": "Sadar Bazar, Agra",
        "services": ["Flat Tire Support", "Towing"],
        "cost": 310,
        "distance_km": 1.5,
        "eta_min": 16,
        "lat": 27.1767,
        "lon": 78.0081
    },
    {
        "name": "Chandigarh AutoFix",
        "region": "North",
        "state": "Chandigarh",
        "city": "Sector 17",
        "location": "Sector 17, Chandigarh",
        "services": ["Engine Trouble", "Battery Jump"],
        "cost": 400,
        "distance_km": 1.2,
        "eta_min": 12,
        "lat": 30.7333,
        "lon": 76.7794
    },
    {
        "name": "Coimbatore FixAll",
        "region": "South",
        "state": "Tamil Nadu",
        "city": "Race Course",
        "location": "Race Course, Coimbatore",
        "services": ["Flat Tire Support", "Condition Analysis"],
        "cost": 370,
        "distance_km": 1.1,
        "eta_min": 15,
        "lat": 11.0168,
        "lon": 76.9558
    },
    {
        "name": "Nashik Car Doctor",
        "region": "West",
        "state": "Maharashtra",
        "city": "Gangapur Road",
        "location": "Gangapur Road, Nashik",
        "services": ["Towing", "Battery Jump"],
        "cost": 340,
        "distance_km": 1.2,
        "eta_min": 17,
        "lat": 20.0110,
        "lon": 73.7898
    },
    {
        "name": "Vadodara Car Garage",
        "region": "West",
        "state": "Gujarat",
        "city": "Alkapuri",
        "location": "Alkapuri, Vadodara",
        "services": ["Engine Trouble", "Towing"],
        "cost": 460,
        "distance_km": 1.7,
        "eta_min": 20,
        "lat": 22.3070,
        "lon": 73.1812
    },
    {
        "name": "Trivandrum Fixers",
        "region": "South",
        "state": "Kerala",
        "city": "Kumarapuram",
        "location": "Kumarapuram, Trivandrum",
        "services": ["Battery Jump", "Flat Tire Support"],
        "cost": 300,
        "distance_km": 1.3,
        "eta_min": 14,
        "lat": 8.5241,
        "lon": 76.9366
    },
    {
        "name": "Rajkot Car Rescue",
        "region": "West",
        "state": "Gujarat",
        "city": "Sadar Bazaar",
        "location": "Sadar Bazaar, Rajkot",
        "services": ["Towing", "Flat Tire Support"],
        "cost": 350,
        "distance_km": 1.4,
        "eta_min": 16,
        "lat": 22.3039,
        "lon": 70.8022
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

# -----------------------------
# RATING FUNCTIONS
# -----------------------------

def rate_mechanic(name, rating):
    """Store rating for a mechanic"""
    if _use_mock:
        for mech in _mock_mechanics:
            if mech["name"] == name:
                mech.setdefault("ratings", []).append(rating)
                return
    else:
        mechanics_collection.update_one(
            {"name": name},
            {"$push": {"ratings": rating}}
        )

def get_average_rating(mechanic):
    """Calculate average rating for a mechanic"""
    if _use_mock:
        ratings = mechanic.get("ratings", [])
        return round(sum(ratings) / len(ratings), 1) if ratings else "No ratings"
    else:
        mech = mechanics_collection.find_one({"name": mechanic["name"]})
        ratings = mech.get("ratings", [])
        return round(sum(ratings) / len(ratings), 1) if ratings else "No ratings"
