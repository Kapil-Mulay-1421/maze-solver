# maze-solver

Contains the algorithms to determine, solve and maneuver a maze.

## How to Use

1. **Update the Walls Array**: 
   - Open the `flood_fill.py` file.
   - Locate the `walls` array in the `main` function. This array defines the walls in the maze as a list of tuples representing blocked paths. For example, `((4, 0), (4, 1))` represents a wall between squares `(4, 0)` and `(4, 1)`.
   - Update the `walls` array to create your own maze. Each wall should be defined as a tuple of tuples, where each inner tuple represents a coordinate in the maze.

2. **Run the Script**:
   - Open a terminal or command prompt.
   - Navigate to the directory containing the `flood_fill.py` file.
   - Run the script using the following command:

     ```bash
     python flood_fill.py
     ```

3. **Observe the Output**:
   - The script will print the mouse's movements and the walls it encounters.
   - The mouse will navigate the maze and print the number of moves it took to reach the goal.

## Example

In this example, the mouse starts at position `(4, 0)` and navigates to the goal at position `(2, 2)` while avoiding the walls defined in the `walls` array.

Feel free to modify the `walls` array and the maze dimensions to create your own custom mazes and test the mouse's navigation capabilities.