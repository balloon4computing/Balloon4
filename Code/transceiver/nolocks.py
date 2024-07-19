
from RFM9X import RFM9X
import csv
import struct
import time
import os
from filelock import FileLock
import board
import busio
from digitalio import DigitalInOut
import adafruit_rfm9x

# File paths
temperature_file_path = '/home/jumiknows/Balloon4/Code/MCP9808/temperature_readings.csv'
sensor_file_path = '/home/jumiknows/Balloon4/Code/BN0085/sensor_readings.csv'
pressure_file_path = '/home/jumiknows/Balloon4/Code/BME680/sensor_readings.csv'
geiger_file_path = '/home/jumiknows/Balloon4/Code/GEIGER/geiger_log.csv'
ultrasonic_file_path = '/home/jumiknows/Balloon4/Code/ULTRASONIC/sensor_readings.csv'
gps_file_path = '/home/jumiknows/Balloon4/Code/GPS/sensor_readings.csv'

class DataMonitor:
    def __init__(self, rfm9x):
        self.rfm9x = rfm9x
        self.last_transmitted_data = {}  # Dictionary to store the last transmitted data row for each file

    def log_sent_data(self, data):
        print(data)

    def read_and_send_data(self):
        file_paths = [
            (temperature_file_path, 0x03),
            (sensor_file_path, 0x05),
            (pressure_file_path, 0x01),
            (geiger_file_path, 0x02),
            (ultrasonic_file_path, 0x04),
            (gps_file_path, 0x00)
        ]

        for file_path, identifier in file_paths:
            try:
                if not os.path.exists(file_path):
                    continue
                with open(file_path, mode='r', newline='') as file:
                    reader = csv.reader((line.replace('\0', '') for line in file))
                    # Skip the header line
                    next(reader, None)
                    
                    last_data = self.last_transmitted_data.get(file_path, None)
                    new_data_rows = []

                    for row in reader:
                        # Skip rows that match the last transmitted data (ignoring the first column)
                        if last_data and row[1:] == last_data[1:]:
                            continue
                        new_data_rows.append(row)
                        last_data = row
                    
                    # If new data rows are found, update last transmitted data and process the data
                    if new_data_rows:
                        self.last_transmitted_data[file_path] = new_data_rows[-1]  # Store the last row of new data
                        for row in new_data_rows:
                            try:
                                timestamp = row[0].split(' ')[1].replace(':','')
                                timestamp = int(timestamp)
                                if identifier == 0x03:
                                    # Temperature Outside
                                    temperature = float(row[1])  # row[1] is the temperature value
                                    data = struct.pack("=Bif", identifier, timestamp, temperature)
                                elif identifier == 0x05:
                                    # BNO085
                                    ax, ay, az, gx, gy, gz, mx, my, mz = map(float, row[1:10])  # row[1] to row[9] are the sensor values
                                    data = struct.pack("=Bi9f", identifier, timestamp, ax, ay, az, gx, gy, gz, mx, my, mz)
                                elif identifier == 0x01:
                                    # BME680
                                    barometer = float(row[1])  # row[1] is the barometer value
                                    humidity = float(row[2])  # row[2] is the humidity value
                                    temp_inside = float(row[3])  # row[3] is the inside temperature value
                                    data = struct.pack("=BifHf", identifier, timestamp, barometer, int(humidity*100), int(temp_inside*100))
                                elif identifier == 0x02:
                                    # Geiger
                                    geiger = int(row[1])  # row[1] is the geiger count value
                                    data = struct.pack("=BiH", identifier, timestamp, geiger)
                                elif identifier == 0x04:
                                    # Sound Experiment
                                    reserved = float(row[1])  # row[1] is the distance value
                                    data = struct.pack("=Bif", identifier, timestamp, reserved)
                                elif identifier == 0x00:
                                    # GPS
                                    latitude = float(row[1])  # row[1] is the latitude value
                                    longitude = float(row[2])  # row[2] is the longitude value
                                    altitude = int(row[3])  # row[3] is the altitude value
                                    data = struct.pack("=Biffi", identifier, timestamp, latitude, longitude, altitude)
                                else:
                                    continue
                                
                                self.rfm9x.send_data(data)
                                print("Unpacked data:")
                                self.unpack_data(data)
                                print("Corresponding row in the csv file:")
                                print(row)
                            except Exception as e:
                                print(f"Exception occurred while processing row {row}: {e}")
                                continue
            except Exception as e:
                print(f"Exception occurred while reading {file_path}: {e}")
                continue

    def unpack_data(self, data):
        try:
            identifier = data[0]
            if identifier == 0x03:
                unpacked_data = struct.unpack("=if", data[1:])
                print(unpacked_data[0], unpacked_data[1])
            elif identifier == 0x05:
                unpacked_data = struct.unpack("=i9f", data[1:])
                print(*unpacked_data)
            elif identifier == 0x01:
                unpacked_data = struct.unpack("=ifHf", data[1:])
                print(*unpacked_data)
            elif identifier == 0x02:
                unpacked_data = struct.unpack("=iH", data[1:])
                print(*unpacked_data)
            elif identifier == 0x04:
                unpacked_data = struct.unpack("=if", data[1:])
                print(*unpacked_data)
            elif identifier == 0x00:
                unpacked_data = struct.unpack("=iffi", data[1:])
                print(*unpacked_data)
        except Exception as e:
            print(f"Exception occurred while unpacking data: {e}")

