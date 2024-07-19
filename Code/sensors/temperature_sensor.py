import time
import board
import busio
import adafruit_mcp9808
from sensors.sensor_base import Sensor

class TemperatureSensor(Sensor):
    def __init__(self, pause_event, pause_condition):
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.sensor = adafruit_mcp9808.MCP9808(i2c)
            super().__init__('/home/jumiknows/Balloon4/Code/MCP9808/temperature_readings.csv', pause_event, pause_condition)
        except ValueError as e:
            print(f"Error initializing TemperatureSensor: {e}")
            self.sensor = None

    def csv_headers(self):
        return ['Timestamp', 'Temperature (C)']

    def read_sensor_data(self):
        if self.sensor:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            temperature = self.sensor.temperature
            return [timestamp, temperature]
        else:
            return ["No sensor", "No data"]
