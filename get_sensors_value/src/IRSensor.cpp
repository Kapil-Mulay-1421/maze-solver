#include "IRSensor.h"

IRSensor::IRSensor(int pin, const String& position) {
  this->pin = pin;
  this->position = position;
}

void IRSensor::begin() {
  pinMode(pin, INPUT);
}

bool IRSensor::isObstacleDetected() {
  return digitalRead(pin) == LOW;  // LOW means obstacle detected
}

String IRSensor::getPosition() {
  return position;
}
