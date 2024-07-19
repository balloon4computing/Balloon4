import subprocess
import time

class CAMERA:
    def __init__(self):
        # Initialize default settings for the camera
        self.default_width = 3840   # Default width of the image or video
        self.default_height = 2160  # Default height of the image or video
        self.default_fps = 30       # Default frames per second for video or timelapse playback

    def capture_timelapse(self, width, height, duration, interval, fps):
        """Captures a timelapse sequence with specified settings.
        
        Parameters:
            width (int): The width of the image in pixels.
            height (int): The height of the image in pixels.
            duration (int): The total duration of the timelapse capture in milliseconds.
            interval (int): The time interval between each image capture in milliseconds.
            fps (int): The frame rate at which the timelapse video should be played back.
        """
        command = [
            "libcamera-still",
            "--width", str(width),
            "--height", str(height),
            "--framerate", str(fps),
            "-t", str(duration),
            "--datetime",
            "-n",
            "--timelapse", str(interval)
        ]

        subprocess.run(command)
        print("Timelapse capture completed.")

    def capture_video(self, width, height, duration, fps):
        """Records a video with specified settings.
        
        Parameters:
            width (int): The width of the video in pixels.
            height (int): The height of the video in pixels.
            duration (int): The length of the video recording in milliseconds.
            fps (int): The frames per second rate of the video recording.
        """
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"/home/jumiknows/Balloon4/Code/CAMERA/video-{timestamp}.h264"

        command = [
            "libcamera-vid",
            "--width", str(width),
            "--height", str(height),
            "--framerate", str(fps),
            "-t", str(duration),
            "-o", filename
        ]

        subprocess.run(command)
        print(f"Video capture completed. Saved as {filename}")

    def run(self, mode='timelapse', width=None, height=None, duration=5000, interval=1000, fps=None, loop=True, sleep_time=20):
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
        # Use default values if specific settings are not provided
        width = width if width is not None else self.default_width
        height = height if height is not None else self.default_height
        fps = fps if fps is not None else self.default_fps
        count = 0
        cycle = 12

        try:
            while True:
                if count > cycle:
                    break
                if mode == 'timelapse':
                    self.capture_timelapse(width, height, duration, interval, fps)
                elif mode == 'video':
                    self.capture_video(width, height, duration, fps)
                    count = count + 1
                if not loop:
                    break
                time.sleep(sleep_time)  # Rest before starting the next session
        except KeyboardInterrupt:
            print("Stopped by User")
