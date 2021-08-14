# Armstrap pyAnalogDiscovery
Python wrappers and tools to control Digilent Analog Discovery devices.  These wrappers call into the official c-driver, allowing you to control Analog Discover devices from a Python application.

THIS IS NOT A COMPLETE API.  IT IS A WORK IN PROGRESS.

![AnalogDiscoveryPro](https://github.com/armstrap/armstrap-pyanalogdiscovery/raw/main/images/digilent-analog-discovery-pro.png)
![AnalogDiscovery2](https://github.com/armstrap/armstrap-pyanalogdiscovery/raw/main/images/digilent-analog-discovery-2.png)
![Python](https://github.com/armstrap/armstrap-pyanalogdiscovery/raw/main/images/python-logo-and-wordmark.png)

# What are Digilent Analog Discovery Devices?

Digilent Analog Discovery devices are companion devices that engineers use to troubleshoot hardware.  They are a USB oscilloscope, logic analyzer, and multi-function instrument that allows users to measure, visualize, generate, record, and control mixed-signal circuits of all kinds. Developed in conjunction with Analog Devices and supported by Xilinx University Program. This test and measurement device is small enough to fit in your pocket, but powerful enough to replace a stack of lab equipment, providing engineering professionals, students, hobbyists, and electronic enthusiasts the freedom to work with analog and digital circuits in virtually any environment, in or out of the lab. The analog and digital inputs and outputs can be connected to a circuit using simple wire probes; alternatively, the Analog Discovery BNC Adapter and BNC probes can be used to connect and utilize the inputs and outputs.

More information can be found on [digilent.com](https://store.digilentinc.com).

## Requirements
* [Digilent Analog Discover Pro hardware](https://store.digilentinc.com/analog-discovery-pro-3000-series-portable-high-resolution-mixed-signal-oscilloscopes/)
* [Digilent Analog Discover 2 hardware](https://store.digilentinc.com/analog-discovery-2-100msps-usb-oscilloscope-logic-analyzer-and-variable-power-supply/)
* [Latest Digilent Waveforms software](https://reference.digilentinc.com/reference/software/waveforms/waveforms-3/previous-versions)
* [Python >= 3.4](https://www.python.org/downloads/)

## Quickstart Guide

Run the following on a Command Line terminal

### Mac/Linux
```
git clone https://github.com/armstrap/armstrap-pyanalogdiscovery.git
cd armstrap-pyanalogdiscovery
export PYTHONPATH=lib
python3 examples/i2c_example.py
```

### Windows
```
git clone https://github.com/armstrap/armstrap-pyanalogdiscovery.git
cd armstrap-pyanalogdiscovery
set PYTHONPATH=lib
python3 examples\i2c_example.py
```
