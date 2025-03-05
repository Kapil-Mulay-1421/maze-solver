# Import the Mouse class from mouse.py
from mouse import Mouse
import numpy as np

def main():
    # Initialize a 5x5 maze with zeros
    maze = np.zeros((5, 5))
    
    # Set the goal position
    goal = (2, 2)
    maze[goal] = 0
    
    # Create a mouse instance and navigate the maze
    mouse = Mouse(0, 0, [], goal)
    mouse.scan_walls()
    maze = mouse.flood_fill()
    mouse.navigate(maze)

# Run the main function
if __name__ == "__main__":
    main()