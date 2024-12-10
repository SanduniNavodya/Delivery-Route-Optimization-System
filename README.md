# Phoenix Coder: Delivery Route Optimization

## Description:
This project simulates a delivery route optimization system for a logistics company. The company aims to optimize delivery times by considering vehicle types, road conditions, and traffic delays in a city grid.

## Features:
- Dynamic road and vehicle input.
- Calculates optimal delivery routes based on vehicle type.
- Visualizes the city grid with road details and delivery routes.
- Supports multiple vehicle categories: bike, car, three-wheeler, lorry.

## Requirements:
- Python 3.8+
- `networkx`
- `matplotlib`

## Setup:
1. Clone the repository or download the files.
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the program:
    ```bash
    python src/main.py
    ```

## Usage:
- The program will ask you for the number of roads you want to add and their details (source, target, distance, traffic delay, damage status).
- You will then select the vehicle type (bike, car, three-wheeler, lorry).
- The program will calculate and display the optimal route based on the selected vehicle type and road conditions.
