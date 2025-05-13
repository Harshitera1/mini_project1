import math
import random

def estimate_repair_time(service_type):
    estimates = {
        "Flat Tire Support": 15,
        "Engine Trouble": 45,
        "Condition Analysis": 20,
        "Vehicle Towing": 30,
        "Battery Jump": 25,
    }
    return estimates.get(service_type, random.randint(20, 60))

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

def estimate_eta_and_cost(distance_km, service_type):
    base_time = estimate_repair_time(service_type)
    eta = round(base_time + distance_km * 2)
    base_cost = 200
    cost_per_km = 50
    total_cost = base_cost + int(distance_km * cost_per_km)
    return eta, total_cost

def get_youtube_link(service_type):
    query_map = {
        "Flat Tire Support": "how to fix flat tire",
        "Engine Trouble": "engine not starting fix",
        "Battery Jump": "how to jumpstart car",
        "Vehicle Towing": "how car towing works",
        "Condition Analysis": "car inspection tutorial"
    }
    query = query_map.get(service_type, "roadside assistance tips")
    return f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
