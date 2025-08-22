#include "Sim.hpp"
#include <iostream>


bool Sim::moveForward(double distance) {
    // Stubbed simulation: always return success
    std::cout << "Simulated move forward by " << distance << " units." << std::endl;
    return true;
}

bool Sim::turnLeft() {
    // Stubbed simulation: always return success
    std::cout << "Simulated turn left." << std::endl;
    return true;
}

bool Sim::turnRight() {
    // Stubbed simulation: always return success
    std::cout << "Simulated turn right. " << std::endl;
    return true;
}
