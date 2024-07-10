import time
import csv
import os
from filelock import FileLock
import board
import busio
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER, BNO_REPORT_GYROSCOPE, BNO_REPORT_MAGNETOMETER

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

sensor_file_path = '/home/jumiknows/Balloon4/Code/BN0085/sensor_readings.csv'
sensor_lock = FileLock(sensor_file_path + ".lock")

class GyroscopeSensor:
    def __init__(self):
        self.initialize_file()
        try:
            self.sensor = BNO08X_I2C(i2c)
            self.sensor.enable_feature(BNO_REPORT_ACCELEROMETER)
            self.sensor.enable_feature(BNO_REPORT_GYROSCOPE)
            self.sensor.enable_feature(BNO_REPORT_MAGNETOMETER)
        except Exception as e:
            print(f"Error initializing BNO08X: {e}")
            self.sensor = None

    def initialize_file(self):
        if not os.path.exists(sensor_file_path):
            with open(sensor_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Accel X', 'Accel Y', 'Accel Z', 'Gyro X', 'Gyro Y', 'Gyro Z', 'Magnet X', 'Magnet Y', 'Magnet Z'])

    def log_data(self):
        while True:
            try:
                if self.sensor is None:
                    self.sensor = BNO08X_I2C(i2c)
                    self.sensor.enable_feature(BNO_REPORT_ACCELEROMETER)
                    self.sensor.enable_feature(BNO_REPORT_GYROSCOPE)
                    self.sensor.enable_feature(BNO_REPORT_MAGNETOMETER)
                with sensor_lock:
                    with open(sensor_file_path, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        while True:
                            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                            accel_x, accel_y, accel_z = self.sensor.acceleration if self.sensor else ('N/A', 'N/A', 'N/A')
                            gyro_x, gyro_y, gyro_z = self.sensor.gyro if self.sensor else ('N/A', 'N/A', 'N/A')
                            magnet_x, magnet_y, magnet_z = self.sensor.magnetic if self.sensor else ('N/A', 'N/A', 'N/A')
                            writer.writerow([timestamp, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, magnet_x, magnet_y, magnet_z])
                            file.flush()
                            print(f"Gyroscope - Timestamp: {timestamp}, Accel: ({accel_x}, {accel_y}, {accel_z}), Gyro: ({gyro_x}, {gyro_y}, {gyro_z}), Magnet: ({magnet_x}, {magnet_y}, {magnet_z})")
                            time.sleep(1)
            except Exception as e:
                print(f"Error logging sensors: {e}")
                self.sensor = None
                time.sleep(5)  # Wait before retrying
