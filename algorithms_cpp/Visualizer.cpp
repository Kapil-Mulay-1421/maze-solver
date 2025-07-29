#include <iostream>
#include <vector>
#include <set>
#include <utility>
#include <iomanip>

class Visualizer {
public:
    int x, y; // Mouse's current position
    std::set<std::pair<std::pair<int, int>, std::pair<int, int>>> knownWalls;

    void visualizeMaze(const std::vector<std::vector<int>>& maze) {
        std::cout << "calling visualize maze from Visualizer.cpp" << std::endl;

        int rows = maze.size();
        int cols = maze[0].size();

        // Print the top border
        for (int i = 0; i < cols; ++i) std::cout << "----";
        std::cout << std::endl;

        for (int i = 0; i < rows; ++i) {
            std::string row = "|";

            for (int j = 0; j < cols; ++j) {
                if (i == x && j == y) {
                    row += " M ";
                } else if (maze[i][j] == 0) {
                    row += " G ";
                } else {
                    row += (maze[i][j] < 10 ? " " : "") + std::to_string(maze[i][j]) + " ";
                }

                if (j == cols - 1 || wallExists({i, j}, {i, j + 1})) {
                    row += "|";
                } else {
                    row += " ";
                }
            }

            std::cout << row << std::endl;

            // Print horizontal walls
            if (i < rows - 1) {
                std::string hRow = " ";
                for (int j = 0; j < cols; ++j) {
                    if (wallExists({i, j}, {i + 1, j})) {
                        hRow += "--- ";
                    } else {
                        hRow += "    ";
                    }
                }
                std::cout << hRow << std::endl;
            }
        }

        // Print the bottom border
        for (int i = 0; i < cols; ++i) std::cout << "----";
        std::cout << std::endl;
    }

private:
    bool wallExists(const std::pair<int, int>& a, const std::pair<int, int>& b) const {
        return knownWalls.count({a, b}) || knownWalls.count({b, a});
    }
};
