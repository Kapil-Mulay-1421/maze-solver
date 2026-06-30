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
// Motor Pin Definitions
#define LEFT_PWM_PIN     7
#define RIGHT_PWM_PIN    8
#define LEFT_DIR_PIN1    3
#define LEFT_DIR_PIN2    2
#define RIGHT_DIR_PIN1   5
#define RIGHT_DIR_PIN2   6
#define STDBY 4
#define BASE_PWM         100  // Base speed for forward motion

///////////////////////////////////////////////////////////
// Encoder Configuration
#define RIGHT_ENC_DIR 20
#define RIGHT_ENC_INT 21
#define LEFT_ENC_DIR 23
#define LEFT_ENC_INT 22

// Encoder constants
const float COUNTS_PER_REV = 366.375;
const float WHEEL_DIAMETER_CM = 4.52;
const float DIST_PER_COUNT = (PI * WHEEL_DIAMETER_CM) / COUNTS_PER_REV;

// Encoder counters
volatile long leftCount = 0;
volatile long rightCount = 0;

///////////////////////////////////////////////////////////
// Button (IMU reset)
#define BUTTON_PIN 11
#define DEBOUNCE_MS 50

int lastButtonReading = HIGH;
int buttonState = HIGH;
unsigned long lastDebounceTime = 0;

///////////////////////////////////////////////////////////
// Encoder Interrupt Service Routines
void rightEncoderISR() {
    if (digitalRead(RIGHT_ENC_DIR) == HIGH) {
        rightCount++;
    } else {
        rightCount--;
    }
}

void leftEncoderISR() {
    if (digitalRead(LEFT_ENC_DIR) == HIGH) {
        leftCount++;
    } else {
        leftCount--;
    }
}

///////////////////////////////////////////////////////////
// Get distances in cm
float getLeftDistance() {
    return leftCount * DIST_PER_COUNT;
}

float getRightDistance() {
    return rightCount * DIST_PER_COUNT;
}

float getAverageDistance() {
    return (getLeftDistance() + getRightDistance()) / 2.0;
}

// Reset encoder counts
void resetEncoders() {
    noInterrupts();
    leftCount = 0;
    rightCount = 0;
    interrupts();
}

///////////////////////////////////////////////////////////
void resetIMU() {
    Serial.println("Resetting IMU...");
    Wire1.end();
    delay(20);
    Wire1.begin();
    delay(10);

    bool ok = imuSensor.begin();
    if (ok) {
        Serial.println("IMU reinitialized successfully.");
        display.clearDisplay();
        display.setTextSize(2);
        display.setCursor(0, 20);
        display.println("IMU RESET");
        display.display();
        delay(800);
    } else {
        Serial.println("IMU reinit FAILED!");
        display.clearDisplay();
        display.setTextSize(1);
        display.setCursor(0, 20);
        display.println("IMU REINIT FAIL");
        display.display();
        delay(800);
    }
    display.clearDisplay();
}

