import time
import csv
import os
from filelock import FileLock
import RPi.GPIO as GPIO

ultrasonic_file_path = '/home/jumiknows/Balloon4/Code/ULTRASONIC/sensor_readings.csv'
ultrasonic_lock = FileLock(ultrasonic_file_path + ".lock")

class UltrasonicSensor:
    def __init__(self):
        self.initialize_file()
        self.TRIG_PIN = 12
        self.ECHO_PIN = 13
        self.delayTime = 0.2
        GPIO.setup(self.TRIG_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)

    def initialize_file(self):
        if not os.path.exists(ultrasonic_file_path):
            with open(ultrasonic_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'PingTravelTime','Distance (inches)'])

    def log_data(self):
        while True:
            try:
                with ultrasonic_lock:
                    with open(ultrasonic_file_path, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        while True:
                            GPIO.output(self.TRIG_PIN, 0)
                            time.sleep(2E-6)
                            GPIO.output(self.TRIG_PIN, 1)
                            time.sleep(10E-6)
                            GPIO.output(self.TRIG_PIN, 0)
                            while GPIO.input(self.ECHO_PIN) == 0:
                                pass
                            echoStartTime = time.time()
                            while GPIO.input(self.ECHO_PIN) == 1:
                                pass
                            echoStopTime = time.time()
                            pingTravelTime = echoStopTime - echoStartTime
                            dist_cm = (pingTravelTime * 34444) / 2
                            dist_inch = dist_cm * 0.3937008
                            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                            writer.writerow([timestamp, pingTravelTime, dist_inch])
                            file.flush()
                            print(f"Ultrasonic - Timestamp: {timestamp}, PingTravelTime: {pingTravelTime}, Distance: {dist_inch:.1f} inches | {dist_cm:.1f} cm")
                            time.sleep(self.delayTime)
            except Exception as e:
                print(f"Error logging ultrasonic sensor: {e}")
                time.sleep(5)  # Wait before retrying
