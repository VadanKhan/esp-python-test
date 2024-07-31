from machine import ADC, Pin
import time
import uos

# Initialize ADC channels
adc1 = ADC(Pin(1))  # ADC1 on GPIO 1
adc2 = ADC(Pin(11))  # ADC2 on GPIO 11

# Function to read ADC values and save to CSV
def read_adc_and_save_to_csv(filename, duration, interval):
    end_time = time.ticks_add(time.ticks_ms(), int(duration * 1000))  # Calculate end time
    with open(filename, 'w') as file:
        file.write('Time (ms),ADC1,ADC2\n')  # Write CSV header
        while time.ticks_diff(end_time, time.ticks_ms()) > 0:
            adc1_value = adc1.read()
            adc2_value = adc2.read()
            current_time = time.ticks_ms()
            file.write(f'{current_time},{adc1_value},{adc2_value}\n')
            time.sleep_ms(interval)

# Main function to run the script
def main(filename, duration, interval):
    read_adc_and_save_to_csv(filename, duration, interval)

# Example usage: main('adc_data.csv', 10, 100) for 10 seconds with 100 ms interval
main('adc_data.csv', 10, 100)
