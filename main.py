
from data_loader import load_tsp_file
from heuristics import greedy_p_median, nearest_neighbor_tsp, two_opt
from visualization import plot_points, plot_solution
from plne_compact import solve_ring_star_plne, build_cycle_from_edges


def main():

    coordinates, distances, n = load_tsp_file("../data/att48.tsp")
    res_greedy_p_median = greedy_p_median(coordinates,10,n,distances)
    res_tsp = nearest_neighbor_tsp(res_greedy_p_median["stations"],distances)


    plot_points(coordinates)

    plot_solution(
            coordinates, 
            res_greedy_p_median['stations'], 
            res_tsp["path"],
            res_greedy_p_median['assignments'],
        )
    final_tour = two_opt(res_tsp["path"],distances)
    plot_solution(
            coordinates, 
            res_greedy_p_median['stations'], 
            final_tour["path"],
            res_greedy_p_median['assignments'],
            "After 2 OPT"
        )
    print(
    f"walking {res_greedy_p_median['cost']}\n"
    f"tsp {res_tsp['cost']}\n"
    f"2-opt {final_tour['cost']}"
    )

    solution = solve_ring_star_plne(coordinates, distances,p=10)
    cycle_path = build_cycle_from_edges(solution["cycle"])
    
    plot_solution(
        coordinates,
        solution["stations"],
        cycle_path,
        solution["assignments"],
        title=f"PLNE solution – cost = {solution['cost']:.2f}"
    )




if __name__ == "__main__":
    main()