from machine import ADC, Pin
import time
import uos

# Initialize ADC channels
adc1 = ADC(Pin(1))  # ADC1 on GPIO 1
adc2 = ADC(Pin(11))  # ADC2 on GPIO 11

# Set attenuation (example: 11 dB for a wider range)
adc1.atten(ADC.ATTN_11DB)
adc2.atten(ADC.ATTN_11DB)

# Reference voltage and ADC resolution
VREF = 2.5
ADC_RESOLUTION = 8191

# Function to read ADC values and save to CSV
def read_adc_and_save_to_csv(filename, duration, interval, buffer_size=100):
    start_time = time.ticks_us()  # Record the start time in microseconds
    end_time = time.ticks_add(start_time, int(duration * 1_000_000))  # Calculate end time in microseconds
    data = []  # Buffer to store data
    with open(filename, 'w') as file:
        file.write('Time (us),ADC1,ADC2\n')  # Write CSV header
        while time.ticks_diff(end_time, time.ticks_us()) > 0:
            t1 = time.ticks_us()
            adc1_value = adc1.read()
            adc2_value = adc2.read()
            t2 = time.ticks_us()
            adc1_voltage = (adc1_value / ADC_RESOLUTION) * VREF
            adc2_voltage = (adc2_value / ADC_RESOLUTION) * VREF
            t3 = time.ticks_us()
            current_time = time.ticks_diff(time.ticks_us(), start_time)  # Calculate elapsed time in microseconds
            data.append(f'{current_time},{adc1_voltage:.3f},{adc2_voltage:.3f}\n')
            t4 = time.ticks_us()
            if len(data) >= buffer_size:
                for line in data:
                    file.write(line)
                data = []  # Clear the buffer
            t5 = time.ticks_us()
            time.sleep_us(interval)  # Use interval in microseconds
            t6 = time.ticks_us()
            print(f"ADC Read: {t2 - t1} us, Voltage Conversion: {t3 - t2} us, Data Append: {t4 - t3} us, File Write: {t5 - t4} us, Sleep: {t6 - t5} us")
        if data:
            t7 = time.ticks_us()
            for line in data:
                file.write(line)  # Write any remaining data in the buffer
            t8 = time.ticks_us()
            print(f"Final Data Write: {t8 - t7} us")

# Main function to run the script
def main(filename, duration, interval, buffer_size=100):
    read_adc_and_save_to_csv(filename, duration, interval, buffer_size)

# Example usage: main('adc_data.csv', 10, 100, 100) for 10 seconds with 100 microseconds interval and buffer size of 100
