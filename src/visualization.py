import matplotlib.pyplot as plt


def plot_points(coordinates, title="Original Problem"):

    plt.figure(figsize=(10, 8))
    plt.scatter(coordinates[:, 0], coordinates[:, 1], c='blue', s=150, alpha=0.7,  marker='x', )

    for i, point in enumerate(coordinates):
        x = point[0]
        y = point[1]
        plt.text(x, y, str(i), fontsize=14, ha='right')
    
    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"results/{title.replace(' ', '_')}.png")
    plt.show()


def plot_solution(coordinates, stations, path, assignments, title="Solution"):

    plt.figure(figsize=(12, 10))
    
    for i, point in enumerate(coordinates):
        x = point[0]
        y = point[1]
        plt.text(x, y, str(i), fontsize=14, ha='right')

    # All points
    all_indices = list(range(len(coordinates)))
    non_stations = [i for i in all_indices if i not in stations]
    
    # Points non-stations
    plt.scatter(coordinates[non_stations, 0], coordinates[non_stations, 1], 
                c='gray', s=30, alpha=0.5, label="Points non-stations")
    
    # Stations
    plt.scatter(coordinates[stations, 0], coordinates[stations, 1], 
                c='red', s=100, marker='s', label="Stations", edgecolors='black')
    
    # Path of metro 
    for i in range(len(path)):
        j = (i + 1) % len(path)
        idx1, idx2 = path[i], path[j]
        plt.plot([coordinates[idx1, 0], coordinates[idx2, 0]],
                 [coordinates[idx1, 1], coordinates[idx2, 1]], 
                 'b-', linewidth=3, alpha=0.7, label="Cycle" if i == 0 else "")
    
    # Path for walking 
    if assignments is not None:
        for point_idx, station_idx in enumerate(assignments):
            if point_idx not in stations:
                plt.plot([coordinates[point_idx, 0], coordinates[station_idx, 0]],
                         [coordinates[point_idx, 1], coordinates[station_idx, 1]], 
                         'k:', linewidth=0.5, alpha=1)

    
    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"results/{title.replace(' ', '_')}.png")
    plt.show()
