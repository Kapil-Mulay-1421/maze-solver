#ifndef MOUSE_HPP
#define MOUSE_HPP

#include <vector>
#include <string>
#include <utility>
#include <tuple>
#include <unordered_map>
#include <set>
#include "Path.cpp"
#include "Sim.hpp"
#include "Visualizer.cpp"
#include <memory>

struct pair_hash {
    template <class T1, class T2>
    std::size_t operator()(const std::pair<T1, T2>& p) const {
        auto h1 = std::hash<T1>{}(p.first);
        auto h2 = std::hash<T2>{}(p.second);
        return h1 ^ h2;
    }
};

class Mouse {
public:
    Mouse(int x, int y,
      const std::set<std::pair<std::pair<int, int>, std::pair<int, int>>>& walls,
      std::pair<int, int> goal,
      const std::vector<std::vector<int>>& distances,
      const std::vector<Path>& knownPaths,
      const std::string& mode);

    void moveForward();
    void turnLeft();
    void turnRight();
    void setGoal(const std::pair<int, int>& newGoal);
    std::vector<Path> getKnownPaths() const;

    std::vector<std::vector<int>> floodFill();
    std::pair<std::vector<std::pair<int, int>>, std::vector<std::pair<int, int>>> reversePath(
        std::vector<std::pair<int, int>> moves,
        std::vector<std::pair<int, int>> wallHits);

    void removeLoopsAndMemorize(const std::vector<std::pair<int, int>>& moves,
                                const std::vector<std::pair<int, int>>& wallHits);

    void removeLoopsAndMemorize(const std::vector<std::pair<int, int> >&, std::vector<std::pair<int, int> >&);

    void explore();
    void run();

    void navigate(
        const std::vector<std::vector<int>>& distances,
        bool reverse = false);

    std::vector<std::pair<int, int>> scanWalls();

    std::tuple<bool, bool, bool, bool> analyzeTofDistances(float front, float left, float right);

    void turnAround();

    void changeDirection(std::pair<int, int> new_direction);

    bool moveForward(double distance);

    void calibrateFront();

    std::shared_ptr<Path> getBestPath() const;

    std::pair<int, int> getLeft();
    std::pair<int, int> getRight();

    std::unordered_map<std::pair<int, int>, int, pair_hash> floodFill(
        std::pair<int, int> start,
        const std::vector<std::pair<std::pair<int, int>, std::pair<int, int>>>& walls,
        const std::set<std::pair<int, int>>& visited);

private:
    int x_, y_;
    std::pair<int, int> direction_;
    std::pair<int, int> goal_;
    std::vector<Path> knownPaths_;
    std::vector<std::pair<int, int>> knownMoves_;
    std::vector<std::pair<std::pair<int, int>, std::pair<int, int>>> wallMemory_;
    std::string mode_;
    Sim sim_;
    int moves_ = 0;
    Visualizer visualizer_;
    std::set<std::pair<std::pair<int, int>, std::pair<int, int>>> knownWalls_;
    std::vector<std::vector<int>> maze_;
};

#endif // MOUSE_HPP