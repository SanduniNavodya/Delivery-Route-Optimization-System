vehicle_types = {
    "bike": {
        "penalty_factor": 0.5,
        "max_distance": 30,
        "can_travel_on_damaged": True  # Bikes can handle damaged roads
    },
    "car": {
        "penalty_factor": 1,
        "max_distance": 50,
        "can_travel_on_damaged": False  # Cars cannot travel on damaged roads
    },
    "three_wheeler": {
        "penalty_factor": 1.2,
        "max_distance": 40,
        "can_travel_on_damaged": True  # Three-wheelers can navigate damaged roads
    },
    "lorry": {
        "penalty_factor": 2,
        "max_distance": 80,
        "can_travel_on_damaged": False  # Lorries cannot travel on damaged roads
    }
}
