import time
import csv
from filelock import FileLock
import os

class Sensor:
    def __init__(self, file_path, pause_event, pause_condition):
        self.file_path = file_path
        self.lock = FileLock(file_path + ".lock")
        self.pause_event = pause_event
        self.pause_condition = pause_condition
        self.initialize_file()

    def initialize_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.csv_headers())

    def csv_headers(self):
        raise NotImplementedError("This method should be implemented by subclasses")

    def read_sensor_data(self):
        raise NotImplementedError("This method should be implemented by subclasses")

    def log_data(self):
        try:
            while True:
                with self.pause_condition:
                    while not self.pause_event.is_set():
                        self.pause_condition.wait()

                data = self.read_sensor_data()
                with self.lock:
                    with open(self.file_path, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(data)
                        file.flush()
                        print(f"{self.__class__.__name__} - Data: {data}")
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"{self.__class__.__name__} logging stopped by user.")
        except Exception as e:
            print(f"Error logging {self.__class__.__name__}: {e}")
            time.sleep(5)
