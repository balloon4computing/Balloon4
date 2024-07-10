import time
import csv
from filelock import FileLock

# File paths
temperature_file_path = '/home/jumiknows/Balloon4/Code/MCP9808/temperature_readings.csv'
sensor_file_path = '/home/jumiknows/Balloon4/Code/BN0085/sensor_readings.csv'
pressure_file_path = '/home/jumiknows/Balloon4/Code/BME680/sensor_readings.csv'
geiger_file_path = '/home/jumiknows/Balloon4/Code/GEIGER/geiger_log.csv'
ultrasonic_file_path = '/home/jumiknows/Balloon4/Code/ULTRASONIC/sensor_readings.csv'
gps_file_path = '/home/jumiknows/Balloon4/Code/GPS/sensor_readings.csv'

# Locks for file access
temperature_lock = FileLock(temperature_file_path + ".lock")
sensor_lock = FileLock(sensor_file_path + ".lock")
pressure_lock = FileLock(pressure_file_path + ".lock")
geiger_lock = FileLock(geiger_file_path + ".lock")
ultrasonic_lock = FileLock(ultrasonic_file_path + ".lock")
gps_lock = FileLock(gps_file_path + ".lock")

def read_csv_files():
    file_paths = [
        temperature_file_path,
        sensor_file_path,
        pressure_file_path,
        geiger_file_path,
        ultrasonic_file_path,
        gps_file_path
    ]
    file_locks = [
        temperature_lock,
        sensor_lock,
        pressure_lock,
        geiger_lock,
        ultrasonic_lock,
        gps_lock
    ]

    while True:
        try:
            for file_path, file_lock in zip(file_paths, file_locks):
                with file_lock:
                    with open(file_path, mode='r', newline='') as file:
                        reader = csv.reader(file)
                        last_row = None
                        for last_row in reader:
                            pass
                        if last_row:
                            print(f"Last entry in {file_path}: {last_row}")
            time.sleep(10)  # Read every 10 seconds
        except Exception as e:
            print(f"Error reading CSV files: {e}")
            time.sleep(5)  # Wait before retrying
