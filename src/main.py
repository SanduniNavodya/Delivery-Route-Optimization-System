import networkx as nx
from input_handler import get_vehicle_type_input, get_start_end_input
from graph_utils import find_shortest_path, plot_graph, add_random_road
from vehicle_types import vehicle_types


def main():
    # Initialize a directed graph
    G = nx.DiGraph()

    # Get number of nodes
    while True:
        try:
            num_nodes = int(input("How many intersections (nodes) do you want to add? "))
            if num_nodes > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")

    # Get number of roads
    while True:
        try:
            num_roads = int(input("How many roads (edges) do you want to create between the intersections? "))
            if num_roads > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")

    # Add roads
    for _ in range(num_roads):
        add_random_road(G, num_nodes, vehicle_types)

    # Display all edges with their statuses
    print("\nRoad conditions:")
    for u, v, d in G.edges(data=True):
        print(f"From {u} to {v}: {'Damaged' if d['is_damaged'] else 'Undamaged'} road, "
              f"Distance: {d['distance']} km, Traffic delay: {d['traffic_delay']} minutes")

    # Plot the graph
    print("\nPlotting the road network...")
    plot_graph(G)

    while True:
        # Get inputs
        vehicle_type = get_vehicle_type_input()
        try:
            start, end = get_start_end_input()
            if start > num_nodes or end > num_nodes:
                print(f"Please enter node numbers between 1 and {num_nodes}")
                continue
        except ValueError:
            print("Please enter valid numbers for start and end points.")
            continue

        # Find shortest path
        shortest_path, path_details = find_shortest_path(G, vehicle_type, start, end, vehicle_types)

        # Output results
        if shortest_path:
            print(f"\nBest delivery route for {vehicle_type.replace('_', ' ').title()}:")
            print(f"Path: {' → '.join(map(str, shortest_path))}")
            print(f"Total estimated time: {path_details['total_time']:.1f} minutes")
            print("\nDetailed route information:")
            for step in path_details['details']:
                print(f"From {step['from']} to {step['to']}:")
                print(f"  Distance: {step['distance']} km")
                print(f"  Traffic delay: {step['traffic_delay']} minutes")
                print(f"  Road condition: {'Damaged' if step['damaged'] == 'Yes' else 'Normal'}")
                print(f"  Road suitable for: {step['road_vehicle_type'].replace('_', ' ').title()}")
                print(f"  Your vehicle type: {step['selected_vehicle_type'].replace('_', ' ').title()}")
                note = "Note: This road is damaged but included as it's part of the best available route." \
                    if step['damaged'] == 'Yes' else \
                    "Note: This road is undamaged and included as it's part of the best available route."
                print(f"  {note}")
                print()
        else:
            print("\nNo valid route exists between the selected intersections.")
            if not nx.has_path(G, start, end):
                print(f"Reason: There is no path connecting intersection {start} to intersection {end}.")
            else:
                print(f"Reason: The roads available are not suitable for the {vehicle_type.replace('_', ' ').title()}.")
                print("Ensure that your vehicle can travel on the available road conditions.")
                print("\nNearby roads for reference:")
                for u, v, d in G.edges(data=True):
                    if u == start or v == start or u == end or v == end:
                        print(f"From {u} to {v}: {'Damaged' if d['is_damaged'] else 'Normal'} road, "
                              f"Distance: {d['distance']} km, Traffic delay: {d['traffic_delay']} minutes")

        # Ask if the user wants to find another route
        choice = input("\nDo you want to find another route? (yes/no): ").strip().lower()
        if choice != 'yes':
            print("\nExiting the program. Goodbye!")
            break


if __name__ == "__main__":
    main()
