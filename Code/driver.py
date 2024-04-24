import time
import threading
from some_sensor_library import Sensor1, Sensor2  # Hypothetical sensor libraries

# Initialize sensors
sensor1 = Sensor1()
sensor2 = Sensor2()

def read_sensor1():
    while True:
        data1 = sensor1.read_data()
        print("Sensor 1 data:", data1)
        time.sleep(1)

def read_sensor2():
    while True:
        data2 = sensor2.read_data()
        print("Sensor 2 data:", data2)
        time.sleep(1)

# Create threads for each sensor reading
thread1 = threading.Thread(target=read_sensor1)
thread2 = threading.Thread(target=read_sensor2)

# Start the threads
thread1.start()
thread2.start()

# You can use join if you want to wait for the threads to finish (usually for scripts that have an end)
# thread1.join()
# thread2.join()
