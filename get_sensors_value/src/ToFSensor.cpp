#include "ToFSensor.h"

ToFSensor::ToFSensor(uint8_t shutdownPin, uint8_t i2cAddress, String name) {
    this->shutdownPin = shutdownPin;
    this->i2cAddress = i2cAddress;
    this->name = name;
}

bool ToFSensor::begin() {
    pinMode(shutdownPin, OUTPUT);
    digitalWrite(shutdownPin, LOW);  // Reset sensor
    delay(10);
    digitalWrite(shutdownPin, HIGH); // Power on sensor
    delay(10);

    initialized = lox.begin(i2cAddress);
    if (!initialized) {
        Serial.print(F("Failed to start VL53L0X sensor: "));
        Serial.println(name);
    }
    return initialized;
}

bool ToFSensor::isInitialized() {
    return initialized;
}

bool ToFSensor::read() {
    if (!initialized) return false;

    lox.rangingTest(&measurement, false);
    return measurement.RangeStatus != 4; // True if valid
}

uint16_t ToFSensor::getDistance() {
    return measurement.RangeMilliMeter;
}

bool ToFSensor::isOutOfRange() {
    return measurement.RangeStatus == 4;
}

String ToFSensor::getName() {
    return name;
}
