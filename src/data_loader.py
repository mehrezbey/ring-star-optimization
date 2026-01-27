import tsplib95
import numpy as np
from utils import euclidean_distance


def load_tsp_file(path):
    try:
        problem = tsplib95.load(path)
        n = problem.dimension
        coordinates = []
        # Read the coordinates of points
        for i in range(1,n+1):
            coordinates.append(problem.node_coords[i])
        coordinates = np.array(coordinates)

        # Calculate the distance between each 2 points
        distances = np.zeros((n,n))
        for i in range(n):
            for j in range(i+1,n):
                distance = euclidean_distance(coordinates[i], coordinates[j])
                distances[i][j] = distance
                distances[j][i] = distance
        
        return coordinates, distances, n
    
    except FileNotFoundError:
        print(f"Error: File not found.")
        return None
    
    except Exception as e:
        print(f"Unexpected exception  {e}.")
        return None