
import BME680



sensor = BME680.BME680()

while(True):
    #print(sensor.read_altitude())
    print(sensor.read_temperature())
    print(sensor.read_pressure())
