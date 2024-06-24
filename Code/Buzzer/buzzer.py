from rpi_hardware_pwm import HardwarePWM 
# pwm_channel = 0 for GPIO 12,
#             = 1 for GPIO 13
pwm = HardwarePWM(pwm_channel=0, hz=60, chip=0) 
pwm.start(100) # full duty cycle

# Affects distance between gaps
# i.e. volume, tone quality
# duty_cycle = 50% -> pulseWidth = (period / 2)
pwm.change_duty_cycle(50)

# Affects actual pitch
pwm.change_frequency(25000)

pwm.stop()
