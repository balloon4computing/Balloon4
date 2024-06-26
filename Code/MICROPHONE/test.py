import board
import adafruit_i2s
import adafruit_i2s_microphone

i2s = adafruit_i2s.Microphone(
    bit_depth=16,
    sample_rate=16000,
    pins=(board.D18, board.D19, board.D20)
)

samples = i2s.record(16000)
print(samples)
