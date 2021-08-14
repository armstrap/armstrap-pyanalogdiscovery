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

from ctypes import create_string_buffer, c_double, c_uint8, c_int, cdll, byref
from enum import IntEnum
import sys
import dwf
from typing import List

class Pins(IntEnum):
    DIO_0 = 0
    DIO_1 = 1
    DIO_2 = 2
    DIO_3 = 3
    DIO_4 = 4
    DIO_5 = 5
    DIO_6 = 6
    DIO_7 = 7
    DIO_8 = 8
    DIO_9 = 9
    DIO_10 = 10
    DIO_11 = 11
    DIO_12 = 12
    DIO_13 = 13
    DIO_14 = 14
    DIO_15 = 15
    def __str__(self):
        return self.name.replace("_", " ").title()

class AnalogIoChannel(IntEnum):
    POSITIVE_SUPPLY = 0
    NEGATIVE_SUPPLY = 1
    def __str__(self):
        return self.name.replace("_", " ").title()

class AnalogIoProperty(IntEnum):
    ENABLE = 0
    VOLTAGE = 1
    CURRENT = 2
    def __str__(self):
        return self.name.replace("_", " ").title()

class I2cClockRate(IntEnum):
    ONE_HUNDRED_KHZ = 100000
    FOUR_HUNDRED_KHZ = 400000
    ONE_MHZ = 1000000
    def __str__(self):
        return self.name.replace("_", " ").title()

class ClockPhase(IntEnum):
    FIRST_EDGE = 0
    SECOND_EDGE = 1
    def __str__(self):
        return self.name.replace("_", " ").title()

class Polarity(IntEnum):
    IDLE_LOW = 0
    IDLE_HIGH = 1
    def __str__(self):
        return self.name.replace("_", " ").title()

class Status(IntEnum):
    SUCCESS = 0
    ERROR_FAILED_TO_OPEN_DEVICE = -1
    ERROR_I2C_BUS_ERROR_CHECK_THE_PULLUPS = -2
    def __str__(self):
        return self.name.replace("_", " ").title()

class PyAnalogDiscoveryException(dwf.DwfApiException):
    def __init__(self, status):
        self.status = status

    def __str__(self):
        error_message = dwf.GetLastErrorMsg()
        if (len(error_message) == 0):
            return str(self.status)
        else:
            return str(self.status) + "\n" + error_message

class AnalogDiscovery2Configuration(IntEnum):
    SCOPE_8K_WAVEGEN_4K_LOGIC_4K_PATTERNS_1K = 0
    SCOPE_16K_WAVEGEN_1K_LOGIC_1K_PATTERNS_NONE = 1
    SCOPE_2K_WAVEGEN_16K_LOGIC_NONE_PATTERNS_NONE = 2
    SCOPE_512_WAVEGEN_256_LOGIC_16K_PATTERNS_16K = 3
    SCOPE_8K_WAVEGEN_4K_LOGIC_4K_PATTERNS_1K_1V8 = 4
    SCOPE_8K_WAVEGEN_4K_LOGIC_2K_PATTERNS_256_POWER = 5
    SCOPE_512_WAVEGEN_256_LOGIC_16K_PATTERNS_16K_1V8 = 6
    def __str__(self):
        return self.name.replace("_", " ").title()

class AnalogDiscoveryProConfiguration(IntEnum):
    SCOPE_32K_WAVEGEN_32K_LOGIC_32K_PATTERNS_16K = 0
    SCOPE_64K_WAVEGEN_4K_LOGIC_8K_PATTERNS_1K = 1
    def __str__(self):
        return self.name.replace("_", " ").title()

