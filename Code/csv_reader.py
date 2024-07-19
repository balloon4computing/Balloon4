import time
import csv
from filelock import FileLock

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

def read_csv_files():
    try:
        print("Reading CSV files...")
        for name, file_path in file_paths.items():
            with file_locks[name]:
                print(f"Reading from {file_path}...")
                with open(file_path, mode='r', newline='') as file:
                    reader = csv.reader(file)
                    last_row = None
                    for last_row in reader:
                        pass
                    if last_row:
                        print(f"Last entry in {file_path}: {last_row}")
    except Exception as e:
        print(f"Error reading CSV files: {e}")
