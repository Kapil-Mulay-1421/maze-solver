#include <Wire.h>

void scanI2C() {
  Serial.println("Scanning I2C bus...");
  byte count = 0;
  
  for (byte i = 8; i < 120; i++) {
    Wire.beginTransmission(i);
    if (Wire.endTransmission() == 0) {
      Serial.print("Found device at 0x");
      if (i < 16) Serial.print("0");
      Serial.println(i, HEX);
      count++;
    }
  }
  
  if (count == 0) {
    Serial.println("No I2C devices found!");
  }
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  scanI2C();
}

void loop() {
  delay(1000);
}