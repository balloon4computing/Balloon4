#pip install filelock

import sys
import os
import time
import threading
import csv
from filelock import FileLock

# Add the directory containing your modules to sys.path
module_path = '/home/jumiknows/.local/lib/python3.9/site-packages'
if module_path not in sys.path:
    sys.path.append(module_path)

import board
import busio
import adafruit_mcp9808
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER, BNO_REPORT_GYROSCOPE, BNO_REPORT_MAGNETOMETER
import adafruit_bme680
import RPi.GPIO as GPIO
import serial
import adafruit_gps

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Function to initialize sensors
def create_sensors():
    try:
        mcp = adafruit_mcp9808.MCP9808(i2c)
    except Exception as e:
        print(f"Error initializing MCP9808: {e}")
        mcp = None

    try:
        bno = BNO08X_I2C(i2c)
        bno.enable_feature(BNO_REPORT_ACCELEROMETER)
        bno.enable_feature(BNO_REPORT_GYROSCOPE)
        bno.enable_feature(BNO_REPORT_MAGNETOMETER)
    except Exception as e:
        print(f"Error initializing BNO08X: {e}")
        bno = None

    try:
        bme680_sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    except Exception as e:
        print(f"Error initializing BME680: {e}")
        bme680_sensor = None

    return mcp, bno, bme680_sensor

# Initialize sensors
mcp, bno, bme680_sensor = create_sensors()

# Geiger counter setup
GEIGER_PIN = 17
usvh_ratio = 0.00332  # This is for the J305 tube
tubeCounts = 0
GPIO.setup(GEIGER_PIN, GPIO.IN)

def impulse(channel):
    global tubeCounts
    tubeCounts += 1

GPIO.add_event_detect(GEIGER_PIN, GPIO.FALLING, callback=impulse)

# Ultrasonic sensor setup
TRIG_PIN = 12
ECHO_PIN = 13
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
delayTime = 0.2

# GPS sensor setup
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b'PMTK314,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1')
gps.send_command(b'PMTK220,1000')

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

