import csv
import serial
import time
import adafruit_gps

# Setup serial connection for GPS
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)  # Set debug=True to see detailed GPS data

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b'PMTK314,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1')

# Set update rate to once every second (1Hz)
gps.send_command(b'PMTK220,1000')

# Open a CSV file in write mode with the specified path
csv_file_path = '/home/jumiknows/Balloon4/Code/GPS/sensor_readings.csv'
with open(csv_file_path, mode='a+', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Latitude', 'Longitude'])  # Write header

    try:
        print("Writing GPS data to '{}'".format(csv_file_path))
        while True:
            gps.update()  # This needs to be called in your loop to keep the GPS module updated

            # Check if there's new GPS data available
            if gps.has_fix:
                # Print out details about the fix like location, date, etc.
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                latitude = gps.latitude
                longitude = gps.longitude
                print(f"Time: {current_time}, Lat: {latitude}, Long: {longitude}")
                writer.writerow([current_time, latitude, longitude])
                file.flush()  # Flush data to file immediately after writing
            else:
                print("Waiting for fix...")

            time.sleep(1)
    except KeyboardInterrupt:
        print("Logging stopped by user.")
    finally:
        print("File closed.")
