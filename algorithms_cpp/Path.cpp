#include <vector>
#include <utility>
#include <cmath>
#include <limits>
#include <tuple>
#include <iostream>
#include "Regression.hpp"  // regress() -> std::tuple<double,double,double>

class Path {
public:
    std::vector<std::pair<int, int>> positions;   // optional, not required for metrics
    std::vector<std::pair<int, int>> moves;       // unit steps like (1,0),(0,1),(-1,0),(0,-1)

    int turns = 0;                // total 45° turn units
    double length = 0.0;          // raw path length (grid units)
    double optimizedLength = 0.0; // length after diagonal smoothing
    int optimizedTurns = 0;       // turns after smoothing (45° units)
    double feasibilityScore = 0;

    Path() = default;

    Path(const std::vector<std::pair<int, int>>& positions_,
         const std::vector<std::pair<int, int>>& moves_)
        : positions(positions_), moves(moves_) {

        // Raw metrics
        length = static_cast<double>(moves.size());
        turns  = calculateTurns(moves);

        // Optimized metrics (diagonal smoothing over zig-zag runs)
        std::tie(optimizedLength, optimizedTurns) = optimizeLengthAndTurns(moves, length, turns);

        // Feasibility (higher is better)
        feasibilityScore = calculateFeasibilityScore(optimizedLength, optimizedTurns);
    }

private:
    static bool isOpposite(const std::pair<int,int>& a, const std::pair<int,int>& b) {
        return a.first == -b.first && a.second == -b.second;
    }

    static int calculateTurns(const std::vector<std::pair<int,int>>& m) {
        int t = 0;
        for (size_t i = 0; i + 1 < m.size(); ++i) {
            if (m[i] == m[i+1]) {
                // straight
            } else if (isOpposite(m[i], m[i+1])) {
                t += 4; // 180° = 4 * 45°
            } else {
                t += 2; // 90° = 2 * 45°
            }
        }
        return t;
    }

    // Collapse maximal alternating runs (A,B,A,B,...) greedily into diagonals
    static std::pair<double,int> optimizeLengthAndTurns(const std::vector<std::pair<int,int>>& m,
                                                        double rawLen,
                                                        int rawTurns) {
        const double diag = std::sqrt(2.0);
        double optLen = 0.0;
        int optTurns = rawTurns;

        size_t i = 0;
        while (i < m.size()) {
            if (i + 1 < m.size() && m[i] != m[i+1]) {
                // Start a zig-zag run alternating between two orthogonal directions
                auto A = m[i];
                auto B = m[i+1];
                size_t start = i;
                size_t s = 2; // run length in steps
                i += 2;
                // extend while perfectly alternating A,B,A,B,...
                while (i < m.size() && m[i] == m[i-2]) {
                    ++s;
                    ++i;
                }

                // Length: floor(s/2) diagonals + (s % 2) straight
                optLen += (static_cast<int>(s/2)) * diag + (s % 2) * 1.0;

                // Turn reduction: in run there are (s-1) corners (90° = 2 units each).
                // After smoothing a run (s >= 2) needs only 2 units to enter/exit the diagonal envelope.
                int cornersInRun = static_cast<int>(s) - 1;
                int reduction = std::max(0, 2 * cornersInRun - 2);
                optTurns -= reduction;
            } else {
                // Single straight step (or end of a non-alternating segment)
                optLen += 1.0;
                ++i;
            }
        }

        // Sanity clamp
        if (optLen <= 0.0) optLen = rawLen;
        if (optTurns < 0)  optTurns = 0;

        return {optLen, optTurns};
    }

    static double calculateFeasibilityScore(double optLen, int optTurns) {
        auto wLen = 0.06056929;
        auto wTurns = 0.03632959;
        auto intercept = 0.001;
        double time = wLen * optLen + wTurns * static_cast<double>(optTurns) + intercept;

        // Guard against non-positive/NaN times
        if (!(time > 0.0)) {
            return 0.0; // worst feasible
        }
        return 1.0 / time;
    }
};
