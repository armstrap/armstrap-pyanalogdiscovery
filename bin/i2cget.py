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
# host:~$ python3 ./bin/i2cget.py 0x18 0x00
# 16

# host:~$ python3 ./bin/i2cget.py 0x18 0x00 16
# 16 23 00 10 00 00 00 00 00 00 00 00 00 00 00 00

from pyanalogdiscovery import PyAnalogDiscovery, PyAnalogDiscoveryException, AnalogDiscoveryProConfiguration, I2cClockRate, Pins
from dwf import DwfApiException
import argparse
import sys

def main(argv):

    analogdiscovery = None
    try:
        parser = argparse.ArgumentParser(description='i2cget is a small helper program to read registers visible through the I2C bus (or SMBus) using a Digilent Analog Discovery device. The bus is specified via the scl and sda DIO lines of the Analog Discovery device.')
        parser.add_argument('--scl', default=0, help='The DIO pin to use as the I2C clock line (default 0 if not specified).')
        parser.add_argument('--sda', default=1, help='The DIO pin to use as the I2C data line (default 1 if not specified).')
        parser.add_argument('--clock-rate', default=100000, help='The I2C clock rate in Herz (default 100,000 Hz (or 100 KHz) if not specified).')
        parser.add_argument('chip_address', metavar='chip-address', type=lambda x: int(x,0), help='Specified the I2C chip address to use, and is an integer between 0x03 and 0x77.')
        parser.add_argument('data_address', metavar='data-address', type=lambda x: int(x,0), help='Specifies the data (or register) address on that chip to read from, and is an integer between 0x00 and 0xFF.')
        parser.add_argument('read_amount', metavar='read-amount', default=1, type=int, nargs='?', help='Specifies the number of bytes to read (default 1 byte if not specified).')
        args = parser.parse_args()

        chip_address = args.chip_address
        data_address = args.data_address
        read_amount = args.read_amount
        scl = Pins(args.scl)
        sda = Pins(args.sda)
        clock_rate = I2cClockRate(args.clock_rate)

        analogdiscovery = PyAnalogDiscovery(AnalogDiscoveryProConfiguration.SCOPE_32K_WAVEGEN_32K_LOGIC_32K_PATTERNS_16K)
        i2c = analogdiscovery.acquire_inter_integrated_circuit()

        i2c.configure_bus(clock_rate, chip_address, scl, sda)

        data_read, is_nak = i2c.write_read(write_data = [data_address], read_data_size = read_amount)

        data_read_str = "%s" % format(data_read[0], '#04x').replace("0x","")

        # We start at index 1 because we already processed index 0 (above)
        for each_data in data_read[1:]:
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