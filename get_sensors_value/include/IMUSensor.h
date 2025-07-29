#ifndef IMU_SENSOR_H
#define IMU_SENSOR_H

#include <Arduino.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

class IMUSensor {
private:
    Adafruit_BNO055 bno;

public:
    IMUSensor();
    bool begin();
    void printAllData();
    sensors_event_t getOrientation();
    sensors_event_t getAccel();
    sensors_event_t getGyro();
    sensors_event_t getMag();
};

#endif
