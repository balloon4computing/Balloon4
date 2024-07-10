import time
import csv
import os
from filelock import FileLock
import serial
import adafruit_gps

gps_file_path = '/home/jumiknows/Balloon4/Code/GPS/sensor_readings.csv'
gps_lock = FileLock(gps_file_path + ".lock")

class GPSSensor:
    def __init__(self):
        self.initialize_file()
        self.uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
        self.gps = adafruit_gps.GPS(self.uart, debug=False)
        # Configure the GPS module to update every second (1000 milliseconds)
        self.gps.send_command(b'PMTK314,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1')
        self.gps.send_command(b'PMTK220,1000')

    def initialize_file(self):
        if not os.path.exists(gps_file_path):
            with open(gps_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Latitude', 'Longitude', 'Velocity (knots)', 'Altitude (m)'])

    def log_data(self):
        while True:
            try:
                with gps_lock:
                    with open(gps_file_path, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        while True:
                            self.gps.update()
                            if self.gps.has_fix:
                                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                latitude = self.gps.latitude
                                longitude = self.gps.longitude
                                velocity = self.gps.speed_knots  # Velocity in knots
                                altitude = self.gps.altitude_m  # Altitude in meters
                                writer.writerow([current_time, latitude, longitude, velocity, altitude])
                                file.flush()
                                print(f"GPS - Time: {current_time}, Lat: {latitude}, Long: {longitude}, Velocity: {velocity} knots, Altitude: {altitude} m")
                            else:
                                print("Waiting for GPS fix...")
                            time.sleep(1)
            except Exception as e:
                print(f"Error logging GPS data: {e}")
                time.sleep(5)  # Wait before retrying
