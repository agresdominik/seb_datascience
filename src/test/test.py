import smbus2
import time
import os
import math

# Get I2C bus
bus = smbus2.SMBus(1)

def adc_to_ppm(adc_value):
    # Constants (These values should be adjusted based on your calibration data)
    V_in = 5.0  # Supply voltage (5V)
    R_load = 10_000  # Load resistor value in ohms (10kΩ typical)
    ADC_max = 65535  # Maximum ADC value (10-bit ADC)

    # Calibration constants (These should be replaced with your own experimental values or from the datasheet)
    a = 0.1  # Example constant a (need to adjust based on calibration data)
    b = 2.2  # Example constant b (need to adjust based on calibration data)

    # Step 1: Calculate the output voltage from the ADC value
    V_out = (adc_value / ADC_max) * V_in

    # Step 2: Calculate Rs (sensor resistance)
    Rs = (V_out / V_in) * R_load

    # Step 3: Assuming Ro (resistance in clean air) is pre-measured or taken from the datasheet
    Ro = 10000  # Example Ro value (adjust as needed for clean air measurement)

    rs_ro = (Rs/Ro)
    smoke_curve = [2.301,0.544,-0.497]
    PPM = pow(10,(((math.log(rs_ro) - smoke_curve[1]) / smoke_curve[2]) + smoke_curve[0]));

    # Step 4: Calculate PPM using the formula (based on the calibration curve)
    #PPM = a * (Rs / Ro) ** b

    print(f"Calculated PPM: {PPM}")


while True:
    
    # ADS1115 address, 0x48(72)
    # Select configuration register, 0x01(01)
    #		0x8483(33923)	AINP = AIN0 and AINN = AIN1, +/- 2.048V
    #				Continuous conversion mode, 128SPS
    data = [0x84,0x83]
    bus.write_i2c_block_data(0x48, 0x01, data)

    time.sleep(0.5)

    # ADS1115 address, 0x48(72)
    # Read data back from 0x00(00), 2 bytes
    # raw_adc MSB, raw_adc LSB
    data = bus.read_i2c_block_data(0x48, 0x00, 2)

    # Convert the data
    raw_adc = data[0] * 256 + data[1]

    #if raw_adc > 32767:
    #    raw_adc -= 65535

    # Output data to screen
    print ("Digital Value of Analog Input : %d" %raw_adc)
    adc_to_ppm(raw_adc)
    time.sleep(10)


