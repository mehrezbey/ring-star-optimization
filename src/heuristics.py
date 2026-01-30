import numpy as np
from utils import euclidean_distance
import time


def greedy_p_median(coordinates, p, n, distances):

    x_min = coordinates[:,0].min()
    x_max = coordinates[:,0].max()
    y_min = coordinates[:,1].min()
    y_max = coordinates[:,1].max()

    q = int(np.ceil(np.sqrt(p)))
    stations = []

    for i in range(q):
        for j in range(q):
            center_x = x_min + (i+0.5)*(x_max-x_min)/q
            center_y = y_min + (j+0.5)*(y_max-y_min)/q

            # Corners of each rectangle
            min_x_corner = x_min + i*(x_max-x_min)/q
            max_x_corner = x_min + (i+1)*(x_max-x_min)/q
            min_y_corner = y_min + j*(y_max-y_min)/q
            max_y_corner = y_min + (j+1)*(y_max-y_min)/q

            contained = []
            for index, point in enumerate(coordinates):
                x = point[0]
                y = point[1]

                if(x>=min_x_corner and x<=max_x_corner and y>=min_y_corner and y<=max_y_corner):
                    contained.append(index)

            if contained:
                distances_to_center = [
                    euclidean_distance(coordinates[index],[center_x, center_y])

                    for index in contained
                ]
                best_point_index = contained[distances_to_center.index(min(distances_to_center))]
                stations.append(best_point_index)

    if 0 not in stations:
        stations.insert(0,0)

    while len(stations)>p:
        min_distance = float('inf')
        couple_to_merge= (0,0)


        for i in range(len(stations)):
            for j in range(i+1, len(stations)):
                distance = distances[stations[i]][stations[j]]
                if distance < min_distance : 
                    min_distance = distance
                    couple_to_merge = (i,j)

        stations.pop(couple_to_merge[1])

    assigned_to = np.zeros(n, dtype=int)
    cost = 0

    for index in range(n):

        if index in stations:
            assigned_to[index] = index
        else:
            min_distance = float('inf')
            closest = 0

            for station_index in stations:
                distance = euclidean_distance(coordinates[index], coordinates[station_index])
                if distance < min_distance:
                    min_distance = distance
                    closest = station_index

            assigned_to[index]= closest
            cost+=min_distance
    stations.sort()
    return {
        'stations': stations,
        'assignments': assigned_to,
        'cost': cost,
    }


def nearest_neighbor_tsp(stations, distances):
    unvisited = stations.copy()
    current = unvisited.pop(0)
    path = [current]
    cost = 0

    while unvisited:
        distances_to_current = [distances[current][s] for s in unvisited]

        nearest_station_index = distances_to_current.index(min(distances_to_current))
        cost+=distances_to_current[nearest_station_index]
        current = unvisited.pop(nearest_station_index)
        path.append(current)
    
    return {
        'path': path,
        'cost': cost,
    }


def two_opt(path, distances):
    n = len(path)
    improved = True

    while improved:
        improved = False
        best_delta = 0
        best_i, best_j = None, None

        for i in range(n - 2):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue

                a, b = path[i], path[i + 1]
                c, d = path[j], path[(j + 1) % n]

                delta = (
                    distances[a][c] + distances[b][d]
                    - distances[a][b] - distances[c][d]
                )

                if delta < best_delta:
                    best_delta = delta
                    best_i, best_j = i, j

        if best_delta < 0:
            path[best_i+1:best_j+1] = reversed(path[best_i+1:best_j+1])
            improved = True

    cost = sum(
        distances[path[i]][path[(i+1) % n]] for i in range(n)
    )

    return {"path": path, "cost": cost}
