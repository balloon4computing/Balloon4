import sys
import os
import threading

# Add the directory containing the sensor modules to sys.path
sys.path.append('/home/jumiknows/Balloon4/Code/MCP9808')
sys.path.append('/home/jumiknows/Balloon4/Code/BN0085')
sys.path.append('/home/jumiknows/Balloon4/Code/BME680')
sys.path.append('/home/jumiknows/Balloon4/Code/GEIGER')
sys.path.append('/home/jumiknows/Balloon4/Code/ULTRASONIC')
sys.path.append('/home/jumiknows/Balloon4/Code/GPS')

# Import sensor classes
from temperature_sensor import TemperatureSensor
from gyroscope_sensor import GyroscopeSensor
from pressure_sensor import PressureSensor
from geiger_counter import GeigerCounter
from ultrasonic_sensor import UltrasonicSensor
from gps_sensor import GPSSensor
from csv_reader import read_csv_files

if __name__ == "__main__":
    # Create sensor instances
    temperature_sensor = TemperatureSensor()
    gyroscope_sensor = GyroscopeSensor()
    pressure_sensor = PressureSensor()
    geiger_counter = GeigerCounter()
    ultrasonic_sensor = UltrasonicSensor()
    gps_sensor = GPSSensor()

    # Create threads for logging temperature, sensor data, pressure, Geiger data, ultrasonic data, and GPS data
    temperature_thread = threading.Thread(target=temperature_sensor.log_data)
    sensors_thread = threading.Thread(target=gyroscope_sensor.log_data)
    pressure_thread = threading.Thread(target=pressure_sensor.log_data)
    geiger_thread = threading.Thread(target=geiger_counter.log_data)
    ultrasonic_thread = threading.Thread(target=ultrasonic_sensor.log_data)
    gps_thread = threading.Thread(target=gps_sensor.log_data)
    read_thread = threading.Thread(target=read_csv_files)

    # Start the threads
    temperature_thread.start()
    sensors_thread.start()
    pressure_thread.start()
    geiger_thread.start()
    ultrasonic_thread.start()
    gps_thread.start()
    read_thread.start()

    # Join the threads to keep the script running
    temperature_thread.join()
    sensors_thread.join()
    pressure_thread.join()
    geiger_thread.join()
    ultrasonic_thread.join()
    gps_thread.join()
    read_thread.join()
