
from MCP9808 import MCP9808


tempSensor = MCP9808()

while(True):

    print(tempSensor.average_temp())


