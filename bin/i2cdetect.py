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
# host:~$ python3 ./bin/i2cdetect.py
#      0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
# 00:          -- -- -- -- -- -- -- -- -- -- -- -- --
# 10: -- -- -- -- -- -- -- -- 18 -- -- -- -- -- -- --
# 20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 70: -- -- -- -- -- -- -- --

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
        args = parser.parse_args()

        scl = Pins(args.scl)
        sda = Pins(args.sda)
        clock_rate = I2cClockRate(args.clock_rate)

        analogdiscovery = PyAnalogDiscovery(AnalogDiscoveryProConfiguration.SCOPE_32K_WAVEGEN_32K_LOGIC_32K_PATTERNS_16K)
        i2c = analogdiscovery.acquire_inter_integrated_circuit()

        # Print Address Columnn Headers
        print("   ", end='')
        for lsb in range(16):
            print("  %s" % hex(lsb).replace("0x",""), end='')

        # Print Address Row Headers - with address if chip found
        for msb in range(8):
            print()
            print("%s:" % format((msb << 4), '#04x').replace("0x",""), end='')

            for lsb in range(16):
                address = ((msb << 4) | lsb)
                address_str = " %s" % format(address, '#04x').replace("0x","")

                if ((address >= 0 and address < 3) or address > 0x77):
                    address_str = "   "
                else:
                    is_nak = -1
                    try:
                        i2c.configure_bus(clock_rate, address, scl, sda)
                        data_read, is_nak = i2c.write_read(write_data = [ 0x0 ], read_data_size = 1)
                    except:
                        pass
                    if (is_nak != 0):
                        address_str = " --"
                print(address_str, end='')
        print()

    except PyAnalogDiscoveryException as e:
        print("Error/Warning %d occurred\n%s" % (e.status, e))
    except DwfApiException as e:
        print("Error/Warning %d occurred\n%s" % (e.status, e))
    finally:
        if (analogdiscovery != None):
            analogdiscovery.release()

if __name__ == "__main__":
    main(sys.argv[1:])
