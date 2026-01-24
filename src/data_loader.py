import tsplib95
import numpy as np



def load_tsp_file(path):
    problem = tsplib95.load(path)
    n = problem.dimension
    coordinates = []
    
    for i in range(1,n+1):
        coordinates.append(problem.node_coords[i])
    coordinates = np.array(coordinates)
    distances = np.zeros((n,n))

    for i in range(n):
        for j in range(i+1,n):
            distance = np.linalg.norm(coordinates[i] - coordinates[j])
            distances[i][j] = distance
            distances[i][j] = distance
    
    return coordinates, distances, n

def get_instance_info(path):
    problem = tsplib95.load(path)
    print(f"Nom: {problem.name}")
    print(f"Dimension: {problem.dimension}")
    print(f"Type: {problem.type}")
    return problem

print(get_instance_info("./data/att48.tsp"))