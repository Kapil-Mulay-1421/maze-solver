import matplotlib.pyplot as plt
from lidar import get_walls
import matplotlib.animation as animation
import matplotlib.patches as patches
from scipy.interpolate import make_splprep

def show_optimized_trajectory(plot_path, maze, start_point):
    fig, ax = plt.subplots()
    visual_maze = maze.copy()
    ax.set_xlim(0, visual_maze.shape[1])
    ax.set_ylim(0, visual_maze.shape[0])
    ax.set_aspect('equal')
    # for point in bez_segment.control_points:
    #     ax.plot(point[1], point[0], 'ro')
    # t_values = [t / 100 for t in range(101)]  # 101 points from t=0 to t=1
    # curve_points = [bez_segment.point_at_t(t) for t in t_values]  # Compute Bézier curve

    # Extract X and Y coordinates
    # x_vals, y_vals = zip(*curve_points)
    # ax.plot(y_vals, x_vals, 'b-', label="Bézier Curve")  # Bézier curve
    print('plot path: ', plot_path)
    print('array  of x: ', [x for x, y in plot_path])
    spl, u = make_splprep([[y for x, y in plot_path], [x for x, y in plot_path]], s=0.1)
    ax.plot(spl(u), '--')
    ax.plot(plot_path, 'o')
    plt.gca().invert_yaxis()

    walls = get_walls()
    visual_maze[start_point[1], start_point[0]] = -1
    wall_set = set(walls)

    for i in range(visual_maze.shape[0]):
        for j in range(visual_maze.shape[1]):
            if visual_maze[i, j] == -1:
                scat = ax.scatter(j + 0.5, i+0.5, color='blue', s=100)
                ax.add_artist(scat)
            # elif visual_maze[i, j] == 0:
            #     rect = patches.Rectangle((j, i+1), 1, 1, linewidth=1, edgecolor='black', facecolor='green')
            #     ax.add_patch(rect)
            
            if ((i, j), (i, j + 1)) in wall_set or ((i, j + 1), (i, j)) in wall_set:
                ax.plot([j + 1, j + 1], [i+1, i], color='red', linewidth=2)
            if ((i, j), (i + 1, j)) in wall_set or ((i + 1, j), (i, j)) in wall_set:
                ax.plot([j, j + 1], [i+1, i+1], color='red', linewidth=2)

    # def update(i):
    #     scat.set_offsets((curve_points[i][1], curve_points[i][0]))
    #     return (scat,)
    
    # ani = animation.FuncAnimation(fig, update, repeat=True, frames=len(curve_points) - 1, interval=10)

    plt.grid()
    plt.show()