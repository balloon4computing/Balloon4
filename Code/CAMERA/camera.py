import subprocess
import time
import os

def capture_timelapse():
    # Define the command components
    command = [
        "libcamera-still",
        # "-t", "5000",            # Run for 5 seconds
        "--datetime",            # Save files with the datetime as the filename
        "-n",                    # No preview
        "--timelapse", "1000"    # Capture every 1 second
    ]

    # Run the command
    subprocess.run(command)
    print("Timelapse capture completed.")


def capture_video():
    # Define the filename with a timestamp to avoid overwriting previous files
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"video-{timestamp}.h264"

    # Define the command components
    command = [
        "libcamera-vid",
        "-t", "10000",       # Record video for 10000 milliseconds (10 seconds)
        "-o", filename       # Output file name with timestamp
    ]

    # Run the command
    subprocess.run(command)
    print(f"Video capture completed. Saved as {filename}")

try:
    while True:
        # capture_timelapse()
        capture_video()
        # Optional: Adjust the sleep time to change the delay between each 5 second capture session
        time.sleep(15)  # Rest for 15 seconds before starting the next session
except KeyboardInterrupt:
    print("Stopped by User")

