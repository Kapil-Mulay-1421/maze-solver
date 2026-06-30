#ifndef REGRESSION_HPP
#define REGRESSION_HPP

#include <vector>
#include <tuple>

// Replace this with real experimental data
extern const std::vector<std::pair<std::pair<double, double>, double>> data;

// Performs regression on the `data` vector
std::tuple<double, double, double> regress();

#endif // REGRESSION_HPP
