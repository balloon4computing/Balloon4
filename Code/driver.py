import sys
import threading
import time
import board
import busio
from digitalio import DigitalInOut
import adafruit_rfm9x
from sensors.temperature_sensor import TemperatureSensor
from sensors.gyroscope_sensor import GyroscopeSensor
from sensors.pressure_sensor import PressureSensor
from sensors.geiger_counter import GeigerCounter
from sensors.ultrasonic_sensor import UltrasonicSensor
from sensors.gps_sensor import GPSSensor
from data_monitor import DataMonitor

# Ensure the current directory and its parent are in the sys.path
sys.path.insert(0, '/home/jumiknows/Balloon4/Code')
sys.path.insert(0, '/home/jumiknows/Balloon4')

print("All classes imported successfully.")

def data_monitor_thread(data_monitor):
    try:
        while True:
            data_monitor.read_and_send_data()
            time.sleep(10)
    except KeyboardInterrupt:
        print("Data monitor thread stopped by user.")

if __name__ == "__main__":
    print("Initializing sensors...")

    # Create an event and condition to control pausing and resuming
    pause_event = threading.Event()
    pause_event.set()  # Initially set the event to allow logging
    pause_condition = threading.Condition()

    # Initialize RFM9x (example)
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = DigitalInOut(board.CE1)
    reset = DigitalInOut(board.D25)
    rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)
    
    # Initialize DataMonitor
    monitor = DataMonitor(rfm9x)

    # Create sensor instances
    sensors = []
    sensors.append(TemperatureSensor(pause_event, pause_condition))
    sensors.append(GyroscopeSensor(pause_event, pause_condition))
    sensors.append(PressureSensor(pause_event, pause_condition))
    sensors.append(GeigerCounter(pause_event, pause_condition))
    sensors.append(UltrasonicSensor(pause_event, pause_condition))
    sensors.append(GPSSensor(pause_event, pause_condition))

    print("Sensor instances created.")

    # Filter out None sensors
    sensors = [sensor for sensor in sensors if getattr(sensor, 'sensor', True)]

    # Create threads for each sensor
    sensor_threads = [threading.Thread(target=sensor.log_data) for sensor in sensors]

    # Start sensor threads
    for thread in sensor_threads:
        thread.start()

    print("All sensor threads started.")

    # Create and start a data monitor thread
    monitor_thread = threading.Thread(target=data_monitor_thread, args=(monitor,))
    monitor_thread.start()

    print("Data monitor thread started.")
    
    try:
        for thread in sensor_threads:
            thread.join()
        monitor_thread.join()
    except KeyboardInterrupt:
        print("Logging stopped by user.")
    finally:
        print("All threads joined.")