def log_temperature():
    global mcp
    while True:
        try:
            if mcp is None:
                mcp = adafruit_mcp9808.MCP9808(i2c)
            with temperature_lock:
                with open(temperature_file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    while True:
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        temperature = mcp.temperature if mcp else 'N/A'
                        writer.writerow([timestamp, temperature])
                        file.flush()
                        print(f"Temperature - Timestamp: {timestamp}, Temperature: {temperature:.2f} C")
                        time.sleep(1)
        except Exception as e:
            print(f"Error logging temperature: {e}")
            mcp = None
            time.sleep(5)  # Wait before retrying

def log_sensors():
    global bno
    while True:
        try:
            if bno is None:
                bno = BNO08X_I2C(i2c)
                bno.enable_feature(BNO_REPORT_ACCELEROMETER)
                bno.enable_feature(BNO_REPORT_GYROSCOPE)
                bno.enable_feature(BNO_REPORT_MAGNETOMETER)
            with sensor_lock:
                with open(sensor_file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    while True:
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        accel_x, accel_y, accel_z = bno.acceleration if bno else ('N/A', 'N/A', 'N/A')
                        gyro_x, gyro_y, gyro_z = bno.gyro if bno else ('N/A', 'N/A', 'N/A')
                        magnet_x, magnet_y, magnet_z = bno.magnetic if bno else ('N/A', 'N/A', 'N/A')
                        writer.writerow([timestamp, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, magnet_x, magnet_y, magnet_z])
                        file.flush()
                        print(f"Gyroscope - Timestamp: {timestamp}, Accel: ({accel_x}, {accel_y}, {accel_z}), Gyro: ({gyro_x}, {gyro_y}, {gyro_z}), Magnet: ({magnet_x}, {magnet_y}, {magnet_z})")
                        time.sleep(1)
        except Exception as e:
            print(f"Error logging sensors: {e}")
            bno = None
            time.sleep(5)  # Wait before retrying

def log_pressure():
    global bme680_sensor
    while True:
        try:
            if bme680_sensor is None:
                bme680_sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
            with pressure_lock:
                with open(pressure_file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    while True:
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        temperature = bme680_sensor.temperature if bme680_sensor else 'N/A'
                        pressure = bme680_sensor.pressure if bme680_sensor else 'N/A'
                        humidity = bme680_sensor.humidity if bme680_sensor else 'N/A'
                        writer.writerow([timestamp, temperature, pressure, humidity])
                        file.flush()
                        print(f"Pressure - Timestamp: {timestamp}, Temperature: {temperature:.2f} C, Pressure: {pressure:.2f} hPa, Humidity: {humidity:.2f} %")
                        time.sleep(1)
        except Exception as e:
            print(f"Error logging pressure: {e}")
            bme680_sensor = None
            time.sleep(5)  # Wait before retrying

def log_geiger():
    global tubeCounts
    while True:
        try:
            startTime = time.time()
            while time.time() - startTime <= 1:
                pass
            currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            cps = tubeCounts
            usvh = tubeCounts * usvh_ratio
            with geiger_lock:
                with open(geiger_file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([currentTime, cps, usvh])
                    file.flush()
            print(f"Geiger - Time: {currentTime}, CPS: {cps}, uSv/h: {usvh}")
            tubeCounts = 0
        except Exception as e:
            print(f"Error logging Geiger counter: {e}")
            time.sleep(5)  # Wait before retrying

def log_ultrasonic():
    while True:
        try:
            with ultrasonic_lock:
                with open(ultrasonic_file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    while True:
                        GPIO.output(TRIG_PIN, 0)
                        time.sleep(2E-6)
                        GPIO.output(TRIG_PIN, 1)
                        time.sleep(10E-6)
                        GPIO.output(TRIG_PIN, 0)
                        while GPIO.input(ECHO_PIN) == 0:
                            pass
                        echoStartTime = time.time()
                        while GPIO.input(ECHO_PIN) == 1:
                            pass
                        echoStopTime = time.time()
                        pingTravelTime = echoStopTime - echoStartTime
                        dist_cm = (pingTravelTime * 34444) / 2
                        dist_inch = dist_cm * 0.3937008
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        writer.writerow([timestamp, pingTravelTime, dist_inch])
                        file.flush()
                        print(f"Ultrasonic - Timestamp: {timestamp}, PingTravelTime: {pingTravelTme},  Distance: {dist_inch:.1f} inches | {dist_cm:.1f} cm")
                        time.sleep(delayTime)
        except Exception as e:
            print(f"Error logging ultrasonic sensor: {e}")
            time.sleep(5)  # Wait before retrying

def log_gps():
    while True:
        try:
            with gps_lock:
                with open(gps_file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    while True:
                        gps.update()
                        if gps.has_fix:
                            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            latitude = gps.latitude
                            longitude = gps.longitude
                            writer.writerow([current_time, latitude, longitude])
                            file.flush()
                            print(f"GPS - Time: {current_time}, Lat: {latitude}, Long: {longitude}")
                        else:
                            print("Waiting for GPS fix...")
                        time.sleep(1)
        except Exception as e:
            print(f"Error logging GPS data: {e}")
            time.sleep(5)  # Wait before retrying

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
                        rows = list(reader)
                        if rows:
                            print(f"Last entry in {file_path}: {rows[-1]}")
            time.sleep(10)  # Read every 10 seconds
        except Exception as e:
            print(f"Error reading CSV files: {e}")
            time.sleep(5)  # Wait before retrying

# Initialize CSV files with headers if not already done
def initialize_files():
    with temperature_lock:
        if not os.path.exists(temperature_file_path):
            with open(temperature_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Temperature (C)'])

    with sensor_lock:
        if not os.path.exists(sensor_file_path):
            with open(sensor_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Accel X', 'Accel Y', 'Accel Z', 'Gyro X', 'Gyro Y', 'Gyro Z', 'Magnet X', 'Magnet Y', 'Magnet Z'])

    with pressure_lock:
        if not os.path.exists(pressure_file_path):
            with open(pressure_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Temperature (C)', 'Pressure (hPa)', 'Humidity (RH)'])

    with geiger_lock:
        if not os.path.exists(geiger_file_path):
            with open(geiger_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Time", "CPS", "uSv/h"])

    with ultrasonic_lock:
        if not os.path.exists(ultrasonic_file_path):
            with open(ultrasonic_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'PingTravelTime', 'Distance (inches)'])

    with gps_lock:
        if not os.path.exists(gps_file_path):
            with open(gps_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Latitude', 'Longitude'])

if __name__ == "__main__":
    initialize_files()

    # Create threads for logging temperature, sensor data, pressure, Geiger data, ultrasonic data, and GPS data
    temperature_thread = threading.Thread(target=log_temperature)
    sensors_thread = threading.Thread(target=log_sensors)
    pressure_thread = threading.Thread(target=log_pressure)
    geiger_thread = threading.Thread(target=log_geiger)
    ultrasonic_thread = threading.Thread(target=log_ultrasonic)
    gps_thread = threading.Thread(target=log_gps)
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
