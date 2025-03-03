import numpy as np

# Define a class mouse that will be used to represent the mouse in the maze
class Mouse:

    def __init__(self, x, y, known_walls, goal):
        self.x = x
        self.y = y
        self.known_walls = known_walls    
        self.goal = goal
        self.moves = 0

    def scan_walls(self):
        # simulates lidar by scanning the walls around the mouse
        # Define the walls as a list of tuples representing blocked paths. For example, ((4, 0), (4, 1)) represents a wall between squares (4, 0) and (4, 1).
        walls = [((4, 0), (4, 1)), ((3, 1), (3, 0)), ((2, 0), (1, 0)), ((0, 1), (1, 1)), ((0, 2), (1, 2)), ((1, 3), (1, 2)), ((1, 4), (1, 3)), ((1, 2), (2, 2)), ((2, 2), (2, 1)), ((3, 2), (3, 1)), ((3, 2), (4, 2)), ((3, 3), (4, 3)), ((2, 3), (2, 2)), ((2, 3), (3, 3)), ((2, 3), (2, 4))]
        for wall in walls:
            if (self.x, self.y) == wall[0] or (self.x, self.y) == wall[1]:
                print("Found wall: ", wall)
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
    
    def navigate(self, maze):
        l = maze.shape[0]
        b = maze.shape[1]
        while self.x != self.goal[0] or self.y != self.goal[1]:
            print(maze)
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

        print("Goal reached in {} moves".format(self.moves))
        return
       

def main():
        
    # Initialize a 5x5 maze with zeros
    maze = np.zeros((5, 5))
    
    # Set the goal position
    goal = (2, 2)
    maze[goal] = 0
    
    mouse = Mouse(2, 1, [], goal) # Initialize the mouse at position (2, 1), pass empty known_walls list
    mouse.scan_walls()
    maze = mouse.flood_fill()
    mouse.navigate(maze)

# Run the main function
main()