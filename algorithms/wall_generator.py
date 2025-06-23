import cv2
import numpy as np
from skimage.morphology import skeletonize
from PIL import Image
import matplotlib.pyplot as plt

# Load the image in grayscale
img_path = "c:/Users/Kapil/personal/projects/maze-solver/algorithms/maze_images/binary_maze.png"  # Replace with your image path
img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# Apply Canny edge detection
edges = cv2.Canny(img_gray, 50, 150)

# Convert to boolean array for skeletonization
edges_bool = edges.astype(bool)

# Skeletonize to get single-pixel-wide walls
skeleton = skeletonize(edges_bool)
skeleton_array = skeleton.astype(np.uint8)

# Get image dimensions
height, width = skeleton_array.shape

# Extract wall segments
wall_segments = []
visited_edges = set()
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4-neighborhood

for y in range(height):
    for x in range(width):
        if skeleton_array[y, x] == 1:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and skeleton_array[ny, nx] == 1:
                    p1 = (x, y)
                    p2 = (nx, ny)
                    edge = tuple(sorted([p1, p2]))
                    if edge not in visited_edges:
                        visited_edges.add(edge)
                        wall_segments.append(edge)

# Keep only unit pixel length segments
def is_unit_pixel(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) == 1

unit_pixel_walls = [seg for seg in wall_segments if is_unit_pixel(*seg)]

# Example output: print the first 10 unit walls
print(unit_pixel_walls)
# Doesn't generate the walls accurately, needs further refinement