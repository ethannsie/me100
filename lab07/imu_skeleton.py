from machine import Pin, I2C, Timer
from time import sleep
from lsm6dsox import LSM6DSOX

# Initialize I2C (adjust pins if needed)
i2c = I2C(0, scl=Pin(XX), sda=Pin(XX))

# Create IMU object
imu = LSM6DSOX(i2c)

def imu_cb(timer):
    # IMU: Take measurement and report results
    ax, ay, az = imu.accel()
    gx, gy, gz = imu.gyro()
    temp = imu.temperature()

    print("Acceleration (m/s^2):  X = {:.4f}, Y = {:.4f}, Z = {:.4f}".format(ax, ay, az))
    print("Gyroscope (rad/s):   X = {:.4f}, Y = {:.4f}, Z = {:.4f}".format(gx, gy, gz))
    print("Temperature (°C):  {:.2f}".format(temp))

# Ask for a measurement every 200ms from the IMU
timer_imu_cb = Timer(3)
timer_imu_cb.init(period=200, mode=timer_imu_cb.PERIODIC, callback=imu_cb)


sleep(15)
timer_imu_cb.deinit()