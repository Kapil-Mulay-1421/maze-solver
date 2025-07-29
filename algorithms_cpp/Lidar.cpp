#include <vector>
#include <utility>
#include <iostream>

using Cell = std::pair<int, int>;
using Wall = std::pair<Cell, Cell>;

std::vector<Wall> getWalls() {
    std::vector<Wall> walls = {
        {{4, 0}, {4, 1}}, {{3, 1}, {3, 2}}, {{8, 0}, {8, 1}}, {{1, 1}, {2, 1}},
        {{2, 1}, {3, 1}}, {{9, 1}, {10, 1}}, {{10, 1}, {11, 1}},
        // ... Continue populating full list here as from Python version ...
        {{8, 16}, {8, 17}}, {{9, 16}, {9, 17}}
    };
    return walls;
}

std::vector<Wall> scan(int x, int y, std::pair<int, int> direction) {
    std::vector<Wall> allWalls = getWalls();
    std::vector<Wall> foundWalls;

    int dx = direction.first;
    int dy = direction.second;
    Cell current = {x, y};
    Cell forward = {x + dx, y + dy};

    std::cout << "Scanning from: (" << x << ", " << y << ") towards (" << forward.first << ", " << forward.second << ")\n";

    for (const Wall& wall : allWalls) {
        if ((wall.first == current && wall.second == forward) ||
            (wall.second == current && wall.first == forward)) {
            foundWalls.push_back(wall);
            std::cout << "Returning wall in front at: (" << forward.first << ", " << forward.second << ")\n";
            return foundWalls;
        }
    }

    // If no wall directly ahead, look for surrounding walls of cell in front
    for (const Wall& wall : allWalls) {
        if (wall.first == forward || wall.second == forward) {
            foundWalls.push_back(wall);
        }
    }

    return foundWalls;
}
