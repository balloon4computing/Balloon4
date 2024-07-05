import time
import board
import busio
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER
from adafruit_bno08x import BNO_REPORT_GYROSCOPE
from adafruit_bno08x import BNO_REPORT_MAGNETOMETER
import csv

i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_GYROSCOPE)
bno.enable_feature(BNO_REPORT_MAGNETOMETER)


# Open a CSV file in write mode
with open('/home/jumiknows/Balloon4/Code/BN0085/sensor_readings.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['Timestamp', 'Accel X', 'Accel Y', 'Accel Z', 'Gyro X', 'Gyro Y', 'Gyro Z', 'Magnet X', 'Magnet Y', 'Magnet Z'])

    while True:
        
        # Get current timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        accel_x, accel_y, accel_z = bno.acceleration  # pylint:disable=no-member
        gyro_x, gyro_y, gyro_z = bno.gyro
        magnet_x,magnet_y,magnet_z = bno.magnetic

        print("X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (accel_x, accel_y, accel_z))
        print("X: %0.6f  Y: %0.6f Z: %0.6f  rad/s" % (gyro_x, gyro_y, gyro_z))
        print("X: %0.6f  Y: %0.6f Z: %0.6f  uT" % (magnet_x, magnet_y, magnet_z))
        
        # Write data to CSV file
        writer.writerow([timestamp, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, magnet_x, magnet_y, magnet_z])
        file.flush()
        
        # Wait for 1 second before taking the next reading
        time.sleep(1)
