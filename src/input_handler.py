# Function to get dynamic vehicle type input
def get_vehicle_type_input():
    print("Select Vehicle Type:")
    print("1. Bike")
    print("2. Car")
    print("3. Three-Wheeler")
    print("4. Lorry")

    choice = int(input("Enter your choice (1-4): "))
    vehicle_types = ["bike", "car", "three_wheeler", "lorry"]
    if 1 <= choice <= 4:
        return vehicle_types[choice - 1]
    else:
        print("Invalid choice, defaulting to Car.")
        return "car"

# Function to get starting and ending nodes
def get_start_end_input():
    start = int(input("Enter the start intersection: "))
    end = int(input("Enter the destination intersection: "))
    return start, end
