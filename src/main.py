from data_loader import load_tsp_file
from heuristics import greedy_p_median, nearest_neighbor_tsp, two_opt
from visualization import plot_points, plot_solution ,plot_points_with_rectangles
from plne_compact import solve_ring_star_plne, build_cycle_from_edges
from meta import simulated_annealing
import time
import os

def main():
    # Ensure results directory exists
    os.makedirs('results', exist_ok=True)
    
    while True:
        test=-1
        exec_data = []
        while(not 0<=test<=2):
            print("--------------------------------Menu--------------------------------\n"
            "0 - Quitter\n"
            "1 - att48\n"
            "2 - berlin52\n"
            )
            test=int(input("Saisie ton choix : "))
        if test==0:
                break
        elif test==2:
                file_name= "berlin52.tsp"
        else:
                file_name= "att48.tsp"
        coordinates, distances, n = load_tsp_file(f"data/{file_name}")
        plot_points(coordinates, file_name)
        p=10
        while(not 1<=p<=n):
            print("Donne la valeur de p : ")
            p=int(input(""))
        choix=0
        while(not 1<=choix<=2):
            print("--------------------------------Methode--------------------------------\n"
            "1 - Heuristique & 2-Opt & Metaheuristique\n"
            "2 - Compacte\n"
            )
            choix=int(input("Saisie ton choix : "))
        if choix==1:
            plot_points_with_rectangles(coordinates, p, file_name)
            start_time_heuristique= time.time()
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
                f"After 2 OPT_{file_name}",
                res_greedy_p_median["cost"],
                final_tour["cost"]
            )
            print(
            f"walking {res_greedy_p_median['cost']}\n"
            f"tsp {res_tsp['cost']}\n"
            f"2-opt {final_tour['cost']}"
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
                'compact_time': 30
            }
            exec_data.append(row)
            # Save results: use pandas if installed, otherwise fallback to csv
            try:
                import pandas as pd
            except Exception:
                pd = None

            if pd:
                df = pd.DataFrame(exec_data)
                print(df)
                df.to_csv('results.csv', index=False, float_format='%.4f')
            else:
                import csv
                if exec_data:
                    fieldnames = list(exec_data[0].keys())
                else:
                    fieldnames = ['p','heuristique_time','heuristique_2opt_time','metaheuristique_time','compact_time']
                with open('results.csv', 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for r in exec_data:
                        formatted = {k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in r.items()}
                        writer.writerow(formatted)
                for r in exec_data:
                    print(r)
        else:
            alpha=1.0
            while(not 0<=alpha<=10):
                print("Donne la valeur de alpha : ")
                alpha=float(input(""))
            solution = solve_ring_star_plne(coordinates, distances,p,alpha)
            cycle_path = build_cycle_from_edges(solution["cycle"])
            plot_solution(
                coordinates,
                solution["stations"],
                cycle_path,
                solution["assignments"],
                title=f"PLNE solution",
                walking_cost=solution["cost2"],
                inter_station_cost=solution["cost"]
            )



if __name__ == "__main__":
    main()