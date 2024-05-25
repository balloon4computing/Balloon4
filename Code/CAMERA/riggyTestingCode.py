from CAMERA import CAMERA

"""Runs the capture loop until interrupted, in the specified mode, with dynamic settings.

        Parameters:
            mode (str): The type of capture ('timelapse' or 'video').
            width (int): The width of the image or video in pixels (defaults to preset width).
            height (int): The height of the image or video in pixels (defaults to preset height).
            duration (int): The duration for which to capture video or images in milliseconds.
            interval (int): The interval between shots in milliseconds (only for 'timelapse').
            fps (int): The frames per second for video or compiled timelapse video.
            loop (bool): Whether to continue running the captures in a loop.
            sleep_time (int): The time to wait between each capture session in seconds.
"""

# Example usage:
camera = CAMERA()  # Create a camera controller instance with defaults

# Reference Usage
# camera.run(mode='video', width=1920, height=1080, duration=10000, interval = 1000, fps=24, loop=True, sleep_time=10)

# Timelapse  3840 x 2160 1 fps 
# NOTE: (there shouldnt be a frame rate since we are taking photos, I'm assuming just one photo per second interval = 1000)
# camera.run(mode='timelapse', width=3840, height=2160, duration=2000, interval = 1000, loop=False)

# Timelapse 2560 x 1440 1 fps
# Note: (Same reasoning as above where 1 fps is not possible)
# camera.run(mode='timelapse', width=2560, height=1440, duration=2000, interval=1000, loop=False)

# Video 2560 x 1440, 24 fps
# NOTE: (Might be this resolution... But it fails)
# camera.run(mode='video', width=2560, height=1440, duration=10000, fps=24, loop=False)

# Video 1920 x 1080p, 24 fps

# Change Amount of loops
# count = 0
# cycles = 2

# time in minutes
minutes = 0.5

milliseconds = int(minutes * 60000)

# while(count < cycles):
    # count = count + 1
camera.run(mode='video', width=1920, height=1080, duration=milliseconds, fps=24, loop=True)


