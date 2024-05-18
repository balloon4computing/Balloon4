import RPi.GPIO as GPIO
import time

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
    # print("Pulse detected. Tube counts: ", tubeCounts)

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setup(GEIGER_PIN, GPIO.IN)

# Add event detect for the Geiger counter pin
GPIO.add_event_detect(GEIGER_PIN, GPIO.FALLING, callback=impulse)

# Setup code equivalent
def setup():
    global tubeCounts, currentTime
    print("Commencing Tests")
    tubeCounts = 0
    currentTime = 0

# Loop code equivalent
def loop(log_file):
    global currentTime, tubeCounts
    startTime = time.time()  # Record start time
    while time.time() - startTime <= 60:  # Run loop for 60 seconds
        pass  # Wait for impulses to be counted in the background
    currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    cpm = tubeCounts
    usvh = tubeCounts * usvh_ratio
    print(f"Time: {currentTime}, cpm: {cpm}, uSv/h: {usvh}")
    log_file.write(f"{currentTime}, {cpm}, {usvh}\n")
    tubeCounts = 0  # Reset tubeCounts for the next minute

if __name__ == '__main__':
    try:
        setup()
        with open("geiger_log.csv", "a") as log_file:
            log_file.write("Time, CPM, uSv/h\n")
            while True:
                loop(log_file)
    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        GPIO.cleanup()  # Clean up GPIO to ensure no pins are left high
