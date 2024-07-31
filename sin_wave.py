from machine import DAC, Pin
import time
import math

# Initialize DAC channels
dac1 = DAC(Pin(17))  # DAC1 on GPIO 17
dac2 = DAC(Pin(18))  # DAC2 on GPIO 18

# Function to generate a sinusoidal wave
def generate_sine_wave(dac, frequency, duration, sample_rate=10000):
    # Number of samples per second
    num_samples = sample_rate // frequency  # Number of samples per cycle
    amplitude = 127  # Amplitude of the sine wave (0-255 for 8-bit DAC)
    offset = 128  # Offset to center the wave around 128 (midpoint of 0-255)
    period_us = int(1_000_000 / sample_rate)  # Period in microseconds

    end_time = time.ticks_add(time.ticks_us(), int(duration * 1_000_000))  # Calculate end time

    while time.ticks_diff(end_time, time.ticks_us()) > 0:
        for i in range(num_samples):
            angle = 2 * math.pi * i / num_samples
            value = int(amplitude * math.sin(angle) + offset)
            dac.write(value)
            time.sleep_us(period_us)

# Main function to run the script with a specified frequency and duration
def main(frequency, duration, samplerate=10000):
    generate_sine_wave(dac1, frequency, duration, samplerate)
    # generate_sine_wave(dac2, frequency, duration, samplerate)

# Example usage: main(100, 10) for 100 Hz sine wave for 10 seconds