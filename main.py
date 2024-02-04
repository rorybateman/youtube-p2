import mpu6050
import time

# Create a new Mpu6050 object
mpu6050 = mpu6050.mpu6050(0x68)

# Define a function to read the sensor data
def read_sensor_data():
    # Read the accelerometer values
    accelerometer_data = mpu6050.get_accel_data()

    # Read the gyroscope values
    gyroscope_data = mpu6050.get_gyro_data()

    return accelerometer_data, gyroscope_data

# Start a while loop to continuously read the sensor data
t0 = time.time()
# Wait for MPU to Settle
settling_time = 4
print('Settling MPU for %d seconds' % settling_time)
time.sleep(4)
print('MPU is Done Settling')


def get_gyro():
    gyroscope_data = mpu6050.get_gyro_data()
    gx= gyroscope_data.get('x')
    gy= gyroscope_data.get('y')
    gz= gyroscope_data.get('z')
    return gx, gy, gz

while true:
  print(get_gyro())
  time.sleep(0.5)
#test
