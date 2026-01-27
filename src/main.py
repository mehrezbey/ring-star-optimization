
from data_loader import load_tsp_file
from heuristics import greedy_p_median, nearest_neighbor_tsp
from visualization import plot_points, plot_solution

def main():

    coordinates, distances, n = load_tsp_file("./data/att48.tsp")
    res_greedy_p_median = greedy_p_median(coordinates,10,n,distances)
    res_tsp = nearest_neighbor_tsp(res_greedy_p_median["stations"],distances)

    plot_points(coordinates)

    plot_solution(
            coordinates, 
            res_greedy_p_median['stations'], 
            res_tsp["path"],
            res_greedy_p_median['assignments'],
        )

if __name__ == "__main__":
    main()