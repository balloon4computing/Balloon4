import sys
import board
import busio
import adafruit_gps
import serial
# import numpy as np

LOG_FILE = 'gpslog.txt'
LOG_MODE = 'wb'

# uart = busio.UART(board.TX, board.RX, baudrate = 9600, timeout = 10)
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart,debug=False)
# gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
# gps.send_command(b"PMTK220,1000")

with open(LOG_FILE, LOG_MODE) as outfile:
    while True:
        gps.update()
        sentence = gps.readline()
        if not sentence:
            continue
        print(str(sentence,"ascii").strip())

        if not gps.has_fix:
            print('Waiting for fix...')
            continue

        #print("Latitude: {0:.6f} degrees".format(gps.latitude))
        #print("Longitude: {0:.6f} degrees".format(gps.longitude))

        outfile.write(sentence)
        outfile.flush()
