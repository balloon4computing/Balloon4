import os
import time
import csv
import struct
from filelock import FileLock, Timeout
import board
import busio
from digitalio import DigitalInOut
import adafruit_rfm9x

# File paths
file_paths = {
    'temperature': '/home/jumiknows/Balloon4/Code/MCP9808/temperature_readings.csv',
    'sensor': '/home/jumiknows/Balloon4/Code/BN0085/sensor_readings.csv',
    'pressure': '/home/jumiknows/Balloon4/Code/BME680/sensor_readings.csv',
    'geiger': '/home/jumiknows/Balloon4/Code/GEIGER/geiger_log.csv',
    'ultrasonic': '/home/jumiknows/Balloon4/Code/ULTRASONIC/sensor_readings.csv',
    'gps': '/home/jumiknows/Balloon4/Code/GPS/sensor_readings.csv'
}

# Locks for file access
file_locks = {name: FileLock(path + ".lock") for name, path in file_paths.items()}

class DataMonitor:
    def __init__(self, rfm9x):
        self.rfm9x = rfm9x
        self.last_transmitted_data = {}

    def log_sent_data(self, data):
        print(data)

    def read_and_send_data(self):
        identifier_map = {
            'temperature': 0x03,
            'sensor': 0x05,
            'pressure': 0x01,
            'geiger': 0x02,
            'ultrasonic': 0x04,
            'gps': 0x00
        }

        for name, file_path in file_paths.items():
            file_lock = file_locks[name]
            identifier = identifier_map[name]
            try:
                if not os.path.exists(file_path):
                    continue
                
                try:
                    with file_lock.acquire(timeout=1):
                        with open(file_path, mode='r', newline='') as file:
                            reader = csv.reader((line.replace('\0', '') for line in file))
                            next(reader, None)
                            
                            last_data = self.last_transmitted_data.get(file_path, None)
                            new_data_rows = []

                            for row in reader:
                                if last_data and row[1:] == last_data[1:]:
                                    continue
                                new_data_rows.append(row)
                                last_data = row
                            
                            if new_data_rows:
                                self.last_transmitted_data[file_path] = new_data_rows[-1]
                                for row in new_data_rows:
                                    try:
                                        timestamp = row[0].split(' ')[1].replace(':','')
                                        timestamp = int(timestamp)
                                        if identifier == 0x03:
                                            temperature = float(row[1])
                                            data = struct.pack("=Bif", identifier, timestamp, temperature)
                                        elif identifier == 0x05:
                                            ax, ay, az, gx, gy, gz, mx, my, mz = map(float, row[1:10])
                                            data = struct.pack("=Bi9f", identifier, timestamp, ax, ay, az, gx, gy, gz, mx, my, mz)
                                        elif identifier == 0x01:
                                            barometer = float(row[1])
                                            humidity = float(row[2])
                                            temp_inside = float(row[3])
                                            data = struct.pack("=BifHf", identifier, timestamp, barometer, int(humidity*100), int(temp_inside*100))
                                        elif identifier == 0x02:
                                            geiger = int(row[1])
                                            data = struct.pack("=BiH", identifier, timestamp, geiger)
                                        elif identifier == 0x04:
                                            reserved = float(row[1])
                                            data = struct.pack("=Bif", identifier, timestamp, reserved)
                                        elif identifier == 0x00:
                                            latitude = float(row[1])
                                            longitude = float(row[2])
                                            altitude = int(row[3])
                                            data = struct.pack("=Biffi", identifier, timestamp, latitude, longitude, altitude)
                                        else:
                                            continue
                                        
                                        self.rfm9x.send(data)
                                        print("Unpacked data:")
                                        self.unpack_data(data)
                                        print("Corresponding row in the csv file:")
                                        print(row)
                                    except Exception as e:
                                        print(f"Exception occurred while processing row {row}: {e}")
                                        continue
                except Timeout:
                    print(f"Could not acquire lock for {file_path}. Skipping.")
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
