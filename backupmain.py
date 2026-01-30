
from data_loader import load_tsp_file
from heuristics import greedy_p_median, nearest_neighbor_tsp, two_opt
from visualization import plot_points, plot_solution,plot_points_with_rectangles

from meta import simulated_annealing
import time
import pandas as pd

def main():
    p=10
    file_name= "berlin52.tsp"
    exec_data = []

    coordinates, distances, n = load_tsp_file(f"./data/{file_name}")
    plot_points(coordinates,file_name)
    plot_points_with_rectangles(coordinates,p,file_name)

    start_time_heuristique = time.time()
    res_greedy_p_median = greedy_p_median(coordinates,p,n,distances)
    res_tsp = nearest_neighbor_tsp(res_greedy_p_median["stations"],distances)
    end_time_heuristique = time.time()
    exec_time_heuristique = end_time_heuristique - start_time_heuristique
    plot_solution(
            coordinates, 
            res_greedy_p_median['stations'], 
            res_tsp["path"],
            res_greedy_p_median['assignments'],
            f"Initial_Heuristic_Solution_{file_name}",
            res_greedy_p_median["cost"],
            res_tsp["cost"]
        )
    start_time_2opt = time.time()
    final_tour = two_opt(res_tsp["path"],distances)
    end_time_2opt = time.time()
    exec_time_2opt = end_time_2opt - start_time_2opt + exec_time_heuristique
    plot_solution(
            coordinates, 
            res_greedy_p_median['stations'], 
            final_tour["path"],
            res_greedy_p_median['assignments'],
            f"Final_Heuristic_Solution_{file_name}",
            res_greedy_p_median["cost"],
            final_tour["cost"]
        )
    
    start_time_meta = time.time()
    best = simulated_annealing(
        res_greedy_p_median["stations"],
        coordinates,
        distances,
        n
    )
    end_time_meta = time.time()
    exec_time_meta = end_time_meta - start_time_meta

    plot_solution(
        coordinates,
        best["stations"],
        best["path"],
        best["assignments"],
        f"simulated_annealing_{file_name}",
        best["cost"]
    )

    row = {
        'p': p,
        'heuristique_time': exec_time_heuristique,
        'heuristique_2opt_time': exec_time_2opt,
        'metaheuristique_time': exec_time_meta,
        'compact_time': 0
    }
    exec_data.append(row)
    df = pd.DataFrame(exec_data)
    print(df)

    # Save to CSV
    df.to_csv('results.csv', index=False, float_format='%.4f')
if __name__ == "__main__":
    main()