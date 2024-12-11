import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation
import heapq
import itertools

# Function to create the graph with unidirectional roads and traffic delays
def create_fixed_graph():
    G = nx.DiGraph()  # Directed graph for unidirectional roads

    # Define the intersections and roads with traffic delays
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
        G.add_edge(u, v, weight=distance + traffic_delay, distance=distance, traffic_delay=traffic_delay)

    return G

# Dijkstra's Algorithm to find the shortest path from source to all other nodes
def dijkstra(graph, source):
    distances = {node: float('inf') for node in graph.nodes()}
    distances[source] = 0
    previous_nodes = {node: None for node in graph.nodes()}
    pq = [(0, source)]  # (distance, node)

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        for neighbor in graph.neighbors(current_node):
            edge_weight = graph[current_node][neighbor]['weight']
            new_distance = current_distance + edge_weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (new_distance, neighbor))

    return distances, previous_nodes

# Function to find the shortest path between two nodes using Dijkstra
def find_path_with_distance(graph, source, target):
    distances, previous_nodes = dijkstra(graph, source)

    if distances[target] == float('inf'):
        return None, float('inf')

    path = []
    current_node = target
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    path.reverse()

    return path, distances[target]

# Function to calculate the total time for a given route (considering both distance and traffic delay)
def calculate_route_time(graph, route):
    total_time = 0
    for i in range(len(route) - 1):
        _, time = find_path_with_distance(graph, route[i], route[i + 1])
        total_time += time
    return total_time

# Greedy nearest neighbor heuristic for finding an approximate TSP route
def find_optimal_route(graph, start_node, delivery_points):
    best_route = None
    best_time = float('inf')
    all_routes = itertools.permutations(delivery_points)

    for route in all_routes:
        route_with_start = [start_node] + list(route)
        route_time = calculate_route_time(graph, route_with_start)
        if route_time < best_time:
            best_time = route_time
            best_route = route_with_start

    return best_route, best_time

# Function to plot the graph with improved spacing and curved roads
def plot_graph(graph, pos=None):
    fig, ax = plt.subplots(figsize=(16, 12))  # Increased figure size for better layout

    # Use spring layout with a higher k-value to increase spacing
    if pos is None:
        pos = nx.spring_layout(graph, seed=42, k=1.0, iterations=50)  # Increased k-value to spread nodes more

    # Draw nodes with larger size and distinctive color
    nx.draw_networkx_nodes(
        graph, pos,
        node_color='skyblue',
        node_size=800,
        edgecolors='black',  # Add border to nodes for better visibility
        ax=ax
    )

    # Draw edges with varying thickness and color based on weights
    edge_weights = nx.get_edge_attributes(graph, 'weight')
    edges = graph.edges(data=True)
    edge_colors = [data['weight'] for _, _, data in edges]
    edge_widths = [data['weight'] / 10 for _, _, data in edges]  # Scale edge widths for better visualization

    # Use a bezier curve for edges to make them curved
    nx.draw_networkx_edges(
        graph, pos,
        edge_color=edge_colors,
        edge_cmap=plt.cm.viridis,  # Use colormap for edge colors
        width=edge_widths,
        alpha=0.8,
        style='-',  # Solid edges
        ax=ax,
        connectionstyle='arc3,rad=0.1'  # Apply curvature to the edges
    )

    # Add edge labels to show weights (distance + traffic delay)
    edge_labels = {
        (u, v): f"D:{data['distance']} T:{data['traffic_delay']}"
        for u, v, data in graph.edges(data=True)
    }
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10, ax=ax)

    # Add labels to nodes
    nx.draw_networkx_labels(
        graph, pos,
        font_size=12,
        font_color='black',
        font_weight='bold',
        ax=ax
    )

    # Customize plot appearance
    plt.title("City Road Network with Traffic Information", fontsize=16)
    plt.axis('off')  # Turn off axis for better aesthetics
    plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.viridis), ax=ax, label="Road Weight (Distance + Delay)")
    plt.tight_layout()
    plt.show()

    return pos  # Return the positions to be used in the animation

# Function to create animated visualization of the optimal route
def create_animated_route_visualization(graph, route, total_distance, pos):
    fig, ax = plt.subplots(figsize=(16, 10))  # Increased figure size

    def update(frame):
        ax.clear()
        plt.title("Optimal Delivery Route", fontsize=16)

        # Re-plot the graph with all the details
        nx.draw_networkx_nodes(graph, pos, node_color='lightgray', node_size=500, ax=ax)
        nx.draw_networkx_edges(graph, pos, edge_color='gray', style='dashed', ax=ax)

        edge_labels = {(u, v): graph[u][v]['weight'] for (u, v) in graph.edges()}
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)
        nx.draw_networkx_labels(graph, pos, ax=ax)

        # Draw edges for the current frame
        for i in range(frame + 1):
            start, end = route[i], route[i + 1]
            path, distance = find_path_with_distance(graph, start, end)
            path_edges = list(zip(path[:-1], path[1:]))

            # Draw the edges for the current route
            nx.draw_networkx_edges(
                graph, pos,
                edgelist=path_edges,
                edge_color='blue',
                width=3,
                ax=ax
            )

            nx.draw_networkx_nodes(
                graph, pos,
                nodelist=path,
                node_color='blue',
                node_size=500,
                ax=ax
            )

    anim = animation.FuncAnimation(
        fig, update,
        frames=len(route) - 1,
        interval=3000,  # 3 seconds between frames
        repeat=False
    )

    plt.tight_layout()
    plt.show()

# Main function
def main():
    G = create_fixed_graph()

    print("\nPlotting the road network...")
    pos = plot_graph(G)  # Save the positions for consistent use in animation

    start = int(input("Enter the start intersection: "))

    # Check if start node is valid
    if start not in G.nodes:
        print(f"Invalid start node: {start}. Please enter a valid node.")
        return

    deliveries = []
    while True:
        end = int(input("Enter a delivery intersection (or -1 to stop): "))
        if end == -1:
            break
        if end not in G.nodes:
            print(f"Invalid delivery intersection: {end}. Please enter a valid node.")
        else:
            deliveries.append(end)

    optimal_route, total_distance = find_optimal_route(G, start, deliveries)

    if optimal_route:
        print(f"\nOptimal Route: {optimal_route}")
        print(f"Total Distance: {total_distance}")
        create_animated_route_visualization(G, optimal_route, total_distance, pos)
    else:
        print("No valid route found.")

if __name__ == "__main__":
    main()
