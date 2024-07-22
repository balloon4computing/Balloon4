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

    def read_and_send_data(self):
        identifier_map = {
            'temperature': (0x03, "=ie"),
            'sensor': (0x05, "=i9e"),
            'pressure': (0x01, "=ifee"),
            'geiger': (0x02, "=iH"),
            'ultrasonic': (0x04, "=if"),
            'gps': (0x00, "=iffi")
        }

        for name, file_path in file_paths.items():
            if not os.path.exists(file_path):
                continue

            file_lock = file_locks[name]
            identifier, struct_format = identifier_map[name]

            try:
                with file_lock.acquire(timeout=1):
                    second_last_row = self.get_second_last_row(file_path)
                    if second_last_row:
                        try:
                            timestamp = self.convert_timestamp_to_id(second_last_row[0])  # Convert timestamp to unique ID
                            data = self.pack_data(identifier, struct_format, timestamp, second_last_row[1:])  # Skip timestamp
                            self.rfm9x.send(data)
                            print("Sent data:", self.unpack_data(struct_format, data))
                            print("Corresponding row in the CSV file:", second_last_row)
                        except Exception as e:
                            print(f"Exception occurred while processing row {second_last_row}: {e}")
            except Timeout:
                print(f"Could not acquire lock for {file_path}. Skipping.")
            except Exception as e:
                print(f"Exception occurred while reading {file_path}: {e}")

    def get_second_last_row(self, file_path):
        try:
            with open(file_path, mode='r', newline='') as file:
                reader = csv.reader((line.replace('\0', '') for line in file))
                next(reader, None)  # Skip header

                second_last_row = None
                last_row = None
                for row in reader:
                    second_last_row = last_row
                    last_row = row

                return second_last_row
        except Exception as e:
            print(f"Exception occurred while reading {file_path}: {e}")
            return None

    def convert_timestamp_to_id(self, timestamp_str):
        # Convert the timestamp string to a unique integer identifier
        struct_time = time.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return int(time.mktime(struct_time))

    def pack_data(self, identifier, struct_format, timestamp, row):
        print(f"Packing data for identifier {identifier} with format {struct_format}")
        print(f"Row data: {row}")
        try:
            if identifier == 0x03:  # Temperature Inside
                values = [float(row[0])]
            elif identifier == 0x05:  # BNO085 Sensor
                values = [float(row[i]) for i in range(9)]
            elif identifier == 0x01:  # BME680 Sensor
                values = [float(row[i]) for i in range(3)]
            elif identifier == 0x02:  # Geiger Counter
                values = [int(float(row[0]))]
            elif identifier == 0x04:  # Ultrasonic Sensor
                values = [float(row[i]) for i in range(1)]
            elif identifier == 0x00:  # GPS Sensor
                if 'No fix' in row:
                    raise ValueError("Invalid GPS data")
                values = [float(row[i]) for i in range(2)] + [int(round(float(row[2])))]
            else:
                raise ValueError("Unknown identifier")

            packed_data = struct.pack(struct_format, timestamp, *values)
            return packed_data
        except Exception as e:
            print(f"Error packing data: {e}")
            raise

    def unpack_data(self, struct_format, data):
        unpacked_data = struct.unpack(struct_format, data)
        return unpacked_data

# Example usage
if __name__ == "__main__":
    # Initialize RFM9x with the provided pin configuration
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = DigitalInOut(board.D23)
    reset = DigitalInOut(board.D24)
    rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)

    # Initialize DataMonitor
    monitor = DataMonitor(rfm9x, tx_power=23)

    # Read and send data
    monitor.read_and_send_data()
