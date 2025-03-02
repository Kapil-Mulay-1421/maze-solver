import numpy as np

def flood_fill(maze, goal, walls):
    # Get the dimensions of the maze
    l = maze.shape[0]
    b = maze.shape[1]
    
    # Initialize the queue with the goal position
    queue = [goal]
    
    # Process the queue until it's empty
    while queue: 
        # Get the current position from the queue
        x, y = queue.pop(0)
        
        # Check all four possible directions (right, left, down, up)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            # Skip if the move is blocked by a wall
            if ((x, y), (x + dx, y + dy)) in walls or ((x + dx, y + dy), (x, y)) in walls:
                continue
            
            # Check if the new position is within the maze boundaries
            if 0 <= x + dx < l and 0 <= y + dy < b:
                # If the new position is empty and not the goal, update its value and add to the queue
                if maze[x + dx, y + dy] == 0 and (x + dx, y + dy) != goal:
                    maze[x + dx, y + dy] = maze[x, y] + 1
                    queue.append((x + dx, y + dy))
    
    # Return the updated maze
    return maze

def main():
    # Define the walls as a list of tuples representing blocked paths. For example, ((4, 0), (4, 1)) represents a wall between squares (4, 0) and (4, 1)
    walls = [((4, 0), (4, 1)), ((3, 1), (3, 0)), ((2, 0), (1, 0)), ((0, 1), (1, 1)), ((0, 2), (1, 2)), ((1, 3), (1, 2)), ((1, 4), (1, 3)), ((1, 2), (2, 2)), ((2, 2), (2, 1)), ((3, 2), (3, 1)), ((3, 2), (4, 2)), ((3, 3), (4, 3)), ((2, 3), (2, 2)), ((2, 3), (3, 3)), ((2, 3), (2, 4))]
    
    # Initialize a 5x5 maze with zeros
    maze = np.zeros((5, 5))
    
    # Set the goal position
    goal = (2, 2)
    maze[goal] = 0
    
    # Perform the flood fill algorithm
    maze = flood_fill(maze, goal, walls)
    
    # Print the resulting maze
    print(maze)

# Run the main function
main()