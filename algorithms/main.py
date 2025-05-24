# Import the Mouse class from mouse.py
from mouse import Mouse
import numpy as np
from visualizer import show_optimized_trajectory

def main():
    # Initialize a 5x5 maze with zeros
    maze = np.zeros((16, 16))

    # Set start_point
    start_point = (0, 0)
    
    # Set the goal position
    goal = (8, 8)
    maze[goal] = 0
    
    # Create a mouse instance and navigate the maze
    mouse = Mouse(start_point[0], start_point[1], [], goal, [], [])
    mouse.scan_walls()
    maze = mouse.flood_fill()
    mouse.navigate(maze)

    print(mouse.x, mouse.y)

    mouse.goal = (start_point[0], start_point[1])
    maze = mouse.flood_fill()
    mouse.navigate(maze, reverse=True)

    print(mouse.x, mouse.y)

    mouse.goal = goal
    mouse.flood_fill()
    mouse.navigate(maze)

    print(mouse.x, mouse.y)

    mouse.goal = (start_point[0], start_point[1])
    maze = mouse.flood_fill()
    mouse.navigate(maze, reverse=True)
    # plot_paths = mouse.minimum_time_trajectory_optimize()
    # print('paths', plot_paths)
    # for path in plot_paths:
    #     show_optimized_trajectory(path, maze, start_point)

# Run the main function
if __name__ == "__main__":
    main()