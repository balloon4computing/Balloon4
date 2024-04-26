import csv
from datetime import datetime
import tkinter as tk
from MCP9808 import MCP9808
from threading import Thread

# Function to add a temperature reading with a timestamp to a CSV file
def add_temperature_to_csv(file_path, temperature):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([temperature, timestamp])
    print(f"Temperature '{temperature}°C' with timestamp {timestamp} added to {file_path}.")

# Function to update the GUI thermometer and temperature label
def update_temperature():
    while True:
        temp = tempSensor.average_temp()
        # Convert the temperature to a float if it's not already
        temp = float(temp)
        # Update the GUI elements
        temp_label.config(text=f"{temp}°C")
        update_thermometer(temp)
        add_temperature_to_csv(file_path, temp)
        root.update()
        root.after(1000)  # Update every second

def update_thermometer(temp):
    # Clear previous thermometer content
    canvas.delete("thermometer")
    # Adjustments for thermometer display
    height = 300  # Total height of the thermometer
    temp_min = -10  # Minimum temperature to display
    temp_max = 40   # Maximum temperature to display
    level = ((temp - temp_min) / (temp_max - temp_min)) * height
    # Draw the thermometer
    canvas.create_rectangle(40, 350 - height, 160, 350, fill='#F0F0F0', outline='black', width=1, tag="thermometer")
    canvas.create_rectangle(50, 350 - level, 150, 350, fill='#ff6347', tag="thermometer")
    # Add detailing for the mercury
    canvas.create_oval(50, 350 - level - 5, 150, 350 - level + 5, fill='#ff6347', outline='#ff6347', tag="thermometer")
    canvas.create_text(100, 370, text=f"{temp}°C", font=('Arial', 12, 'bold'), tag="thermometer")

# Create the main window
root = tk.Tk()
root.title("Temperature Monitor")
root.config(bg='white')

# Canvas for thermometer
canvas = tk.Canvas(root, width=200, height=400, bg='white')
canvas.pack(side=tk.LEFT, padx=20)

# Temperature display label
temp_label = tk.Label(root, font=("Arial", 30), pady=20, bg='white')
temp_label.pack(side=tk.RIGHT)

# MCP9808 sensor initialization
tempSensor = MCP9808()

# File path for the CSV
file_path = 'hello_timestamps.csv'

# Start the temperature update thread
thread = Thread(target=update_temperature)
thread.daemon = True
thread.start()

# Start the Tkinter event loop
root.mainloop()
