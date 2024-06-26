import sys
import os

# Add the directory containing your module to sys.path
module_path = '/home/jumiknows/.local/lib/python3.9/site-packages'
if module_path not in sys.path:
    sys.path.append(module_path)

import board
import busio
import adafruit_mcp9808
import csv
import time

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create MCP9808 sensor object
mcp = adafruit_mcp9808.MCP9808(i2c)

# Open a CSV file in write mode
with open('/home/jumiknows/Balloon4/Code/MCP9808/temperature_readings.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['Timestamp', 'Temperature (C)'])
    
    # Loop to read temperature and write to CSV file
    while True:
        # Get current timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        file.flush()
        # Get temperature reading
        temperature = mcp.temperature
        
        # Write data to CSV file
        writer.writerow([timestamp, temperature])
        
        # Print temperature to console (optional)
        print(f"Timestamp: {timestamp}, Temperature: {temperature:.2f} C")
        
        # Wait for some time before taking the next reading (e.g., 1 second)
        time.sleep(1)
