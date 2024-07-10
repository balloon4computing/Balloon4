import RPi.GPIO as GPIO
import time
import csv

# Set up variables
tubeCounts = 0
currentTime = 0
setTime = 0
countPerMinute = 0
usvh_ratio = 0.00332  # This is for the J305 tube

# Pin configuration
GEIGER_PIN = 17  # Assuming you're using GPIO4 for the Geiger counter; adjust as necessary

# Function to increment tubeCounts when a pulse (falling edge) is detected
def impulse(channel):
    global tubeCounts
    tubeCounts += 1
    print("Pulse detected. Tube counts: ", tubeCounts)

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setup(GEIGER_PIN, GPIO.IN)

# Add event detect for the Geiger counter pin
GPIO.add_event_detect(GEIGER_PIN, GPIO.FALLING, callback=impulse)

if __name__ == '__main__':

      tubeCounts = 0
      currentTime = 0
      with open("/home/jumiknows/Balloon4/Code/GEIGER/geiger_log_sec.csv", "a+", newline='') as log_file:
          writer = csv.writer(log_file)
          writer.writerow(["Time", "CPM", "uSv/h"])
          while True:
              startTime = time.time()  # Record start time
              while time.time() - startTime <= 1:  # Run loop for 60 seconds
                  pass  # Wait for impulses to be counted in the background
              currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
              cpm = tubeCounts
              usvh = tubeCounts * usvh_ratio
              print(f"Time: {currentTime}, cpm: {cpm}, uSv/h: {usvh}")
              writer.writerow([currentTime, cpm, usvh])
              log_file.flush()
              tubeCounts = 0  # Reset tubeCounts for the next minute