void move_x_blocks(unsigned long x, int leftPwm, int rightPwm) {
    // Reset encoders at start of movement
    resetEncoders();
    
    delay(2000);  // Short delay to ensure motors are ready
    unsigned long startTime = millis();
    
    while(millis() - startTime <= 1180 * x){
        sensors_event_t orientation = imuSensor.getOrientation();
        float yaw = orientation.orientation.x;

        if (yaw > 180) yaw -= 360;
        else if (yaw < -180) yaw += 360;

        // Run PID
        Input = yaw;
        myPID.Compute();  // Output is updated here

        if(yaw < 0.01 && yaw > -0.01) {
            Output = 0;
        }

        // Compute motor speeds
        if(yaw < 0){
            leftPwm = BASE_PWM -20- 2 * Output;
            rightPwm = BASE_PWM + 30 * Output;
        }
        else if(yaw >= 0){
            leftPwm = BASE_PWM -20 - 2 * Output;
            rightPwm = BASE_PWM + 30 * Output;
        }
        
        leftPwm = constrain(leftPwm, 0, 255);
        rightPwm = constrain(rightPwm, 0, 255);

        analogWrite(LEFT_PWM_PIN, leftPwm);
        analogWrite(RIGHT_PWM_PIN, rightPwm);

        // Display encoder distances during movement
        display.clearDisplay();
        display.setTextSize(1);
        display.setCursor(0, 0);
        display.print("Time: ");
        display.print((millis() - startTime) / 1000.0, 1);
        display.println("s");
        
        display.setCursor(0, 12);
        display.print("Yaw: ");
        display.print(yaw, 1);
        display.println(" deg");
        
        display.setTextSize(1);
        display.setCursor(0, 24);
        display.println("Distance (cm):");
        
        display.setTextSize(2);
        display.setCursor(0, 36);
        display.print("L:");
        display.println(getLeftDistance(), 1);
        
        display.setCursor(0, 52);
        display.print("R:");
        display.println(getRightDistance(), 1);
        
        display.display();

        // Debug output
        Serial.print("Time: "); Serial.print((millis() - startTime) / 1000.0, 1);
        Serial.print("s | Yaw: "); Serial.print(yaw, 1);
        Serial.print(" | Left: "); Serial.print(getLeftDistance(), 2);
        Serial.print("cm | Right: "); Serial.print(getRightDistance(), 2);
        Serial.print("cm | Avg: "); Serial.print(getAverageDistance(), 2);
        Serial.println("cm");
    }
    
    analogWrite(LEFT_PWM_PIN, 0);
    analogWrite(RIGHT_PWM_PIN, 0);

    // Show final distances after movement
    display.clearDisplay();
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.println("Movement Complete!");
    
    display.setCursor(0, 16);
    display.println("Final Distance:");
    
    display.setTextSize(2);
    display.setCursor(0, 28);
    display.print("L:");
    display.print(getLeftDistance(), 1);
    display.println("cm");
    
    display.setCursor(0, 48);
    display.print("R:");
    display.print(getRightDistance(), 1);
    display.println("cm");
    
    display.display();
    
    Serial.println("=== MOVEMENT COMPLETE ===");
    Serial.print("Final Left Distance: "); Serial.print(getLeftDistance(), 2); Serial.println(" cm");
    Serial.print("Final Right Distance: "); Serial.print(getRightDistance(), 2); Serial.println(" cm");
    Serial.print("Final Average Distance: "); Serial.print(getAverageDistance(), 2); Serial.println(" cm");

    delay(3000); // Show final results for 3 seconds
}

///////////////////////////////////////////////////////////
void setup() {
    // Ensure STDBY is set as output before writing
    pinMode(STDBY, OUTPUT);
    digitalWrite(STDBY, 1);

    Serial.begin(115200);

    // Button pin with internal pullup
    pinMode(BUTTON_PIN, INPUT_PULLUP);

    // Encoder pin setup
    pinMode(RIGHT_ENC_DIR, INPUT);
    pinMode(RIGHT_ENC_INT, INPUT);
    pinMode(LEFT_ENC_DIR, INPUT);
    pinMode(LEFT_ENC_INT, INPUT);
    
    // Attach encoder interrupts
    attachInterrupt(digitalPinToInterrupt(RIGHT_ENC_INT), rightEncoderISR, RISING);
    attachInterrupt(digitalPinToInterrupt(LEFT_ENC_INT), leftEncoderISR, RISING);

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
    myPID.SetOutputLimits(-maxPwm, maxPwm);
    
    Serial.println("System ready with encoder monitoring!");
}

///////////////////////////////////////////////////////////
void loop() {
    int leftPwm = 0;
    int rightPwm = 0;
    
    // Button handling with debounce
    int reading = digitalRead(BUTTON_PIN);
    if (reading != lastButtonReading) {
        lastDebounceTime = millis();
    }

    if ((millis() - lastDebounceTime) > DEBOUNCE_MS) {
        if (reading != buttonState) {
            buttonState = reading;
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
    myPID.Compute();

    if(yaw < 0.01 && yaw > -0.01) {
        Output = 0;
    }

    // Compute motor speeds
    if(yaw < 0){
        leftPwm = BASE_PWM -20- 2 * Output;
        rightPwm = BASE_PWM + 20 * Output;
    }
    else if(yaw >= 0){
        leftPwm = BASE_PWM -20 - 2 * Output;
        rightPwm = BASE_PWM + 20 * Output;
    }
    
    leftPwm = constrain(leftPwm, 0, 255);
    rightPwm = constrain(rightPwm, 0, 255);

    // Move 1 block (same as original code)
    move_x_blocks(1.0, leftPwm, rightPwm);
    delay(10000);

    // Display current encoder readings while stationary
    display.clearDisplay();
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.print("Yaw: ");
    display.print(yaw, 1);
    display.println(" deg");
    
    display.setCursor(0, 12);
    display.println("Current Distance:");
    
    display.setTextSize(2);
    display.setCursor(0, 28);
    display.print("L:");
    display.print(getLeftDistance(), 1);
    display.println("cm");
    
    display.setCursor(0, 48);
    display.print("R:");
    display.print(getRightDistance(), 1);
    display.println("cm");
    
    display.display();

    delay(25);
}
