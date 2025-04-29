import streamlit as st
import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import optuna


# -----------------------------
# Chennai Sample Locations
# -----------------------------
locations = [
    (13.0418, 80.2337),  # Depot - T. Nagar (School)
    (13.0067, 80.2628),  # Adyar
    (13.0827, 80.2707),  # Anna Nagar
    (13.0180, 80.2245),  # Guindy
    (13.0333, 80.2500),  # Mylapore
    (13.0735, 80.2565),  # Kilpauk
]
depot = 0


# -----------------------------
# Distance matrix
# -----------------------------
def compute_euclidean_distance_matrix(locations):
    distances = {}
    for from_idx, from_node in enumerate(locations):
        distances[from_idx] = {}
        for to_idx, to_node in enumerate(locations):
            if from_idx == to_idx:
                distances[from_idx][to_idx] = 0
            else:
                distances[from_idx][to_idx] = int(
                    np.hypot((from_node[0] - to_node[0]), (from_node[1] - to_node[1])) * 100000
                )
    return distances

# -----------------------------
# Routing Solver
# -----------------------------
def solve_bus_routing(num_buses, bus_capacity):
    distance_matrix = compute_euclidean_distance_matrix(locations)
    manager = pywrapcp.RoutingIndexManager(len(locations), num_buses, depot)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    demands = [0] + [1] * (len(locations) - 1)

    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return demands[from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,
        [bus_capacity] * num_buses,
        True,
        'Capacity'
    )

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 5

    solution = routing.SolveWithParameters(search_parameters)

    total_distance = 0
    if solution:
        for vehicle_id in range(num_buses):
            index = routing.Start(vehicle_id)
            route_distance = 0
            while not routing.IsEnd(index):
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
            total_distance += route_distance
        return total_distance
    else:
        return float('inf')

# -----------------------------
# Optuna Objective
# -----------------------------
def run_optimization(min_buses, max_buses, min_cap, max_cap, n_trials):
    def objective(trial):
        num_buses = trial.suggest_int('num_buses', min_buses, max_buses)
        bus_capacity = trial.suggest_int('bus_capacity', min_cap, max_cap)
        return solve_bus_routing(num_buses, bus_capacity)

    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=n_trials)

    return study.best_params, study.best_value

# -----------------------------
# Streamlit App UI
# -----------------------------
st.set_page_config(page_title="School Bus Route Optimizer", layout="centered")
st.title("🚍 School Bus Route Optimization")
st.markdown("Optimize bus routes to reduce total distance and improve efficiency.")
with st.sidebar:
    st.header("🔧 Settings")
    min_buses = st.slider("Min Buses", 1, 5, 2)
    max_buses = st.slider("Max Buses", min_buses, 8, 3)
    min_cap = st.slider("Min Capacity", 40, 60, 40)  
    max_cap = st.slider("Max Capacity", min_cap, 60, 50)  
    n_trials = st.slider("Optimization Trials", 5, 100, 20)


if st.button("Run Optimization"):
    with st.spinner("Optimizing..."):
        best_params, best_distance = run_optimization(min_buses, max_buses, min_cap, max_cap, n_trials)
    
    st.success("Optimization complete! 🎉")
    st.metric("Best Total Distance", f"{best_distance} meters")
    st.json(best_params)

    st.map(data={"lat": [lat for lat, lon in locations],
                 "lon": [lon for lat, lon in locations]})

