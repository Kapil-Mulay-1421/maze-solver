#include <PID_v1.h>
#include <Arduino.h>
#include "IMUSensor.hpp"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

///////////////////////////////////////////////////////////
// PID Configuration
#define setPoint 0.0
#define offSet 1.0
#define Kp 0.75
#define Ki 0.01
#define Kd 0.01
#define maxPwm 125

double Setpoint, Input, Output;
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);

///////////////////////////////////////////////////////////
// IMU on Wire1 (SCL1/SDA1)
IMUSensor imuSensor(Wire1);

// OLED on Wire2 (SCL2/SDA2)
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire2, -1);  // -1 = no reset pin

///////////////////////////////////////////////////////////
// Motor Pin Definitions (Update as per your wiring)
#define LEFT_PWM_PIN     7
#define RIGHT_PWM_PIN    8

#define LEFT_DIR_PIN1    3
#define LEFT_DIR_PIN2    2
#define RIGHT_DIR_PIN1   5
#define RIGHT_DIR_PIN2   6

#define STDBY 4

#define BASE_PWM         100  // Base speed for forward motion

///////////////////////////////////////////////////////////
// Button (IMU reset)
#define BUTTON_PIN 11          // button connected to pin 11 and to GND when pressed
#define DEBOUNCE_MS 50

int lastButtonReading = HIGH;  // last raw reading from the pin
int buttonState = HIGH;        // debounced stable state
unsigned long lastDebounceTime = 0;

///////////////////////////////////////////////////////////
void resetIMU() {
    Serial.println("Resetting IMU...");
    // Try a clean re-init: stop and restart Wire1 then call begin()
    Wire1.end();
    delay(20);
    Wire1.begin();
    delay(10);

    bool ok = imuSensor.begin(); // reinitialize sensor; assumes begin() works as reinit
    if (ok) {
        Serial.println("IMU reinitialized successfully.");
        // optional: show on OLED
        display.clearDisplay();
        display.setTextSize(2);
        display.setCursor(0, 20);
        display.println("IMU RESET");
        display.display();
        delay(800); // display message briefly
    } else {
        Serial.println("IMU reinit FAILED!");
        display.clearDisplay();
        display.setTextSize(1);
        display.setCursor(0, 20);
        display.println("IMU REINIT FAIL");
        display.display();
        delay(800);
    }
    // Restore normal display (small delay to let loop draw normal info)
    display.clearDisplay();
}

///////////////////////////////////////////////////////////
void setup() {
    // Ensure STDBY is set as output before writing
    pinMode(STDBY, OUTPUT);
    digitalWrite(STDBY, 1);

    Serial.begin(115200);

    // Button pin with internal pullup (pressed = LOW)
    pinMode(BUTTON_PIN, INPUT_PULLUP);

    // IMU Setup
    Wire1.begin();
    if (!imuSensor.begin()) {
        Serial.println("IMU initialization failed. Check wiring or address.");
        while (1);
    }
    Serial.println("IMU initialized successfully.");

    // OLED Setup
    Wire2.begin();
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
        Serial.println("OLED initialization failed!");
        while (1);
    }

    display.clearDisplay();
    display.setTextSize(2);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.println("Init OK");
    display.display();
    delay(1000);

    // Motor Pin Setup
    pinMode(LEFT_PWM_PIN, OUTPUT);
    pinMode(RIGHT_PWM_PIN, OUTPUT);
    pinMode(LEFT_DIR_PIN1, OUTPUT);
    pinMode(LEFT_DIR_PIN2, OUTPUT);
    pinMode(RIGHT_DIR_PIN1, OUTPUT);
    pinMode(RIGHT_DIR_PIN2, OUTPUT);

    // Set initial direction to forward
    digitalWrite(LEFT_DIR_PIN1, HIGH);
    digitalWrite(LEFT_DIR_PIN2, LOW);
    digitalWrite(RIGHT_DIR_PIN1, LOW);
    digitalWrite(RIGHT_DIR_PIN2, HIGH);

    // PID Setup
    Setpoint = setPoint;
    myPID.SetMode(AUTOMATIC);
    myPID.SetOutputLimits(-maxPwm, maxPwm);  // Output used as correction offset
    
}


///////////////////////////////////////////////////////////
void loop() {
    int leftPwm = 0;
    int rightPwm = 0;
    // --- Button handling with debounce ---
    int reading = digitalRead(BUTTON_PIN); // HIGH normally, LOW when pressed
    if (reading != lastButtonReading) {
        // reset debounce timer
        lastDebounceTime = millis();
    }

    if ((millis() - lastDebounceTime) > DEBOUNCE_MS) {
        // if the reading has been stable for the debounce time
        if (reading != buttonState) {
            buttonState = reading;
            // Only act on the transition to PRESSED (LOW)
            if (buttonState == LOW) {
                resetIMU();
            }
        }
    }
    lastButtonReading = reading;

    // Get Yaw from IMU
    sensors_event_t orientation = imuSensor.getOrientation();
    float yaw = orientation.orientation.x;

    // Normalize yaw to [-180, 180]
    if (yaw > 180) yaw -= 360;
    else if (yaw < -180) yaw += 360;

    // Run PID
    Input = yaw;
    myPID.Compute();  // Output is updated here

    if(yaw < 0.01 && yaw > -0.01) {
        Output = 0;
    }

    // Deadzone to avoid jitter

    // Compute motor speeds


    if(yaw < 0){
      leftPwm = BASE_PWM -20- 2 * Output;
      rightPwm = BASE_PWM + 20 * Output;

    }

    else if(yaw > 0){
      leftPwm = BASE_PWM -20 - 2 * Output;
      rightPwm = BASE_PWM + 20 * Output;
    }
    
    leftPwm = constrain(leftPwm, 0, 255);
    rightPwm = constrain(rightPwm, 0, 255);

    // Apply PWM
    analogWrite(LEFT_PWM_PIN, leftPwm);
    analogWrite(RIGHT_PWM_PIN, rightPwm);

    // Debug Info
    Serial.print("Yaw: "); Serial.print(yaw, 1);
    Serial.print(" | PID Output: "); Serial.print(Output, 1);
    Serial.print(" | L_PWM: "); Serial.print(leftPwm);
    Serial.print(" | R_PWM: "); Serial.println(rightPwm);

    // OLED Display
    display.clearDisplay();
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.print("Yaw (deg):");

    display.setTextSize(2);
    display.setCursor(0, 20);
    display.print(yaw, 1);
    display.display();

    delay(25);
}
