import os
from pymongo import MongoClient, errors
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "").strip()

# Connect to MongoDB Atlas
if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env file. Please set it up.")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
try:
    client.admin.command("ping")
    print("✅ Connected to MongoDB Atlas.")
except errors.PyMongoError as e:
    raise ConnectionError(f"Failed to connect to MongoDB: {e}")

db = client["road_guardian"]
mechanics_collection = db["mechanics"]
bookings_collection = db["bookings"]
users_collection = db["users"]

def get_mechanics():
    return list(mechanics_collection.find({}, {"_id": 0}))

def add_mechanic(mechanic_data):
    mechanics_collection.insert_one(mechanic_data)

def add_booking(booking_data):
    bookings_collection.insert_one(booking_data)

def get_user_bookings(user_name):
    return list(bookings_collection.find({"user_name": user_name}, {"_id": 0}))

def rate_mechanic(name, review):
    mechanics_collection.update_one(
        {"name": name},
        {"$push": {"reviews": review}}
    )

def get_average_rating(mechanic):
    reviews = mechanic.get("reviews", [])
    ratings = [r["rating"] for r in reviews if "rating" in r]
    return round(sum(ratings) / len(ratings), 1) if ratings else "No ratings"