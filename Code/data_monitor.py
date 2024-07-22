import os
import csv
import struct
import time
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
    def __init__(self, rfm9x, tx_power=23):
        self.rfm9x = rfm9x
        self.rfm9x.tx_power = tx_power
        self.rfm9x.spreading_factor = 10
        self.rfm9x.signal_bandwidth = 125000
        self.rfm9x.enable_crc = True
        self.rfm9x.coding_rate = 8
        self.last_transmitted_data = {}

    def read_and_send_data(self):
        identifier_map = {
            'temperature': (0x03, "=ie", self.unpack_temperature),
            'sensor': (0x05, "=i9e", self.unpack_sensor),
            'pressure': (0x01, "=ifee", self.unpack_pressure),
            'geiger': (0x02, "=iH", self.unpack_geiger),
            'ultrasonic': (0x04, "=if", self.unpack_ultrasonic),
            'gps': (0x00, "=iffi", self.unpack_gps)
        }

        for name, file_path in file_paths.items():
            file_lock = file_locks[name]
            identifier, struct_format, unpack_func = identifier_map[name]

            try:
                if not os.path.exists(file_path):
                    continue
                
                try:
                    with file_lock.acquire(timeout=1):
                        with open(file_path, mode='r', newline='') as file:
                            reader = csv.reader((line.replace('\0', '') for line in file))
                            next(reader, None)  # Skip header
                            
                            last_row = None
                            for row in reader:
                                last_row = row
                            
                            if last_row:
                                try:
                                    timestamp = int(time.time())
                                    data = self.pack_data(identifier, struct_format, timestamp, last_row)
                                    self.rfm9x.send(data)
                                    print("Sent data:")
                                    unpack_func(data)
                                    print("Corresponding row in the CSV file:")
                                    print(last_row)
                                except Exception as e:
                                    print(f"Exception occurred while processing row {last_row}: {e}")
                except Timeout:
                    print(f"Could not acquire lock for {file_path}. Skipping.")
            except Exception as e:
                print(f"Exception occurred while reading {file_path}: {e}")

    def pack_data(self, identifier, struct_format, timestamp, row):
        if identifier == 0x03:  # Temperature Inside
            return struct.pack("=" + struct_format, timestamp, float(row[1]))
        elif identifier == 0x05:  # BNO085 Sensor
            return struct.pack("=" + struct_format, timestamp, *map(float, row[1:10]))
        elif identifier == 0x01:  # BME680 Sensor
            return struct.pack("=" + struct_format, timestamp, float(row[1]), float(row[2]), float(row[3]))
        elif identifier == 0x02:  # Geiger Counter
            return struct.pack("=" + struct_format, timestamp, int(row[1]))
        elif identifier == 0x04:  # Ultrasonic Sensor
            return struct.pack("=" + struct_format, timestamp, float(row[1]), float(row[2]))
        elif identifier == 0x00:  # GPS Sensor
            return struct.pack("=" + struct_format, timestamp, float(row[1]), float(row[2]), int(float(row[3])))

    def unpack_temperature(self, data):
        unpacked_data = struct.unpack("=ie", data[1:])
        print("Temperature:", unpacked_data)

    def unpack_sensor(self, data):
        unpacked_data = struct.unpack("=i9e", data[1:])
        print("Gyroscope:", unpacked_data)

    def unpack_pressure(self, data):
        unpacked_data = struct.unpack("=ifee", data[1:])
        print("Pressure:", unpacked_data)

    def unpack_geiger(self, data):
        unpacked_data = struct.unpack("=iH", data[1:])
        print("Geiger:", unpacked_data)

    def unpack_ultrasonic(self, data):
        unpacked_data = struct.unpack("=if", data[1:])
        print("Ultrasonic:", unpacked_data)

    def unpack_gps(self, data):
        unpacked_data = struct.unpack("=iffi", data[1:])
        print("GPS:", unpacked_data)
