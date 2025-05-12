def get_available_services():
    return ["Flat Tire", "Vehicle Malfunction", "Condition Analysis", "Fuel Issue", "Battery Jumpstart"]

def find_mechanics_nearby(location, service_type):
    # Simulated data
    return [
        {"name": "Raj Mechanic Works", "location": f"{location} Central", "cost": 300},
        {"name": "AutoFix Garage", "location": f"{location} East", "cost": 450},
    ]
