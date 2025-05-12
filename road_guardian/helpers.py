import random

def estimate_repair_time(service_type):
    estimates = {
        "Flat Tire": 15,
        "Vehicle Malfunction": 45,
        "Condition Analysis": 20,
        "Fuel Issue": 30,
        "Battery Jumpstart": 25,
    }
    return estimates.get(service_type, random.randint(20, 60))
