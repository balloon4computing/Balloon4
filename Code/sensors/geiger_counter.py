import time
import RPi.GPIO as GPIO
from sensors.sensor_base import Sensor

class GeigerCounter(Sensor):
    def __init__(self, pause_event, pause_condition):
        try:
            self.GEIGER_PIN = 17
            self.usvh_ratio = 0.00332
            self.tubeCounts = 0
            GPIO.setup(self.GEIGER_PIN, GPIO.IN)
            GPIO.add_event_detect(self.GEIGER_PIN, GPIO.FALLING, callback=self.impulse)
            super().__init__('/home/jumiknows/Balloon4/Code/GEIGER/geiger_log.csv', pause_event, pause_condition)
            print("GeigerCounter initialized successfully.")
        except ValueError as e:
            print(f"Error initializing GeigerCounter: {e}")
            self.sensor = None

    def impulse(self, channel):
        self.tubeCounts += 1

    def csv_headers(self):
        return ["Time", "CPM", "uSv/h"]

    def read_sensor_data(self):
        startTime = time.time()
        while time.time() - startTime <= 1:
            pass
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cps = self.tubeCounts
        usvh = self.tubeCounts * 60 * self.usvh_ratio
        self.tubeCounts = 0
        print(f"GeigerCounter - Timestamp: {currentTime}, CPS: {cps}, uSv/h: {usvh}")
        return [currentTime, cps, usvh]
