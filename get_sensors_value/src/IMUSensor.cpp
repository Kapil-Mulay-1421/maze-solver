#include "IMUSensor.h"
#include <Arduino.h>
IMUSensor::IMUSensor() : bno(55) {}  // ID 55 is default for Adafruit_BNO055

bool IMUSensor::begin() {
    if (!bno.begin()) {
        Serial.println("Failed to initialize BNO055!");
        return false;
    }

    delay(1000);
    bno.setExtCrystalUse(true);
    return true;
}

sensors_event_t IMUSensor::getOrientation() {
    sensors_event_t orientation;
    bno.getEvent(&orientation, Adafruit_BNO055::VECTOR_EULER);
    return orientation;
}

sensors_event_t IMUSensor::getAccel() {
    sensors_event_t accel;
    bno.getEvent(&accel, Adafruit_BNO055::VECTOR_ACCELEROMETER);
    return accel;
}

sensors_event_t IMUSensor::getGyro() {
    sensors_event_t gyro;
    bno.getEvent(&gyro, Adafruit_BNO055::VECTOR_GYROSCOPE);
    return gyro;
}

sensors_event_t IMUSensor::getMag() {
    sensors_event_t mag;
    bno.getEvent(&mag, Adafruit_BNO055::VECTOR_MAGNETOMETER);
    return mag;
}

void IMUSensor::printAllData() {
    sensors_event_t orientation = getOrientation();
    sensors_event_t accel = getAccel();
    sensors_event_t gyro = getGyro();
    sensors_event_t mag = getMag();

    Serial.print("Orientation (Euler): ");
    Serial.print("Heading: ");
    Serial.print(orientation.orientation.x);
    Serial.print("°, Pitch: ");
    Serial.print(orientation.orientation.y);
    Serial.print("°, Roll: ");
    Serial.println(orientation.orientation.z);

    Serial.print("Acceleration (m/s^2): X=");
    Serial.print(accel.acceleration.x);
    Serial.print(" Y=");
    Serial.print(accel.acceleration.y);
    Serial.print(" Z=");
    Serial.println(accel.acceleration.z);

    Serial.print("Gyroscope (rad/s): X=");
    Serial.print(gyro.gyro.x);
    Serial.print(" Y=");
    Serial.print(gyro.gyro.y);
    Serial.print(" Z=");
    Serial.println(gyro.gyro.z);

    Serial.print("Magnetometer (uT): X=");
    Serial.print(mag.magnetic.x);
    Serial.print(" Y=");
    Serial.print(mag.magnetic.y);
    Serial.print(" Z=");
    Serial.println(mag.magnetic.z);

    Serial.println();
}
