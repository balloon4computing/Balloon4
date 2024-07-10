import time
import csv
import os
from filelock import FileLock
import board
import busio
import adafruit_mcp9808

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

temperature_file_path = '/home/jumiknows/Balloon4/Code/MCP9808/temperature_readings.csv'
temperature_lock = FileLock(temperature_file_path + ".lock")

class TemperatureSensor:
    def __init__(self):
        self.initialize_file()
        try:
            self.sensor = adafruit_mcp9808.MCP9808(i2c)
        except Exception as e:
            print(f"Error initializing MCP9808: {e}")
            self.sensor = None

    def initialize_file(self):
        if not os.path.exists(temperature_file_path):
            with open(temperature_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Temperature (C)'])

    def log_data(self):
        while True:
            try:
                if self.sensor is None:
                    self.sensor = adafruit_mcp9808.MCP9808(i2c)
                with temperature_lock:
                    with open(temperature_file_path, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        while True:
                            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                            temperature = self.sensor.temperature if self.sensor else 'N/A'
                            writer.writerow([timestamp, temperature])
                            file.flush()
                            print(f"Temperature - Timestamp: {timestamp}, Temperature: {temperature:.2f} C")
                            time.sleep(1)
            except Exception as e:
                print(f"Error logging temperature: {e}")
                self.sensor = None
                time.sleep(5)  # Wait before retrying
