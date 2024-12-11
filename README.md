# TSP Solver for City Road Network

This Python program calculates the optimal route for deliveries in a city road network using Dijkstra's algorithm and a greedy nearest neighbor heuristic for solving the Traveling Salesman Problem (TSP). It considers both the distance and traffic delays for each road segment to determine the most efficient route.

## Features
- Visualize a city road network with nodes (intersections) and edges (roads).
- Calculate the shortest path between intersections using Dijkstra's algorithm.
- Approximate the optimal delivery route through multiple delivery points using a nearest-neighbor heuristic.
- Animated visualization of the delivery route on the road network.

## Requirements
This program requires the following Python libraries:
- `matplotlib`
- `networkx`
- `heapq` (built-in)
- `itertools` (built-in)

Install the necessary dependencies using the following command:
```bash
pip install matplotlib networkx
```

## File Structure
- `tsp_solver.py`: Main script containing the program logic.

## Usage
1. Save the script as `tsp_solver.py`.
2. Run the program using Python:
   ```bash
   python tsp_solver.py
   ```
3. Follow the prompts:
   - Enter the starting intersection.
   - Enter one or more delivery intersections. Use `-1` to stop adding delivery points.
4. The program will calculate and display:
   - The optimal route.
   - Total distance (in km) and time (in minutes).
5. The road network and delivery route will be visualized using an animated graph.
6. You can repeat the process or exit the program.

## Input Details
- **Start Intersection**: A valid node ID in the graph.
- **Delivery Intersections**: One or more valid node IDs to visit during the delivery.

## Output Details
- **Optimal Route**: The sequence of nodes representing the delivery route.
- **Total Distance**: The sum of distances for the entire route.
- **Total Time**: The total time for the route, including traffic delays.

## Visualization
The program plots the road network with the following features:
- Nodes (intersections) are displayed as blue circles.
- Roads are visualized as lines with varying thickness and color based on weights (distance + delay).
- Edge labels show the distance (in km) and delay (in minutes).
- An animation shows the optimal delivery route being traversed step by step.

## Example
### Input
```
Enter the start intersection: 0
Enter a delivery intersection (or -1 to stop): 3
Enter a delivery intersection (or -1 to stop): 4
Enter a delivery intersection (or -1 to stop): -1
```

### Output
```
Optimal Route: [0, 3, 4]
Total Distance: 45 km
Total Time: 25 minutes
```

## Notes
- The program uses a fixed graph with predefined intersections and roads. You can modify the `create_fixed_graph()` function to define your own road network.
- The algorithm calculates an approximate solution for the TSP. For exact solutions, consider more advanced techniques.

## License
This project is open-source and available under the MIT License.
