
from data_loader import load_tsp_file
from heuristics import greedy_p_median

def main():

    coords, distances, n = load_tsp_file("./data/att48.tsp")
    print(greedy_p_median(coords,20,n))

if __name__ == "__main__":
    main()