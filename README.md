# maze-solver

Contains the algorithms to determine, solve and maneuver a maze.

## How to Use

1. **Update the Walls Array**: 
   - Open the `lidar.py` file.
   - Locate the `get_walls` function. This function defines the walls in the maze as a list of tuples representing blocked paths. For example, `((4, 0), (4, 1))` represents a wall between squares `(4, 0)` and `(4, 1)`.
   - Update the `walls` array within the `get_walls` function to create your own maze. Each wall should be defined as a tuple of tuples, where each inner tuple represents a coordinate in the maze.

2. **Update the Start and Goal Points**:
   - Open the `main.py` file.
   - Locate the `main` function. This function sets the start and goal points for the mouse.
   - Update the `mouse` initialization to set the start point and the `goal` variable to set the goal point.

3. **Run the Script**:
   - Open a terminal or command prompt.
   - Navigate to the directory containing the `main.py` file.
   - Run the script using the following command:

     ```bash
     python main.py
     ```

4. **Observe the Output**:
   - The script will print the mouse's movements and the walls it encounters.
   - The mouse will navigate the maze and print the number of moves it took to reach the goal.

## Example

In this example, the mouse starts at position `(4, 0)` and navigates to the goal at position `(2, 2)` while avoiding the walls defined in the `walls` array.

Feel free to modify the `walls` array in the [lidar.py] file and the start/goal points in the [main.py] file to create your own custom mazes and test the mouse's navigation capabilities.