#! /usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2021 Charles Armstrap <charles@armstrap.org>
# If you like this library, consider donating to: https://bit.ly/armstrap-opensource-dev
# Anything helps.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from pyanalogdiscovery import PyAnalogDiscovery, PyAnalogDiscoveryException, AnalogDiscoveryProConfiguration, I2cClockRate, Pins
from dwf import DwfApiException

analogdiscovery = None

# This examples demonstrates how to master an I2C bus using the digital lines.
# This example was tested with an Digilent Analog Discovery 2 and a Digilent
# Analog Discovery Pro 3450

try:
    # Hardware: BOSCH Digital, triaxial acceleration sensor
    # Company: Bosch Sensortec
    # Part Number: BMA456

    # For I2C wiring:
    # SCL (Serial Clock) output maps to Digital I/O Pin 0 on AnalogDiscovery device
    # SDA (Serial Data) input/output maps to Digital I/O Pin 1 on AnalogDiscovery device
    #
    # For this to work, you need to pullup the SCL and SDA lines to VCC by manually
    # adding a 10K resistor from SCL to VCC and adding another 10K resistor from SDA to
    # VCC.
    #
    # The default I2C address of the device is 0b0011000 (0x18). It is used if the SDO
    # pin is pulled to GND.  The alternative address 0b0011001 (0x19) is selected by
    # pulling the SDO pin to  ́VCCIO.
    #
    # Breakout Board: BMA456 Shuttle Board
    # Pin 1: VCC   --> 3.3V
    # Pin 2: VCCIO --> 3.3V
    # Pin 3: GND   --> GND flywire cable for Analog Discovery
    # Pin 4: SDO   --> GND to select I2C Address 0x18
    # Pin 5: SDI   --> DIO1 on flywire cable for Analog Discovery, 10K Pull resistor to VCC
    # Pin 6: SCK   --> DIO0 on flywire cable for Analog Discovery, 10K Pull resistor to VCC

    scl = Pins.DIO_0
    sda = Pins.DIO_1

    # Channel Configuration
    clock_rate = I2cClockRate.ONE_HUNDRED_KHZ # 100kHz

    # You can find the i2c address by looking at the datasheet for your attached chip.
    address = 0x18

    # Data
    # Read operation on CHIP_ID register (0x0) on attached I2C BMA456 device
    # According to the datasheet, we expect to read back the fixed CHIP_ID value of 0x16
    data_to_write = [ 0x0 ]
    data_read_size = len(data_to_write)

    analogdiscovery = PyAnalogDiscovery(AnalogDiscoveryProConfiguration.SCOPE_32K_WAVEGEN_32K_LOGIC_32K_PATTERNS_16K)
    i2c = analogdiscovery.acquire_inter_integrated_circuit()

    i2c.configure_bus(clock_rate, address, scl, sda)

    # Write and read from the bus
    data_read = i2c.write_read2(data_to_write, data_read_size)

    print("Received %d bytes:" % len(data_read))
    for i in range(len(data_read)):
        print("[%d] = %d (0x%02x)" % (i, data_read[i], data_read[i]))

except PyAnalogDiscoveryException as e:
    print("Error/Warning %d occurred\n%s" % (e.status, e))
except DwfApiException as e:
    print("Error/Warning %d occurred\n%s" % (e.status, e))
finally:
    if (analogdiscovery != None):
        analogdiscovery.release()

# Console Output
# -----------------------
# Received 1 bytes:
# [0] = 22 (0x16)
