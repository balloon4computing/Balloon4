import logging
import board
import busio
import sys
import time
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER
import numpy as np

i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_GYROSCOPE)
bno.enable_feature(BNO_REPORT_MAGNETOMETER)

while True:
    accel_x, accel_y, accel_z = bno.acceleration
    gyro_x, gyro_y, gyro_z = bno.gyro
    magnet_x,magnet_y,magnet_z = bno.magnetic
    
    np.savetext('AccelLog.csv', (accel_x,accel_y,accel_z))
    np.savetext('AccelLog.csv', (gyro_x,gyro_y,gyro_z))
    np.savetext('AccelLog.csv', (magnet_x,magnet_y,magnet_z))
    time.sleep(1)
