#ifndef IRSENSOR_H
#define IRSENSOR_H

#include <Arduino.h>

class IRSensor {
  private:
    int pin;
    String position;

  public:
    IRSensor(int pin, const String& position);
    void begin();
    bool isObstacleDetected();
    String getPosition();
};

#endif
