import numpy as np
from lidar import scan, get_walls

# Define a class mouse that will be used to represent the mouse in the maze
class Mouse:

    def __init__(self, x, y, known_walls, goal):
        self.x = x
        self.y = y
        self.known_walls = known_walls    
        self.goal = goal
        self.moves = 0

    def scan_walls(self):
        # use lidar for scanning the walls around the mouse
        # Define the walls as a list of tuples representing blocked paths. For example, ((4, 0), (4, 1)) represents a wall between squares (4, 0) and (4, 1).
        found_walls = scan(self.x, self.y)
        for wall in found_walls:
            if wall not in self.known_walls:
                print("Found a new wall between {} and {}".format(wall[0], wall[1]))
                self.known_walls.append(wall)

    def move(self, dx, dy):
        # Move the mouse
        self.x += dx
        self.y += dy
        print("Moved to position ({}, {})".format(self.x, self.y))
        return True

    def flood_fill(self):
        maze = np.zeros((5, 5))
        l = maze.shape[0]
        b = maze.shape[1]
        
        # Initialize the queue with the goal position
        queue = [self.goal]
        
        # Process the queue until it's empty
        while queue: 
            # Get the current position from the queue
            x, y = queue.pop(0)
            
            # Check all four possible directions (right, left, down, up)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                # Skip if the move is blocked by a wall
                if ((x, y), (x + dx, y + dy)) in self.known_walls or ((x + dx, y + dy), (x, y)) in self.known_walls:
                    continue
                
                # Check if the new position is within the maze boundaries
                if 0 <= x + dx < l and 0 <= y + dy < b:
                    # If the new position is empty and not the goal, update its value and add to the queue
                    if maze[x + dx, y + dy] == 0 and (x + dx, y + dy) != self.goal:
                        maze[x + dx, y + dy] = maze[x, y] + 1
                        queue.append((x + dx, y + dy))
        
        # Return the updated maze
        return maze

    def visualize_maze(self, maze):
        walls = get_walls()
        # Create a copy of the maze to visualize
        visual_maze = maze.copy()
        # Mark the mouse's current position
        visual_maze[self.x, self.y] = -1
        
        # Create a set of walls for easy lookup
        wall_set = set(walls)
        
        # Print the top border
        print("----" * visual_maze.shape[1])
        
        # Print the maze with walls
        for i in range(visual_maze.shape[0]):
            row = "|"
            for j in range(visual_maze.shape[1]):
                if visual_maze[i, j] == -1:
                    row += " M "
                elif visual_maze[i, j] == 0:
                    row += " G "
                else:
                    row += "{:2d} ".format(int(visual_maze[i, j])) 
                    # use row += "   " to view without flood_fill numbers, 
                    # and row += "{:2d} ".format(int(visual_maze[i, j])) to view with flood_fill numbers
                
                # Check for vertical walls
                if ((i, j), (i, j + 1)) in wall_set or ((i, j + 1), (i, j)) in wall_set or j == visual_maze.shape[1] - 1:
                    row += "|"
                else:
                    row += " "
            print(row)
            
            # Check for horizontal walls
            if i < visual_maze.shape[0] - 1:
                row = " "
                for j in range(visual_maze.shape[1]):
                    if ((i, j), (i + 1, j)) in wall_set or ((i + 1, j), (i, j)) in wall_set:
                        row += "--- "
                    else:
                        row += "    "
                print(row)
        
        # Print the bottom border
        print("----" * visual_maze.shape[1])


    def navigate(self, maze):
        l = maze.shape[0]
        b = maze.shape[1]
        while self.x != self.goal[0] or self.y != self.goal[1]:
            self.visualize_maze(maze)
            best_value = -1
            best_move = (0, 0)
            # Moves to the adjacent square with the least value
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    # Skip if the move is blocked by a wall
                    if ((self.x, self.y), (self.x + dx, self.y + dy)) in self.known_walls or ((self.x + dx, self.y + dy), (self.x, self.y)) in self.known_walls:
                        continue
                    
                    # Check if the new position is within the maze boundaries
                    if 0 <= self.x + dx < l and 0 <= self.y + dy < b:
                        if maze[self.x + dx, self.y + dy] < best_value or best_value == -1:
                            best_value = maze[self.x + dx, self.y + dy]
                            best_move = (dx, dy)
            # Move the mouse to the best position
            self.move(best_move[0], best_move[1])
            self.moves += 1
            self.scan_walls()
            maze = self.flood_fill()

        self.visualize_maze(maze)
        print("Goal reached in {} moves".format(self.moves))
        return