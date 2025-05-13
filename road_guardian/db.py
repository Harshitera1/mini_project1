import os
from pymongo import MongoClient, errors
from dotenv import load_dotenv
import bcrypt
from datetime import datetime  # Import is correct

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "").strip()

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

def register_user(user_data):
    # Validate phone field
    phone = user_data.get("phone")
    if not phone:
        raise ValueError("Phone number is required.")
    if phone is None or phone.strip() == "":
        raise ValueError("Phone number cannot be null or empty.")
    
    # Debug: Log the user_data as received
    print(f"Debug: Received user_data in register_user: {user_data}")
    
    # Check if user already exists
    existing_user = users_collection.find_one({"phone": user_data['phone']})
    if existing_user:
        print(f"Debug: User with phone {user_data['phone']} already exists: {existing_user}")
        return False  # User already exists
    
    # Hash the password
    hashed_password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
    
    # Explicitly construct the document to be inserted
    insert_doc = {
        "name": user_data.get("name", ""),
        "phone": user_data.get("phone"),  # Ensure phone is explicitly set
        "email": user_data.get("email", ""),
        "password": hashed_password,
        "region": user_data.get("region", ""),
        "state": user_data.get("state", ""),
        "city": user_data.get("city", ""),
        "registered_at": user_data.get("registered_at", datetime.now().isoformat())  # Fixed datetime usage
    }
    
    # Debug: Log the exact document to be inserted
    print(f"Debug: Explicitly constructed document to be inserted: {insert_doc}")
    
    # Insert the user
    try:
        result = users_collection.insert_one(insert_doc)
        print(f"Debug: Successfully registered user with phone {insert_doc['phone']}. Inserted ID: {result.inserted_id}")
        return True
    except Exception as e:
        print(f"Debug: Failed to insert user: {str(e)}")
        raise e

def verify_user(mobile, password):
    user = users_collection.find_one({"phone": mobile})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return True
    return False