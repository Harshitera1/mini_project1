import math
import random

# Estimate repair time based on service
def estimate_repair_time(service_type):
    estimates = {
        "Flat Tire Support": 15,
        "Engine Trouble": 45,
        "Condition Analysis": 20,
        "Vehicle Towing": 30,
        "Battery Jump": 25,
    }
    return estimates.get(service_type, random.randint(20, 60))

# Haversine Distance Calculator (in km)
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of earth in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

# Estimate ETA and Cost based on distance
def estimate_eta_and_cost(distance_km, service_type):
    base_time = estimate_repair_time(service_type)
    eta = round(base_time + distance_km * 2)  # Each km adds ~2 minutes
    base_cost = 200
    cost_per_km = 50
    total_cost = base_cost + int(distance_km * cost_per_km)
    return eta, total_cost
