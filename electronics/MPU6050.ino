#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

const int num_samples = 2000;
float accelX_offset = 0, accelY_offset = 0, accelZ_offset = 0;
float gyroX_offset = 0, gyroY_offset = 0, gyroZ_offset = 0;

float ax = 0, ay = 0, az = 0;
float gx = 0, gy = 0, gz = 0;

void setup(){
  Serial.begin(115200);
  while (!Serial){
    delay(10);
  }
  Serial.println("MPU6050 Callibration begin.");

  if(!mpu.begin()){
    Serial.println("Failed to find MPU6050 Chip");
    while(1){
      delay(10);
    }
  }
  Serial.println("MPU6050 test started");

  mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  Serial.println("");
  delay(100);
  Serial.println("Callibration Started.");
  callibrateSensor();

  Serial.print("accelX_offset: ");
  Serial.print(accelX_offset);
  Serial.print(", ");
  Serial.print("accelY_offset: ");
  Serial.print(accelY_offset);
  Serial.print(", ");
  Serial.print("accelZ_offset: ");
  Serial.println(accelZ_offset);
  
  Serial.print("gyroX_offset: ");
  Serial.print(gyroX_offset);
  Serial.print(", ");
  Serial.print("gyroY_offset: ");
  Serial.print(gyroY_offset);
  Serial.print(", ");
  Serial.print("gyroZ_offset: ");
  Serial.print(gyroZ_offset);
  Serial.print(", ");
}

void loop(){
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  ax = a.acceleration.x - accelX_offset;
  ay = a.acceleration.y - accelY_offset;
  az = a.acceleration.z - accelZ_offset;
  gx= g.gyro.x - gyroX_offset;
  gy = g.gyro.y - gyroY_offset;
  gz = g.gyro.z - gyroZ_offset;

  Serial.print("AccelerationX: ");
  Serial.print(ax);
  Serial.print(", ");
  Serial.print("AccelerationY: ");
  Serial.print(ay);
  Serial.print(", ");
  Serial.print("AccelerationZ: ");
  Serial.println(az);

  Serial.print("RotationX: ");
  Serial.print(gx);
  Serial.print(", ");
  Serial.print("RotationY: ");
  Serial.print(gy);
  Serial.print(", ");
  Serial.print("RotationZ: ");
  Serial.println(gz);

  delay(100);
}

void callibrateSensor(){
float ax_sum = 0, ay_sum = 0, az_sum = 0;
float gx_sum = 0, gy_sum = 0, gz_sum = 0;

  for (int i=0; i<num_samples; i++){
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    
    ax_sum += a.acceleration.x;
    ay_sum += a.acceleration.y;
    az_sum += a.acceleration.z;
    gx_sum += g.gyro.x;
    gy_sum += g.gyro.y;
    gz_sum += g.gyro.z;

    if (i%100 == 0){
      Serial.println(".");
      delay(10);
    }
  }

  accelX_offset = ax_sum / num_samples;
  accelY_offset = ay_sum / num_samples;
  accelZ_offset = az_sum / num_samples;
  gyroX_offset = gx_sum / num_samples;
  gyroY_offset = gy_sum / num_samples;
  gyroZ_offset = gz_sum / num_samples;

  accelX_offset -= 9.8;
}