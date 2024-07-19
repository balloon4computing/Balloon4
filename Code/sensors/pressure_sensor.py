import time
import board
import busio
import adafruit_bme680
from sensors.sensor_base import Sensor

class PressureSensor(Sensor):
    def __init__(self, pause_event, pause_condition):
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
            super().__init__('/home/jumiknows/Balloon4/Code/BME680/sensor_readings.csv', pause_event, pause_condition)
            print("PressureSensor initialized successfully.")
        except ValueError as e:
            print(f"Error initializing PressureSensor: {e}")
            self.sensor = None

    def csv_headers(self):
        return ['Timestamp', 'Temperature (C)', 'Pressure (hPa)', 'Humidity (RH)']

    def read_sensor_data(self):
        if self.sensor:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            temperature = self.sensor.temperature
            pressure = self.sensor.pressure
            humidity = self.sensor.humidity
            print(f"Pressure - Timestamp: {timestamp}, Temperature: {temperature:.2f} C, Pressure: {pressure:.2f} hPa, Humidity: {humidity:.2f} RH")
            return [timestamp, temperature, pressure, humidity]
        else:
            return ["No sensor"] * 4
