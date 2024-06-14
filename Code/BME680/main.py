
import BME680



sensor = BME680.BME680()

while(True):
    #print(sensor.read_altitude())
    print("temp: ", sensor.read_temperature())
    print("pres: ", sensor.read_pressure())
    print("humi: ", sensor.read_humidity())
