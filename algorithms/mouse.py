import numpy as np
from lidar import scan, get_walls
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as mpath
import matplotlib.bezier as bz
import matplotlib.animation as animation
from scipy.interpolate import make_splprep

# Define a class mouse that will be used to represent the mouse in the maze
class Mouse:

    def __init__(self, x, y, known_walls, goal, known_paths, known_moves):
        self.x = x
        self.y = y
        self.direction = (1, 0) # (1, 0): +x, (0, 1): +y, (-1, 0): -x, (0, -1): -y
        self.known_walls = known_walls
        self.goal = goal
        self.moves = 0
        self.known_moves = known_moves
        self.known_paths = known_paths

    def scan_walls(self):
        # use lidar for scanning the walls around the mouse
        # Define the walls as a list of tuples representing blocked paths. For example, ((4, 0), (4, 1)) represents a wall between squares (4, 0) and (4, 1).
        found_walls = scan(self.x, self.y, self.direction)
        for wall in found_walls:
            if wall not in self.known_walls:
                print("Found a new wall between {} and {}".format(wall[0], wall[1]))
                self.known_walls.append(wall)

    def move_forward(self):
        # Move the mouse
        self.x += self.direction[0]
        self.y += self.direction[1]
        print("Moved to position ({}, {})".format(self.x, self.y))
        return True

    def flood_fill(self):
        maze = np.zeros((16, 16))
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

    def visualize_maze_gui(self, maze, positions, known_walls_at_each_step):
        walls = get_walls()
        wall_set = set(walls)
        # print(known_walls_at_each_step)
        
        fig = plt.figure()
        for k in range(len(positions)):
            known_walls_set = set(known_walls_at_each_step[k])
            # print("known walls at step {}: {}".format(k, known_walls_at_each_step[k]))
            visual_maze = maze.copy()
            plt.clf()
            ax = fig.add_subplot(111)
            ax.set_xlim(0, visual_maze.shape[1])
            ax.set_ylim(0, visual_maze.shape[0])
            ax.set_aspect('equal')
            ax.set_title("step {}".format(k))
            visual_maze[positions[k][0], positions[k][1]] = -1

            for i in range(visual_maze.shape[0]):
                for j in range(visual_maze.shape[1]):
                    if visual_maze[i, j] == -1:
                        scat = ax.scatter(j + 0.5, i+0.5, color='blue', s=100)
                        ax.add_artist(scat)
                    elif visual_maze[i, j] == 0 and (i, j) == self.goal:
                        rect = patches.Rectangle((j, i), 1, 1, linewidth=1, edgecolor='black', facecolor='green')
                        ax.add_patch(rect)
                    
                    if ((i, j), (i, j + 1)) in wall_set or ((i, j + 1), (i, j)) in wall_set:
                        if ((i, j), (i, j + 1)) in known_walls_set or ((i, j + 1), (i, j)) in known_walls_set:
                            ax.plot([j + 1, j + 1], [i+1, i], color='blue', linewidth=2)
                        else:
                            ax.plot([j + 1, j + 1], [i+1, i], color='red', linewidth=2)
                    if ((i, j), (i + 1, j)) in wall_set or ((i + 1, j), (i, j)) in wall_set:
                        if ((i, j), (i + 1, j)) in known_walls_set or ((i + 1, j), (i, j)) in known_walls_set:
                            ax.plot([j, j + 1], [i+1, i+1], color='blue', linewidth=2)
                        else:
                            ax.plot([j, j + 1], [i+1, i+1], color='red', linewidth=2)

            plt.gca().invert_yaxis()
            plt.grid()
            plt.draw()
            plt.pause(0.01)  # Pause to allow the plot to update
        plt.show()        



    def navigate(self, maze, reverse=False):
        self.moves = 0
        l = maze.shape[0]
        b = maze.shape[1]
        print(maze.shape)

        moves = []
        known_walls_at_each_step = [self.known_walls.copy()] # for visualization purposes. Remove during production.
        positions = [(self.x, self.y)]
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
            if self.direction == (best_move[0], best_move[1]):
                # If the best move is in the same direction, move forward
                self.move_forward()
            else:
                # If the best move is in a different direction, change direction
                self.direction = (best_move[0], best_move[1])
                print("Changed direction to ({}, {})".format(self.direction[0], self.direction[1]))
                # Scan the walls in the new direction
                self.scan_walls()
                self.move_forward()

            moves += [best_move]

            self.moves += 1
            positions += [(self.x, self.y)]
            self.scan_walls()
            known_walls_at_each_step.append(self.known_walls.copy())
            print("known walls at step {}: {}".format(self.moves, known_walls_at_each_step[-1]))
            maze = self.flood_fill()

        print("known walls in first step: ", known_walls_at_each_step[0])
        self.visualize_maze(maze)
        print("initializing gui")
        self.visualize_maze_gui(maze, positions, known_walls_at_each_step)
        if reverse:
            print("moves in reverse: ", moves)
            moves, positions = self.reverse(moves, positions)
        self.optimize_and_memorize(moves, positions)
        print("Goal reached in {} moves".format(self.moves))
        print("Path: {}".format(self.known_paths[-1]))
        return
    
    def optimize_and_memorize(self, moves, positions):
        # removes the moves between instances when the same position is reached
        for i in range(len(moves)):
            for j in range(len(moves), i, -1):
                if positions[i] == positions[j]:
                    del moves[i:j]
                    del positions[i:j]
                    break
        self.known_moves += [moves]
        self.known_paths += [positions]
        return
    
    def reverse(self, moves, positions):
        # given the path taken from goal to starting point, determines the path from starting point to goal
        for i in range(len(moves)):
            moves[i] = (-moves[i][0], -moves[i][1])
        moves.reverse()
        positions.reverse() 
        return moves, positions
    
    def segmentize(self, moves, path):
        segments = [] 
        l = 0
        for i in range(len(moves)):
            if i+2<len(moves):
                if moves[i+1] != moves[i+2]:
                    segments.append(path[l:i+2])
                    l = i+1
        return segments

    def get_positions_for_plotting(self, moves, path):
        # change function to get the correct control points
        plot_path = []
        print(moves)
        intensity = 0.0
        for i, position in enumerate(path):
            offset = [0.5, 0.5]
            if i+1<len(moves):
                if moves[i+1] != moves[i]:
                    offset[0] += -intensity*moves[i+1][0]
                    offset[1] += -intensity*moves[i+1][1]
                elif i+2<len(moves):
                    if moves[i+2] != moves[i+1]:
                        offset[0] += -intensity*moves[i+2][0]
                        offset[1] += -intensity*moves[i+2][1]
            plot_path.append((position[0]+offset[0], position[1]+offset[1]))
        return plot_path
    
    def minimum_time_trajectory_optimize(self):
        plot_paths = []
        for i, path in enumerate(self.known_paths): 
            plot_path = self.get_positions_for_plotting(self.known_moves[i], path)    
            plot_paths.append(plot_path)
        return plot_paths
    
