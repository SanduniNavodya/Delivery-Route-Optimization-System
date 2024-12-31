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

    # Ensure there is a valid path
    if distances[target] == float('inf'):
        return None, None  # No valid path

    path = []
    current_node = target
    total_distance = 0

    # Build the path and calculate actual distance (not including delays)
    while current_node is not None:
        path.append(current_node)
        if previous_nodes[current_node] is not None:
            total_distance += graph[previous_nodes[current_node]][current_node]['distance']
        current_node = previous_nodes[current_node]
    path.reverse()

    return path, total_distance

# Function to calculate the total time for a given route (considering both distance and traffic delay)
def calculate_route_time(graph, route):
    total_time = 0
    total_distance = 0
    for i in range(len(route) - 1):
        if graph.has_edge(route[i], route[i + 1]):  # Check if the edge exists
            edge_data = graph[route[i]][route[i + 1]]
            total_distance += edge_data['distance']
            total_time += (edge_data['distance'] / 50) * 60 + edge_data['traffic_delay']  # time in minutes
        else:
            return None, None  # Return None if any part of the route is invalid
    return total_distance, total_time


# Greedy nearest neighbor heuristic for finding an approximate TSP route
def find_optimal_route(graph, start_node, delivery_points):
    best_route = None
    best_distance = float('inf')
    best_time = float('inf')
    unreachable_deliveries = []  # To track delivery points that are unreachable

    # Try all permutations of delivery points
    all_routes = itertools.permutations(delivery_points)

    for route in all_routes:
        route_with_start = [start_node] + list(route)

        # Check if the route is valid for all delivery points
        route_valid = True
        for i in range(len(route_with_start) - 1):
            path, _ = find_path_with_distance(graph, route_with_start[i], route_with_start[i + 1])
            if path is None:  # If any part of the route is invalid, mark as invalid
                unreachable_deliveries.append(route_with_start[i + 1])
                route_valid = False
                break

        if route_valid:
            route_distance, route_time = calculate_route_time(graph, route_with_start)

            if route_time is not None and route_distance is not None and route_time < best_time:
                best_time = route_time
                best_route = route_with_start
                best_distance = route_distance

    # If no valid route found, print unreachable points and return None
    if best_route is None:
        unreachable_deliveries = list(set(unreachable_deliveries))  # Remove duplicates
        print(f"Cannot reach the following delivery points: {', '.join(map(str, unreachable_deliveries))}")
        return None, None, None, unreachable_deliveries

    return best_route, best_distance, best_time, unreachable_deliveries


# Function to plot the graph with improved spacing and curved roads
def plot_graph(graph, pos=None):
    fig, ax = plt.subplots(figsize=(16, 12))  

    # Use spring layout with a higher k-value to increase spacing
    if pos is None:
        pos = nx.spring_layout(graph, seed=42, k=1.2, iterations=50)  

    # Calculate the boundaries of the graph for consistent axis scaling
    x_values, y_values = zip(*pos.values())
    min_x, max_x = min(x_values), max(x_values)
    min_y, max_y = min(y_values), max(y_values)

    # Set axis limits and aspect ratio to prevent distortion
    ax.set_xlim(min_x - 0.1, max_x + 0.1)
    ax.set_ylim(min_y - 0.1, max_y + 0.1)
    ax.set_aspect('equal', adjustable='box')

    # Draw nodes with larger size and distinctive color
    nx.draw_networkx_nodes(
        graph, pos,
        node_color='skyblue',
        node_size=800,
        edgecolors='black',  
        ax=ax
    )

    # Draw all edges except the specified ones
    normal_edges = [
        (u, v) for u, v in graph.edges()
        if (u, v) not in [(3, 4), (1, 3)]
    ]
    nx.draw_networkx_edges(
        graph, pos,
        edgelist=normal_edges,
        edge_color=[graph[u][v]['weight'] for u, v in normal_edges],
        edge_cmap=plt.cm.viridis,
        width=[graph[u][v]['weight'] / 10 for u, v in normal_edges],
        alpha=0.8,
        style='-',  
        ax=ax,
        connectionstyle='arc3,rad=0.1',  # Default curvature
        arrows=True,
        arrowstyle='->',
        arrowsize=20
    )

    # Draw the specific edges with higher curvature
    curved_edges = [(3, 4), (1, 3)]
    for u, v in curved_edges:
        nx.draw_networkx_edges(
            graph, pos,
            edgelist=[(u, v)],
            edge_color=[graph[u][v]['weight']],
            edge_cmap=plt.cm.viridis,
            width=[graph[u][v]['weight'] / 10],
            alpha=0.8,
            style='-',  
            ax=ax,
            connectionstyle='arc3,rad=0.2',  # Increased curvature
            arrows=True,
            arrowstyle='->',
            arrowsize=20
        )

    # Add edge labels to show weights (distance in km and delay in min)
    edge_labels = {
        (u, v): f"D: {data['distance']} km T: {data['traffic_delay']} min"
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
    plt.title("City Road Network with Traffic Information", fontsize=16, y=0.95)
    plt.axis('off')  # Turn off axis for better aesthetics
    plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.viridis), ax=ax, label="Road Weight (Distance + Delay)")
    plt.tight_layout()
    plt.show()

    return pos  # Return the layout (positioning of nodes) for consistency


