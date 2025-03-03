def flood_fill(self, goal, walls):
        maze = np.zeros((5, 5))
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