class PyAnalogDiscovery:
    '''Analog Discovery is a series of hardware devices sold by Digilent which
       integrates a mixed-signal oscilloscope, function generator, digital
       multimeter, programmable DC power supply, and digital I/O into a single
       form-factor device.  This class simply wraps that C-API, allowing us
       to control the device from python.
    '''
    def __init__(self, configuration, device_name: str = None):
        ''' Initialize the Analog Discovery library.  This must be called at least
            once for the application.
        '''
        self.device_name = device_name
        self.configuration = configuration
        self.serial_num = ''
        self.device_index = -1
        self.device_config_index = -1
        self.hdwf = dwf.hdwfNone
        self.user_name = ''

        filter = dwf.EnumFilter.ALL
        if (type(configuration) == AnalogDiscovery2Configuration):
            filter = dwf.EnumFilter.ANALOG_DISCOVERY2
            if (self.device_name == None):
                self.device_name = "Discovery2"
        elif (type(configuration) == AnalogDiscoveryProConfiguration):
            filter = dwf.EnumFilter.ANALOG_DISCOVERY_PRO_3X50
            if (self.device_name == None):
                self.device_name = "ADP3450"

        device_count = dwf.EnumDevices(filter)

        for each_device_index in range(device_count):
            if (self.device_name == dwf.EnumUserName(each_device_index)):
                self.device_index = each_device_index
                break

        if (self.device_index < 0):
            raise PyAnalogDiscoveryException(Status.ERROR_FAILED_TO_OPEN_DEVICE)

        self.device_name = dwf.EnumDeviceName(self.device_index)
        self.serial_num = dwf.EnumSN(self.device_index)

        self.hdwf = dwf.DeviceConfigOpen(self.device_index, self.configuration)

        if (self.hdwf == dwf.hdwfNone):
            raise PyAnalogDiscoveryException(Status.ERROR_FAILED_TO_OPEN_DEVICE)


    def release(self):
        ''' Finalize the AnalogDiscovery library.
        '''
        dwf.DeviceClose(self.hdwf)
        self.dwf = None
        self.hdwf = None

# #------------------------------------------------------------------------------

    def acquire_inter_integrated_circuit(self, reset: bool = True):
        ''' Creates and returns a new I2C session for the device. The session
            is used in all subsequent I2C method calls. This method should be
            called once per session.

            You can use AnalogDiscovery to master an I2C (Inter-Integrated Circuit)
            bus. When you configure an I2C bus, a set of lines are reserved for
            the bus and each line's direction is automatically configured.
        '''
        return self.InterIntegratedCircuit(self, reset)

    class InterIntegratedCircuit(object):
        def __init__(self, outer, reset):
            self.hdwf = outer.hdwf
            self.address = 0
            if (reset == True):
                dwf.DigitalI2cReset(self.hdwf)

        def configure_bus(self, i2c_clock_rate, address, scl_pin: int, sda_pin: int, clock_stretching_enabled: bool = True) -> None:
            ''' Configures the basic parameters of the I2C engine.
            '''
            is_bus_available = c_int()
            self.address = address
            dwf.DigitalI2cRateSet(self.hdwf, i2c_clock_rate)
            dwf.DigitalI2cSclSet(self.hdwf, scl_pin)
            dwf.DigitalI2cSdaSet(self.hdwf, sda_pin)
            if (clock_stretching_enabled == True):
                dwf.DigitalI2cStretchSet(self.hdwf, True)
            else:
                dwf.DigitalI2cStretchSet(self.hdwf, False)
            is_bus_available = dwf.DigitalI2cClear(self.hdwf)
            if (is_bus_available == 0):
                raise PyAnalogDiscoveryException(Status.ERROR_I2C_BUS_ERROR_CHECK_THE_PULLUPS)

        def read(self, read_data_size: int) -> (List[int], int):
            ''' Performs a read on an I2C slave device.
            '''
            read_data_out, is_nak = dwf.DigitalI2cRead(self.hdwf, self.address, read_data_size)
            return read_data_out, is_nak

        def write(self, write_data: List[int]) -> int:
            ''' Performs a write on an I2C slave device.
            '''
            is_nak = dwf.DigitalI2cWrite(self.hdwf, self.address, write_data)
            return is_nak

        def write_read(self, write_data: List[int], read_data_size: int) -> (List[int], int):
            ''' Performs a write followed by read (combined format) on an I2C
                slave device.
            '''
            read_data_out, is_nak = dwf.DigitalI2cWriteRead(self.hdwf, self.address, write_data, read_data_size)
            return read_data_out, is_nak

        def reset_instrument(self) -> None:
            ''' Resets the session configuration to default values, and resets
                the device and driver software to a known state.
            '''
            dwf.DigitalI2cReset(self.hdwf)

