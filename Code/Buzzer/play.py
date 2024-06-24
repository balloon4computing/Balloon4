from rpi_hardware_pwm import HardwarePWM
import time

# Function to play a note
def play_note(pwm, frequency, duration):
    pwm.change_frequency(frequency)
    pwm.start(50)  # Duty cycle of 50%
    time.sleep(duration)
    pwm.stop()

# Function to play the melody
def play_melody(pwm, melody):
    for note in melody:
        frequency, duration = note
        play_note(pwm, frequency, duration)

# Initialize PWM for GPIO 12
pwm_channel = 0  # GPIO 12
pwm = HardwarePWM(pwm_channel=pwm_channel, hz=60, chip=0)

# Play the melody
melody = [
    (261.63, 0.5),  # C4
    (293.66, 0.5),  # D4
    (329.63, 0.5),  # E4
    (349.23, 0.5),  # F4
    (392.00, 0.5),  # G4
    (440.00, 0.5),  # A4
    (493.88, 0.5),  # B4
    (523.25, 0.5)   # C5
]

play_melody(pwm, melody)

# Clean up PWM
pwm.stop()
