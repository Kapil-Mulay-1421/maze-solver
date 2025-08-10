// main.cpp

#include "Mouse.hpp"
int main(int argc, char** argv) {

    // Initialize a 16x16 maze with zeros
    std::vector<std::vector<int>> maze(16, std::vector<int>(16, 0));

    std::pair<int, int> start_point = {0, 0};
    std::pair<int, int> goal = {8, 8};

    // Create a Mouse object
    Mouse mouse(start_point.first, start_point.second, {}, goal, maze, {}, "right_first");

    // First navigation to goal
    std::cout << "scanning walls" << std::endl;
    mouse.scanWalls();
    std::cout << "flood filling maze" << std::endl;
    maze = mouse.floodFill();
    std::cout << "navigating to goal" << std::endl;
    mouse.navigate(maze);


    // Navigate back to start
    mouse.setGoal(start_point);
    mouse.scanWalls();
    maze = mouse.floodFill();
    mouse.navigate(maze, true);


    // Navigate to goal again
    mouse.setGoal(goal);
    mouse.scanWalls();
    maze = mouse.floodFill();
    mouse.navigate(maze);


    // Navigate back again to start
    mouse.setGoal(start_point);
    mouse.scanWalls();
    maze = mouse.floodFill();
    mouse.navigate(maze, true);

    // Print all found paths
    std::cout << "All paths found:\n";
    for (const auto& path : mouse.getKnownPaths()) {
        std::cout << "Path: ";
        for (auto& p : path.positions) {
            std::cout << "(" << p.first << "," << p.second << ") ";
        }
        std::cout << "\nLength: " << path.optimizedLength
                  << ", Turns: " << path.optimizedTurns
                  << ", Feasibility Score: " << path.feasibilityScore << "\n\n";
    }

    // Get and print best path
    auto best_path = mouse.getBestPath();
    std::cout << "The best path is:\n";
    for (auto& p : best_path->positions) {
        std::cout << "(" << p.first << "," << p.second << ") ";
    }
    std::cout << "\nLength: " << best_path->optimizedLength
              << ", Turns: " << best_path->optimizedTurns
              << ", Feasibility Score: " << best_path->feasibilityScore << "\n";

    return 0;
}
