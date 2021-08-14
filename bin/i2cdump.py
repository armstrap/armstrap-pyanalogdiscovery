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

# Sample Output
# host:~$ python3 ./bin/i2cdump.py 0x18
#      0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
# 00: 16 23 00 10 00 00 00 00 00 00 00 00 00 00 00 00
# 10: 00 00 00 00 00 00 00 00 36 00 00 01 00 00 00 00
# 20: 00 00 80 00 00 00 80 80 80 80 80 80 80 80 80 80
# 30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
# 40: a8 01 00 00 46 80 00 02 02 10 00 20 83 42 4c 02
# 50: 00 00 00 00 00 00 00 00 00 90 00 00 00 00 00 00
# 60: 00 00 00 00 00 00 00 00 03 00 00 00 00 00 00 00
# 70: 00 ff 2d 00 00 00 00 00 0c 00 00 00 00 00 00 00
# 80: 16 23 00 10 00 00 00 00 00 00 00 00 00 00 00 00
# 90: 00 00 00 00 00 00 00 00 36 00 00 00 00 00 00 00
# a0: 00 00 80 00 00 00 80 80 80 80 80 80 80 80 80 80
# b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
# c0: a8 01 00 00 46 80 00 02 02 10 00 20 83 42 4c 02
# d0: 00 00 00 00 00 00 00 00 00 90 00 00 00 00 00 00
# e0: 00 00 00 00 00 00 00 00 03 00 00 00 00 00 00 00
# f0: 00 ff 2d 00 00 00 00 00 00 00 00 00 03 00 00 00

from pyanalogdiscovery import PyAnalogDiscovery, PyAnalogDiscoveryException, AnalogDiscoveryProConfiguration, I2cClockRate, Pins
from dwf import DwfApiException
import argparse
import sys

def main(argv):

    analogdiscovery = None
    try:
        parser = argparse.ArgumentParser(description='i2cdetect is a userspace program to scan an I2C bus for devices using a Digilent Analog Discovery device. It outputs a table with the list of detected devices on the specified bus. The bus is specified via the scl and sda DIO lines of the Analog Discovery device.')
        parser.add_argument('--scl', default=0, help='The DIO pin to use as the I2C clock line (default 0 if not specified).')
        parser.add_argument('--sda', default=1, help='The DIO pin to use as the I2C data line (default 1 if not specified).')
        parser.add_argument('--clock-rate', default=100000, help='The I2C clock rate in Herz (default 100,000 Hz-- or 100 KHz--if not specified).')
        parser.add_argument('address', type=lambda x: int(x,0), help='The I2C address to be scanned, and is an integer/hex number between 0x03 and 0x77.')
        args = parser.parse_args()

        address = args.address
        scl = Pins(args.scl)
        sda = Pins(args.sda)
        clock_rate = I2cClockRate(args.clock_rate)

        analogdiscovery = PyAnalogDiscovery(AnalogDiscoveryProConfiguration.SCOPE_32K_WAVEGEN_32K_LOGIC_32K_PATTERNS_16K)
        i2c = analogdiscovery.acquire_inter_integrated_circuit()

        i2c.configure_bus(clock_rate, address, scl, sda)

        # Print Address Columnn Headers
        print("   ", end='')
        for least_significant_addr_byte in range(16):
            print("  %s" % hex(least_significant_addr_byte).replace("0x",""), end='')
        print()

        # Print Address Row Headers - with values
        for most_significant_addr_byte in range(16):
            register_addr = (most_significant_addr_byte << 4)
            print("%s:" % format(register_addr, '#04x').replace("0x",""), end='')

            data_read, is_nak = i2c.write_read(write_data = [register_addr], read_data_size = 16)

            data_read_str = ''
            for each_data in data_read:
                data_read_str += " %s" % format(each_data, '#04x').replace("0x","")

            print(data_read_str)

    except PyAnalogDiscoveryException as e:
        print("Error/Warning %d occurred\n%s" % (e.status, e))
    except DwfApiException as e:
        print("Error/Warning %d occurred\n%s" % (e.status, e))
    finally:
        if (analogdiscovery != None):
            analogdiscovery.release()

if __name__ == "__main__":
    main(sys.argv[1:])