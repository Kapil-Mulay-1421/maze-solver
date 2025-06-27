import numpy as np
from lidar import scan
from path import Path
from visualizer import visualize_maze, visualize_maze_gui
from ros_simulator_copy import RosSimulator
import time


# Define a class mouse that will be used to represent the mouse in the maze
class Mouse:

    def __init__(self, x, y, known_walls, goal, known_paths, known_moves, mode='left_first'):
        self.x = x
        self.y = y
        self.direction = (1, 0) # (1, 0): +x, (0, 1): +y, (-1, 0): -x, (0, -1): -y
        self.known_walls = known_walls
        self.goal = goal
        self.moves = 0
        self.known_paths = known_paths
        self.mode = mode  # 'left_first' or 'right_first'
        self.sim = RosSimulator()

    def analyze_tof_distances(self, tof_front, tof_left, tof_right):
        """
        Returns booleans for specific ToF distance conditions.

        Args:
            tof_front (float): Front ToF sensor distance (in cm).
            tof_left (float): Left ToF sensor distance (in cm).
            tof_right (float): Right ToF sensor distance (in cm).

        Returns:
            Tuple[bool, bool, bool, bool]: 
                1. Front distance between 10 and 15 cm
                2. Front distance between 35 and 40 cm
                3. Left distance between 24.438 and 33.425 cm
                4. Right distance between 24.438 and 33.425 cm
        """
        front_close = 0.01 <= tof_front <= 0.23
        front_far = 0.35 <= tof_front <= 0.5
        left_in_range = 0.21438 <= tof_left <= 0.36425
        right_in_range = 0.21438 <= tof_right <= 0.36425

        return front_close, front_far, left_in_range, right_in_range

    def scan_walls(self):
        # use lidar for scanning the walls around the mouse
        # Define the walls as a list of tuples representing blocked paths. For example, ((4, 0), (4, 1)) represents a wall between squares (4, 0) and (4, 1).
        # found_walls = scan(self.x, self.y, self.direction)
        # for wall in found_walls:
        #     if wall not in self.known_walls or ((wall[1], wall[0]) not in self.known_walls):
        #         print("Found a new wall between {} and {}".format(wall[0], wall[1]))
        #         self.known_walls.append(wall)

        tof_front = self.sim.get_tof_front_distance()
        tof_left = self.sim.get_tof_left_distance()
        tof_right = self.sim.get_tof_right_distance()
        print(tof_front, tof_left, tof_right)
        front_close, front_far, left_in_range, right_in_range = self.analyze_tof_distances(tof_front, tof_left, tof_right)
        print(front_close, front_far, left_in_range, right_in_range )
        if front_close:
            wall = ((self.x, self.y), (self.x+self.direction[0], self.y+self.direction[1]))
            if wall not in self.known_walls:
                self.known_walls.append(wall)
            return
        
        if front_far:
            wall = ((self.x+self.direction[0], self.y+self.direction[1]), (self.x+2*self.direction[0], self.y+2*self.direction[1]))
            if wall not in self.known_walls:
                self.known_walls.append(wall)
        if left_in_range:
            wall = ((self.x+self.direction[0], self.y+self.direction[1]), (self.x+self.direction[0]+self.get_left()[0], self.y+self.direction[1]+self.get_left()[1]))
            if wall not in self.known_walls:
                self.known_walls.append(wall)
        if right_in_range:
            wall = ((self.x+self.direction[0], self.y+self.direction[1]), (self.x+self.direction[0]+self.get_right()[0], self.y+self.direction[1]+self.get_right()[1]))
            if wall not in self.known_walls:
                self.known_walls.append(wall)

        print("known walls: ", self.known_walls)

    
    def get_left(self):
        # Get the left direction based on the current direction
        if self.direction == (1, 0):
            return (0, 1)
        elif self.direction == (0, 1):
            return (-1, 0)
        elif self.direction == (-1, 0):
            return (0, -1)
        elif self.direction == (0, -1):
            return (1, 0)
        
    def get_right(self):
        # Get the right direction based on the current direction
        if self.direction == (1, 0):
            return (0, -1)
        elif self.direction == (0, 1):
            return (1, 0)
        elif self.direction == (-1, 0):
            return (0, 1)
        elif self.direction == (0, -1):
            return (-1, 0)
        
    def change_direction(self, new_direction):
        if new_direction == self.get_left():
            self.turn_left()
        elif new_direction == self.get_right():
            self.turn_right()
        elif new_direction[0] == -self.direction[0] and new_direction[1] == -self.direction[1]:
            self.turn_around()
        else:
            print("Invalid direction change requested: {}".format(new_direction))

    # interface functions
    def turn_left(self):
        self.sim.turn_left()
        self.direction = self.get_left()

    def turn_right(self):
        self.sim.turn_right()
        self.direction = self.get_right()

    def turn_around(self):
        self.sim.turn_left()
        self.sim.turn_left()
        self.turn_left()
        self.turn_left()

    def move_forward(self):
        feedback = self.sim.move_forward()
        position = feedback.pose.pose.position
        rel_x = (position.x - (-1.5))/0.25
        rel_y = (position.y - (-2.35))/0.25
        print(rel_x, rel_y)
        # self.x += self.direction[0]
        # self.y += self.direction[1]
        self.x = round(rel_x)
        self.y = round(rel_y)
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

    def navigate(self, maze, reverse=False):
        self.moves = 0
        l = maze.shape[0]
        b = maze.shape[1]
        print(maze.shape)

        moves = []
        known_walls_at_each_step = [self.known_walls.copy()] # for visualization purposes. Remove during production.
        positions = [(self.x, self.y)]
        while self.x != self.goal[0] or self.y != self.goal[1]:
            visualize_maze(self, maze)
            best_value = -1
            best_move = (0, 0)
            # Moves to the adjacent square with the least value
            if self.mode == 'left_first':
                # Check left, forward, right, backward in that order
                directions = [self.direction, self.get_left(), self.get_right(), (-self.direction[0], -self.direction[1])]
            else:
                # Check right, forward, left, backward in that order
                directions = [self.direction, self.get_right(), self.get_left(), (-self.direction[0], -self.direction[1])]
            for dx, dy in directions:
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
                self.moves += 1
                moves += [best_move]
                positions += [(self.x, self.y)]
                known_walls_at_each_step.append(self.known_walls.copy())
            else:
                # If the best move is in a different direction, change direction
                self.change_direction((best_move[0], best_move[1]))
                print("Changed direction to ({}, {})".format(self.direction[0], self.direction[1]))

            self.scan_walls()
            maze = self.flood_fill()

        visualize_maze(self, maze)
        visualize_maze_gui(self, maze, positions, known_walls_at_each_step)
        if reverse:
            # print("moves in reverse: ", moves)
            moves, positions = self.reverse(moves, positions)
        self.remove_loops_and_memorize(moves, positions)
        print("Goal reached in {} moves".format(self.moves))
        print("Number of moves after loop removal and optimization: {}".format(self.known_paths[-1].optimized_length))
        print("Number of turns after loop removal and optimization: {}".format(self.known_paths[-1].optimized_turns))
        print("Path: {}".format(self.known_paths[-1].positions))
        return
    
    def remove_loops_and_memorize(self, moves, positions):
        # removes the moves between instances when the same position is reached
        for i in range(len(moves)):
            for j in range(len(moves), i, -1):
                if positions[i] == positions[j]:
                    del moves[i:j]
                    del positions[i:j]
                    break
        print(len(moves), len(positions))
        self.known_paths.append(Path(positions, moves))
        return
    
    def reverse(self, moves, positions):
        # given the path taken from goal to starting point, determines the path from starting point to goal
        for i in range(len(moves)):
            moves[i] = (-moves[i][0], -moves[i][1])
        moves.reverse()
        positions.reverse() 
        return moves, positions
    
    def get_best_path(self):
        # Return the path with the highest feasibility score
        best_path = None
        for path in self.known_paths:
            if best_path is None or path.feasibility_score > best_path.feasibility_score:
                best_path = path
        return best_path
    
    


    
