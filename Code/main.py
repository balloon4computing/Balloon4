import sys
import threading
import time

# Ensure the current directory and its parent are in the sys.path
sys.path.insert(0, '/home/jumiknows/Balloon4/Code')
sys.path.insert(0, '/home/jumiknows/Balloon4')

# Import sensor classes
print("Importing sensor classes...")
from sensors.temperature_sensor import TemperatureSensor
from sensors.gyroscope_sensor import GyroscopeSensor
from sensors.pressure_sensor import PressureSensor
from sensors.geiger_counter import GeigerCounter
from sensors.ultrasonic_sensor import UltrasonicSensor
from sensors.gps_sensor import GPSSensor
from csv_reader import read_csv_files

print("All classes imported successfully.")

def spinner(pause_event, pause_condition, sensor_threads):
    try:
        while True:
            time.sleep(10)  # Sleep before reading
            with pause_condition:
                pause_event.clear()  # Pause sensor threads
                pause_condition.notify_all()
                
                # Wait for all sensor threads to acknowledge the pause
                for thread in sensor_threads:
                    if thread.is_alive():
                        thread.join(timeout=1)
            
            read_csv_files()
            
            with pause_condition:
                pause_event.set()  # Resume sensor threads
                pause_condition.notify_all()
    except KeyboardInterrupt:
        print("Spinner thread stopped by user.")

if __name__ == "__main__":
    print("Initializing sensors...")

    # Create an event and condition to control pausing and resuming
    pause_event = threading.Event()
    pause_event.set()  # Initially set the event to allow logging
    pause_condition = threading.Condition()

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

    # Create and start a spinner thread for pausing/resuming and reading CSV files
    spinner_thread = threading.Thread(target=spinner, args=(pause_event, pause_condition, sensor_threads))
    spinner_thread.start()

    print("Spinner thread started.")
    
    try:
        for thread in sensor_threads:
            thread.join()
        spinner_thread.join()
    except KeyboardInterrupt:
        print("Logging stopped by user.")
    finally:
        print("All threads joined.")
