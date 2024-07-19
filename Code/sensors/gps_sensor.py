import time
import serial
import adafruit_gps
from sensors.sensor_base import Sensor

class GPSSensor(Sensor):
    def __init__(self, pause_event, pause_condition):
        try:
            self.uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
            self.gps = adafruit_gps.GPS(self.uart, debug=False)
            self.gps.send_command(b'PMTK314,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1')
            self.gps.send_command(b'PMTK220,1000')
            super().__init__('/home/jumiknows/Balloon4/Code/GPS/sensor_readings.csv', pause_event, pause_condition)
        except ValueError as e:
            print(f"Error initializing GPSSensor: {e}")
            self.gps = None

    def csv_headers(self):
        return ['Timestamp', 'Latitude', 'Longitude', 'Velocity (knots)', 'Altitude (m)']

    def read_sensor_data(self):
        if self.gps:
            self.gps.update()
            if self.gps.has_fix:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                latitude = self.gps.latitude
                longitude = self.gps.longitude
                velocity = self.gps.speed_knots
                altitude = self.gps.altitude_m
                return [current_time, latitude, longitude, velocity, altitude]
            else:
                return ["No fix"] * 5
        else:
            return ["No sensor"] * 5
