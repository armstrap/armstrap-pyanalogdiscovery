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
# host:~$ python3 ./bin/adinfo.py
# DWF Version: 3.16.3
# Number of Devices: 1
# -------------------------------------------------------------------------------
# Device 0 :
#   Name: 'Analog Discovery Pro 3450' SN:210018B04951
#   ID: Analog Discovery Pro 3X50 rev: 0x204
#   Configurations:
#   0. AnalogIn: 4 x 32768 	AnalogOut: 2 x 32768 	DigitalIn: 16 x 32768 	DigitalOut: 16 x 16384
#   1. AnalogIn: 4 x 65536 	AnalogOut: 2 x 4096 	DigitalIn: 16 x 8192 	DigitalOut: 16 x 1024



import dwf

print("DWF Version: " + dwf.GetVersion())

number_of_devices = dwf.EnumDevices()
print("Number of Devices: " + str(dwf.EnumDevices()))

for each_device_index in range(0, number_of_devices):

    device_name = dwf.EnumDeviceName(each_device_index)
    serialnum = dwf.EnumSN(each_device_index)
    device_type, device_revision = dwf.EnumDeviceType(each_device_index)

    print("-------------------------------------------------------------------------------")
    print("Device " + str(each_device_index) + " : ")
    print("\tName: \'" + str(device_name) + "' " + serialnum)
    print("\tID: " + str(device_type) + " rev: " + hex(device_revision))

    print("\tConfigurations:")

    config_count = dwf.EnumConfig(each_device_index)

    for each_config_index in range (0, config_count):
        config_str = "\t" + str(each_config_index)+"."

        config_str += " AnalogIn: " + str(dwf.EnumConfigInfo(each_config_index, dwf.ConfigInfo.ANALOG_IN_CHANNEL_COUNT))
        config_str += " x " + str(dwf.EnumConfigInfo(each_config_index, dwf.ConfigInfo.ANALOG_IN_BUFFER_SIZE))
        config_str += " \tAnalogOut: " + str(dwf.EnumConfigInfo(each_config_index, dwf.ConfigInfo.ANALOG_OUT_CHANNEL_COUNT))
        config_str += " x " + str(dwf.EnumConfigInfo(each_config_index, dwf.ConfigInfo.ANALOG_OUT_BUFFER_SIZE))
        config_str += " \tDigitalIn: " + str(dwf.EnumConfigInfo(each_config_index, dwf.ConfigInfo.DIGITAL_IN_CHANNEL_COUNT))
        config_str += " x " + str(dwf.EnumConfigInfo(each_config_index, dwf.ConfigInfo.DIGITAL_IN_BUFFER_SIZE))
        config_str += " \tDigitalOut: " + str(dwf.EnumConfigInfo(each_config_index, dwf.ConfigInfo.DIGITAL_OUT_CHANNEL_COUNT))
        config_str += " x " + str(dwf.EnumConfigInfo(each_config_index, dwf.ConfigInfo.DIGITAL_OUT_BUFFER_SIZE))

        print(config_str)