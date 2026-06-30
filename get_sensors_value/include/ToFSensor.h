#ifndef TOF_SENSOR_H
#define TOF_SENSOR_H

#include <Arduino.h>
#include <Adafruit_VL53L0X.h>

class ToFSensor {
public:
    // Constructor
    ToFSensor(uint8_t shutdownPin, uint8_t i2cAddress, String name);

    // Initializes the sensor
    bool begin();

    // Returns whether the sensor was successfully initialized
    bool isInitialized();

    // Reads the distance measurement; returns true if valid
    bool read();

    // Returns the measured distance in millimeters
    uint16_t getDistance();

    // Checks if the reading is out of range
    bool isOutOfRange();

    // Returns the name/identifier of the sensor
    String getName();

private:
    uint8_t shutdownPin;
    uint8_t i2cAddress;
    String name;
    bool initialized = false;

    Adafruit_VL53L0X lox;
    VL53L0X_RangingMeasurementData_t measurement;
};

#endif // TOF_SENSOR_H
