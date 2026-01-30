import matplotlib.pyplot as plt
import os
import numpy as np

def plot_points(coordinates, title):


    plt.figure(figsize=(10, 8))
    plt.scatter(coordinates[:, 0], coordinates[:, 1], c='blue', s=150, alpha=0.7,  marker='x', )

    for i, point in enumerate(coordinates):
        x = point[0]
        y = point[1]
        plt.text(x, y, str(i), fontsize=14, ha='right')
    title = "Original Problem " + title
    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"results/{title.replace(' ', '_')}.png")
    plt.show()

def plot_solution(coordinates, stations, path, assignments, title="Solution", walking_cost=0, inter_station_cost=0):

    plt.figure(figsize=(12, 10))

    for i, point in enumerate(coordinates):
        x = point[0]
        y = point[1]
        plt.text(x, y, str(i), fontsize=14, ha='right')

    # All points
    all_indices = list(range(len(coordinates)))
    non_stations = [i for i in all_indices if i not in stations]
    
    # Points nonn stations
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

    
    plt.title(title + f"Total = {(walking_cost+ inter_station_cost):.2f} | Walking Cost = {walking_cost:.2f} | Interstation Cost = {inter_station_cost:.2f}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"results/{title.replace(' ', '_')}.png")
    plt.show()



def plot_points_with_rectangles(coordinates, p, title):

    plt.figure(figsize=(12, 10))
    plt.scatter(coordinates[:, 0], coordinates[:, 1],  
                c='blue', s=100, alpha=0.7, marker='o', label="Points")
    
    for i, point in enumerate(coordinates):
        x, y = point[0], point[1]
        plt.text(x, y, str(i), fontsize=9, ha='right', va='bottom')
    
    x_min, x_max = coordinates[:, 0].min(), coordinates[:, 0].max()
    y_min, y_max = coordinates[:, 1].min(), coordinates[:, 1].max()
    
    q = int(np.ceil(np.sqrt(p)))
    rectangles_info = []  
    
    for i in range(q):
        for j in range(q):
            rect_x_min = x_min + i * (x_max - x_min) / q
            rect_x_max = x_min + (i + 1) * (x_max - x_min) / q
            rect_y_min = y_min + j * (y_max - y_min) / q
            rect_y_max = y_min + (j + 1) * (y_max - y_min) / q
            center_x = x_min + (i + 0.5) * (x_max - x_min) / q
            center_y = y_min + (j + 0.5) * (y_max - y_min) / q
            rect_info = {
                'id': (i, j),
                'bounds': (rect_x_min, rect_x_max, rect_y_min, rect_y_max),
                'center': (center_x, center_y),
                'color': plt.cm.tab20((i * q + j) / (q * q))
            }
            rectangles_info.append(rect_info)
            
            rect_color = rect_info['color']
            rect_alpha = 0.3
            
            rect = plt.Rectangle(
                (rect_x_min, rect_y_min),
                rect_x_max - rect_x_min,
                rect_y_max - rect_y_min,
                linewidth=1.5,
                edgecolor=rect_color,
                facecolor=rect_color,
                alpha=rect_alpha,
                linestyle='--'
            )
            plt.gca().add_patch(rect)
            
            plt.scatter([center_x], [center_y], 
                       c=[rect_color], s=200, marker='+', linewidths=2,
                       label=f"Centre rectangle ({i},{j})" if i == 0 and j == 0 else "")
    
    
    plt.title(f"{title}\nDivision en {q}×{q} rectangles, p={p}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()
    filename = f"results/rectangles_p{p}_{title.replace(' ', '_')}.png"
    plt.savefig(filename, dpi=150)    
    plt.show()
    return rectangles_info