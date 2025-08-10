#include <vector>
#include <utility>
#include <cmath>
#include <limits>
#include "Regression.hpp"  // Assumed to return weights as a tuple or struct
#include <iostream>

class Path {
public:
    std::vector<std::pair<int, int>> positions;
    std::vector<std::pair<int, int>> moves;
    int turns;
    double length;
    double optimizedLength;
    int optimizedTurns;
    double feasibilityScore;

    Path() {}

    Path(const std::vector<std::pair<int, int>>& positions_, const std::vector<std::pair<int, int>>& moves_)
        : positions(positions_), moves(moves_) {
        std::cout << "Creating Path object" << std::endl;
        std::cout << "Positions: ";
        for (const auto& pos : positions) {
            std::cout << "(" << pos.first << ", " << pos.second << ") ";
        }
        std::cout << std::endl;
        std::cout << "Moves: ";
        for (const auto& move : moves) {
            std::cout << "(" << move.first << ", " << move.second << ") ";
        }
        std::cout << std::endl;
        turns = calculateTurns(moves);
        std::cout << "Turns: " << turns << std::endl;
        length = moves.size();
        std::cout << "Length: " << length << std::endl;
        std::tie(optimizedLength, optimizedTurns) = optimizeLengthAndTurns();
        std::cout << "Optimized Length: " << optimizedLength << std::endl;
        std::cout << "Optimized Turns: " << optimizedTurns << std::endl;
        feasibilityScore = calculateFeasibilityScore();
    }

private:
    int calculateTurns(const std::vector<std::pair<int, int>>& moves) {
        int turns = 0;
        for (size_t i = 0; i + 1 < moves.size(); ++i) {
            if (moves[i] != moves[i + 1]) {
                turns += 2; // Each change in direction counts as two 45 degree turns
            }
        }
        return turns;
    }

    std::pair<double, int> optimizeLengthAndTurns() {
        double optLength = length;
        int optTurns = turns;
        int streak = 0;
        size_t i = 0;

        while (i + 2 < moves.size()) {
            if (moves[i] != moves[i + 1] && moves[i] == moves[i + 2]) {
                ++streak;
                i += 2;
            } else {
                optLength = optLength - 2 * streak + streak * std::sqrt(2);
                if (streak > 0) {
                    optTurns = optTurns - 4 * streak + 2;
                }
                streak = 0;
                ++i;
            }
        }

        return {optLength, optTurns};
    }

    double calculateFeasibilityScore() {
        auto [weightLength, weightTurns, intercept] = regress(); // Assumes regress() returns std::tuple<double, double, double>
        double time = weightLength * optimizedLength + weightTurns * optimizedTurns + intercept;
        if (time == 0) return std::numeric_limits<double>::infinity();
        return 1.0 / time;
    }
};
