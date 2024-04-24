import bme680


class BME680:
    def __init__(self):

        # Initialize BME680 sensor
        self.sensor = bme680.BME680(0x77)
        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)

    def read_temperature(self):
        # Read temperature from the sensor
	#In celsius
        return self.sensor.data.temperature
    def read_humidity(self):
	# Read humidity from the sensor
	# In RH(realtive humidity)
        return self.sensor.data.humidity

    def read_pressure(self):
        # Read pressure from the sensor
        #in hpa(1hpa = 0.01pa)
        return self.sensor.data.pressure

    def read_gas(self):
        # Read gas resistance from the sensor
        return self.sensor.data.gas_resistance

