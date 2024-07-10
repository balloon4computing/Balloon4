import time
import csv
import os
from filelock import FileLock
import board
import busio
import adafruit_bme680

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

pressure_file_path = '/home/jumiknows/Balloon4/Code/BME680/sensor_readings.csv'
pressure_lock = FileLock(pressure_file_path + ".lock")

class PressureSensor:
    def __init__(self):
        self.initialize_file()
        try:
            self.sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
        except Exception as e:
            print(f"Error initializing BME680: {e}")
            self.sensor = None

    def initialize_file(self):
        if not os.path.exists(pressure_file_path):
            with open(pressure_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Temperature (C)', 'Pressure (hPa)', 'Humidity (RH)'])

    def log_data(self):
        while True:
            try:
                if self.sensor is None:
                    self.sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
                with pressure_lock:
                    with open(pressure_file_path, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        while True:
                            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                            temperature = self.sensor.temperature if self.sensor else 'N/A'
                            pressure = self.sensor.pressure if self.sensor else 'N/A'
                            humidity = self.sensor.humidity if self.sensor else 'N/A'
                            writer.writerow([timestamp, temperature, pressure, humidity])
                            file.flush()
                            print(f"Pressure - Timestamp: {timestamp}, Temperature: {temperature:.2f} C, Pressure: {pressure:.2f} hPa, Humidity: {humidity:.2f} %")
                            time.sleep(1)
            except Exception as e:
                print(f"Error logging pressure: {e}")
                self.sensor = None
                time.sleep(5)  # Wait before retrying
