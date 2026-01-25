import numpy as np
import random


def greedy_p_median(coordinates, p, n):
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
                distances = [np.linalg.norm(coordinates[index] - [center_x, center_y]) 
                            for index in contained]
                best_point_index = contained[np.argmin(distances)]
                stations.append(best_point_index)

    if 0 not in stations:
        stations.insert(0,0)

    while len(stations)>p:
        min_distance = float('inf')
        couple_to_merge= (0,0)


        for i in range(len(stations)):
            for j in range(i+1, len(stations)):
                distance = np.linalg.norm(coordinates[stations[i]] - coordinates[stations[j]])
                if distance < min_distance : 
                    min_distance = distance
                    couple_to_merge = (i,j)

        stations.pop(couple_to_merge[1])

    assigned_to = np.zeros(n)
    cost = 0

    for index in range(n):
        if index in stations:
            assigned_to[index] = index
        else:
            min_distance = float('inf')
            closest = 0

            for station_index in stations:
                distance = np.linalg.norm(coordinates[index] - coordinates[station_index])
                if distance < min_distance:
                    min_distance = distance
                    closest = station_index

            assigned_to[index]= closest
            cost+=min_distance

    return {
        'stations': stations,
        'assignments': assigned_to,
        'cost': cost,
    }






