import time
import board
import busio
import adafruit_bme680
import csv

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize BME680 sensor
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# Open a CSV file in write mode
with open('/home/jumiknows/Balloon4/Code/BME680/sensor_readings.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['Timestamp', 'Temperature (C)', 'Pressure (hPa)', 'Humidity (RH)'])

    # Main loop to read and log sensor data
    while True:
        # Get current timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Read temperature and pressure
        temperature = sensor.temperature
        pressure = sensor.pressure
        humidity = sensor.humidity

        # Write data to CSV file
        writer.writerow([timestamp, temperature, pressure, humidity])
        file.flush()
        # Print the sensor readings
        print(f"Timestamp: {timestamp}")
        print(f"Temperature: {temperature:.2f} C")
        print(f"Pressure: {pressure:.2f} hPa")
        print(f"Humidity: {humidity:.2f} HV")

        # Wait for 1 second before taking the next reading
        time.sleep(1)
