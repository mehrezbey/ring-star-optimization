import random
import math
from heuristics import greedy_p_median, nearest_neighbor_tsp, two_opt
import random


def evaluate_solution(stations, coordinates, distances, n):
    assignments = [0]*n
    cost_assign = 0

    for i in range(n):
        if i in stations:
            assignments[i] = i
        else:
            closest = min(stations, key=lambda s: distances[i][s])
            assignments[i] = closest
            cost_assign += distances[i][closest]

    tsp = nearest_neighbor_tsp(stations, distances)
    tsp = two_opt(tsp["path"], distances)

    return {
        "stations": stations,
        "assignments": assignments,
        "path": tsp["path"],
        "cost": cost_assign + tsp["cost"]
    }



def neighbor(stations, n):
    all_points = list(range(n))

    s_out = random.choice(stations)
    s_in = random.choice(list(set(all_points) - set(stations)))

    new_stations = stations.copy()
    new_stations.remove(s_out)
    new_stations.append(s_in)

    return new_stations


def simulated_annealing(
    initial_stations,
    coordinates,
    distances,
    n,
    T0=1000,
    alpha=0.95,
    iterations=100
):
    current = evaluate_solution(
        initial_stations.copy(),
        coordinates,
        distances,
        n
    )

    best = current
    T = T0

    while T > 1e-3:
        for _ in range(iterations):

            new_stations = neighbor(current["stations"], n)
            candidate = evaluate_solution(
                new_stations,
                coordinates,
                distances,
                n
            )
            delta = candidate["cost"] - current["cost"]

            if delta < 0 or random.random() < math.exp(-delta / T):
                current = candidate

                if current["cost"] < best["cost"]:
                    best = current
        T *= alpha
    return best