import time
import board
import busio
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER, BNO_REPORT_GYROSCOPE, BNO_REPORT_MAGNETOMETER
from sensors.sensor_base import Sensor

class GyroscopeSensor(Sensor):
    def __init__(self, pause_event, pause_condition):
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.sensor = BNO08X_I2C(i2c)
            self.sensor.enable_feature(BNO_REPORT_ACCELEROMETER)
            self.sensor.enable_feature(BNO_REPORT_GYROSCOPE)
            self.sensor.enable_feature(BNO_REPORT_MAGNETOMETER)
            print("GyroscopeSensor initialized successfully.")
            super().__init__('/home/jumiknows/Balloon4/Code/BN0085/sensor_readings.csv', pause_event, pause_condition)
        except ValueError as e:
            print(f"Error initializing GyroscopeSensor: {e}")
            self.sensor = None

    def csv_headers(self):
        return ['Timestamp', 'Accel X', 'Accel Y', 'Accel Z', 'Gyro X', 'Gyro Y', 'Gyro Z', 'Magnet X', 'Magnet Y', 'Magnet Z']

    def read_sensor_data(self):
        if self.sensor:
            try:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                accel_x, accel_y, accel_z = self.sensor.acceleration
                gyro_x, gyro_y, gyro_z = self.sensor.gyro
                magnet_x, magnet_y, magnet_z = self.sensor.magnetic
                print(f"Gyroscope - Timestamp: {timestamp}, Accel: ({accel_x}, {accel_y}, {accel_z}), Gyro: ({gyro_x}, {gyro_y}, {gyro_z}), Magnet: ({magnet_x}, {magnet_y}, {magnet_z})")
                return [timestamp, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, magnet_x, magnet_y, magnet_z]
            except Exception as e:
                print(f"Error reading GyroscopeSensor data: {e}")
                return ["No data"] * 10
        else:
            return ["No sensor"] * 10