# Function to create animated visualization of the optimal route
def create_animated_route_visualization(graph, route, total_distance, total_time, pos, unreachable_deliveries):
    fig, ax = plt.subplots(figsize=(16, 12))  

    # Calculate the boundaries of the graph for consistent axis scaling
    x_values, y_values = zip(*pos.values())
    min_x, max_x = min(x_values), max(x_values)
    min_y, max_y = min(y_values), max(y_values)

    # Set axis limits and aspect ratio to prevent distortion
    ax.set_xlim(min_x - 0.1, max_x + 0.1)
    ax.set_ylim(min_y - 0.1, max_y + 0.1)
    ax.set_aspect('equal', adjustable='box')

    def update(frame):
        ax.clear()
        ax.set_title(
            f"Optimal Delivery Route (with 50 km/h speed) - Total Distance: {total_distance} km, Total Time: {total_time:.2f} min",
            fontsize=16, y=1.05
        )

        # Draw all nodes
        nx.draw_networkx_nodes(
            graph, pos,
            node_color='skyblue',
            node_size=800,
            edgecolors='black',
            ax=ax
        )

        # Draw all edges except the specified ones
        normal_edges = [
            (u, v) for u, v in graph.edges()
            if (u, v) not in [(3, 4), (1, 3)]
        ]
        nx.draw_networkx_edges(
            graph, pos,
            edgelist=normal_edges,
            edge_color=[graph[u][v]['weight'] for u, v in normal_edges],
            edge_cmap=plt.cm.viridis,
            width=[graph[u][v]['weight'] / 10 for u, v in normal_edges],
            alpha=0.8,
            style='-',  
            ax=ax,
            connectionstyle='arc3,rad=0.1',  # Default curvature
            arrows=True,
            arrowstyle='->',
            arrowsize=20    
        )

        # Draw the specific edges with higher curvature (1 -> 3 and 3 -> 4)
        curved_edges = [(1, 3), (3, 4)]
        for u, v in curved_edges:
            nx.draw_networkx_edges(
                graph, pos,
                edgelist=[(u, v)],
                edge_color=[graph[u][v]['weight']],
                edge_cmap=plt.cm.viridis,
                width=[graph[u][v]['weight'] / 10],
                alpha=0.8,
                style='-',  
                ax=ax,
                connectionstyle='arc3,rad=0.2',  # Increased curvature for these edges
                arrows=True,
                arrowstyle='->',
                arrowsize=20
            )

        # Add edge labels
        edge_labels = {
            (u, v): f"D: {graph[u][v]['distance']} km T: {graph[u][v]['traffic_delay']} min"
            for u, v in graph.edges()
        }
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10, ax=ax)

        # Add node labels
        nx.draw_networkx_labels(
            graph, pos,
            font_size=12,
            font_color='black',
            font_weight='bold',
            ax=ax
        )

        # Highlight the path progressively up to the current frame
        path_edges = []
        path_nodes = [route[0]]

        for i in range(frame + 1):
            start, end = route[i], route[i + 1]
            path_nodes.append(end)
            path_edges.append((start, end))

        # Draw animated path
        for u, v in path_edges:
            # Use curvature 0.2 for the special edges (1 -> 3) and (3 -> 4)
            connection_style = 'arc3,rad=0.2' if (u, v) in [(1, 3), (3, 4)] else 'arc3,rad=0.1'
            nx.draw_networkx_edges(
                graph, pos,
                edgelist=[(u, v)],
                edge_color='blue',
                width=3,
                style='solid',
                ax=ax,
                connectionstyle=connection_style  # Apply different curvature based on edge
            )

        # Highlight nodes in the animated path
        nx.draw_networkx_nodes(
            graph, pos,
            nodelist=path_nodes,
            node_color='blue',
            node_size=800,
            edgecolors='black',
            ax=ax
        )

        # Display the unreachable delivery points message if any
        if unreachable_deliveries:
            ax.text(
                0.5, 1.0, f"Unreachable Delivery Points: {', '.join(map(str, unreachable_deliveries))}",
                horizontalalignment='center', verticalalignment='center',
                fontsize=14, color='red', transform=ax.transAxes
            )

        # Turn off the axis for cleaner appearance
        plt.axis('off')
        plt.tight_layout()

    anim = animation.FuncAnimation(
        fig, update,
        frames=len(route) - 1,  # One frame per route segment
        interval=2000,  # 2 seconds per frame
        repeat=False
    )

    plt.show()


# Main function
def main():
    G = create_fixed_graph()

    print("\nPlotting the road network...")
    pos = plot_graph(G)

    while True:
        start = int(input("Enter the start intersection: "))

        if start not in G.nodes:
            print(f"Invalid start node: {start}. Please enter a valid node.")
            continue

        deliveries = []
        while True:
            end = int(input("Enter a delivery intersection (or -1 to stop): "))
            if end == -1:
                break
            if end not in G.nodes:
                print(f"Invalid delivery intersection: {end}. Please enter a valid node.")
            else:
                deliveries.append(end)

        # Find the optimal route
        optimal_route, total_distance, total_time, unreachable_deliveries = find_optimal_route(G, start, deliveries)

        if optimal_route:
            print(f"\nOptimal Route: {optimal_route}")
            print(f"Total Distance: {total_distance} km")
            print(f"Total Time: {total_time:.2f} minutes")
            create_animated_route_visualization(G, optimal_route, total_distance, total_time, pos, unreachable_deliveries)
        else:
            print("No valid route found for all deliveries.")

            for delivery in deliveries:
                route, distance = find_path_with_distance(G, start, delivery)
                if route:
                    time = calculate_route_time(G, route)[1]
                    print(f"Suggested Route for delivery to {delivery}: {route}")
                    print(f"Total Distance: {distance} km")
                    print(f"Total Time: {time:.2f} minutes")
                    create_animated_route_visualization(G, route, distance, time, pos, unreachable_deliveries)
                else:
                    print(f"No route found for delivery to {delivery}.")

        cont = input("\nDo you want to try another route? (y/n): ")
        if cont.lower() != 'y':
            print("Exiting the program... Good Bye!")
            break


# Run the main function
if __name__ == "__main__":
    main()
