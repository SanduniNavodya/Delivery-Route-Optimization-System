import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import os

# Fixed graph setup
def create_fixed_graph():
    # Define the fixed set of intersections (nodes)
    G = nx.complete_graph(5, nx.DiGraph())  # 5 intersections for example
    
    # Predefined edge data (for example, distances and conditions)
    # Here, each tuple is (u, v, distance, traffic_delay)
    edges = [
        (0, 1, 10, 5),
        (0, 2, 15, 10),
        (0, 3, 20, 15),
        (0, 4, 25, 20),
        (1, 2, 10, 5),
        (1, 3, 12, 7),
        (1, 4, 18, 10),
        (2, 3, 10, 5),
        (2, 4, 12, 6),
        (3, 4, 10, 5)
    ]
    
    for u, v, distance, traffic_delay in edges:
        # Set attributes for the forward edge
        G[u][v]['weight'] = distance + traffic_delay
        G[u][v]['distance'] = distance  # Ensure 'distance' attribute is set
        G[u][v]['traffic_delay'] = traffic_delay  # Ensure 'traffic_delay' attribute is set
        G[u][v]['vehicle_type'] = "car"
        
        # For directed graph, manually add reverse edge with the same attributes if not already added
        if not G.has_edge(v, u):
            G.add_edge(v, u, weight=distance + traffic_delay,
                       distance=distance, traffic_delay=traffic_delay,
                       vehicle_type="car")
        else:
            # Ensure reverse edge has the same attributes
            G[v][u]['weight'] = distance + traffic_delay
            G[v][u]['distance'] = distance
            G[v][u]['traffic_delay'] = traffic_delay
            G[v][u]['vehicle_type'] = "car"
    
    return G

# TSP Nearest Neighbor Heuristic
def tsp_nearest_neighbor(G, start_node):
    tour = [start_node]
    total_distance = 0
    visited = {start_node}
    current_node = start_node
    while len(visited) < len(G.nodes()):
        min_dist = float('inf')
        next_node = None
        for neighbor in G.neighbors(current_node):
            if neighbor not in visited:
                dist = G[current_node][neighbor]["weight"]
                if dist < min_dist:
                    min_dist = dist
                    next_node = neighbor
        visited.add(next_node)
        tour.append(next_node)
        total_distance += min_dist
        current_node = next_node
    total_distance += G[tour[-1]][tour[0]]["weight"]
    tour.append(tour[0])  # Complete the cycle
    return tour, total_distance

# Plot the fixed graph
def plot_fixed_graph(G):
    plt.figure(figsize=(16, 12))
    pos = nx.kamada_kawai_layout(G)
    
    nx.draw_networkx_nodes(
        G, pos, node_size=700, 
        node_color='lightblue', 
        edgecolors='black', 
        linewidths=2
    )

    curved_rad = 0.1
    # No more damaged roads, so we can simplify
    undamaged_edges = [(u, v) for u, v, d in G.edges(data=True)]

    nx.draw_networkx_edges(
        G, pos, edgelist=undamaged_edges, 
        edge_color='green', width=2, 
        connectionstyle=f'arc3,rad={curved_rad}', 
        arrows=True, arrowstyle='-|>', arrowsize=20
    )

    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

    # Ensure that the edge labels reference the correct attributes
    edge_labels = {}
    for u, v, d in G.edges(data=True):
        if 'distance' in d and 'traffic_delay' in d:
            edge_labels[(u, v)] = f"{d['distance']}km\n{d['traffic_delay']}min"

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Legend for the roads
    legend_elements = [
        mpatches.Patch(color='green', label='Roads')
    ]
    plt.legend(handles=legend_elements, loc='upper left')

    plt.title("City Road Network", pad=20, size=16)
    plt.axis('off')

    output_dir = 'assets'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(f'{output_dir}/city_road_graph.png', dpi=300, bbox_inches='tight')
    plt.show()

# Function to get starting and ending nodes (Delivery points)
def get_delivery_points():
    start = int(input("Enter the start intersection: "))
    deliveries = []
    while True:
        end = int(input("Enter a delivery intersection (or -1 to stop): "))
        if end == -1:
            break
        deliveries.append(end)
    return start, deliveries

def main():
    # Create the fixed graph
    G = create_fixed_graph()

    # Plot the graph
    print("\nPlotting the road network...")
    plot_fixed_graph(G)

    # Get delivery points and start node
    start, deliveries = get_delivery_points()

    # For each delivery point, compute the TSP path
    print(f"\nFinding the shortest TSP route from Intersection {start} to the delivery points...")
    tsp_route, total_distance = tsp_nearest_neighbor(G, start)

    # Output the results
    print(f"\nBest route from Intersection {start} to the delivery points:")
    print(f"Path: {' → '.join(map(str, tsp_route))}")
    print(f"Total estimated time: {total_distance:.1f} minutes")
    
    # Ask if the user wants to find another route
    choice = input("\nDo you want to find another route? (yes/no): ").strip().lower()
    if choice != 'yes':
        print("\nExiting the program. Goodbye!")

if __name__ == "__main__":
    main()
