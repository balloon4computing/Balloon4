
import adafruit_mcp9808
import board
import time

class MCP9808:
    def __init__(self):
        self.i2c = board.I2C()
        self.mcp = adafruit_mcp9808.MCP9808(self.i2c)
        self.tempReadings = []

    # Returns average temperature over a second (in Celsius)
    def average_temp(self):
        self.tempReadings.clear()

        for counter in range(0, 9):
            self.tempReadings.append(self.mcp.temperature)
            time.sleep(0.1)
        return "{:.2f}".format(sum(self.tempReadings) / 9)

    def instantaneous_temp(self):
        return "{:.2f}".format(self.mcp.temperature)
