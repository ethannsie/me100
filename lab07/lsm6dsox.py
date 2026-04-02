from machine import I2C, Pin
import time
import math

# LSM6DSOX Registers
LSM6DSOX_ADDR = 0x6A  # sometimes 0x6B

WHO_AM_I = 0x0F
CTRL1_XL = 0x10
CTRL2_G  = 0x11
CTRL3_C  = 0x12

OUT_TEMP_L = 0x20
OUTX_L_G = 0x22
OUTX_L_A = 0x28


class LSM6DSOX:
    def __init__(self, i2c, addr=LSM6DSOX_ADDR):
        self.i2c = i2c
        self.addr = addr

        who = self._read_reg(WHO_AM_I)[0]

        self._init_sensor()

        # Gyro bias (deg/s)
        self.gyro_bias = (0.0, 0.0, 0.0)

        # Calibrate at startup (sensor must be still)
        self.calibrate_gyro()

    def _write_reg(self, reg, val):
        self.i2c.writeto_mem(self.addr, reg, bytes([val]))

    def _read_reg(self, reg, n=1):
        return self.i2c.readfrom_mem(self.addr, reg, n)

    def _init_sensor(self):
        # Accelerometer: 104 Hz, ±2g
        self._write_reg(CTRL1_XL, 0x40)

        # Gyroscope: 104 Hz, 250 dps
        self._write_reg(CTRL2_G, 0x40)

        # Enable auto increment
        self._write_reg(CTRL3_C, 0x04)

    def _read_vector(self, reg):
        data = self._read_reg(reg, 6)
        x = self._twos_comp(data[0] | (data[1] << 8))
        y = self._twos_comp(data[2] | (data[3] << 8))
        z = self._twos_comp(data[4] | (data[5] << 8))
        return (x, y, z)

    def _twos_comp(self, val):
        if val & 0x8000:
            val -= 65536
        return val

    # -------- Calibration --------

    def calibrate_gyro(self, samples=200, delay=0.01):
        gx_sum = gy_sum = gz_sum = 0.0

        for _ in range(samples):
            gx, gy, gz = self._gyro_raw()
            gx_sum += gx
            gy_sum += gy
            gz_sum += gz
            time.sleep(delay)

        self.gyro_bias = (
            gx_sum / samples,
            gy_sum / samples,
            gz_sum / samples
        )

    # -------- Raw readings --------

    def _accel_raw(self):
        x, y, z = self._read_vector(OUTX_L_A)
        scale = 0.061 / 1000  # mg/LSB → g
        return (x * scale, y * scale, z * scale)

    def _gyro_raw(self):
        x, y, z = self._read_vector(OUTX_L_G)
        scale = 8.75 / 1000  # mdps/LSB → dps
        return (x * scale, y * scale, z * scale)

    # -------- Public API --------

    def accel(self):
        """
        Returns acceleration in m/s^2
        """
        x, y, z = self._accel_raw()
        g_to_ms2 = 9.80
        return (
            x * g_to_ms2,
            y * g_to_ms2,
            z * g_to_ms2
        )

    def gyro(self):
        """
        Returns angular velocity in rad/s (bias corrected)
        """
        x, y, z = self._gyro_raw()
        bx, by, bz = self.gyro_bias

        # remove bias
        x -= bx
        y -= by
        z -= bz

        deg_to_rad = math.pi / 180.0

        return (
            x * deg_to_rad,
            y * deg_to_rad,
            z * deg_to_rad
        )

    def temperature(self):
        data = self._read_reg(OUT_TEMP_L, 2)
        temp_raw = self._twos_comp(data[0] | (data[1] << 8))
        return 25 + (temp_raw / 256.0)
    
i2c = I2C(0, scl=Pin(14), sda=Pin(22))

imu = LSM6DSOX(i2c)

while True:
    ax, ay, az = imu.accel()
    gx, gy, gz = imu.gyro()
    temp = imu.temperature()

    print("Accel:", ax, ay, az)
    print("Gyro:", gx, gy, gz)
    print("Temp:", temp)
    print("------")

    time.sleep(0.2)
