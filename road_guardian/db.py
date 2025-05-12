# db.py

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["road_guardian"]
mechanics_collection = db["mechanics"]

def seed_mechanics():
    if mechanics_collection.count_documents({}) == 0:
        sample_data = [
            {
                "name": "Raj Mechanic Works",
                "location": "Andheri West",
                "cost": 300,
                "distance_km": 1.5,
                "eta_min": 12,
                "lat": 19.119677,
                "lon": 72.846264
            },
            {
                "name": "AutoFix Garage",
                "location": "Bandra East",
                "cost": 450,
                "distance_km": 2.3,
                "eta_min": 18,
                "lat": 19.0558,
                "lon": 72.8401
            },
        ]
        mechanics_collection.insert_many(sample_data)
        print("✅ Seeded mechanics collection.")
    else:
        print("ℹ️ Mechanics already seeded — skipping.")

def get_mechanics():
    return list(mechanics_collection.find({}, {"_id": 0}))
