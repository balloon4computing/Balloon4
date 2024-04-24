import RPi.GPIO as GPIO
import time

# Pin configuration
GEIGER_PIN = 4  # Assuming you're using GPIO4 for the Geiger counter; adjust as necessary

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setup(GEIGER_PIN, GPIO.IN)

# Setup code equivalent
def setup():
    global tubeCounts, currentTime
    print("Commencing...")
    tubeCounts = 0
    currentTime = 0

# Loop code equivalent
def loop():
    global currentTime, tubeCounts
    startTime = time.time()  # Record start time
    while time.time() - startTime <= 5:  # Run loop for 5 seconds
        if (GPIO.input(4) == True):  
            tubeCounts += 1 #Increments tubeCounts when a pulse is detected
        pass  # Wait for impulses to be counted in the background

    print("Time: " + str(time.time()) + " seconds")
    print("Counts: " + str(tubeCounts/(time.time()-startTime)) + " counts per second")  # After 5 seconds, print the tubeCounts
    tubeCounts = 0  # Reset tubeCounts for the next minute

if __name__ == '__main__':
    try:
        setup()
        while True:
            loop()
    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        GPIO.cleanup()  # Clean up GPIO to ensure no pins are left high
