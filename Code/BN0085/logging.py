import logging
import board
import busio
import sys
import time
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER, BNO_REPORT_GYROSCOPE, BNO_REPORT_MAGNETOMETER
import numpy as np
import os
from datetime import datetime

# Initialize I2C bus and BNO08X sensor
i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)

# Enable features (accelerometer, gyroscope, magnetometer)
bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_GYROSCOPE)
bno.enable_feature(BNO_REPORT_MAGNETOMETER)

# Define CSV file paths and headers
accel_file = 'AccelLog.csv'
gyro_file = 'GyroLog.csv'
magnet_file = 'MagnetLog.csv'

accel_header = 'timestamp,accel_x (m/s^2),accel_y (m/s^2),accel_z (m/s^2)'
gyro_header = 'timestamp,gyro_x (rad/s),gyro_y (rad/s),gyro_z (rad/s)'
magnet_header = 'timestamp,magnet_x (uT),magnet_y (uT),magnet_z (uT)'

# Check if files exist; create headers if they don't
if not os.path.exists(accel_file):
    with open(accel_file, 'w') as f_accel:
        f_accel.write(accel_header + '\n')

if not os.path.exists(gyro_file):
    with open(gyro_file, 'w') as f_gyro:
        f_gyro.write(gyro_header + '\n')

if not os.path.exists(magnet_file):
    with open(magnet_file, 'w') as f_magnet:
        f_magnet.write(magnet_header + '\n')

# Main loop to read sensor data and save to CSV
while True:
    try:
        # Get current timestamp
        current_time = datetime.now().isoformat()
        
        # Read sensor data
        accel_x, accel_y, accel_z = bno.acceleration
        gyro_x, gyro_y, gyro_z = bno.gyro
        magnet_x, magnet_y, magnet_z = bno.magnetic
        
        # Append data to CSV files with timestamp
        with open(accel_file, 'a') as f_accel:
            np.savetxt(f_accel, [[current_time, accel_x, accel_y, accel_z]], delimiter=',', fmt='%s')
        
        with open(gyro_file, 'a') as f_gyro:
            np.savetxt(f_gyro, [[current_time, gyro_x, gyro_y, gyro_z]], delimiter=',', fmt='%s')
        
        with open(magnet_file, 'a') as f_magnet:
            np.savetxt(f_magnet, [[current_time, magnet_x, magnet_y, magnet_z]], delimiter=',', fmt='%s')
        
        # Sleep for 1 second
        time.sleep(1)
    
    except Exception as e:
        logging.exception("Exception occurred", exc_info=True)
        # Handle exceptions here if needed
