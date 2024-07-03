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

gps = adafruit_gps.GPS(uart)

with open(LOG_FILE, LOG_MODE) as outfile:
    while True:
        sentence = gps.readline()
        if not sentence:
            continue
        print(str(sentence,"ascii").strip())
        outfile.write(sentence)
        outfile.flush()