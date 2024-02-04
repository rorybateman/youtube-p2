import mpu6050
import time

# Create a new Mpu6050 object
mpu6050 = mpu6050.mpu6050(0x68)

t0 = time.time()
# Wait for MPU to Settle
settling_time = 4
print('Settling MPU for %d seconds' % settling_time)
time.sleep(4)
print('MPU is Done Settling')



def get_linear_acceleration():
    accelerometer_data = mpu6050.get_accel_data()
    ax= accelerometer_data.get('x')
    ay= accelerometer_data.get('y')
    az= accelerometer_data.get('z')
    return ax, ay, az

def linear_calibration(calibration_time=5, axis=0):
    
    """
        Description: This is a function to get the offset values
            for linear acceleration calibration for mpu6050. In this function
            essentially what were doing is calculating a line of best fit in
            which the x-axis is the acceleration and the y axis is the offset.
            The line is assumed to be a linear fit and we are using least squares
            method to find the slope and the y-intercept. For more details on the math
            please see https://www.youtube.com/watch?v=P8hT5nDai6A
            
        Parameters:
        calibration_time[int]: Time in seconds you want to calibrate
            mpu6050. The longer the time the more accurate the
            calibration
        axis[int]: type in what axis you will be calibrating. You should do all 3
            ideally but this code you can only do one at a time.
            Three choices ax -> 0, ay -> 1, az -> 2

        Outputs: Outputs an an m and b value for the equation:
            y = (m * x) + b! You can plug in x (aka measured acceleration)
            to get the offset y in your application of the sensor! 
    """
    # This is for the math to approximate slope and y-intercept. See video in description :)
    num_of_points = 0
    x_sum = 0
    y_sum = 0
    x_squared_sum = 0
    x_times_y_sum = 0
    print('-' * 50)
    print('Orient the axis upwards against gravity - Click Enter When Ready' )
    # Gravity should be 1g in this scenerio
    x = input()
    end_loop_time = time.time() + calibration_time
    print('Beginning to Calibrate Part 1 (Acceleration = 1g) for %d seconds' % calibration_time)
    # We end the loop once the calibration time has passed
    
    while end_loop_time > time.time():
        
        num_of_points += 1
        offset = get_linear_acceleration()[axis] - 1
        
        x_sum += 1
        y_sum += offset
        x_squared_sum += 1
        x_times_y_sum += 1 * offset

        if num_of_points % 100 == 0:
            print('Still Calibrating Gyro... %d points so far' % num_of_points)
            
    print('-' * 50)
    print('Orient the axis downwards against gravity - Click Enter When Ready' )
    # Gravity should be 1g in this scenerio
    x = input()
    end_loop_time = time.time() + calibration_time
    print('Beginning to Calibrate Part 2 (Acceleration = -1g) for %d seconds' % calibration_time)
    # We end the loop once the calibration time has passed

    while end_loop_time > time.time():
        
        num_of_points += 1
        offset = get_linear_acceleration()[axis] + 1
        # Because acceleration should be -1g
        x_sum += (-1 * 1)
        y_sum += offset
        x_squared_sum += (-1 * 1) * (-1 * 1)
        x_times_y_sum += (-1 * 1) * offset

        if num_of_points % 100 == 0:
            print('Still Calibrating Gyro... %d points so far' % num_of_points)
    
    print('-' * 50)
    print('Orient the axis perpendicular against gravity - Click Enter When Ready' )
    # Gravity should be 1g in this scenerio
    x = input()
    end_loop_time = time.time() + calibration_time
    print('Beginning to Calibrate Part 3 (Acceleration = 0g) for %d seconds' % calibration_time)
    # We end the loop once the calibration time has passed

    while end_loop_time > time.time():
        
        num_of_points += 1
        # Just showing the zero for consistency purposes
        offset = get_linear_acceleration()[axis] + 0
        # Because acceleration should be -1g
        x_sum += 0
        y_sum += offset
        x_squared_sum += (0) * (0)
        x_times_y_sum += (0) * offset

        if num_of_points % 100 == 0:
            print('Still Calibrating Gyro... %d points so far' % num_of_points)
            
    # now I just utilize the equation for m and b in least sqaures theory
    m = (num_of_points * x_times_y_sum - (x_sum * y_sum)) / ((num_of_points * x_squared_sum) - (x_sum)**2)
    b = (y_sum - (m * x_sum)) / num_of_points
    
    return m, b



def get_linear_accelerationrun():
    accelerometer_data = mpu6050.get_accel_data()
    ax= accelerometer_data.get('x')*8.8 -1.1
    ay= accelerometer_data.get('y')
    az= accelerometer_data.get('z')
    return ax, ay, az

while True:
    print(get_linear_accelerationrun())
    time.sleep(0.5)
print(linear_calibration())
