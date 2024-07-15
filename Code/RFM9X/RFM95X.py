import time
import busio
import digitalio
from digitalio import DigitalInOut
import board
import adafruit_rfm9x

class RFM9X:
    def __init__(self, tx_power):
        try:
            self.spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
            self.RESET = digitalio.DigitalInOut(board.D24)
            self.CS = digitalio.DigitalInOut(board.D23)
            self.rfm9x = adafruit_rfm9x.RFM9x(self.spi, self.CS, self.RESET, frequency=915.0)
            self.rfm9x.tx_power = tx_power
            self.rfm9x.spreading_factor = 10
            self.rfm9x.signal_bandwidth = 125000
            self.rfm9x.enable_crc = True
            self.rfm9x.coding_rate = 8
        except Exception as e:
            self.rfm9x = None

    def send_data(self, data):
        if self.rfm9x is not None:
            try:
                self.rfm9x.send(data)
            except Exception as e:
                print("Error", e)
        else:
            print("RFM9x not initialized.")