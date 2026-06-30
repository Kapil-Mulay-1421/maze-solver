from lidar import get_walls
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def visualize_maze(self, maze):
        print("calling visualize maze from visualizer.py")
        walls = self.known_walls
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
                
                # if ((i, j), (i, j + 1)) in wall_set or ((i, j + 1), (i, j)) in wall_set:
                if ((i, j), (i, j + 1)) in known_walls_set or ((i, j + 1), (i, j)) in known_walls_set:
                    ax.plot([j + 1, j + 1], [i+1, i], color='black', linewidth=2)
                else:
                    ax.plot([j + 1, j + 1], [i+1, i], color='white', linewidth=2)
                # if ((i, j), (i + 1, j)) in wall_set or ((i + 1, j), (i, j)) in wall_set:
                if ((i, j), (i + 1, j)) in known_walls_set or ((i + 1, j), (i, j)) in known_walls_set:
                    ax.plot([j, j + 1], [i+1, i+1], color='black', linewidth=2)
                else:
                    ax.plot([j, j + 1], [i+1, i+1], color='white', linewidth=2)

        plt.gca().invert_yaxis()
        plt.grid()
        plt.draw()
        plt.pause(0.01)  # Pause to allow the plot to update
    plt.show()        
