import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import os
import random

def calculate_weight(distance, traffic_delay, is_damaged, vehicle_type, vehicle_types):
    base_weight = distance + traffic_delay
    if is_damaged:
        return base_weight + (10 * vehicle_types[vehicle_type]["penalty_factor"])
    return base_weight

def add_random_road(G, num_nodes, vehicle_types):
    source = random.randint(1, num_nodes)
    target = random.randint(1, num_nodes)
    
    # Avoid duplicate edges and self-loops
    attempts = 0
    while (source == target or G.has_edge(source, target)) and attempts < 50:
        target = random.randint(1, num_nodes)
        attempts += 1
    
    if attempts < 50:
        distance = random.randint(1, 10)
        traffic_delay = random.randint(0, 30)
        is_damaged = random.choice([True, False])
        vehicle_type = random.choice(list(vehicle_types.keys()))
        weight = calculate_weight(distance, traffic_delay, is_damaged, vehicle_type, vehicle_types)
        G.add_edge(source, target, weight=weight, distance=distance, 
                  traffic_delay=traffic_delay, is_damaged=is_damaged, 
                  vehicle_type=vehicle_type)

def find_shortest_path(G, selected_vehicle_type, start, end, vehicle_types):
    try:
        # Use Dijkstra's algorithm to find the shortest path
        shortest_path = nx.shortest_path(G, source=start, target=end, weight='weight')
        
        total_time = 0
        path_details = {'total_time': 0, 'details': []}
        is_valid = True
        
        for i in range(len(shortest_path) - 1):
            u, v = shortest_path[i], shortest_path[i + 1]
            edge_data = G[u][v]
            distance = edge_data['distance']
            traffic_delay = edge_data['traffic_delay']
            is_damaged = edge_data['is_damaged']
            
            # Check if the road is suitable for the selected vehicle
            if is_damaged and not vehicle_types[selected_vehicle_type]["can_travel_on_damaged"]:
                is_valid = False
                break

            # Calculate the actual time for the vehicle type
            actual_time = calculate_weight(distance, traffic_delay, is_damaged, selected_vehicle_type, vehicle_types)
            
            total_time += actual_time
            path_details['details'].append({
                'from': u,
                'to': v,
                'distance': distance,
                'traffic_delay': traffic_delay,
                'damaged': 'Yes' if is_damaged else 'No',
                'road_vehicle_type': edge_data['vehicle_type'],
                'selected_vehicle_type': selected_vehicle_type
            })

        # If path is valid, return the details, else return None
        if is_valid:
            path_details['total_time'] = total_time
            return shortest_path, path_details
        else:
            return None, {'total_time': float('inf'), 'details': []}

    except nx.NetworkXNoPath:
        return None, {'total_time': float('inf'), 'details': []}


def plot_graph(G):
    plt.figure(figsize=(16, 12))
    pos = nx.kamada_kawai_layout(G)  # Using different layout algorithm
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=700, 
                          node_color='lightblue', 
                          edgecolors='black', 
                          linewidths=2)
    
    # Draw edges with different colors for damaged/undamaged roads
    damaged_edges = [(u, v) for u, v, d in G.edges(data=True) if d['is_damaged']]
    undamaged_edges = [(u, v) for u, v, d in G.edges(data=True) if not d['is_damaged']]
    
    nx.draw_networkx_edges(G, pos, edgelist=damaged_edges, 
                          edge_color='red', width=2, 
                          connectionstyle='arc3,rad=0.2')
    nx.draw_networkx_edges(G, pos, edgelist=undamaged_edges, 
                          edge_color='green', width=2, 
                          connectionstyle='arc3,rad=0.2')
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    # Add edge labels
    edge_labels = {(u, v): f"{d['distance']}km\n{d['traffic_delay']}min"
                  for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    # Add legend
    legend_elements = [
        mpatches.Patch(color='green', label='Normal Roads'),
        mpatches.Patch(color='red', label='Damaged Roads')
    ]
    plt.legend(handles=legend_elements, loc='upper left')
    
    plt.title("City Road Network", pad=20, size=16)
    plt.axis('off')
    
    # Save and show
    output_dir = 'assets'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(f'{output_dir}/city_road_graph.png', dpi=300, bbox_inches='tight')
    plt.show()