#ifndef LIDAR_HPP
#define LIDAR_HPP

#include <vector>
#include <utility>

// Type aliases for convenience
using Cell = std::pair<int, int>;
using Wall = std::pair<Cell, Cell>;

// Returns the full set of known walls
std::vector<Wall> getWalls();

// Scans from the given (x, y) position in the given direction
// Returns the walls detected in front and around
std::vector<Wall> scan(int x, int y, std::pair<int, int> direction);

#endif // LIDAR_HPP
