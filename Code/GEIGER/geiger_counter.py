import time
import csv
import os
from filelock import FileLock
import RPi.GPIO as GPIO

geiger_file_path = '/home/jumiknows/Balloon4/Code/GEIGER/geiger_log.csv'
geiger_lock = FileLock(geiger_file_path + ".lock")

class GeigerCounter:
    def __init__(self):
        self.initialize_file()
        self.GEIGER_PIN = 17
        self.usvh_ratio = 0.00332  # This is for the J305 tube
        self.tubeCounts = 0
        GPIO.setup(self.GEIGER_PIN, GPIO.IN)
        GPIO.add_event_detect(self.GEIGER_PIN, GPIO.FALLING, callback=self.impulse)

    def initialize_file(self):
        if not os.path.exists(geiger_file_path):
            with open(geiger_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Time", "CPS", "uSv/h"])

    def impulse(self, channel):
        self.tubeCounts += 1

    def log_data(self):
        while True:
            try:
                startTime = time.time()
                while time.time() - startTime <= 1:
                    pass
                currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                cps = self.tubeCounts
                # 60 to change from cps to cpm
                usvh = self.tubeCounts * 60 * self.usvh_ratio
                with geiger_lock:
                    with open(geiger_file_path, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([currentTime, cps, usvh])
                        file.flush()
                print(f"Geiger - Time: {currentTime}, CPS: {cps}, uSv/h: {usvh}")
                self.tubeCounts = 0
            except Exception as e:
                print(f"Error logging Geiger counter: {e}")
                time.sleep(5)  # Wait before retrying
