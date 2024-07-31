from machine import DAC, Pin
import time

# Initialize DAC channels
dac1 = DAC(Pin(17))  # DAC1 on GPIO 17
dac2 = DAC(Pin(18))  # DAC2 on GPIO 18

# Variables to keep track of the DAC state
dac1_state = 0
dac2_state = 0

DISCOVERED_COMPUTING_DELAY_US = 50 # Vdiscovered 50us delay

# Function to generate a square wave using time module
def generate_square_wave(dac, frequency, duration, dac_state):
    period = (1 / frequency)*1_000_000 - DISCOVERED_COMPUTING_DELAY_US
    if period < 0:
        print("Freq too high!")
        return
    half_period_us = int(period / 2)  # Convert half period to microseconds
    end_time = time.ticks_add(time.ticks_us(), int(duration * 1_000_000))  # Calculate end time

    while time.ticks_diff(end_time, time.ticks_us()) > 0:
        dac_state = 255 if dac_state == 0 else 0
        dac.write(dac_state)
        time.sleep_us(half_period_us)

# Main function to run the script with a specified frequency and duration
def main(frequency, duration):
    global dac1_state, dac2_state
    generate_square_wave(dac1, frequency, duration, dac1_state)
    generate_square_wave(dac2, frequency, duration, dac2_state)

# Example usage: main(10000, 10) for 10 kHz
