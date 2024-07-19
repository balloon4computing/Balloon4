import time
import RPi.GPIO as GPIO
from sensors.sensor_base import Sensor

class UltrasonicSensor(Sensor):
    def __init__(self, pause_event, pause_condition):
        self.TRIG_PIN = 12
        self.ECHO_PIN = 13
        GPIO.setup(self.TRIG_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)
        super().__init__('/home/jumiknows/Balloon4/Code/ULTRASONIC/sensor_readings.csv', pause_event, pause_condition)

    def csv_headers(self):
        return ['Timestamp', 'PingTravelTime', 'Distance (inches)']

    def read_sensor_data(self):
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
        pingTravelTime = pingTravelTime / 2
        return [timestamp, pingTravelTime, dist_inch]
