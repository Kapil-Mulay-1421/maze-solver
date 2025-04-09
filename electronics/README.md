# maze-solver - Electronics
Team aims to build a robust electrical system to act as a solid bridge between software and hardware.

## MPU6050 Callibration and Data Logging
This project uses MPU6050 accelerometer and gyroscope over the standard odometry data from motor encoders for precise control and localisation of the bot. **Adafruit MPU6050** library, which an I2C hardware driver specially for MPU6050, for getting accelerometer and gyroscope data.

### 📦 Depends
Make sure to install the following libraries via the Arduino Library Manager or manually from GitHub:

- [Adafruit MPU6050](https://github.com/adafruit/Adafruit_MPU6050)
- [Adafruit Sensor](https://github.com/adafruit/Adafruit_Sensor)
- [Wire (built-in)](https://www.arduino.cc/en/reference/wire)


To install these:
1. Open Arduino IDE
2. Go to **Tools>Manage Libraries**
3. Search for the libraries and install the latest version.
`
### 🔧 Hardware Needed for Callibration
1. Breadboard (Optional)
2. Any Arduino Compatible Board (say, Arduino UNO, Arduino Nano, Teensy, ESP32 etc.)
3. MPU6050 
4. Jumper Wires
5. USB Cable for Serial Communication

### 🔌Pin Diagram
1. Connect VCC (MPU6050) to 5V pin (Arduino UNO).
2. Make sure sensor and microcontroller have a common GND.
3. Connect SDA (MPU6050) to A4.
4. Connect SCL  (MPU6050) to A5.

| Board         | SDA Pin       | SCL Pin       | Notes                                |
|---------------|---------------|---------------|--------------------------------------|
| Arduino Uno   | A4            | A5            | Default I2C pins                     |
| Arduino Nano  | A4            | A5            | Same as Uno                          |
| Arduino Mega  | 20            | 21            | Dedicated I2C pins                   |
| Teensy 4.1    | Pin 18 (SDA1) | Pin 19 (SCL1) | I2C1 is default; multiple I2C buses available |
| ESP32         | GPIO 21       | GPIO 22       | Default I2C pins (can be reconfigured) |

📝 **Note**: On boards like ESP32 and Teensy, you can use other pins for I2C with `Wire.begin(SDA, SCL);` in your code.


<img width="517" alt="MPU6050-Circuit Diagram" src="https://github.com/user-attachments/assets/1ae46421-b835-48a0-9577-b38b4384f71c" />

### Getting Started
1. Clone Repository
2. Make the desired connections
3. Copy the code (MPU6050.ino) in Arduino IDE.
4. Select the desired Port and Board.
5. Upload the code.

**Note:** Make sure the Sensor is kept on flat surface with Z-Axis of the sensor pointing downwards.

### Algorithm Used for Callibration
A global variable **num_samples** is defined which sets the number of data samples MPU6050 takes for the accelorometer and gyroscope in all the three directions. These valued are then sumed over for num_samples iterations in their respective variables. The **offset variables** for acceleration and rotation in all 6 directions are then set by taking an average of the data collected in num_samples iterations. In the main loop, these offset values are subtracted from the real time readings recorded by the sensor. 
