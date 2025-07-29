#ifndef REGRESSION_H
#define REGRESSION_H

#include <vector>
#include <tuple>
#include <numeric>
#include <cmath>

// Replace this with real experimental data
static const std::vector<std::pair<std::pair<double, double>, double>> data = {
    {{60, 20}, 4.0},
    {{65, 25}, 4.5},
    {{70, 22}, 4.7},
    {{75, 30}, 5.2},
    {{80, 35}, 5.8}
};

inline std::tuple<double, double, double> regress() {
    size_t n = data.size();
    double sum_x1 = 0, sum_x2 = 0, sum_y = 0;
    double sum_x1x1 = 0, sum_x2x2 = 0, sum_x1x2 = 0;
    double sum_x1y = 0, sum_x2y = 0;

    for (const auto& entry : data) {
        double x1 = entry.first.first;
        double x2 = entry.first.second;
        double y = entry.second;

        sum_x1 += x1;
        sum_x2 += x2;
        sum_y += y;

        sum_x1x1 += x1 * x1;
        sum_x2x2 += x2 * x2;
        sum_x1x2 += x1 * x2;

        sum_x1y += x1 * y;
        sum_x2y += x2 * y;
    }

    // Solve normal equations using Cramer's Rule for 2 variables + intercept
    double denom = n * sum_x1x1 * sum_x2x2 + 2 * sum_x1 * sum_x2 * sum_x1x2
                - sum_x1x1 * sum_x2 * sum_x2 - sum_x2x2 * sum_x1 * sum_x1 - n * sum_x1x2 * sum_x1x2;

    if (denom == 0) return {0.0, 0.0, 0.0};

    double w_length = (sum_y * sum_x1x1 * sum_x2x2 + sum_x1 * sum_x2 * sum_x1y * 2 + n * sum_x1y * sum_x2x2 -
                      sum_x1x1 * sum_x2 * sum_x2y - sum_x2x2 * sum_x1 * sum_x1y - sum_y * sum_x1x2 * sum_x1x2) / denom;

    double w_turns = (n * sum_x1x1 * sum_x2y + sum_x1 * sum_x1y * sum_x2 + sum_y * sum_x1 * sum_x1x2 -
                      sum_x1x1 * sum_y * sum_x2 - sum_x2 * sum_x2y * sum_x1 - n * sum_x1x2 * sum_x1y) / denom;

    double intercept = (sum_y * sum_x1x1 * sum_x2x2 + sum_x1 * sum_x2 * sum_x1y * 2 + sum_x1y * sum_x2 * sum_x2 -
                       sum_x1x1 * sum_x2 * sum_x2y - sum_x2x2 * sum_x1 * sum_x1y - sum_x1x2 * sum_x1y * n) / denom;

    return {w_length, w_turns, intercept};
}

#endif // REGRESSION_H
