def get_walls():
    # Define the walls as a list of tuples representing blocked paths. For example, ((4, 0), (4, 1)) represents a wall between squares (4, 0) and (4, 1).
    walls = [((4, 0), (4, 1)), ((3, 1), (3, 0)), ((2, 0), (1, 0)), ((0, 1), (1, 1)), ((0, 2), (1, 2)), ((1, 3), (1, 2)), ((1, 4), (1, 3)), ((1, 2), (2, 2)), ((2, 2), (2, 1)), ((3, 2), (3, 1)), ((3, 2), (4, 2)), ((3, 3), (4, 3)), ((2, 3), (2, 2)), ((2, 3), (3, 3)), ((2, 3), (2, 4))]
    return walls

def scan(x, y):
    # simulates lidar by returning the walls around the current position of the mouse
    walls = get_walls()
    found_walls = []
    for wall in walls:
        if (x, y) == wall[0] or (x, y) == wall[1]:
            found_walls.append(wall)
    return found_walls