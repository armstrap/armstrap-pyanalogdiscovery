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

import ctypes
import sys
import time
from enum import IntEnum
from typing import List

# device handle
# typedef int HDWF;

# const HDWF hdwfNone = 0;
hdwfNone = 0

# device enumeration filters
# typedef int ENUMFILTER;
class EnumFilter(IntEnum):
    ALL                       = 0
    ELECTRONICS_EXPLORER      = 1
    ANALOG_DISCOVERY          = 2
    ANALOG_DISCOVERY2         = 3
    DIGITAL_DISCOVERY         = 4
    ANALOG_DISCOVERY_PRO_3X50 = 6
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef int DEVID;
class Device(IntEnum):
    ELECTRONICS_EXPLORER      = 1
    ANALOG_DISCOVERY          = 2
    ANALOG_DISCOVERY2         = 3
    DIGITAL_DISCOVERY         = 4
    ANALOG_DISCOVERY_PRO_3X50 = 6
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef int DEVVER;
class DeviceVersion(IntEnum):
    ELECTRONICS_EXPLORER_C = 1
    ELECTRONICS_EXPLORER_E = 4
    ELECTRONICS_EXPLORER_F = 5
    DISCOVERY_A            = 1
    DISCOVERY_B            = 2
    DISCOVERY_C            = 3
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef unsigned char TRIGSRC;
class TriggerSource(IntEnum):
    NONE                = 0
    PC                  = 1
    DETECTOR_ANALOG_IN  = 2
    DETECTOR_DIGITAL_IN = 3
    ANALOG_IN           = 4
    DIGITAL_IN          = 5
    DIGITAL_OUT         = 6
    ANALOG_OUT1         = 7
    ANALOG_OUT2         = 8
    ANALOG_OUT3         = 9
    ANALOG_OUT4         = 10
    EXTERNAL1           = 11
    EXTERNAL2           = 12
    EXTERNAL3           = 13
    EXTERNAL4           = 14
    HIGH                = 15
    LOW                 = 16
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef unsigned char DwfState;
class InstrumentState(IntEnum):
    READY     = 0
    CONFIG    = 4
    PREFILL   = 5
    ARMED     = 1
    WAIT      = 7
    TRIGGERED = 3
    RUNNING   = 3
    DONE      = 2
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef int DwfEnumConfigInfo;
class ConfigInfo(IntEnum):
    ANALOG_IN_CHANNEL_COUNT   = 1
    ANALOG_OUT_CHANNEL_COUNT  = 2
    ANALOG_IO_CHANNEL_COUNT   = 3
    DIGITAL_IN_CHANNEL_COUNT  = 4
    DIGITAL_OUT_CHANNEL_COUNT = 5
    DIGITAL_IO_CHANNEL_COUNT  = 6
    ANALOG_IN_BUFFER_SIZE     = 7
    ANALOG_OUT_BUFFER_SIZE    = 8
    DIGITAL_IN_BUFFER_SIZE    = 9
    DIGITAL_OUT_BUFFER_SIZE   = 10
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef int ACQMODE;
class AcquisitionMode(IntEnum):
    SINGLE      = 0
    SCAN_SHIFT  = 1
    SCAN_SCREEN = 2
    RECORD      = 3
    OVERS       = 4
    SINGLE1     = 5
    def __str__(self):
        return self.name.replace("_", " ").title()

# analog acquisition filter:
# typedef int FILTER;
class Filter(IntEnum):
    DECIMATE = 0
    AVERAGE  = 1
    MINMAX   = 2
    def __str__(self):
        return self.name.replace("_", " ").title()

# analog in trigger mode:
# typedef int TRIGTYPE;
class TriggerType(IntEnum):
    EDGE       = 0
    PULSE      = 1
    TRANSITION = 2
    WINDOW     = 3
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef int DwfTriggerSlope;
class TriggerSlope(IntEnum):
    RISE   = 0
    FALL   = 1
    EITHER = 2
    def __str__(self):
        return self.name.replace("_", " ").title()

# trigger length condition
# typedef int TRIGLEN;
class TriggerLengthCondition(IntEnum):
    LESS    = 0
    TIMEOUT = 1
    MORE    = 2
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef int DWFERC;
class ErrorCodes(IntEnum):
    NO_ERC             = 0 # No error occurred
    UNKNOWN_ERROR      = 1 # API waiting on pending API timed out
    API_LOCK_TIMEOUT   = 2 # API waiting on pending API timed out
    ALREADY_OPENED     = 3 # Device already opened
    NOT_SUPPORTED      = 4 # Device not supported
    INVALID_PARAMETER0 = 5 # Parameter 0 was invalid in last API call.
    INVALID_PARAMETER1 = 6 # Parameter 1 was invalid in last API call.
    INVALID_PARAMETER2 = 7 # Parameter 2 was invalid in last API call.
    INVALID_PARAMETER3 = 8 # Parameter 3 was invalid in last API call.
    INVALID_PARAMETER4 = 9 # Parameter 4 was invalid in last API call.
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef unsigned char FUNC;
class Function(IntEnum):
    DC         = 0
    SINE       = 1
    SQUARE     = 2
    TRIANGLE   = 3
    RAMP_UP    = 4
    RAMP_DOWN  = 5
    NOISE      = 6
    PULSE      = 7
    TRAPEZIUM  = 8
    SINE_POWER = 9
    CUSTOM     = 30
    PLAY       = 31
    def __str__(self):
        return self.name.replace("_", " ").title()

# analog io channel node types
# typedef unsigned char ANALOGIO;
class AnalogNodeType(IntEnum):
    ENABLE      = 1
    VOLTAGE     = 2
    CURRENT     = 3
    POWER       = 4
    TEMPERATURE = 5
    DMM         = 6
    RANGE       = 7
    MEASURE     = 8
    TIME        = 9
    FREQUENCY   = 10
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef int AnalogOutNode;
class AnalogOutNode(IntEnum):
    CARRIER = 0
    FM      = 1
    AM      = 2
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef int DwfAnalogOutMode;
class AnalogOutMode(IntEnum):
    VOLTAGE = 0
    CURRENT = 1
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef int DwfAnalogOutIdle;
class AnalogOutIdle(IntEnum):
    DISABLE = 0
    OFFSET  = 1
    INITIAL = 2
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef int DwfDigitalInClockSource;
class DigitalInClockSource(IntEnum):
    INTERNAL  = 0
    EXTERNAL  = 1
    EXTERNAL2 = 2
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef int DwfDigitalInSampleMode;
class DigitalInSampleMode(IntEnum):
    SIMPLE = 0
# alternate samples: noise|sample|noise|sample|...
# where noise is more than 1 transition between 2 samples
    NOISE = 1
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef int DwfDigitalOutOutput;
class DigitalOutOutput(IntEnum):
    PUSH_PULL   = 0
    OPEN_DRAIN  = 1
    OPEN_SOURCE = 2
    THREE_STATE = 3 # for custom and random
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef int DwfDigitalOutType;
class DigitalOutType(IntEnum):
    PULSE  = 0
    CUSTOM = 1
    RANDOM = 2
    ROM    = 3
    STATE  = 4
    PLAY   = 5
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef int DwfDigitalOutIdle;
class DigitalOutIdle(IntEnum):
    INIT = 0
    LOW  = 1
    HIGH = 2
    ZET  = 3
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef int DwfAnalogImpedance;
class AnalogImpedance(IntEnum):
    IMPEDANCE            = 0 # Ohms
    IMPEDANCE_PHASE      = 1 # Radians
    RESISTANCE           = 2 # Ohms
    REACTANCE            = 3 # Ohms
    ADMITTANCE           = 4 # Siemen
    ADMITTANCE_PHASE     = 5 # Radians
    CONDUCTANCE          = 6 # Siemen
    SUSCEPTANCE          = 7 # Siemen
    SERIES_CAPACTANCE    = 8 # Farad
    PARALLEL_CAPACITANCE = 9 # Farad
    SERIES_INDUCTANCE    = 10 # Henry
    PARALLEL_INDUCTANCE  = 11 # Henry
    DISSIPATION          = 12 # factor
    QUALITY              = 13 # factor
    def __str__(self):
        return self.name.replace("_", " ").title()

# typedef int DwfParam;
class Param(IntEnum):
    USB_POWER      = 2 # 1 keep the USB power enabled even when AUX is connected, Analog Discovery 2
    LED_BRIGHTNESS = 3 # LED brightness 0 ... 100%, Digital Discovery
    ON_CLOSE       = 4 # 0 continue, 1 stop, 2 shutdown
    AUDIO_OUT      = 5 # 0 disable / 1 enable audio output, Analog Discovery 1, 2
    USB_LIMIT      = 6 # 0..1000 mA USB power limit, -1 no limit, Analog Discovery 1, 2
    ANALOG_OUT     = 7 # 0 disable / 1 enable
    FREQUENCY      = 8 # MHz
    def __str__(self):
        return self.name.replace("_", " ").title()

_dwf = None
if sys.platform.startswith("win"):
    _dwf = ctypes.cdll.dwf
elif sys.platform.startswith("darwin"):
    _dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    _dwf = ctypes.cdll.LoadLibrary("libdwf.so")

class DwfApiException(Exception):
    def __init__(self, status):
        self.status = status

    def __str__(self):
        string_buffer = ctypes.create_string_buffer(512)
        _dwf.FDwfGetLastErrorMsg(string_buffer)
        if (len(string_buffer.value) == 0):
            return str(self.status)
        else:
            return str(self.status) + "\n" + str(string_buffer.value.decode('utf-8'))

# Macro used to verify if bit is 1 or 0 in given bit field
# #define IsBitSet(fs, bit) ((fs & (1<<bit)) != 0)
def IsBitSet(fs, bit):
    return ((fs & (1 << bit)) != 0)

def _ThrowIfError(status: ctypes.c_int):
    if (status != 1):
        raise DwfApiException(status)

#------------------------------------------------------------------------------
# Error and version APIs:
#------------------------------------------------------------------------------

# DWFAPI int FDwfGetLastError(DWFERC *pdwferc);
def GetLastError() -> ErrorCodes:
    '''
    Retrieves the last error code in the calling process. The error code is
    cleared when other API functions are called and it only set when an API
    function fails during execution. Error codes are declared in dwf.h:
    '''
    ''' Retrieves the last error code in the calling process. The error code is
    cleared when other API functions are called and it only set when an API
    function fails during execution. Error codes are declared in dwf.h:
    '''
    erc = ctypes.c_int()
    _dwf.FDwfGetLastError(ctypes.byref(erc))
    return ErrorCodes(erc)

# DWFAPI int FDwfGetLastErrorMsg(char szError[512]);
def GetLastErrorMsg() -> str:
    '''
    Retrieves the last error message. This may consist of a chain of messages,
    separated by a new line character, that describe the events leading to
    failure.
    '''
    ''' Retrieves the last error message. This may consist of a chain of
        messages, separated by a new line character, that describe the events
        leading to failure.
    '''
    out_err_message = ctypes.create_string_buffer(512)
    _dwf.FDwfGetLastErrorMsg(ctypes.byref(out_err_message))
    return str(out_err_message.value.decode('utf-8'))

# DWFAPI int FDwfGetVersion(char szVersion[32]);  // Returns DLL version, for instance: "3.8.5"
def GetVersion() -> str:
    '''
    Retrieves the version string. The version string is composed of major,
    minor, and build numbers (i.e., “2.0.19”).
    '''
    out_version_str = ctypes.create_string_buffer(32)
    _ThrowIfError(_dwf.FDwfGetVersion(ctypes.byref(out_version_str)))
    return str(out_version_str.value.decode('utf-8'))

# DWFAPI int FDwfParamSet(DwfParam param, int value);
def ParamSet(param: Param, value: int) -> None:
    '''
    Configures various global parameters that will be applied on newly opened
    devices.
    '''
    _ThrowIfError(_dwf.FDwfParamSet(param, ctypes.c_int(value)))

# DWFAPI int FDwfParamGet(DwfParam param, int *pvalue);
# Warning no docs found for FDwfParamGet
def ParamGet(param: Param) -> int:
    result = ctypes.c_int()
    _ThrowIfError(_dwf.FDwfParamGet(param, ctypes.byref(result)))
    return int(result.value)

###############################################################################
# DEVICE MANAGMENT FUNCTIONS
###############################################################################

#------------------------------------------------------------------------------
# Enumeration: The FDwfEnum functions are used to discover all connected,
# compatible devices.
#------------------------------------------------------------------------------

# DWFAPI int FDwfEnum(ENUMFILTER enumfilter, int *pcDevice);
def EnumDevices(filter : EnumFilter = EnumFilter.ALL) -> int:
    '''
    Builds an internal list of detected devices filtered by the enumfilter
    parameter. It must be called before using other FDwfEnum functions because
    they obtain information about enumerated devices from the list identified
    by the device index.
    '''
    out_device_count = ctypes.c_int()
    _ThrowIfError(_dwf.FDwfEnum(filter, ctypes.byref(out_device_count)))
    return int(out_device_count.value)

# DWFAPI int FDwfEnumDeviceType(int idxDevice, DEVID *pDeviceId, DEVVER *pDeviceRevision);
def EnumDeviceType(device_index: int) -> (Device, int) :
    '''
    Returns the device ID and version ID.
    '''
    out_device_id = ctypes.c_int()
    out_device_revision = ctypes.c_int()
    _ThrowIfError(_dwf.FDwfEnumDeviceType(ctypes.c_int(device_index), ctypes.byref(out_device_id), ctypes.byref(out_device_revision)))
    return (Device(out_device_id.value), int(out_device_revision.value))

# DWFAPI int FDwfEnumDeviceIsOpened(int idxDevice, int *pfIsUsed);
def EnumDeviceIsOpened(device_index: int) -> bool:
    '''
    Retrieves a Boolean specifying if a device is already opened by this, or any
    other process.
    '''
    out_device_is_opened = ctypes.c_int()
    _ThrowIfError(_dwf.FDwfEnumDeviceType(ctypes.c_int(device_index), ctypes.byref(out_device_is_opened)))
    return bool(out_device_is_opened.value != 0)

# DWFAPI int FDwfEnumUserName(int idxDevice, char szUserName[32]);
def EnumUserName(device_index: int) -> str:
    '''
    Retrieves the user name of the enumerated device.
    '''
    out_username = ctypes.create_string_buffer(32)
    _ThrowIfError(_dwf.FDwfEnumUserName(ctypes.c_int(device_index), ctypes.byref(out_username)))
    return str(out_username.value.decode('utf-8'))

# DWFAPI int FDwfEnumDeviceName(int idxDevice, char szDeviceName[32]);
def EnumDeviceName(device_index: int) -> str:
    '''
    Retrieves the device name of the enumerated device.
    '''
    out_devicename = ctypes.create_string_buffer(32)
    _ThrowIfError(_dwf.FDwfEnumDeviceName(ctypes.c_int(device_index), ctypes.byref(out_devicename)))
    return str(out_devicename.value.decode('utf-8'))

# DWFAPI int FDwfEnumSN(int idxDevice, char szSN[32]);
def EnumSN(device_index: int) -> str:
    '''
    Retrieves the 12-digit, unique serial number of the enumerated device.
    '''
    out_serialnum_str = ctypes.create_string_buffer(32)
    _ThrowIfError(_dwf.FDwfEnumSN(ctypes.c_int(device_index), ctypes.byref(out_serialnum_str)))
    return str(out_serialnum_str.value.decode('utf-8'))

# DWFAPI int FDwfEnumConfig(int idxDevice, int *pcConfig);
def EnumConfig(device_index: int) -> int:
    '''
    Builds an internal list of detected configurations for the selected device.
    The function above must be called before using other FDwfEnumConfigInfo
    function because this obtains information about configurations from this
    list identified by the configuration index.
    '''
    out_config_count = ctypes.c_int()
    _ThrowIfError(_dwf.FDwfEnumConfig(ctypes.c_int(device_index), ctypes.byref(out_config_count)))
    return int(out_config_count.value)

# DWFAPI int FDwfEnumConfigInfo(int idxConfig, DwfEnumConfigInfo info, int *pv);
def EnumConfigInfo(config_index: int, config_info: ConfigInfo) -> int:
    '''
    Returns information about the configuration. The information types are
    declared in dwf.h:
    '''
    out_value = ctypes.c_int()
    _ThrowIfError(_dwf.FDwfEnumConfigInfo(ctypes.c_int(config_index), ctypes.c_int(config_info), ctypes.byref(out_value)))
    return int(out_value.value)

#------------------------------------------------------------------------------
# Open/Close:
#------------------------------------------------------------------------------

# DWFAPI int FDwfDeviceOpen(int idxDevice, HDWF *phdwf);
def DeviceOpen(device_index: int) -> int:
    '''
    Opens a device identified by the enumeration index and retrieves a handle.
    To automatically enumerate all connected devices and open the first
    discovered device, use index -1.
    '''
    out_hdwf = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDeviceOpen(ctypes.c_int(device_index), ctypes.byref(out_hdwf)))
    return int(out_hdwf.value)

# DWFAPI int FDwfDeviceConfigOpen(int idxDev, int idxCfg, HDWF *phdwf);
def DeviceConfigOpen(device_index: int, config_index: int) -> int:
    '''
    Opens a device identified by the enumeration index with the selected
    configuration and retrieves a handle.
    '''
    out_hdwf = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDeviceConfigOpen(ctypes.c_int(device_index), ctypes.c_int(config_index), ctypes.byref(out_hdwf)))
    return int(out_hdwf.value)

# DWFAPI int FDwfDeviceClose(HDWF hdwf);
def DeviceClose(hdwf: int) -> None:
    '''
    Closes an interface handle when access to the device is no longer needed.
    Once the function above has returned, the specified interface handle can no
    longer be used to access the device.
    '''
    _ThrowIfError(_dwf.FDwfDeviceClose(ctypes.c_int(hdwf)))

# DWFAPI int FDwfDeviceCloseAll();
def DeviceCloseAll() -> None:
    '''
    Closes all opened devices by the calling process. It does not close all
    devices across all processes.
    '''
    _ThrowIfError(_dwf.FDwfDeviceCloseAll())

# DWFAPI int FDwfDeviceAutoConfigureSet(HDWF hdwf, int fAutoConfigure);
def DeviceAutoConfigureSet(hdwf: int, auto_configure: bool) -> None:
    '''
    Enables or disables the AutoConfig setting for a specific device. When this
    setting is enabled, the device is automatically configured every time an
    instrument parameter is set. For example, when AutoConfigure is enabled,
    FDwfAnalogOutConfigure does not need to be called after FDwfAnalogOutRunSet.
    This adds latency to every Set function; just as much latency as calling the
    corresponding Configure function directly afterward. With value 3 the
    analog-out configuration will be applied dynamically, without stopping the
    instrument.
    '''
    _ThrowIfError(_dwf.FDwfDeviceAutoConfigureSet(ctypes.c_int(hdwf), ctypes.c_int(auto_configure)))
    return int(out_hdwf.value)

# DWFAPI int FDwfDeviceAutoConfigureGet(HDWF hdwf, int *pfAutoConfigure);
def DeviceAutoConfigureGet(hdwf: int) -> bool:
    '''
    Returns the AutoConfig setting in the device. See the function description
    for FDwfDeviceAutoConfigureSet for details on this setting.
    '''
    out_auto_configure = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDeviceAutoConfigureGet(ctypes.c_int(hdwf), ctypes.byref(out_auto_configure)))
    return bool(out_auto_configure.value)

# DWFAPI int FDwfDeviceReset(HDWF hdwf);
def DeviceReset(hdwf: int) -> None:
    '''
    Resets and configures (by default, having auto configure enabled) all
    device and instrument parameters to default values.
    '''
    _ThrowIfError(_dwf.FDwfDeviceReset(ctypes.c_int(hdwf)))

# DWFAPI int FDwfDeviceEnableSet(HDWF hdwf, int fEnable);
# Warning no docs found for FDwfDeviceEnableSet
def DeviceEnableSet(hdwf: int, enable: bool) -> None:
    _ThrowIfError(_dwf.FDwfDeviceEnableSet(ctypes.c_int(hdwf), ctypes.c_int(enable)))

# DWFAPI int FDwfDeviceTriggerInfo(HDWF hdwf, int *pfstrigsrc); // use IsBitSet
def DeviceTriggerInfo(hdwf: int) -> int: # use IsBitSet
    '''
    Returns the supported trigger source option for the global trigger bus. They
    are returned (by reference) as a bit field. This bit field can be parsed
    using the IsBitSet Macro. Individual bits are defined using the TRIGSRC
    constants in dwf.h.
    '''
    out_trigger_source = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDeviceTriggerInfo(ctypes.c_int(hdwf), ctypes.byref(out_trigger_source)))
    return int(out_trigger_source.value)

# DWFAPI int FDwfDeviceTriggerSet(HDWF hdwf, int idxPin, TRIGSRC trigsrc);
def DeviceTriggerSet(hdwf: int, index_pin: int, trigger_source: TriggerSource) -> None:
    '''
    Configures the trigger I/O pin with a specific TRIGSRC option.
    '''
    out_hdwf = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDeviceTriggerSet(ctypes.c_int(hdwf), ctypes.c_int(index_pin), ctypes.c_int(trigger_source)))

# DWFAPI int FDwfDeviceTriggerGet(HDWF hdwf, int idxPin, TRIGSRC *ptrigsrc);
def DeviceTriggerGet(hdwf: int, index_pin: int) -> TriggerSource:
    '''
    Returns the configured trigger setting for a trigger I/O pin. The trigger
    source can be “none”, and internal instrument, or an external trigger.
    '''
    out_trigger_source = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDeviceTriggerGet(ctypes.c_int(hdwf), ctypes.c_int(index_pin), ctypes.byref(out_trigger_source)))
    return TriggerSource(out_trigger_source.value)

# DWFAPI int FDwfDeviceTriggerPC(HDWF hdwf);
def DeviceTriggerPC(hdwf: int):
    '''
    Generates one pulse on the PC trigger line.
    '''
    _ThrowIfError(_dwf.FDwfDeviceTriggerPC(ctypes.c_int(hdwf)))

# DWFAPI int FDwfDeviceTriggerSlopeInfo(HDWF hdwf, int *pfsslope); // use IsBitSet
def DeviceTriggerSlopeInfo(hdwf: int) -> int: # use IsBitSet
    '''
    Returns the supported trigger slopes: rising, falling, and either edge.
    '''
    out_fsslope = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDeviceTriggerSlopeInfo(ctypes.c_int(hdwf), ctypes.byref(out_fsslope)))
    return int(out_fsslope.value)

# DWFAPI int FDwfDeviceParamSet(HDWF hdwf, DwfParam param, int value);
def DeviceParamSet(hdwf: int, param: Param, value: int) -> None:
    '''
    Configures various parameters for the respective device.
    '''
    _ThrowIfError(_dwf.FDwfDeviceParamSet(ctypes.c_int(hdwf), ctypes.c_int(param), ctypes.c_int(value)))

# DWFAPI int FDwfDeviceParamGet(HDWF hdwf, DwfParam param, int *pvalue);
def DeviceParamGet(hdwf: int, param: Param) -> int:
    '''
    Retrieves the parameter value.
    '''
    out_value = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDeviceParamGet(ctypes.c_int(hdwf), ctypes.c_int(param), ctypes.byref(out_value)))
    return int(out_value.value)

###############################################################################
# ANALOG IN INSTRUMENT FUNCTIONS
###############################################################################

#------------------------------------------------------------------------------
# Control and status:
#------------------------------------------------------------------------------

# DWFAPI int FDwfAnalogInReset(HDWF hdwf);
def AnalogInReset(hdwf: int) -> None:
    '''
    Resets all AnalogIn instrument parameters to default values. If auto
    configure is enabled (through FDwfDeviceAutoConfigureSet), the instrument is
    also configured.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInReset(ctypes.c_int(hdwf)))

# DWFAPI int FDwfAnalogInConfigure(HDWF hdwf, int fReconfigure, int fStart);
def AnalogInConfigure(hdwf: int, reconfigure: int, fStart: int) -> None:
    '''
    Configures the instrument and start or stop the acquisition. To reset the
    Auto trigger timeout, set fReconfigure to TRUE.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInConfigure(ctypes.c_int(hdwf), ctypes.c_int(reconfigure), ctypes.c_int(fStart)))

# DWFAPI int FDwfAnalogInTriggerForce(HDWF hdwf);
# Warning no docs found for FDwfAnalogInTriggerForce
def AnalogInTriggerForce(hdwf: int) -> None:
    _ThrowIfError(_dwf.FDwfAnalogInTriggerForce(ctypes.c_int(hdwf)))

# DWFAPI int FDwfAnalogInStatus(HDWF hdwf, int fReadData, DwfState *psts);
def AnalogInStatus(hdwf: int, fReadData: int) -> int:
    '''
    Checks the state of the acquisition. To read the data from the device, set
    fReadData to TRUE. For single acquisition mode, the data will be read only
    when the acquisition is finished.
    '''
    out_instrument_state = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInStatus(ctypes.c_int(hdwf), ctypes.c_int(fReadData), ctypes.byref(out_instrument_state)))
    return int(out_instrument_state.value)

# DWFAPI int FDwfAnalogInStatusSamplesLeft(HDWF hdwf, int *pcSamplesLeft);
def AnalogInStatusSamplesLeft(hdwf: int) -> int:
    '''
    Retrieves the number of samples left in the acquisition.
    '''
    out_cSamplesLeft = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInStatusSamplesLeft(ctypes.c_int(hdwf), ctypes.byref(out_cSamplesLeft)))
    return int(out_cSamplesLeft.value)

# DWFAPI int FDwfAnalogInStatusSamplesValid(HDWF hdwf, int *pcSamplesValid);
def AnalogInStatusSamplesValid(hdwf: int) -> int:
    '''
    Retrieves the number of valid/acquired data samples.
    '''
    out_samples_valid = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInStatusSamplesValid(ctypes.c_int(hdwf), ctypes.byref(out_samples_valid)))
    return int(out_samples_valid.value)

# DWFAPI int FDwfAnalogInStatusIndexWrite(HDWF hdwf, int *pidxWrite);
def AnalogInStatusIndexWrite(hdwf: int) -> int:
    '''
    Retrieves the buffer write pointer which is needed in ScanScreen acquisition
    mode to display the scan bar.
    '''
    out_write_index = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInStatusIndexWrite(ctypes.c_int(hdwf), ctypes.byref(out_write_index)))
    return int(out_write_index.value)

# DWFAPI int FDwfAnalogInStatusAutoTriggered(HDWF hdwf, int *pfAuto);
def AnalogInStatusAutoTriggered(hdwf: int) -> int:
    '''
    Verifies if the acquisition is auto triggered.
    '''
    out_auto_triggered = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInStatusAutoTriggered(ctypes.c_int(hdwf), ctypes.byref(out_auto_triggered)))
    return int(out_auto_triggered.value)

# DWFAPI int FDwfAnalogInStatusData(HDWF hdwf, int idxChannel, double *rgdVoltData, int cdData);
def AnalogInStatusData(hdwf: int, channel_index: int, cd_data: int) -> float:
    '''
    Retrieves the acquired data samples from the specified idxChannel on the
    AnalogIn instrument. It copies the data samples to the provided buffer.
    '''
    out_rg_double_volt_data = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInStatusData(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(cd_data), ctypes.byref(out_rg_double_volt_data)))
    return float(out_rg_double_volt_data.value)

# DWFAPI int FDwfAnalogInStatusData2(HDWF hdwf, int idxChannel, double *rgdVoltData, int idxData, int cdData);
def AnalogInStatusData2(hdwf: int, channel_index: int, index_data: int, cd_data: int) -> float:
    '''
    Retrieves the acquired data samples from the specified idxChannel on the
    AnalogIn instrument. It copies the data samples to the provided buffer.
    '''
    out_rg_double_volt_data = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInStatusData2(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(index_data), ctypes.c_int(cd_data), ctypes.byref(out_rg_double_volt_data)))
    return float(out_rg_double_volt_data.value)

# DWFAPI int FDwfAnalogInStatusData16(HDWF hdwf, int idxChannel, short *rgu16Data, int idxData, int cdData);
def AnalogInStatusData16(hdwf: int, channel_index: int, index_data: int, cd_data: int) -> int:
    '''
    Retrieves the acquired raw data samples from the specified idxChannel on the
    AnalogIn instrument. It copies the data samples to the provided buffer.
    '''
    out_rg_u16_data = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInStatusData16(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(index_data), ctypes.c_int(cd_data), ctypes.byref(out_rg_u16_data)))
    return int(out_rg_u16_data.value)

# DWFAPI int FDwfAnalogInStatusNoise(HDWF hdwf, int idxChannel, double *rgdMin, double *rgdMax, int cdData);
def AnalogInStatusNoise(hdwf: int, channel_index: int, cd_data: int) -> (float, float):
    '''
    Retrieves the acquired noise samples from the specified idxChannel on the
    AnalogIn instrument. It copies the data samples to the provided buffer.
    '''
    out_rg_double_min = ctypes.c_double(0.0)
    out_rg_double_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInStatusNoise(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(cd_data), ctypes.byref(out_rg_double_min), ctypes.byref(out_rg_double_max)))
    return float(out_rg_double_min.value), float(out_rg_double_max.value)

# DWFAPI int FDwfAnalogInStatusNoise2(HDWF hdwf, int idxChannel, double *rgdMin, double *rgdMax, int idxData, int cdData);
# Warning no docs found for FDwfAnalogInStatusNoise2
def AnalogInStatusNoise2(hdwf: int, channel_index: int, index_data: int, cd_data: int) -> (float, float):
    out_rg_double_min = ctypes.c_double(0.0)
    out_rg_double_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInStatusNoise2(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(index_data), ctypes.c_int(cd_data), ctypes.byref(out_rg_double_min), ctypes.byref(out_rg_double_max)))
    return float(out_rg_double_min.value), float(out_rg_double_max.value)

# DWFAPI int FDwfAnalogInStatusSample(HDWF hdwf, int idxChannel, double *pdVoltSample);
def AnalogInStatusSample(hdwf: int, channel_index: int) -> float:
    '''
    Gets the last ADC conversion sample from the specified idxChannel on the
    AnalogIn instrument.
    '''
    out_dVoltSample = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInStatusSample(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_dVoltSample)))
    return float(out_dVoltSample.value)

# DWFAPI int FDwfAnalogInStatusTime(HDWF hdwf, unsigned int *psecUtc, unsigned int *ptick, unsigned int *pticksPerSecond);
# Warning no docs found for FDwfAnalogInStatusTime
def AnalogInStatusTime(hdwf: int) -> (int, int, int):
    out_secUtc = c_uint(0)
    out_tick = c_uint(0)
    out_ticksPerSecond = c_uint(0)
    _ThrowIfError(_dwf.FDwfAnalogInStatusTime(ctypes.c_int(hdwf), ctypes.byref(out_secUtc), ctypes.byref(out_tick), ctypes.byref(out_ticksPerSecond)))
    return int(out_secUtc.value), int(out_tick.value), int(out_ticksPerSecond.value)

# DWFAPI int FDwfAnalogInStatusRecord(HDWF hdwf, int *pcdDataAvailable, int *pcdDataLost, int *pcdDataCorrupt);
def AnalogInStatusRecord(hdwf: int) -> (int, int, int):
    '''
    Retrieves information about the recording process. The data loss occurs
    when the device acquisition is faster than the read process to PC. In this
    case, the device recording buffer is filled and data samples are
    overwritten. Corrupt samples indicate that the samples have been overwritten
    by the acquisition process during the previous read. In this case, try
    optimizing the loop process for faster execution or reduce the acquisition
    frequency or record length to be less than or equal to the device buffer size
    (record length <= buffer size/frequency).
    '''
    out_cdDataAvailable = ctypes.c_int(0)
    out_cdDataLost = ctypes.c_int(0)
    out_cdDataCorrupt = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInStatusRecord(ctypes.c_int(hdwf), ctypes.byref(out_cdDataAvailable), ctypes.byref(out_cdDataLost), ctypes.byref(out_cdDataCorrupt)))
    return int(out_cdDataAvailable.value), int(out_cdDataLost.value), int(out_cdDataCorrupt.value)

# DWFAPI int FDwfAnalogInRecordLengthSet(HDWF hdwf, double sLength);
def AnalogInRecordLengthSet(hdwf: int, sLength: float) -> None:
    '''
    Sets the Record length in seconds. With length of zero, the record will run
    indefinitely.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInRecordLengthSet(ctypes.c_int(hdwf), ctypes.c_double(sLength)))

#------------------------------------------------------------------------------
# Acquisition configuration:
#------------------------------------------------------------------------------

# DWFAPI int FDwfAnalogInFrequencyInfo(HDWF hdwf, double *phzMin, double *phzMax);
def AnalogInFrequencyInfo(hdwf: int) -> (float, float):
    '''
    Retrieves the minimum and maximum (ADC frequency) settable sample frequency.
    '''
    out_hz_min = ctypes.c_double(0.0)
    out_hz_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInFrequencyInfo(ctypes.c_int(hdwf), ctypes.byref(out_hz_min), ctypes.byref(out_hz_max)))
    return float(out_hz_min.value), float(out_hz_max.value)

# DWFAPI int FDwfAnalogInFrequencySet(HDWF hdwf, double hzFrequency);
def AnalogInFrequencySet(hdwf: int, frequency_in_hz: float) -> None:
    '''
    Sets the sample frequency for the instrument
    '''
    _ThrowIfError(_dwf.FDwfAnalogInFrequencySet(ctypes.c_int(hdwf), ctypes.c_double(frequency_in_hz)))

# DWFAPI int FDwfAnalogInFrequencyGet(HDWF hdwf, double *phzFrequency);
def AnalogInFrequencyGet(hdwf: int) -> float:
    '''
    Reads the configured sample frequency. The AnalogIn ADC always runs at
    maximum frequency, but the method in which the samples are stored in the
    buffer can be individually configured for each channel with
    FDwfAnalogInChannelFilterSet function.
    '''
    out_frequency_in_hz = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInFrequencyGet(ctypes.c_int(hdwf), ctypes.byref(out_frequency_in_hz)))
    return float(out_frequency_in_hz.value)

# DWFAPI int FDwfAnalogInBitsInfo(HDWF hdwf, int *pnBits); // Returns the number of ADC bits
def AnalogInBitsInfo(hdwf: int) -> int:
    '''
    Retrieves the number bits used by the AnalogIn ADC.
    '''
    out_number_of_bits = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInBitsInfo(ctypes.c_int(hdwf), ctypes.byref(out_number_of_bits)))
    return int(out_number_of_bits.value)

# DWFAPI int FDwfAnalogInBufferSizeInfo(HDWF hdwf, int *pnSizeMin, int *pnSizeMax);
def AnalogInBufferSizeInfo(hdwf: int) -> (int, int):
    '''
    Returns the minimum and maximum allowable buffer sizes for the instrument.
    '''
    out_size_min = ctypes.c_int(0)
    out_size_max = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInBufferSizeInfo(ctypes.c_int(hdwf), ctypes.byref(out_size_min), ctypes.byref(out_size_max)))
    return int(out_size_min.value), int(out_size_max.value)

# DWFAPI int FDwfAnalogInBufferSizeSet(HDWF hdwf, int nSize);
def AnalogInBufferSizeSet(hdwf: int, nSize: int) -> None:
    '''
    Adjusts the AnalogIn instrument buffer size.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInBufferSizeSet(ctypes.c_int(hdwf), ctypes.c_int(nSize)))

# DWFAPI int FDwfAnalogInBufferSizeGet(HDWF hdwf, int *pnSize);
def AnalogInBufferSizeGet(hdwf: int) -> int:
    '''
    Returns the used AnalogIn instrument buffer size.
    '''
    out_nSize = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInBufferSizeGet(ctypes.c_int(hdwf), ctypes.byref(out_nSize)))
    return int(out_nSize.value)

# DWFAPI int FDwfAnalogInNoiseSizeInfo(HDWF hdwf, int *pnSizeMax);
def AnalogInNoiseSizeInfo(hdwf: int) -> int:
    '''
    Returns the maximum buffer size for the instrument.
    '''
    out_size_max = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInNoiseSizeInfo(ctypes.c_int(hdwf), ctypes.byref(out_size_max)))
    return int(out_size_max.value)

# DWFAPI int FDwfAnalogInNoiseSizeSet(HDWF hdwf, int nSize);
# Warning no docs found for FDwfAnalogInNoiseSizeSet
def AnalogInNoiseSizeSet(hdwf: int, nSize: int) -> None:
    _ThrowIfError(_dwf.FDwfAnalogInNoiseSizeSet(ctypes.c_int(hdwf), ctypes.c_int(nSize)))

# DWFAPI int FDwfAnalogInNoiseSizeGet(HDWF hdwf, int *pnSize);
def AnalogInNoiseSizeGet(hdwf: int) -> int:
    '''
    Returns the used AnalogIn instrument noise buffer size. This is
    automatically adjusted according to the sample buffer size. For instance,
    having maximum buffer size of 8192 and noise buffer size of 512, setting the
    sample buffer size to 4096 the noise buffer size will be 256.
    '''
    out_nSize = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInNoiseSizeGet(ctypes.c_int(hdwf), ctypes.byref(out_nSize)))
    return int(out_nSize.value)

# DWFAPI int FDwfAnalogInAcquisitionModeInfo(HDWF hdwf, int *pfsacqmode); // use IsBitSet
def AnalogInAcquisitionModeInfo(hdwf: int) -> int:
    '''
    Returns the supported AnalogIn acquisition modes. They are returned (by
    reference) as a bit field. This bit field can be parsed using the IsBitSet
    Macro. Individual bits are defined using the ACQMODE constants in dwf.h. The
    acquisition mode selects one of the following modes, ACQMODE:
    '''
    out_fsacqmode = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInAcquisitionModeInfo(ctypes.c_int(hdwf), ctypes.byref(out_fsacqmode)))
    return int(out_fsacqmode.value)

# DWFAPI int FDwfAnalogInAcquisitionModeSet(HDWF hdwf, ACQMODE acqmode);
def AnalogInAcquisitionModeSet(hdwf: int, acqmode: int) -> None:
    '''
    Sets the acquisition mode.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInAcquisitionModeSet(ctypes.c_int(hdwf), ctypes.c_int(acqmode)))

# DWFAPI int FDwfAnalogInAcquisitionModeGet(HDWF hdwf, ACQMODE *pacqmode);
def AnalogInAcquisitionModeGet(hdwf: int) -> int:
    '''
    Retrieves the acquisition mode.
    '''
    out_acqmode = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInAcquisitionModeGet(ctypes.c_int(hdwf), ctypes.byref(out_acqmode)))
    return int(out_acqmode.value)

#------------------------------------------------------------------------------
# Channel configuration:
#------------------------------------------------------------------------------

# DWFAPI int FDwfAnalogInChannelCount(HDWF hdwf, int *pcChannel);
def AnalogInChannelCount(hdwf: int) -> int:
    '''
    Reads the number of AnalogIn channels of the device.
    '''
    out_cChannel = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInChannelCount(ctypes.c_int(hdwf), ctypes.byref(out_cChannel)))
    return int(out_cChannel.value)

# DWFAPI int FDwfAnalogInChannelEnableSet(HDWF hdwf, int idxChannel, int fEnable);
def AnalogInChannelEnableSet(hdwf: int, channel_index: int, enable: int) -> None:
    '''
    Enables or disables the specified AnalogIn channel.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInChannelEnableSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(enable)))

# DWFAPI int FDwfAnalogInChannelEnableGet(HDWF hdwf, int idxChannel, int *pfEnable);
def AnalogInChannelEnableGet(hdwf: int, channel_index: int) -> int:
    '''
    Gets the current enable/disable status of the specified AnalogIn channel.
    '''
    out_enable = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInChannelEnableGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_enable)))
    return int(out_enable.value)

# DWFAPI int FDwfAnalogInChannelFilterInfo(HDWF hdwf, int *pfsfilter); // use IsBitSet
def AnalogInChannelFilterInfo(hdwf: int) -> int:
    '''
    Returns the supported acquisition filters. They are returned (by reference)
    as a bit field. This bit field can be parsed using the IsBitSet Macro.
    Individual bits are defined using the FILTER constants in dwf.h. When the
    acquisition frequency (FDwfAnalogInFrequencySet) is less than the ADC
    frequency (maximum acquisition frequency).
    '''
    out_fsfilter = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInChannelFilterInfo(ctypes.c_int(hdwf), ctypes.byref(out_fsfilter)))
    return int(out_fsfilter.value)

# DWFAPI int FDwfAnalogInChannelFilterSet(HDWF hdwf, int idxChannel, FILTER filter);
def AnalogInChannelFilterSet(hdwf: int, channel_index: int, filter: int) -> None:
    '''
    Sets the acquisition filter for each AnalogIn channel. With channel index
    -1, each enabled AnalogIn channel filter will be configured to use the same,
    new option.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInChannelFilterSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(filter)))

# DWFAPI int FDwfAnalogInChannelFilterGet(HDWF hdwf, int idxChannel, FILTER *pfilter);
def AnalogInChannelFilterGet(hdwf: int, channel_index: int) -> int:
    '''
    Returns the configured acquisition filter.
    '''
    out_filter = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInChannelFilterGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_filter)))
    return int(out_filter.value)

# DWFAPI int FDwfAnalogInChannelRangeInfo(HDWF hdwf, double *pvoltsMin, double *pvoltsMax, double *pnSteps);
def AnalogInChannelRangeInfo(hdwf: int) -> (float, float, float):
    '''
    Returns the minimum and maximum range, peak to peak values, and the number
    of adjustable steps.
    '''
    out_volts_min = ctypes.c_double(0.0)
    out_volts_max = ctypes.c_double(0.0)
    out_num_steps = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInChannelRangeInfo(ctypes.c_int(hdwf), ctypes.byref(out_volts_min), ctypes.byref(out_volts_max), ctypes.byref(out_num_steps)))
    return float(out_volts_min.value), float(out_volts_max.value), float(out_num_steps.value)

# DWFAPI int FDwfAnalogInChannelRangeSteps(HDWF hdwf, double rgVoltsStep[32], int *pnSteps);
def AnalogInChannelRangeSteps(hdwf: int) -> (List[float], int):
    '''
    Reads the range of steps supported by the device. For instance: 1, 2, 5, 10, etc.
    '''
    voltage_steps_data = []
    out_voltage_steps_data = (ctypes.c_cdouble * 32)()
    out_number_range_steps = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInChannelRangeSteps(ctypes.c_int(hdwf), ctypes.byref(out_voltage_steps_data), ctypes.byref(out_number_range_steps)))
    for i in range(32): voltage_steps_data.append(out_voltage_steps_data[i])
    return voltage_steps_data, int(out_number_range_steps.value)

# DWFAPI int FDwfAnalogInChannelRangeSet(HDWF hdwf, int idxChannel, double voltsRange);
def AnalogInChannelRangeSet(hdwf: int, channel_index: int, voltsRange: float) -> None:
    '''
    Configures the range for each channel. With channel index -1, each enabled
    Analog In channel range will be configured to the same, new value.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInChannelRangeSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_double(voltsRange)))

# DWFAPI int FDwfAnalogInChannelRangeGet(HDWF hdwf, int idxChannel, double *pvoltsRange);
def AnalogInChannelRangeGet(hdwf: int, channel_index: int) -> float:
    '''
    Returns the real range value for the given channel.
    '''
    out_voltsRange = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInChannelRangeGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_voltsRange)))
    return float(out_voltsRange.value)

# DWFAPI int FDwfAnalogInChannelOffsetInfo(HDWF hdwf, double *pvoltsMin, double *pvoltsMax, double *pnSteps);
def AnalogInChannelOffsetInfo(hdwf: int) -> (float, float, float):
    '''
    Returns the minimum and maximum offset levels supported, and the number of
    adjustable steps.
    '''
    out_volts_min = ctypes.c_double(0.0)
    out_volts_max = ctypes.c_double(0.0)
    out_num_steps = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInChannelOffsetInfo(ctypes.c_int(hdwf), ctypes.byref(out_volts_min), ctypes.byref(out_volts_max), ctypes.byref(out_num_steps)))
    return float(out_volts_min.value), float(out_volts_max.value), float(out_num_steps.value)

# DWFAPI int FDwfAnalogInChannelOffsetSet(HDWF hdwf, int idxChannel, double voltOffset);
def AnalogInChannelOffsetSet(hdwf: int, channel_index: int, voltOffset: float) -> None:
    '''
    Configures the offset for each channel. When channel index is specified as
    -1, each enabled AnalogIn channel offset will be configured to the same
    level.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInChannelOffsetSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_double(voltOffset)))

# DWFAPI int FDwfAnalogInChannelOffsetGet(HDWF hdwf, int idxChannel, double *pvoltOffset);
def AnalogInChannelOffsetGet(hdwf: int, channel_index: int) -> float:
    '''
    Returns for each AnalogIn channel the real offset level.
    '''
    out_voltOffset = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInChannelOffsetGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_voltOffset)))
    return float(out_voltOffset.value)

# DWFAPI int FDwfAnalogInChannelAttenuationSet(HDWF hdwf, int idxChannel, double xAttenuation);
def AnalogInChannelAttenuationSet(hdwf: int, channel_index: int, xAttenuation: float) -> None:
    '''
    Configures the attenuation for each channel. When channel index is specified
    as -1, each enabled AnalogIn channel attenuation will be configured to the
    same level. The attenuation does not change the attenuation on the device,
    just informs the library about the externally applied attenuation.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInChannelAttenuationSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_double(xAttenuation)))

# DWFAPI int FDwfAnalogInChannelAttenuationGet(HDWF hdwf, int idxChannel, double *pxAttenuation);
def AnalogInChannelAttenuationGet(hdwf: int, channel_index: int) -> float:
    '''
    Returns for each AnalogIn channel the configured attenuation.
    '''
    out_xAttenuation = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInChannelAttenuationGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_xAttenuation)))
    return float(out_xAttenuation.value)

# DWFAPI int FDwfAnalogInChannelBandwidthSet(HDWF hdwf, int idxChannel, double hz);
# Warning no docs found for FDwfAnalogInChannelBandwidthSet
def AnalogInChannelBandwidthSet(hdwf: int, channel_index: int, hz: float) -> None:
    _ThrowIfError(_dwf.FDwfAnalogInChannelBandwidthSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_double(hz)))

# DWFAPI int FDwfAnalogInChannelBandwidthGet(HDWF hdwf, int idxChannel, double *hzMin);
# Warning no docs found for FDwfAnalogInChannelBandwidthGet
def AnalogInChannelBandwidthGet(hdwf: int, channel_index: int) -> float:
    out_hz_min = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInChannelBandwidthGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_hz_min)))
    return float(out_hz_min.value)

# DWFAPI int FDwfAnalogInChannelImpedanceSet(HDWF hdwf, int idxChannel, double hz);
# Warning no docs found for FDwfAnalogInChannelImpedanceSet
def AnalogInChannelImpedanceSet(hdwf: int, channel_index: int, hz: float) -> None:
    _ThrowIfError(_dwf.FDwfAnalogInChannelImpedanceSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_double(hz)))

# DWFAPI int FDwfAnalogInChannelImpedanceGet(HDWF hdwf, int idxChannel, double *hzMin);
# Warning no docs found for FDwfAnalogInChannelImpedanceGet
def AnalogInChannelImpedanceGet(hdwf: int, channel_index: int) -> float:
    out_hz_min = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInChannelImpedanceGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_hz_min)))
    return float(out_hz_min.value)

#------------------------------------------------------------------------------
# Trigger configuration:
#------------------------------------------------------------------------------

# DWFAPI int FDwfAnalogInTriggerSourceSet(HDWF hdwf, TRIGSRC trigsrc);
def AnalogInTriggerSourceSet(hdwf: int, trigger_source: int) -> None:
    '''
    Configures the AnalogIn acquisition trigger source.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInTriggerSourceSet(ctypes.c_int(hdwf), ctypes.c_int(trigger_source)))

# DWFAPI int FDwfAnalogInTriggerSourceGet(HDWF hdwf, TRIGSRC *ptrigsrc);
def AnalogInTriggerSourceGet(hdwf: int) -> int:
    '''
    Returns the configured trigger source. The trigger source can be “none” or
    an internal instrument or external trigger. To use the trigger on AnalogIn
    channels (edge, pulse, etc.), use trigsrcDetectorAnalogIn
    '''
    out_trigger_source = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerSourceGet(ctypes.c_int(hdwf), ctypes.byref(out_trigger_source)))
    return int(out_trigger_source.value)

# DWFAPI int FDwfAnalogInTriggerPositionInfo(HDWF hdwf, double *psecMin, double *psecMax, double *pnSteps);
def AnalogInTriggerPositionInfo(hdwf: int) -> (float, float, float):
    '''
    Returns the minimum and maximum values of the trigger position in seconds.
    For Single/Repeated acquisition mode the horizontal trigger position is used
    is relative to the buffer middle point.
    '''
    out_sec_min = ctypes.c_double(0.0)
    out_sec_max = ctypes.c_double(0.0)
    out_num_steps = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerPositionInfo(ctypes.c_int(hdwf), ctypes.byref(out_sec_min), ctypes.byref(out_sec_max), ctypes.byref(out_num_steps)))
    return float(out_sec_min.value), float(out_sec_max.value), float(out_num_steps.value)

# DWFAPI int FDwfAnalogInTriggerPositionSet(HDWF hdwf, double secPosition);
def AnalogInTriggerPositionSet(hdwf: int, secPosition: float) -> None:
    '''
    Configures the horizontal trigger position in seconds.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInTriggerPositionSet(ctypes.c_int(hdwf), ctypes.c_double(secPosition)))

# DWFAPI int FDwfAnalogInTriggerPositionGet(HDWF hdwf, double *psecPosition);
def AnalogInTriggerPositionGet(hdwf: int) -> float:
    '''
    Returns the configured trigger position in seconds.
    '''
    out_secPosition = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerPositionGet(ctypes.c_int(hdwf), ctypes.byref(out_secPosition)))
    return float(out_secPosition.value)

# DWFAPI int FDwfAnalogInTriggerPositionStatus(HDWF hdwf, double *psecPosition);
# Warning no docs found for FDwfAnalogInTriggerPositionStatus
def AnalogInTriggerPositionStatus(hdwf: int) -> float:
    out_secPosition = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerPositionStatus(ctypes.c_int(hdwf), ctypes.byref(out_secPosition)))
    return float(out_secPosition.value)

# DWFAPI int FDwfAnalogInTriggerAutoTimeoutInfo(HDWF hdwf, double *psecMin, double *psecMax, double *pnSteps);
def AnalogInTriggerAutoTimeoutInfo(hdwf: int) -> (float, float, float):
    '''
    Returns the minimum and maximum auto trigger timeout values, and the number
    of adjustable steps. The acquisition is auto triggered when the specified
    time elapses. With zero value the timeout is disabled, performing “Normal”
    acquisitions.
    '''
    out_sec_min = ctypes.c_double(0.0)
    out_sec_max = ctypes.c_double(0.0)
    out_num_steps = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerAutoTimeoutInfo(ctypes.c_int(hdwf), ctypes.byref(out_sec_min), ctypes.byref(out_sec_max), ctypes.byref(out_num_steps)))
    return float(out_sec_min.value), float(out_sec_max.value), float(out_num_steps.value)

# DWFAPI int FDwfAnalogInTriggerAutoTimeoutSet(HDWF hdwf, double secTimeout);
def AnalogInTriggerAutoTimeoutSet(hdwf: int, secTimeout: float) -> None:
    '''
    Configures the auto trigger timeout value in seconds.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInTriggerAutoTimeoutSet(ctypes.c_int(hdwf), ctypes.c_double(secTimeout)))

# DWFAPI int FDwfAnalogInTriggerAutoTimeoutGet(HDWF hdwf, double *psecTimeout);
def AnalogInTriggerAutoTimeoutGet(hdwf: int) -> float:
    '''
    Returns the configured auto trigger timeout value in seconds.
    '''
    out_secTimeout = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerAutoTimeoutGet(ctypes.c_int(hdwf), ctypes.byref(out_secTimeout)))
    return float(out_secTimeout.value)

# DWFAPI int FDwfAnalogInTriggerHoldOffInfo(HDWF hdwf, double *psecMin, double *psecMax, double *pnStep);
def AnalogInTriggerHoldOffInfo(hdwf: int) -> (float, float, float):
    '''
    Returns the supported range of the trigger Hold-Off time in Seconds. The
    trigger hold-off is an adjustable period of time during which the
    acquisition will not trigger. This feature is used when you are triggering
    on burst waveform shapes, so the oscilloscope triggers only on the first
    eligible trigger point.
    '''
    out_sec_min = ctypes.c_double(0.0)
    out_sec_max = ctypes.c_double(0.0)
    out_nStep = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerHoldOffInfo(ctypes.c_int(hdwf), ctypes.byref(out_sec_min), ctypes.byref(out_sec_max), ctypes.byref(out_nStep)))
    return float(out_sec_min.value), float(out_sec_max.value), float(out_nStep.value)

# DWFAPI int FDwfAnalogInTriggerHoldOffSet(HDWF hdwf, double secHoldOff);
def AnalogInTriggerHoldOffSet(hdwf: int, secHoldOff: float) -> None:
    '''
    Sets the trigger hold-off for the AnalongIn instrument in Seconds.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInTriggerHoldOffSet(ctypes.c_int(hdwf), ctypes.c_double(secHoldOff)))

# DWFAPI int FDwfAnalogInTriggerHoldOffGet(HDWF hdwf, double *psecHoldOff);
def AnalogInTriggerHoldOffGet(hdwf: int) -> float:
    '''
    Gets the current trigger hold-off for the AnalongIn instrument in Seconds.
    '''
    out_secHoldOff = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerHoldOffGet(ctypes.c_int(hdwf), ctypes.byref(out_secHoldOff)))
    return float(out_secHoldOff.value)

# DWFAPI int FDwfAnalogInTriggerTypeInfo(HDWF hdwf, int *pfstrigtype); // use IsBitSet
def AnalogInTriggerTypeInfo(hdwf: int) -> int:
    '''
    Returns the supported trigger type options for the instrument. They are
    returned (by reference) as a bit field. This bit field can be parsed using
    the IsBitSet Macro. Individual bits are defined using the TRIGTYPE constants
    in dwf.h. These trigger type options are:
    '''
    out_fstrigtype = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerTypeInfo(ctypes.c_int(hdwf), ctypes.byref(out_fstrigtype)))
    return int(out_fstrigtype.value)

# DWFAPI int FDwfAnalogInTriggerTypeSet(HDWF hdwf, TRIGTYPE trigtype);
def AnalogInTriggerTypeSet(hdwf: int, trigger_type: int) -> None:
    '''
    Sets the trigger type for the instrument.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInTriggerTypeSet(ctypes.c_int(hdwf), ctypes.c_int(trigger_type)))

# DWFAPI int FDwfAnalogInTriggerTypeGet(HDWF hdwf, TRIGTYPE *ptrigtype);
def AnalogInTriggerTypeGet(hdwf: int) -> int:
    '''
    Gets the current trigger type for the instrument.
    '''
    out_trigger_type = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerTypeGet(ctypes.c_int(hdwf), ctypes.byref(out_trigger_type)))
    return int(out_trigger_type.value)

# DWFAPI int FDwfAnalogInTriggerChannelInfo(HDWF hdwf, int *pidxMin, int *pidxMax);
def AnalogInTriggerChannelInfo(hdwf: int) -> (int, int):
    '''
    Returns the range of channels that can be triggered on.
    '''
    out_index_min = ctypes.c_int(0)
    out_index_max = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerChannelInfo(ctypes.c_int(hdwf), ctypes.byref(out_index_min), ctypes.byref(out_index_max)))
    return int(out_index_min.value), int(out_index_max.value)

# DWFAPI int FDwfAnalogInTriggerChannelSet(HDWF hdwf, int idxChannel);
def AnalogInTriggerChannelSet(hdwf: int, channel_index: int) -> None:
    '''
    Sets the trigger channel.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInTriggerChannelSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index)))

# DWFAPI int FDwfAnalogInTriggerChannelGet(HDWF hdwf, int *pidxChannel);
def AnalogInTriggerChannelGet(hdwf: int) -> int:
    '''
    Retrieves the current trigger channel index.
    '''
    out_channel_index = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerChannelGet(ctypes.c_int(hdwf), ctypes.byref(out_channel_index)))
    return int(out_channel_index.value)

# DWFAPI int FDwfAnalogInTriggerFilterInfo(HDWF hdwf, int *pfsfilter); // use IsBitSet
def AnalogInTriggerFilterInfo(hdwf: int) -> int:
    '''
    Returns the supported trigger filters. They are returned (by reference) as a
    bit field which can be parsed using the IsBitSet Macro. Individual bits are
    defined using the FILTER constants in DWF.h.
    '''
    out_fsfilter = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerFilterInfo(ctypes.c_int(hdwf), ctypes.byref(out_fsfilter)))
    return int(out_fsfilter.value)

# DWFAPI int FDwfAnalogInTriggerFilterSet(HDWF hdwf, FILTER filter);
def AnalogInTriggerFilterSet(hdwf: int, filter: int) -> None:
    '''
    Sets the trigger filter.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInTriggerFilterSet(ctypes.c_int(hdwf), ctypes.c_int(filter)))

# DWFAPI int FDwfAnalogInTriggerFilterGet(HDWF hdwf, FILTER *pfilter);
def AnalogInTriggerFilterGet(hdwf: int) -> int:
    '''
    Gets the trigger filter.
    '''
    out_filter = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerFilterGet(ctypes.c_int(hdwf), ctypes.byref(out_filter)))
    return int(out_filter.value)

# DWFAPI int FDwfAnalogInTriggerLevelInfo(HDWF hdwf, double *pvoltsMin, double *pvoltsMax, double *pnSteps);
def AnalogInTriggerLevelInfo(hdwf: int) -> (float, float, float):
    '''
    Retrieves the range of valid trigger voltage levels for the AnalogIn
    instrument in Volts.
    '''
    out_volts_min = ctypes.c_double(0.0)
    out_volts_max = ctypes.c_double(0.0)
    out_num_steps = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerLevelInfo(ctypes.c_int(hdwf), ctypes.byref(out_volts_min), ctypes.byref(out_volts_max), ctypes.byref(out_num_steps)))
    return float(out_volts_min.value), float(out_volts_max.value), float(out_num_steps.value)

# DWFAPI int FDwfAnalogInTriggerLevelSet(HDWF hdwf, double voltsLevel);
def AnalogInTriggerLevelSet(hdwf: int, voltage_level: float) -> None:
    '''
    Sets the trigger voltage level in Volts.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInTriggerLevelSet(ctypes.c_int(hdwf), ctypes.c_double(voltage_level)))

# DWFAPI int FDwfAnalogInTriggerLevelGet(HDWF hdwf, double *pvoltsLevel);
def AnalogInTriggerLevelGet(hdwf: int) -> float:
    '''
    Gets the current trigger voltage level in Volts.
    '''
    out_voltsLevel = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerLevelGet(ctypes.c_int(hdwf), ctypes.byref(out_voltsLevel)))
    return float(out_voltsLevel.value)

# DWFAPI int FDwfAnalogInTriggerHysteresisInfo(HDWF hdwf, double *pvoltsMin, double *pvoltsMax, double *pnSteps);
def AnalogInTriggerHysteresisInfo(hdwf: int) -> (float, float, float):
    '''
    Retrieves the range of valid trigger hysteresis voltage levels for the
    AnalogIn instrument in Volts. The trigger detector uses two levels: low
    level (TriggerLevel - Hysteresis) and high level (TriggerLevel +
    Hysteresis). Trigger hysteresis can be used to filter noise for Edge or
    Pulse trigger. The low and high levels are used in transition time
    triggering.
    '''
    out_volts_min = ctypes.c_double(0.0)
    out_volts_max = ctypes.c_double(0.0)
    out_num_steps = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerHysteresisInfo(ctypes.c_int(hdwf), ctypes.byref(out_volts_min), ctypes.byref(out_volts_max), ctypes.byref(out_num_steps)))
    return float(out_volts_min.value), float(out_volts_max.value), float(out_num_steps.value)

# DWFAPI int FDwfAnalogInTriggerHysteresisSet(HDWF hdwf, double voltsLevel);
def AnalogInTriggerHysteresisSet(hdwf: int, voltage_level: float) -> None:
    '''
    Sets the trigger hysteresis level in Volts.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInTriggerHysteresisSet(ctypes.c_int(hdwf), ctypes.c_double(voltage_level)))

# DWFAPI int FDwfAnalogInTriggerHysteresisGet(HDWF hdwf, double *pvoltsHysteresis);
def AnalogInTriggerHysteresisGet(hdwf: int) -> float:
    '''
    Gets the current trigger hysteresis level in Volts.
    '''
    out_hysteresis_voltage = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerHysteresisGet(ctypes.c_int(hdwf), ctypes.byref(out_hysteresis_voltage)))
    return float(out_hysteresis_voltage.value)

# DWFAPI int FDwfAnalogInTriggerConditionInfo(HDWF hdwf, int *pfstrigcond); // use IsBitSet
def AnalogInTriggerConditionInfo(hdwf: int) -> int:
    '''
    Returns the supported trigger type options for the instrument. They are
    returned (by reference) as a bit field. This bit field can be parsed using
    the IsBitSet Macro. Individual bits are defined using the DwfTriggerSlope
    constants in dwf.h. These trigger condition options are:
    '''
    out_fstrigcond = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerConditionInfo(ctypes.c_int(hdwf), ctypes.byref(out_fstrigcond)))
    return int(out_fstrigcond.value)

# DWFAPI int FDwfAnalogInTriggerConditionSet(HDWF hdwf, DwfTriggerSlope trigcond);
def AnalogInTriggerConditionSet(hdwf: int, trigcond: TriggerSlope) -> None:
    '''
    Sets the trigger condition for the instrument.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInTriggerConditionSet(ctypes.c_int(hdwf), ctypes.c_int(trigcond)))

# DWFAPI int FDwfAnalogInTriggerConditionGet(HDWF hdwf, DwfTriggerSlope *ptrigcond);
def AnalogInTriggerConditionGet(hdwf: int) -> TriggerSlope:
    '''
    Sets the trigger condition for the instrument.
    '''
    out_trigcond = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerConditionGet(ctypes.c_int(hdwf), ctypes.byref(out_trigcond)))
    return TriggerSlope(out_trigcond.value)

# DWFAPI int FDwfAnalogInTriggerLengthInfo(HDWF hdwf, double *psecMin, double *psecMax, double *pnSteps);
def AnalogInTriggerLengthInfo(hdwf: int) -> (float, float, float):
    '''
    Returns the supported range of trigger length for the instrument in Seconds.
    The trigger length specifies the minimal or maximal pulse length or
    transition time.
    '''
    out_sec_min = ctypes.c_double(0.0)
    out_sec_max = ctypes.c_double(0.0)
    out_num_steps = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerLengthInfo(ctypes.c_int(hdwf), ctypes.byref(out_sec_min), ctypes.byref(out_sec_max), ctypes.byref(out_num_steps)))
    return float(out_sec_min.value), float(out_sec_max.value), float(out_num_steps.value)

# DWFAPI int FDwfAnalogInTriggerLengthSet(HDWF hdwf, double secLength);
def AnalogInTriggerLengthSet(hdwf: int, secLength: float) -> None:
    '''
    Sets the trigger length in Seconds.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInTriggerLengthSet(ctypes.c_int(hdwf), ctypes.c_double(secLength)))

# DWFAPI int FDwfAnalogInTriggerLengthGet(HDWF hdwf, double *psecLength);
def AnalogInTriggerLengthGet(hdwf: int) -> float:
    '''
    Gets the current trigger length in Seconds.
    '''
    out_secLength = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerLengthGet(ctypes.c_int(hdwf), ctypes.byref(out_secLength)))
    return float(out_secLength.value)

# DWFAPI int FDwfAnalogInTriggerLengthConditionInfo(HDWF hdwf, int *pfstriglen); // use IsBitSet
def AnalogInTriggerLengthConditionInfo(hdwf: int) -> int:
    '''
    Returns the supported trigger length condition options for the AnalogIn
    instrument. They are returned (by reference) as a bit field. This bit field
    can be parsed using the IsBitSet Macro. Individual bits are defined using
    the TRIGLEN constants in DWF.h. These trigger length condition options are:
    '''
    out_fstriglen = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerLengthConditionInfo(ctypes.c_int(hdwf), ctypes.byref(out_fstriglen)))
    return int(out_fstriglen.value)

# DWFAPI int FDwfAnalogInTriggerLengthConditionSet(HDWF hdwf, TRIGLEN triglen);
def AnalogInTriggerLengthConditionSet(hdwf: int, trigger_length: int) -> None:
    '''
    Sets the trigger length condition for the AnalongIn instrument.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInTriggerLengthConditionSet(ctypes.c_int(hdwf), ctypes.c_int(trigger_length)))

# DWFAPI int FDwfAnalogInTriggerLengthConditionGet(HDWF hdwf, TRIGLEN *ptriglen);
def AnalogInTriggerLengthConditionGet(hdwf: int) -> int:
    '''
    Gets the current trigger length condition for the AnalongIn instrument.
    '''
    out_trigger_length = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerLengthConditionGet(ctypes.c_int(hdwf), ctypes.byref(out_trigger_length)))
    return int(out_trigger_length.value)

# DWFAPI int FDwfAnalogInSamplingSourceSet(HDWF hdwf, TRIGSRC trigsrc);
def AnalogInSamplingSourceSet(hdwf: int, trigger_source: int) -> None:
    '''
    Configures the AnalogIn acquisition data sampling source.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInSamplingSourceSet(ctypes.c_int(hdwf), ctypes.c_int(trigger_source)))

# DWFAPI int FDwfAnalogInSamplingSourceGet(HDWF hdwf, TRIGSRC *ptrigsrc);
def AnalogInSamplingSourceGet(hdwf: int) -> int:
    '''
    Returns the configured sampling source.
    '''
    out_trigger_source = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInSamplingSourceGet(ctypes.c_int(hdwf), ctypes.byref(out_trigger_source)))
    return int(out_trigger_source.value)

# DWFAPI int FDwfAnalogInSamplingSlopeSet(HDWF hdwf, DwfTriggerSlope slope);
def AnalogInSamplingSlopeSet(hdwf: int, slope: TriggerSlope) -> None:
    '''
    Sets the sampling slope for the instrument
    '''
    _ThrowIfError(_dwf.FDwfAnalogInSamplingSlopeSet(ctypes.c_int(hdwf), ctypes.c_int(slope)))

# DWFAPI int FDwfAnalogInSamplingSlopeGet(HDWF hdwf, DwfTriggerSlope *pslope);
def AnalogInSamplingSlopeGet(hdwf: int) -> TriggerSlope:
    '''
    Returns the sampling for the instrument.
    '''
    out_slope = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInSamplingSlopeGet(ctypes.c_int(hdwf), ctypes.byref(out_slope)))
    return TriggerSlope(out_slope.value)

# DWFAPI int FDwfAnalogInSamplingDelaySet(HDWF hdwf, double sec);
def AnalogInSamplingDelaySet(hdwf: int, sec: float) -> None:
    '''
    Sets the sampling delay for the instrument.
    '''
    _ThrowIfError(_dwf.FDwfAnalogInSamplingDelaySet(ctypes.c_int(hdwf), ctypes.c_double(sec)))

# DWFAPI int FDwfAnalogInSamplingDelayGet(HDWF hdwf, double *psec);
def AnalogInSamplingDelayGet(hdwf: int) -> float:
    '''
    Returns the configured sampling delay.
    '''
    out_sec = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogInSamplingDelayGet(ctypes.c_int(hdwf), ctypes.byref(out_sec)))
    return float(out_sec.value)

###############################################################################
# ANALOG OUT INSTRUMENT FUNCTIONS
###############################################################################

#------------------------------------------------------------------------------
# Configuration:
#------------------------------------------------------------------------------

# DWFAPI int FDwfAnalogOutCount(HDWF hdwf, int *pcChannel);
def AnalogOutCount(hdwf: int) -> int:
    '''
    Returns the number of Analog Out channels by the device specified by hdwf.
    '''
    out_cChannel = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutCount(ctypes.c_int(hdwf), ctypes.byref(out_cChannel)))
    return int(out_cChannel.value)

# DWFAPI int FDwfAnalogOutMasterSet(HDWF hdwf, int idxChannel, int idxMaster);
def AnalogOutMasterSet(hdwf: int, channel_index: int, idxMaster: int) -> None:
    '''
    Sets the state machine master of the channel generator. With channel index
    -1, each enabled Analog Out channel will be configured to use the same, new
    option.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutMasterSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(idxMaster)))

# DWFAPI int FDwfAnalogOutMasterGet(HDWF hdwf, int idxChannel, int *pidxMaster);
def AnalogOutMasterGet(hdwf: int, channel_index: int) -> int:
    '''
    Verifies the parameter set by FDwfAnalogOutMasterSet.
    '''
    out_idxMaster = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutMasterGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_idxMaster)))
    return int(out_idxMaster.value)

# DWFAPI int FDwfAnalogOutTriggerSourceSet(HDWF hdwf, int idxChannel, TRIGSRC trigsrc);
def AnalogOutTriggerSourceSet(hdwf: int, channel_index: int, trigger_source: int) -> None:
    '''
    Sets the trigger source for the channel on instrument.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutTriggerSourceSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(trigger_source)))

# DWFAPI int FDwfAnalogOutTriggerSourceGet(HDWF hdwf, int idxChannel, TRIGSRC *ptrigsrc);
def AnalogOutTriggerSourceGet(hdwf: int, channel_index: int) -> int:
    '''
    Gets the current trigger source setting for the channel on instrument.
    '''
    out_trigger_source = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutTriggerSourceGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_trigger_source)))
    return int(out_trigger_source.value)

# DWFAPI int FDwfAnalogOutTriggerSlopeSet(HDWF hdwf, int idxChannel, DwfTriggerSlope slope);
def AnalogOutTriggerSlopeSet(hdwf: int, channel_index: int, slope: int) -> None:
    '''
    Sets the trigger slope for the channel on instrument
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutTriggerSlopeSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(slope)))

# DWFAPI int FDwfAnalogOutTriggerSlopeGet(HDWF hdwf, int idxChannel, DwfTriggerSlope *pslope);
def AnalogOutTriggerSlopeGet(hdwf: int, channel_index: int) -> int:
    '''
    Gets the current trigger slope setting for the channel on instrument.
    '''
    out_slope = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutTriggerSlopeGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_slope)))
    return int(out_slope.value)

# DWFAPI int FDwfAnalogOutRunInfo(HDWF hdwf, int idxChannel, double *psecMin, double *psecMax);
def AnalogOutRunInfo(hdwf: int, channel_index: int) -> (float, float):
    '''
    Returns the supported run length range for the instrument in Seconds. Zero
    values represent an infinite (or continuous) run. Default value is zero.
    '''
    out_sec_min = ctypes.c_double(0.0)
    out_sec_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutRunInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_sec_min), ctypes.byref(out_sec_max)))
    return float(out_sec_min.value), float(out_sec_max.value)

# DWFAPI int FDwfAnalogOutRunSet(HDWF hdwf, int idxChannel, double secRun);
def AnalogOutRunSet(hdwf: int, channel_index: int, secRun: float) -> None:
    '''
    Sets the run length for the instrument in Seconds.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutRunSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_double(secRun)))

# DWFAPI int FDwfAnalogOutRunGet(HDWF hdwf, int idxChannel, double *psecRun);
def AnalogOutRunGet(hdwf: int, channel_index: int) -> float:
    '''
    Reads the configured run length for the instrument in Seconds.
    '''
    out_secRun = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutRunGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_secRun)))
    return float(out_secRun.value)

# DWFAPI int FDwfAnalogOutRunStatus(HDWF hdwf, int idxChannel, double *psecRun);
def AnalogOutRunStatus(hdwf: int, channel_index: int) -> float:
    '''
    Reads the remaining run length. It returns data from the last
    FDwfAnalogOutStatus call.
    '''
    out_secRun = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutRunStatus(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_secRun)))
    return float(out_secRun.value)

# DWFAPI int FDwfAnalogOutWaitInfo(HDWF hdwf, int idxChannel, double *psecMin, double *psecMax);
def AnalogOutWaitInfo(hdwf: int, channel_index: int) -> (float, float):
    '''
    Returns the supported wait length range in Seconds. The wait length is how
    long the instrument waits after being triggered to generate the signal.
    Default value is zero.
    '''
    out_sec_min = ctypes.c_double(0.0)
    out_sec_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutWaitInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_sec_min), ctypes.byref(out_sec_max)))
    return float(out_sec_min.value), float(out_sec_max.value)

# DWFAPI int FDwfAnalogOutWaitSet(HDWF hdwf, int idxChannel, double secWait);
def AnalogOutWaitSet(hdwf: int, channel_index: int, secWait: float) -> None:
    '''
    Sets the wait length for the channel on instrument.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutWaitSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_double(secWait)))

# DWFAPI int FDwfAnalogOutWaitGet(HDWF hdwf, int idxChannel, double *psecWait);
def AnalogOutWaitGet(hdwf: int, channel_index: int) -> float:
    '''
    Gets the current wait length for the channel on instrument.
    '''
    out_secWait = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutWaitGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_secWait)))
    return float(out_secWait.value)

# DWFAPI int FDwfAnalogOutRepeatInfo(HDWF hdwf, int idxChannel, int *pnMin, int *pnMax);
def AnalogOutRepeatInfo(hdwf: int, channel_index: int) -> (int, int):
    '''
    Returns the supported repeat count range. This is how many times the
    generated signal will be repeated upon. Zero value represents infinite
    repeat. Default value is one.
    '''
    out_min = ctypes.c_int(0)
    out_max = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutRepeatInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_min), ctypes.byref(out_max)))
    return int(out_min.value), int(out_max.value)

# DWFAPI int FDwfAnalogOutRepeatSet(HDWF hdwf, int idxChannel, int cRepeat);
def AnalogOutRepeatSet(hdwf: int, channel_index: int, cRepeat: int) -> None:
    '''
    Sets the repeat count.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutRepeatSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(cRepeat)))

# DWFAPI int FDwfAnalogOutRepeatGet(HDWF hdwf, int idxChannel, int *pcRepeat);
def AnalogOutRepeatGet(hdwf: int, channel_index: int) -> int:
    '''
    Reads the current repeat count.
    '''
    out_cRepeat = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutRepeatGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_cRepeat)))
    return int(out_cRepeat.value)

# DWFAPI int FDwfAnalogOutRepeatStatus(HDWF hdwf, int idxChannel, int *pcRepeat);
def AnalogOutRepeatStatus(hdwf: int, channel_index: int) -> int:
    '''
    Reads the remaining repeat counts. It only returns information from the last
    FDwfAnalogOutStatus function call, it does not read from the device.
    '''
    out_cRepeat = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutRepeatStatus(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_cRepeat)))
    return int(out_cRepeat.value)

# DWFAPI int FDwfAnalogOutRepeatTriggerSet(HDWF hdwf, int idxChannel, int fRepeatTrigger);
def AnalogOutRepeatTriggerSet(hdwf: int, channel_index: int, fRepeatTrigger: int) -> None:
    '''
    Sets the repeat trigger option. To include the trigger in wait-run repeat
    cycles, set fRepeatTrigger to TRUE. It is disabled by default.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutRepeatTriggerSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(fRepeatTrigger)))

# DWFAPI int FDwfAnalogOutRepeatTriggerGet(HDWF hdwf, int idxChannel, int *pfRepeatTrigger);
def AnalogOutRepeatTriggerGet(hdwf: int, channel_index: int) -> int:
    '''
    Verifies if the trigger has been included in wait-run repeat cycles.
    '''
    out_fRepeatTrigger = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutRepeatTriggerGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_fRepeatTrigger)))
    return int(out_fRepeatTrigger.value)

# EExplorer channel 3&4 current/voltage limitation
# DWFAPI int FDwfAnalogOutLimitationInfo(HDWF hdwf, int idxChannel, double *pMin, double *pMax);
def AnalogOutLimitationInfo(hdwf: int, channel_index: int) -> (float, float):
    '''
    Retrieves the limitation range supported by the channel. This option is
    supported on Electronics Explorer Analog Out Channel 3 and 4, Positive and
    Negative Power supplies, to set current or voltage limitation.
    '''
    out_number_min = ctypes.c_double(0.0)
    out_number_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutLimitationInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_number_min), ctypes.byref(out_number_max)))
    return float(out_number_min.value), float(out_number_max.value)

# DWFAPI int FDwfAnalogOutLimitationSet(HDWF hdwf, int idxChannel, double limit);
def AnalogOutLimitationSet(hdwf: int, channel_index: int, limit: float) -> None:
    '''
    Sets the limitation value for the specified channel on the instrument. With
    channel index -1, each enabled Analog Out channel limitation will be
    configured to use the same, new option.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutLimitationSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_double(limit)))

# DWFAPI int FDwfAnalogOutLimitationGet(HDWF hdwf, int idxChannel, double *plimit);
def AnalogOutLimitationGet(hdwf: int, channel_index: int) -> float:
    '''
    Gets the current limitation value for the specified channel on the
    instrument.
    '''
    out_limit = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutLimitationGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_limit)))
    return float(out_limit.value)

# DWFAPI int FDwfAnalogOutModeSet(HDWF hdwf, int idxChannel, DwfAnalogOutMode mode);
def AnalogOutModeSet(hdwf: int, channel_index: int, mode: int) -> None:
    '''
    Set the generator output mode for the specified instrument channel. With
    channel index -1, each enabled Analog Out channel mode will be configured to
    use the same, new option. This option is supported on Electronics Explorer
    Analog Out Channel 3 and 4, Positive and Negative Power supplies, to set
    current or voltage waveform generator mode.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutModeSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(mode)))

# DWFAPI int FDwfAnalogOutModeGet(HDWF hdwf, int idxChannel, DwfAnalogOutMode *pmode);
def AnalogOutModeGet(hdwf: int, channel_index: int) -> int:
    '''
    Retrieves the current generator mode option for the specified instrument
    channel.
    '''
    out_mode = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutModeGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_mode)))
    return int(out_mode.value)

# DWFAPI int FDwfAnalogOutIdleInfo(HDWF hdwf, int idxChannel, int *pfsidle);
def AnalogOutIdleInfo(hdwf: int, channel_index: int) -> int:
    '''
    Returns the supported generator idle output options. They are returned (by
    reference) as a bit field. This bit field can be parsed using the IsBitSet
    Macro. Individual bits are defined using the DwfAnalogOutIdle constants in
    dwf.h.
    '''
    out_fsidle = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutIdleInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_fsidle)))
    return int(out_fsidle.value)

# DWFAPI int FDwfAnalogOutIdleSet(HDWF hdwf, int idxChannel, DwfAnalogOutIdle idle);
def AnalogOutIdleSet(hdwf: int, channel_index: int, idle: int) -> None:
    '''
    Sets the generator idle output for the specified instrument channel. The
    idle output selects the output while not running, Ready, Stopped, Done, or
    Wait states.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutIdleSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(idle)))

# DWFAPI int FDwfAnalogOutIdleGet(HDWF hdwf, int idxChannel, DwfAnalogOutIdle *pidle);
def AnalogOutIdleGet(hdwf: int, channel_index: int) -> int:
    '''
    Retrieves the generator idle output option for the specified instrument
    channel.
    '''
    out_idle = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutIdleGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_idle)))
    return int(out_idle.value)

# DWFAPI int FDwfAnalogOutNodeInfo(HDWF hdwf, int idxChannel, int *pfsnode); // use IsBitSet
def AnalogOutNodeInfo(hdwf: int, channel_index: int) -> int:
    '''
    Returns the supported AnalogOut nodes of the AnalogOut channel. They are
    returned (by reference) as a bit field. This bit field can be parsed using
    the IsBitSet Macro.
    '''
    out_fsnode = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodeInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_fsnode)))
    return int(out_fsnode.value)

# DWFAPI int FDwfAnalogOutNodeEnableSet(HDWF hdwf, int idxChannel, AnalogOutNode node, int fEnable);
def AnalogOutNodeEnableSet(hdwf: int, channel_index: int, node: int, enable: int) -> None:
    '''
    Enables or disables the channel node specified by idxChannel and node. The
    Carrier node enables or disables the channel and AM/FM the modulation. With
    channel index -1, each Analog Out channel enable will be configured to use
    the same, new option.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutNodeEnableSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.c_int(enable)))

# DWFAPI int FDwfAnalogOutNodeEnableGet(HDWF hdwf, int idxChannel, AnalogOutNode node, int *pfEnable);
def AnalogOutNodeEnableGet(hdwf: int, channel_index: int, node: int) -> int:
    '''
    Verifies if a specific channel and node is enabled or disabled.
    '''
    out_enable = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodeEnableGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.byref(out_enable)))
    return int(out_enable.value)

# DWFAPI int FDwfAnalogOutNodeFunctionInfo(HDWF hdwf, int idxChannel, AnalogOutNode node, unsigned int *pfsfunc); // use IsBitSet
def AnalogOutNodeFunctionInfo(hdwf: int, channel_index: int, node: int) -> int:
    '''
    Returns the supported generator function options. They are returned (by
    reference) as a bit field. This bit field can be parsed using the IsBitSet
    Macro. Individual bits are defined using the FUNC constants in dwf.h. These
    are:
    '''
    out_fsfunc = c_uint(0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodeFunctionInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.byref(out_fsfunc)))
    return int(out_fsfunc.value)

# DWFAPI int FDwfAnalogOutNodeFunctionSet(HDWF hdwf, int idxChannel, AnalogOutNode node, FUNC func);
def AnalogOutNodeFunctionSet(hdwf: int, channel_index: int, node: int, func: int) -> None:
    '''
    Sets the generator output function for the specified instrument channel.
    With channel index -1, each enabled Analog Out channel function will be
    configured to use the same, new option.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutNodeFunctionSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.c_int(func)))

# DWFAPI int FDwfAnalogOutNodeFunctionGet(HDWF hdwf, int idxChannel, AnalogOutNode node, FUNC *pfunc);
def AnalogOutNodeFunctionGet(hdwf: int, channel_index: int, node: int) -> int:
    '''
    Retrieves the current generator function option for the specified instrument
    channel.
    '''
    out_func = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodeFunctionGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.byref(out_func)))
    return int(out_func.value)

# DWFAPI int FDwfAnalogOutNodeFrequencyInfo(HDWF hdwf, int idxChannel, AnalogOutNode node, double *phzMin, double *phzMax);
def AnalogOutNodeFrequencyInfo(hdwf: int, channel_index: int, node: int) -> (float, float):
    '''
    Returns the supported frequency range for the instrument. The maximum value
    shows the DAC frequency. The frequency of the generated waveform: repetition
    frequency for standard types and custom data; DAC update for noise type;
    sample rate for play type.
    '''
    out_hz_min = ctypes.c_double(0.0)
    out_hz_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodeFrequencyInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.byref(out_hz_min), ctypes.byref(out_hz_max)))
    return float(out_hz_min.value), float(out_hz_max.value)

# DWFAPI int FDwfAnalogOutNodeFrequencySet(HDWF hdwf, int idxChannel, AnalogOutNode node, double hzFrequency);
def AnalogOutNodeFrequencySet(hdwf: int, channel_index: int, node: int, frequency_in_hz: float) -> None:
    '''
    Sets the frequency. With channel index -1, each enabled Analog Out channel
    frequency will be configured to use the same, new option.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutNodeFrequencySet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.c_double(frequency_in_hz)))

# DWFAPI int FDwfAnalogOutNodeFrequencyGet(HDWF hdwf, int idxChannel, AnalogOutNode node, double *phzFrequency);
def AnalogOutNodeFrequencyGet(hdwf: int, channel_index: int, node: int) -> float:
    '''
    Gets the currently set frequency for the specified channel-node on the
    instrument.
    '''
    out_frequency_in_hz = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodeFrequencyGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.byref(out_frequency_in_hz)))
    return float(out_frequency_in_hz.value)

# Carrier Amplitude or Modulation Index
# DWFAPI int FDwfAnalogOutNodeAmplitudeInfo(HDWF hdwf, int idxChannel, AnalogOutNode node, double *pMin, double *pMax);
def AnalogOutNodeAmplitudeInfo(hdwf: int, channel_index: int, node: int) -> (float, float):
    '''
    Retrieves the amplitude range for the specified channel-node on the
    instrument. The amplitude is expressed in Volt units for carrier and in
    percentage units (modulation index) for AM/FM.
    '''
    out_number_min = ctypes.c_double(0.0)
    out_number_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodeAmplitudeInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.byref(out_number_min), ctypes.byref(out_number_max)))
    return float(out_number_min.value), float(out_number_max.value)

# DWFAPI int FDwfAnalogOutNodeAmplitudeSet(HDWF hdwf, int idxChannel, AnalogOutNode node, double vAmplitude);
def AnalogOutNodeAmplitudeSet(hdwf: int, channel_index: int, node: int, vAmplitude: float) -> None:
    '''
    Sets the amplitude or modulation index for the specified channel-node on the
    instrument. With channel index -1, each enabled Analog Out channel amplitude
    (or modulation index) will be configured to use the same, new option.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutNodeAmplitudeSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.c_double(vAmplitude)))

# DWFAPI int FDwfAnalogOutNodeAmplitudeGet(HDWF hdwf, int idxChannel, AnalogOutNode node, double *pvAmplitude);
def AnalogOutNodeAmplitudeGet(hdwf: int, channel_index: int, node: int) -> float:
    '''
    Gets the currently set amplitude or modulation index for the specified
    channel-node on the instrument.
    '''
    out_vAmplitude = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodeAmplitudeGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.byref(out_vAmplitude)))
    return float(out_vAmplitude.value)

# DWFAPI int FDwfAnalogOutNodeOffsetInfo(HDWF hdwf, int idxChannel, AnalogOutNode node, double *pMin, double *pMax);
def AnalogOutNodeOffsetInfo(hdwf: int, channel_index: int, node: int) -> (float, float):
    '''
    Retrieves available the offset range. For carrier node in units of volts,
    and in percentage units for AM/FM nodes
    '''
    out_number_min = ctypes.c_double(0.0)
    out_number_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodeOffsetInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.byref(out_number_min), ctypes.byref(out_number_max)))
    return float(out_number_min.value), float(out_number_max.value)

# DWFAPI int FDwfAnalogOutNodeOffsetSet(HDWF hdwf, int idxChannel, AnalogOutNode node, double vOffset);
def AnalogOutNodeOffsetSet(hdwf: int, channel_index: int, node: int, vOffset: float) -> None:
    '''
    Sets the offset value for the specified channel-node on the instrument. With
    channel index -1, each enabled Analog Out channel offset will be configured
    to use the same, new option.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutNodeOffsetSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.c_double(vOffset)))

# DWFAPI int FDwfAnalogOutNodeOffsetGet(HDWF hdwf, int idxChannel, AnalogOutNode node, double *pvOffset);
def AnalogOutNodeOffsetGet(hdwf: int, channel_index: int, node: int) -> float:
    '''
    Gets the current offset value for the specified channel-node on the
    instrument.
    '''
    out_vOffset = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodeOffsetGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.byref(out_vOffset)))
    return float(out_vOffset.value)

# DWFAPI int FDwfAnalogOutNodeSymmetryInfo(HDWF hdwf, int idxChannel, AnalogOutNode node, double *ppercentageMin, double *ppercentageMax);
def AnalogOutNodeSymmetryInfo(hdwf: int, channel_index: int, node: int) -> (float, float):
    '''
    Obtains the symmetry (or duty cycle) range (0 … 100). This symmetry is
    supported for standard signal types. It the pulse duration divided by the
    pulse period.
    '''
    out_percentage_min = ctypes.c_double(0.0)
    out_percentage_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodeSymmetryInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.byref(out_percentage_min), ctypes.byref(out_percentage_max)))
    return float(out_percentage_min.value), float(out_percentage_max.value)

# DWFAPI int FDwfAnalogOutNodeSymmetrySet(HDWF hdwf, int idxChannel, AnalogOutNode node, double percentageSymmetry);
def AnalogOutNodeSymmetrySet(hdwf: int, channel_index: int, node: int, percentage_symmetry: float) -> None:
    '''
    Sets the symmetry (or duty cycle) for the specified channel-node on the
    instrument. With channel index -1, each enabled Analog Out channel symmetry
    will be configured to use the same, new option.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutNodeSymmetrySet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.c_double(percentage_symmetry)))

# DWFAPI int FDwfAnalogOutNodeSymmetryGet(HDWF hdwf, int idxChannel, AnalogOutNode node, double *ppercentageSymmetry);
def AnalogOutNodeSymmetryGet(hdwf: int, channel_index: int, node: int) -> float:
    '''
    Gets the currently set symmetry (or duty cycle) for the specified channel-
    node of the instrument.
    '''
    out_percentage_symmetry = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodeSymmetryGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.byref(out_percentage_symmetry)))
    return float(out_percentage_symmetry.value)

# DWFAPI int FDwfAnalogOutNodePhaseInfo(HDWF hdwf, int idxChannel, AnalogOutNode node, double *pdegreeMin, double *pdegreeMax);
def AnalogOutNodePhaseInfo(hdwf: int, channel_index: int, node: int) -> (float, float):
    '''
    Retrieves the phase range (in degrees 0 … 360) for the specified channel-
    node of the instrument.
    '''
    out_degree_min = ctypes.c_double(0.0)
    out_degree_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodePhaseInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.byref(out_degree_min), ctypes.byref(out_degree_max)))
    return float(out_degree_min.value), float(out_degree_max.value)

# DWFAPI int FDwfAnalogOutNodePhaseSet(HDWF hdwf, int idxChannel, AnalogOutNode node, double degreePhase);
def AnalogOutNodePhaseSet(hdwf: int, channel_index: int, node: int, degree_phase: float) -> None:
    '''
    Sets the phase for the specified channel-node on the instrument. With
    channel index -1, each enabled Analog Out channel phase will be configured
    to use the same, new option.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutNodePhaseSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.c_double(degree_phase)))

# DWFAPI int FDwfAnalogOutNodePhaseGet(HDWF hdwf, int idxChannel, AnalogOutNode node, double *pdegreePhase);
def AnalogOutNodePhaseGet(hdwf: int, channel_index: int, node: int) -> float:
    '''
    Gets the current phase for the specified channel-node on the instrument.
    '''
    out_degree_phase = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodePhaseGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.byref(out_degree_phase)))
    return float(out_degree_phase.value)

# DWFAPI int FDwfAnalogOutNodeDataInfo(HDWF hdwf, int idxChannel, AnalogOutNode node, int *pnSamplesMin, int *pnSamplesMax);
def AnalogOutNodeDataInfo(hdwf: int, channel_index: int, node: int) -> (int, int):
    '''
    Retrieves the minimum and maximum number of samples allowed for custom data
    generation.
    '''
    out_samples_min = ctypes.c_int(0)
    out_samples_max = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodeDataInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.byref(out_samples_min), ctypes.byref(out_samples_max)))
    return int(out_samples_min.value), int(out_samples_max.value)

# DWFAPI int FDwfAnalogOutNodeDataSet(HDWF hdwf, int idxChannel, AnalogOutNode node, double *rgdData, int cdData);
def AnalogOutNodeDataSet(hdwf: int, channel_index: int, node: int, cd_data: int) -> float:
    '''
    Set the custom data or to prefill the buffer with play samples. The samples
    are double precision floating point values (rgdData) normalized to ±1.
    '''
    out_rgdData = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodeDataSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.c_int(cd_data), ctypes.byref(out_rgdData)))
    return float(out_rgdData.value)

# needed for EExplorer, not used for ADiscovery
# DWFAPI int FDwfAnalogOutCustomAMFMEnableSet(HDWF hdwf, int idxChannel, int fEnable);
# Warning no docs found for FDwfAnalogOutCustomAMFMEnableSet
def AnalogOutCustomAMFMEnableSet(hdwf: int, channel_index: int, enable: int) -> None:
    _ThrowIfError(_dwf.FDwfAnalogOutCustomAMFMEnableSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(enable)))

# DWFAPI int FDwfAnalogOutCustomAMFMEnableGet(HDWF hdwf, int idxChannel, int *pfEnable);
# Warning no docs found for FDwfAnalogOutCustomAMFMEnableGet
def AnalogOutCustomAMFMEnableGet(hdwf: int, channel_index: int) -> int:
    out_enable = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutCustomAMFMEnableGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_enable)))
    return int(out_enable.value)

#------------------------------------------------------------------------------
# Control:
#------------------------------------------------------------------------------

# DWFAPI int FDwfAnalogOutReset(HDWF hdwf, int idxChannel);
def AnalogOutReset(hdwf: int, channel_index: int) -> None:
    '''
    Resets and configures (by default, having auto configure enabled) all
    AnalogOut instrument parameters to default values for the specified channel.
    To reset instrument parameters across all channels, set idxChannel to -1.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutReset(ctypes.c_int(hdwf), ctypes.c_int(channel_index)))

# DWFAPI int FDwfAnalogOutConfigure(HDWF hdwf, int idxChannel, int fStart);
def AnalogOutConfigure(hdwf: int, channel_index: int, fStart: int) -> None:
    '''
    Starts or stops the instrument. Value 3 will apply the configuration
    dynamically without changing the state of the instrument. With channel index
    -1, each enabled Analog Out channel will be configured.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutConfigure(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(fStart)))

# DWFAPI int FDwfAnalogOutStatus(HDWF hdwf, int idxChannel, DwfState *psts);
def AnalogOutStatus(hdwf: int, channel_index: int) -> int:
    '''
    Checks the state of the instrument.
    '''
    out_instrument_state = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutStatus(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_instrument_state)))
    return int(out_instrument_state.value)

# DWFAPI int FDwfAnalogOutNodePlayStatus(HDWF hdwf, int idxChannel, AnalogOutNode node, int *cdDataFree, int *cdDataLost, int *cdDataCorrupted);
def AnalogOutNodePlayStatus(hdwf: int, channel_index: int, node: int) -> (int, int, int):
    '''
    Retrieves information about the play process. The data lost occurs when the
    device generator is faster than the sample send process from the PC. In this
    case, the device buffer gets emptied and generated samples are repeated.
    Corrupt samples are a warning that the buffer might have been emptied while
    samples were sent to the device. In this case, try optimizing the loop for
    faster execution; or reduce the frequency or run time to be less or equal to
    the device buffer size (run time <= buffer size/frequency).
    '''
    out_cdDataFree = ctypes.c_int(0)
    out_cdDataLost = ctypes.c_int(0)
    out_cdDataCorrupted = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodePlayStatus(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.byref(out_cdDataFree), ctypes.byref(out_cdDataLost), ctypes.byref(out_cdDataCorrupted)))
    return int(out_cdDataFree.value), int(out_cdDataLost.value), int(out_cdDataCorrupted.value)

# DWFAPI int FDwfAnalogOutNodePlayData(HDWF hdwf, int idxChannel, AnalogOutNode node, double *rgdData, int cdData);
def AnalogOutNodePlayData(hdwf: int, channel_index: int, node: int, cd_data: int) -> float:
    '''
    Sends new data samples for play mode. Before starting the Analog Out
    instrument, prefill the device buffer with the first set of samples using
    the AnalogOutNodeDataSet function. In the loop of sending the following
    samples, first call AnalogOutStatus to read the information from the device,
    then AnalogOutPlayStatus to find out how many new samples can be sent, then
    send the samples with AnalogOutPlayData.
    '''
    out_rgdData = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutNodePlayData(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node), ctypes.c_int(cd_data), ctypes.byref(out_rgdData)))
    return float(out_rgdData.value)

###############################################################################
# ANALOG IO INSTRUMENT FUNCTIONS
###############################################################################

#------------------------------------------------------------------------------
# Control:
#------------------------------------------------------------------------------

# DWFAPI int FDwfAnalogIOReset(HDWF hdwf);
def AnalogIOReset(hdwf: int) -> None:
    '''
    Resets and configures (by default, having auto configure enabled) all
    AnalogIO instrument parameters to default values.
    '''
    _ThrowIfError(_dwf.FDwfAnalogIOReset(ctypes.c_int(hdwf)))

# DWFAPI int FDwfAnalogIOConfigure(HDWF hdwf);
def AnalogIOConfigure(hdwf: int) -> None:
    '''
    Configures the instrument.
    '''
    _ThrowIfError(_dwf.FDwfAnalogIOConfigure(ctypes.c_int(hdwf)))

# DWFAPI int FDwfAnalogIOStatus(HDWF hdwf);
def AnalogIOStatus(hdwf: int) -> None:
    '''
    Reads the status of the device and stores it internally. The following
    status functions will return the information that was read from the device
    when the function above was called.
    '''
    _ThrowIfError(_dwf.FDwfAnalogIOStatus(ctypes.c_int(hdwf)))

#------------------------------------------------------------------------------
# Configure:
#------------------------------------------------------------------------------

# DWFAPI int FDwfAnalogIOEnableInfo(HDWF hdwf, int *pfSet, int *pfStatus);
def AnalogIOEnableInfo(hdwf: int) -> (int, int):
    '''
    Verifies if Master Enable Setting and/or Master Enable Status are supported
    for the AnalogIO instrument. The Master Enable setting is essentially a
    software switch that “enables” or “turns on” the AnalogIO channels. If
    supported, the status of this Master Enable switch (Enabled/Disabled) can be
    queried by calling FDwfAnalogIOEnableStatus.
    '''
    out_fSet = ctypes.c_int(0)
    out_fStatus = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogIOEnableInfo(ctypes.c_int(hdwf), ctypes.byref(out_fSet), ctypes.byref(out_fStatus)))
    return int(out_fSet.value), int(out_fStatus.value)

# DWFAPI int FDwfAnalogIOEnableSet(HDWF hdwf, int fMasterEnable);
def AnalogIOEnableSet(hdwf: int, master_enable: int) -> None:
    '''
    Sets the master enable switch.
    '''
    _ThrowIfError(_dwf.FDwfAnalogIOEnableSet(ctypes.c_int(hdwf), ctypes.c_int(master_enable)))

# DWFAPI int FDwfAnalogIOEnableGet(HDWF hdwf, int *pfMasterEnable);
def AnalogIOEnableGet(hdwf: int) -> int:
    '''
    Returns the current state of the master enable switch. This is not obtained
    from the device.
    '''
    out_master_enable = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogIOEnableGet(ctypes.c_int(hdwf), ctypes.byref(out_master_enable)))
    return int(out_master_enable.value)

# DWFAPI int FDwfAnalogIOEnableStatus(HDWF hdwf, int *pfMasterEnable);
def AnalogIOEnableStatus(hdwf: int) -> int:
    '''
    Returns the master enable status (if the device supports it). This can be a
    switch on the board or an overcurrent protection circuit state.
    '''
    out_master_enable = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogIOEnableStatus(ctypes.c_int(hdwf), ctypes.byref(out_master_enable)))
    return int(out_master_enable.value)

# DWFAPI int FDwfAnalogIOChannelCount(HDWF hdwf, int *pnChannel);
def AnalogIOChannelCount(hdwf: int) -> int:
    '''
    Returns the number of AnalogIO channels available on the device.
    '''
    out_nChannel = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogIOChannelCount(ctypes.c_int(hdwf), ctypes.byref(out_nChannel)))
    return int(out_nChannel.value)

# DWFAPI int FDwfAnalogIOChannelName(HDWF hdwf, int idxChannel, char szName[32], char szLabel[16]);
def AnalogIOChannelName(hdwf: int, channel_index: int) -> (str, str):
    '''
    Returns the name (long text) and label (short text, printed on the device) for a channel
    '''
    out_name_str = ctypes.create_string_buffer(32)
    out_label_str = ctypes.create_string_buffer(16)
    _ThrowIfError(_dwf.FDwfAnalogIOChannelName(ctypes.c_int(hdwf), ctypes.c_int(channel_index), types.byref(out_name_str), types.byref(out_label_str)))
    return str(out_name_str.value.decode('utf-8')), str(out_label_str.value.decode('utf-8'))

# DWFAPI int FDwfAnalogIOChannelInfo(HDWF hdwf, int idxChannel, int *pnNodes);
def AnalogIOChannelInfo(hdwf: int, channel_index: int) -> int:
    '''
    Returns the number of nodes associated with the specified channel.
    '''
    out_nNodes = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogIOChannelInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_nNodes)))
    return int(out_nNodes.value)

# DWFAPI int FDwfAnalogIOChannelNodeName(HDWF hdwf, int idxChannel, int idxNode, char szNodeName[32], char szNodeUnits[16]);
def AnalogIOChannelNodeName(hdwf: int, channel_index: int, node_index: int) -> (str, str):
    '''
    Returns the node name ("Voltage", "Current" ...) and units ("V", "A") for an Analog I/O node.
    '''
    out_node_name = ctypes.create_string_buffer(32)
    out_node_units_str = ctypes.create_string_buffer(16)
    _ThrowIfError(_dwf.FDwfAnalogIOChannelNodeName(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node_index), types.byref(out_node_name), types.byref(out_node_units_str)))
    return str(out_node_name.value.decode('utf-8')), str(out_node_units_str.value.decode('utf-8'))

# DWFAPI int FDwfAnalogIOChannelNodeInfo(HDWF hdwf, int idxChannel, int idxNode, ANALOGIO *panalogio);
def AnalogIOChannelNodeInfo(hdwf: int, channel_index: int, node_index: int) -> int:
    '''
    Returns the supported channel nodes. They are returned (by reference) as a
    bit field. This bit field can be parsed using the IsBitSet Macro. Individual
    bits are defined using the ANALOGIO constants in dwf.h. The acquisition mode
    selects one of the following modes, ANALOGIO:
    '''
    out_analogio = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogIOChannelNodeInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node_index), ctypes.byref(out_analogio)))
    return int(out_analogio.value)

# DWFAPI int FDwfAnalogIOChannelNodeSetInfo(HDWF hdwf, int idxChannel, int idxNode, double *pmin, double *pmax, int *pnSteps);
def AnalogIOChannelNodeSetInfo(hdwf: int, channel_index: int, node_index: int) -> (float, float, int):
    '''
    Returns node value limits. Since a Node can represent many things (Power
    supply, Temperature sensor, etc.), the Minimum, Maximum, and Steps
    parameters also represent different types of values. In broad terms, the
    (Maximum – Minimum)/Steps = the number of specific input/output values.
    FDwfAnalogIOChannelNodeInfo returns the type of values to expect and
    FDwfAnalogIOChannelNodeName returns the units of these values.
    '''
    out_min = ctypes.c_double(0.0)
    out_max = ctypes.c_double(0.0)
    out_num_steps = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogIOChannelNodeSetInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node_index), ctypes.byref(out_min), ctypes.byref(out_max), ctypes.byref(out_num_steps)))
    return float(out_min.value), float(out_max.value), int(out_num_steps.value)

# DWFAPI int FDwfAnalogIOChannelNodeSet(HDWF hdwf, int idxChannel, int idxNode, double value);
def AnalogIOChannelNodeSet(hdwf: int, channel_index: int, node_index: int, value: float) -> None:
    '''
    Sets the node value for the specified node on the specified channel.
    '''
    _ThrowIfError(_dwf.FDwfAnalogIOChannelNodeSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node_index), ctypes.c_double(value)))

# DWFAPI int FDwfAnalogIOChannelNodeGet(HDWF hdwf, int idxChannel, int idxNode, double *pvalue);
def AnalogIOChannelNodeGet(hdwf: int, channel_index: int, node_index: int) -> float:
    '''
    Returns the currently set value of the node on the specified channel.
    '''
    out_value = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogIOChannelNodeGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node_index), ctypes.byref(out_value)))
    return float(out_value.value)

# DWFAPI int FDwfAnalogIOChannelNodeStatusInfo(HDWF hdwf, int idxChannel, int idxNode, double *pmin, double *pmax, int *pnSteps);
def AnalogIOChannelNodeStatusInfo(hdwf: int, channel_index: int, node_index: int) -> (float, float, int):
    '''
    Returns node the range of reading values available for the specified node on
    the specified channel.
    '''
    out_min = ctypes.c_double(0.0)
    out_max = ctypes.c_double(0.0)
    out_num_steps = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogIOChannelNodeStatusInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node_index), ctypes.byref(out_min), ctypes.byref(out_max), ctypes.byref(out_num_steps)))
    return float(out_min.value), float(out_max.value), int(out_num_steps.value)

# DWFAPI int FDwfAnalogIOChannelNodeStatus(HDWF hdwf, int idxChannel, int idxNode, double *pvalue);
def AnalogIOChannelNodeStatus(hdwf: int, channel_index: int, node_index: int) -> float:
    '''
    Returns the value reading of the node.
    '''
    out_value = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogIOChannelNodeStatus(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(node_index), ctypes.byref(out_value)))
    return float(out_value.value)

###############################################################################
# DIGITAL IO INSTRUMENT FUNCTIONS
###############################################################################

#------------------------------------------------------------------------------
# Control:
#------------------------------------------------------------------------------

# DWFAPI int FDwfDigitalIOReset(HDWF hdwf);
def DigitalIOReset(hdwf: int) -> None:
    '''
    Resets and configures (by default, having auto configure enabled) all
    DigitalIO instrument parameters to default values. It sets the output
    enables to zero (tri-state), output value to zero, and configures the
    DigitalIO instrument
    '''
    _ThrowIfError(_dwf.FDwfDigitalIOReset(ctypes.c_int(hdwf)))

# DWFAPI int FDwfDigitalIOConfigure(HDWF hdwf);
def DigitalIOConfigure(hdwf: int) -> None:
    '''
    Configures the DigitalIO instrument. This doesn’t have to be used if
    AutoConfiguration is enabled.
    '''
    _ThrowIfError(_dwf.FDwfDigitalIOConfigure(ctypes.c_int(hdwf)))

# DWFAPI int FDwfDigitalIOStatus(HDWF hdwf);
def DigitalIOStatus(hdwf: int) -> None:
    '''
    Reads the status and input values, of the device DigitalIO to the PC. The
    status and values are accessed from the FDwfDigitalIOInputStatus function.
    '''
    _ThrowIfError(_dwf.FDwfDigitalIOStatus(ctypes.c_int(hdwf)))

#------------------------------------------------------------------------------
# Configure:
#------------------------------------------------------------------------------

# DWFAPI int FDwfDigitalIOOutputEnableInfo(HDWF hdwf, unsigned int *pfsOutputEnableMask);
def DigitalIOOutputEnableInfo(hdwf: int) -> int:
    '''
    Returns the output enable mask (bit set) that can be used on this device.
    These are the pins that can be used as outputs on the device.
    '''
    out_fsOutputEnableMask = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalIOOutputEnableInfo(ctypes.c_int(hdwf), ctypes.byref(out_fsOutputEnableMask)))
    return int(out_fsOutputEnableMask.value)

# DWFAPI int FDwfDigitalIOOutputEnableSet(HDWF hdwf, unsigned int fsOutputEnable);
def DigitalIOOutputEnableSet(hdwf: int, fsOutputEnable: int) -> None:
    '''
    Enables specific pins for output. This is done by setting bits in the
    fsOutEnable bit field (1 for enabled, 0 for disabled).
    '''
    _ThrowIfError(_dwf.FDwfDigitalIOOutputEnableSet(ctypes.c_int(hdwf), ctypes.c_uint(fsOutputEnable)))

# DWFAPI int FDwfDigitalIOOutputEnableGet(HDWF hdwf, unsigned int *pfsOutputEnable);
def DigitalIOOutputEnableGet(hdwf: int) -> int:
    '''
    Returns a bit field that specifies which output pins have been enabled.
    '''
    out_fsOutputEnable = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalIOOutputEnableGet(ctypes.c_int(hdwf), ctypes.byref(out_fsOutputEnable)))
    return int(out_fsOutputEnable.value)

# DWFAPI int FDwfDigitalIOOutputInfo(HDWF hdwf, unsigned int *pfsOutputMask);
def DigitalIOOutputInfo(hdwf: int) -> int:
    '''
    Returns the settable output value mask (bit set) that can be used on this
    device.
    '''
    out_fsOutputMask = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalIOOutputInfo(ctypes.c_int(hdwf), ctypes.byref(out_fsOutputMask)))
    return int(out_fsOutputMask.value)

# DWFAPI int FDwfDigitalIOOutputSet(HDWF hdwf, unsigned int fsOutput);
def DigitalIOOutputSet(hdwf: int, fsOutput: int) -> None:
    '''
    Sets the output logic value on all output pins.
    '''
    _ThrowIfError(_dwf.FDwfDigitalIOOutputSet(ctypes.c_int(hdwf), ctypes.c_uint(fsOutput)))

# DWFAPI int FDwfDigitalIOOutputGet(HDWF hdwf, unsigned int *pfsOutput);
def DigitalIOOutputGet(hdwf: int) -> int:
    '''
    Returns the currently set output values across all output pins.
    '''
    out_fsOutput = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalIOOutputGet(ctypes.c_int(hdwf), ctypes.byref(out_fsOutput)))
    return int(out_fsOutput.value)

# DWFAPI int FDwfDigitalIOInputInfo(HDWF hdwf, unsigned int *pfsInputMask);
def DigitalIOInputInfo(hdwf: int) -> int:
    '''
    returns the readable input value mask (bit set) that can be used on the
    device.
    '''
    out_fsInputMask = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalIOInputInfo(ctypes.c_int(hdwf), ctypes.byref(out_fsInputMask)))
    return int(out_fsInputMask.value)

# DWFAPI int FDwfDigitalIOInputStatus(HDWF hdwf, unsigned int *pfsInput);
def DigitalIOInputStatus(hdwf: int) -> int:
    '''
    Returns the input states of all I/O pins. Before calling the function above,
    call the FDwfDigitalIOStatus function to read the Digital I/O states from
    the device.
    '''
    out_fsInput = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalIOInputStatus(ctypes.c_int(hdwf), ctypes.byref(out_fsInput)))
    return int(out_fsInput.value)

# DWFAPI int FDwfDigitalIOOutputEnableInfo64(HDWF hdwf, unsigned long long *pfsOutputEnableMask);
# Warning no docs found for FDwfDigitalIOOutputEnableInfo64
def DigitalIOOutputEnableInfo64(hdwf: int) -> int:
    out_fsOutputEnableMask = c_ulonglong(0)
    _ThrowIfError(_dwf.FDwfDigitalIOOutputEnableInfo64(ctypes.c_int(hdwf), ctypes.byref(out_fsOutputEnableMask)))
    return int(out_fsOutputEnableMask.value)

# DWFAPI int FDwfDigitalIOOutputEnableSet64(HDWF hdwf, unsigned long long fsOutputEnable);
# Warning no docs found for FDwfDigitalIOOutputEnableSet64
def DigitalIOOutputEnableSet64(hdwf: int, fsOutputEnable: int) -> None:
    _ThrowIfError(_dwf.FDwfDigitalIOOutputEnableSet64(ctypes.c_int(hdwf), ctypes.c_ulonglong(fsOutputEnable)))

# DWFAPI int FDwfDigitalIOOutputEnableGet64(HDWF hdwf, unsigned long long *pfsOutputEnable);
# Warning no docs found for FDwfDigitalIOOutputEnableGet64
def DigitalIOOutputEnableGet64(hdwf: int) -> int:
    out_fsOutputEnable = c_ulonglong(0)
    _ThrowIfError(_dwf.FDwfDigitalIOOutputEnableGet64(ctypes.c_int(hdwf), ctypes.byref(out_fsOutputEnable)))
    return int(out_fsOutputEnable.value)

# DWFAPI int FDwfDigitalIOOutputInfo64(HDWF hdwf, unsigned long long *pfsOutputMask);
# Warning no docs found for FDwfDigitalIOOutputInfo64
def DigitalIOOutputInfo64(hdwf: int) -> int:
    out_fsOutputMask = c_ulonglong(0)
    _ThrowIfError(_dwf.FDwfDigitalIOOutputInfo64(ctypes.c_int(hdwf), ctypes.byref(out_fsOutputMask)))
    return int(out_fsOutputMask.value)

# DWFAPI int FDwfDigitalIOOutputSet64(HDWF hdwf, unsigned long long fsOutput);
# Warning no docs found for FDwfDigitalIOOutputSet64
def DigitalIOOutputSet64(hdwf: int, fsOutput: int) -> None:
    _ThrowIfError(_dwf.FDwfDigitalIOOutputSet64(ctypes.c_int(hdwf), ctypes.c_ulonglong(fsOutput)))

# DWFAPI int FDwfDigitalIOOutputGet64(HDWF hdwf, unsigned long long *pfsOutput);
# Warning no docs found for FDwfDigitalIOOutputGet64
def DigitalIOOutputGet64(hdwf: int) -> int:
    out_fsOutput = c_ulonglong(0)
    _ThrowIfError(_dwf.FDwfDigitalIOOutputGet64(ctypes.c_int(hdwf), ctypes.byref(out_fsOutput)))
    return int(out_fsOutput.value)

# DWFAPI int FDwfDigitalIOInputInfo64(HDWF hdwf, unsigned long long *pfsInputMask);
# Warning no docs found for FDwfDigitalIOInputInfo64
def DigitalIOInputInfo64(hdwf: int) -> int:
    out_fsInputMask = c_ulonglong(0)
    _ThrowIfError(_dwf.FDwfDigitalIOInputInfo64(ctypes.c_int(hdwf), ctypes.byref(out_fsInputMask)))
    return int(out_fsInputMask.value)

# DWFAPI int FDwfDigitalIOInputStatus64(HDWF hdwf, unsigned long long *pfsInput);
# Warning no docs found for FDwfDigitalIOInputStatus64
def DigitalIOInputStatus64(hdwf: int) -> int:
    out_fsInput = c_ulonglong(0)
    _ThrowIfError(_dwf.FDwfDigitalIOInputStatus64(ctypes.c_int(hdwf), ctypes.byref(out_fsInput)))
    return int(out_fsInput.value)

###############################################################################
# DIGITAL IN INSTRUMENT FUNCTIONS
###############################################################################

# Control and status:
# DWFAPI int FDwfDigitalInReset(HDWF hdwf);
def DigitalInReset(hdwf: int) -> None:
    '''
    Resets and configures (by default, having auto configure enabled) all
    DigitalIn instrument parameters to default values.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInReset(ctypes.c_int(hdwf)))

# DWFAPI int FDwfDigitalInConfigure(HDWF hdwf, int fReconfigure, int fStart);
def DigitalInConfigure(hdwf: int, reconfigure: int, fStart: int) -> None:
    '''
    Configures the instrument and start or stop the acquisition. To reset the
    Auto trigger timeout, set fReconfigure to TRUE.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInConfigure(ctypes.c_int(hdwf), ctypes.c_int(reconfigure), ctypes.c_int(fStart)))

# DWFAPI int FDwfDigitalInStatus(HDWF hdwf, int fReadData, DwfState *psts);
def DigitalInStatus(hdwf: int, fReadData: int) -> int:
    '''
    Checks the state of the instrument. To read the data from the device, set
    fReadData to TRUE. For single acquisition mode, the data will be read only
    when the acquisition is finished.
    '''
    out_instrument_state = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInStatus(ctypes.c_int(hdwf), ctypes.c_int(fReadData), ctypes.byref(out_instrument_state)))
    return int(out_instrument_state.value)

# DWFAPI int FDwfDigitalInStatusSamplesLeft(HDWF hdwf, int *pcSamplesLeft);
def DigitalInStatusSamplesLeft(hdwf: int) -> int:
    '''
    Retrieves the number of samples left in the acquisition.
    '''
    out_cSamplesLeft = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInStatusSamplesLeft(ctypes.c_int(hdwf), ctypes.byref(out_cSamplesLeft)))
    return int(out_cSamplesLeft.value)

# DWFAPI int FDwfDigitalInStatusSamplesValid(HDWF hdwf, int *pcSamplesValid);
def DigitalInStatusSamplesValid(hdwf: int) -> int:
    '''
    Retrieves the number of valid/acquired data samples.
    '''
    out_samples_valid = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInStatusSamplesValid(ctypes.c_int(hdwf), ctypes.byref(out_samples_valid)))
    return int(out_samples_valid.value)

# DWFAPI int FDwfDigitalInStatusIndexWrite(HDWF hdwf, int *pidxWrite);
def DigitalInStatusIndexWrite(hdwf: int) -> int:
    '''
    Retrieves the buffer write pointer. This is needed in ScanScreen acquisition
    mode to display the scan bar.
    '''
    out_write_index = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInStatusIndexWrite(ctypes.c_int(hdwf), ctypes.byref(out_write_index)))
    return int(out_write_index.value)

# DWFAPI int FDwfDigitalInStatusAutoTriggered(HDWF hdwf, int *pfAuto);
def DigitalInStatusAutoTriggered(hdwf: int) -> int:
    '''
    Verifies if the acquisition is auto triggered.
    '''
    out_auto_triggered = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInStatusAutoTriggered(ctypes.c_int(hdwf), ctypes.byref(out_auto_triggered)))
    return int(out_auto_triggered.value)

# DWFAPI int FDwfDigitalInStatusData(HDWF hdwf, void *rgData, int countOfDataBytes);
def DigitalInStatusData(hdwf: int, countOfDataBytes: int) -> int:
    '''
    Retrieves the acquired data samples from the instrument. It copies the data
    samples to the provided buffer. The sample format is specified by
    FDwfDigitalInSampleFormatSet function.
    '''
    out_rgData = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInStatusData(ctypes.c_int(hdwf), ctypes.c_int(countOfDataBytes), ctypes.byref(out_rgData)))
    return int(out_rgData.value)

# DWFAPI int FDwfDigitalInStatusData2(HDWF hdwf, void *rgData, int idxSample, int countOfDataBytes);
def DigitalInStatusData2(hdwf: int, idxSample: int, countOfDataBytes: int) -> int:
    '''
    Retrieves the acquired data samples from the instrument. It copies the data
    samples to the provided buffer. The sample format is specified by
    FDwfDigitalInSampleFormatSet function.
    '''
    out_rgData = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInStatusData2(ctypes.c_int(hdwf), ctypes.c_int(idxSample), ctypes.c_int(countOfDataBytes), ctypes.byref(out_rgData)))
    return int(out_rgData.value)

# DWFAPI int FDwfDigitalInStatusNoise2(HDWF hdwf, void *rgData, int idxSample, int countOfDataBytes);
# Warning no docs found for FDwfDigitalInStatusNoise2
def DigitalInStatusNoise2(hdwf: int, idxSample: int, countOfDataBytes: int) -> int:
    out_rgData = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInStatusNoise2(ctypes.c_int(hdwf), ctypes.c_int(idxSample), ctypes.c_int(countOfDataBytes), ctypes.byref(out_rgData)))
    return int(out_rgData.value)

# DWFAPI int FDwfDigitalInStatusRecord(HDWF hdwf, int *pcdDataAvailable, int *pcdDataLost, int *pcdDataCorrupt);
def DigitalInStatusRecord(hdwf: int) -> (int, int, int):
    '''
    Retrieves information about the recording process. The data loss occurs when
    the device acquisition is faster than the read process to PC. In this case,
    the device recording buffer is filled and data samples are overwritten.
    Corrupt samples indicate that the samples have been overwritten by the
    acquisition process during the previous read. In this case, try optimizing
    the loop process for faster execution or reduce the acquisition frequency or
    record length to be less than or equal to the device buffer size (record
    length <= buffer size/frequency).
    '''
    out_cdDataAvailable = ctypes.c_int(0)
    out_cdDataLost = ctypes.c_int(0)
    out_cdDataCorrupt = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInStatusRecord(ctypes.c_int(hdwf), ctypes.byref(out_cdDataAvailable), ctypes.byref(out_cdDataLost), ctypes.byref(out_cdDataCorrupt)))
    return int(out_cdDataAvailable.value), int(out_cdDataLost.value), int(out_cdDataCorrupt.value)

# DWFAPI int FDwfDigitalInStatusTime(HDWF hdwf, unsigned int *psecUtc, unsigned int *ptick, unsigned int *pticksPerSecond);
# Warning no docs found for FDwfDigitalInStatusTime
def DigitalInStatusTime(hdwf: int) -> (int, int, int):
    out_secUtc = c_uint(0)
    out_tick = c_uint(0)
    out_ticksPerSecond = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalInStatusTime(ctypes.c_int(hdwf), ctypes.byref(out_secUtc), ctypes.byref(out_tick), ctypes.byref(out_ticksPerSecond)))
    return int(out_secUtc.value), int(out_tick.value), int(out_ticksPerSecond.value)

#------------------------------------------------------------------------------
# Acquisition configuration:
#------------------------------------------------------------------------------

# DWFAPI int FDwfDigitalInInternalClockInfo(HDWF hdwf, double *phzFreq);
def DigitalInInternalClockInfo(hdwf: int) -> float:
    '''
    Retrieves the internal clock frequency.
    '''
    out_hzFreq = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfDigitalInInternalClockInfo(ctypes.c_int(hdwf), ctypes.byref(out_hzFreq)))
    return float(out_hzFreq.value)

# DWFAPI int FDwfDigitalInClockSourceInfo(HDWF hdwf, int *pfsDwfDigitalInClockSource); // use IsBitSet
def DigitalInClockSourceInfo(hdwf: int) -> int:
    '''
    Returns the supported clock sources for Digital In instrument. They are
    returned (by reference) as a bit field. This bit field can be parsed using
    the IsBitSet Macro. Individual bits are defined using the
    DwfDigitalInClockSource constants in dwf.h:
    '''
    out_fsDwfDigitalInClockSource = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInClockSourceInfo(ctypes.c_int(hdwf), ctypes.byref(out_fsDwfDigitalInClockSource)))
    return int(out_fsDwfDigitalInClockSource.value)

# DWFAPI int FDwfDigitalInClockSourceSet(HDWF hdwf, DwfDigitalInClockSource v);
def DigitalInClockSourceSet(hdwf: int, v: int) -> None:
    '''
    Sets the clock source of instrument.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInClockSourceSet(ctypes.c_int(hdwf), ctypes.c_int(v)))

# DWFAPI int FDwfDigitalInClockSourceGet(HDWF hdwf, DwfDigitalInClockSource *pv);
def DigitalInClockSourceGet(hdwf: int) -> int:
    '''
    Gets the clock source of instrument.
    '''
    out_v = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInClockSourceGet(ctypes.c_int(hdwf), ctypes.byref(out_v)))
    return int(out_v.value)

# DWFAPI int FDwfDigitalInDividerInfo(HDWF hdwf, unsigned int *pdivMax);
def DigitalInDividerInfo(hdwf: int) -> int:
    '''
    Returns the maximum supported clock divider value. This specifies the sample
    rate.
    '''
    out_div_max = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalInDividerInfo(ctypes.c_int(hdwf), ctypes.byref(out_div_max)))
    return int(out_div_max.value)

# DWFAPI int FDwfDigitalInDividerSet(HDWF hdwf, unsigned int div);
def DigitalInDividerSet(hdwf: int, div: int) -> None:
    '''
    Sets the clock divider value.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInDividerSet(ctypes.c_int(hdwf), ctypes.c_uint(div)))

# DWFAPI int FDwfDigitalInDividerGet(HDWF hdwf, unsigned int *pdiv);
def DigitalInDividerGet(hdwf: int) -> int:
    '''
    Gets the configured clock divider value.
    '''
    out_div = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalInDividerGet(ctypes.c_int(hdwf), ctypes.byref(out_div)))
    return int(out_div.value)

# DWFAPI int FDwfDigitalInBitsInfo(HDWF hdwf, int *pnBits); // Returns the number of Digital In bits
def DigitalInBitsInfo(hdwf: int) -> int:
    '''
    Returns the number of Digital In bits.
    '''
    out_number_of_bits = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInBitsInfo(ctypes.c_int(hdwf), ctypes.byref(out_number_of_bits)))
    return int(out_number_of_bits.value)

# DWFAPI int FDwfDigitalInSampleFormatSet(HDWF hdwf, int nBits);  // valid options 8/16/32
def DigitalInSampleFormatSet(hdwf: int, number_of_bits: int) -> None:
    '''
    Sets the sample format, the number of bits starting from least significant
    bit. Valid options are 8, 16, and 32.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInSampleFormatSet(ctypes.c_int(hdwf), ctypes.c_int(number_of_bits)))

# DWFAPI int FDwfDigitalInSampleFormatGet(HDWF hdwf, int *pnBits);
def DigitalInSampleFormatGet(hdwf: int) -> int:
    '''
    Returns the configured sample format.
    '''
    out_number_of_bits = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInSampleFormatGet(ctypes.c_int(hdwf), ctypes.byref(out_number_of_bits)))
    return int(out_number_of_bits.value)

# DWFAPI int FDwfDigitalInInputOrderSet(HDWF hdwf, bool fDioFirst); // for Digital Discovery
def DigitalInInputOrderSet(hdwf: int, fDioFirst: int) -> None:
    '''
    Configures the order of values stored in the sampling array. If fDIOFirst =
    true DIO24..39 are placed at
    '''
    _ThrowIfError(_dwf.FDwfDigitalInInputOrderSet(ctypes.c_int(hdwf), ctypes.c_int(fDioFirst)))

# DWFAPI int FDwfDigitalInBufferSizeInfo(HDWF hdwf, int *pnSizeMax);
def DigitalInBufferSizeInfo(hdwf: int) -> int:
    '''
    Returns the Digital In maximum buffer size.
    '''
    out_size_max = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInBufferSizeInfo(ctypes.c_int(hdwf), ctypes.byref(out_size_max)))
    return int(out_size_max.value)

# DWFAPI int FDwfDigitalInBufferSizeSet(HDWF hdwf, int nSize);
def DigitalInBufferSizeSet(hdwf: int, nSize: int) -> None:
    '''
    Set the buffer size.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInBufferSizeSet(ctypes.c_int(hdwf), ctypes.c_int(nSize)))

# DWFAPI int FDwfDigitalInBufferSizeGet(HDWF hdwf, int *pnSize);
def DigitalInBufferSizeGet(hdwf: int) -> int:
    '''
    Returns the configured buffer size.
    '''
    out_nSize = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInBufferSizeGet(ctypes.c_int(hdwf), ctypes.byref(out_nSize)))
    return int(out_nSize.value)

# DWFAPI int FDwfDigitalInSampleModeInfo(HDWF hdwf, int *pfsDwfDigitalInSampleMode); // use IsBitSet
def DigitalInSampleModeInfo(hdwf: int) -> int:
    '''
    Returns the supported sample modes. They are returned (by reference) as a
    bit field. This bit field can be parsed using the IsBitSet Macro. Individual
    bits are defined using the DwfDigitalInSampleMode constants in dwf.h:
    '''
    out_fsDwfDigitalInSampleMode = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInSampleModeInfo(ctypes.c_int(hdwf), ctypes.byref(out_fsDwfDigitalInSampleMode)))
    return int(out_fsDwfDigitalInSampleMode.value)

# DWFAPI int FDwfDigitalInSampleModeSet(HDWF hdwf, DwfDigitalInSampleMode v);
def DigitalInSampleModeSet(hdwf: int, v: int) -> None:
    '''
    Set the sample mode.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInSampleModeSet(ctypes.c_int(hdwf), ctypes.c_int(v)))

# DWFAPI int FDwfDigitalInSampleModeGet(HDWF hdwf, DwfDigitalInSampleMode *pv);
def DigitalInSampleModeGet(hdwf: int) -> int:
    '''
    Return the configured sample mode.
    '''
    out_v = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInSampleModeGet(ctypes.c_int(hdwf), ctypes.byref(out_v)))
    return int(out_v.value)

# DWFAPI int FDwfDigitalInSampleSensibleSet(HDWF hdwf, unsigned int fs);
def DigitalInSampleSensibleSet(hdwf: int, fs: int) -> None:
    '''
    Selects the signals to be used for data compression in record acquisition
    mode.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInSampleSensibleSet(ctypes.c_int(hdwf), ctypes.c_uint(fs)))

# DWFAPI int FDwfDigitalInSampleSensibleGet(HDWF hdwf, unsigned int *pfs);
def DigitalInSampleSensibleGet(hdwf: int) -> int:
    '''
    Retrieves the signals being used for data compression in record acquisition
    mode.
    '''
    out_fs = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalInSampleSensibleGet(ctypes.c_int(hdwf), ctypes.byref(out_fs)))
    return int(out_fs.value)

# DWFAPI int FDwfDigitalInAcquisitionModeInfo(HDWF hdwf, int *pfsacqmode); // use IsBitSet
def DigitalInAcquisitionModeInfo(hdwf: int) -> int:
    '''
    Returns the supported DigitalIn acquisition modes. They are returned (by
    reference) as a bit field. This bit field can be parsed using the IsBitSet
    Macro. Individual bits are defined using the ACQMODE constants in DWF.h. The
    acquisition mode selects one of the following modes, ACQMODE:
    '''
    out_fsacqmode = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInAcquisitionModeInfo(ctypes.c_int(hdwf), ctypes.byref(out_fsacqmode)))
    return int(out_fsacqmode.value)

# DWFAPI int FDwfDigitalInAcquisitionModeSet(HDWF hdwf, ACQMODE acqmode);
def DigitalInAcquisitionModeSet(hdwf: int, acqmode: int) -> None:
    '''
    Sets the acquisition mode.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInAcquisitionModeSet(ctypes.c_int(hdwf), ctypes.c_int(acqmode)))

# DWFAPI int FDwfDigitalInAcquisitionModeGet(HDWF hdwf, ACQMODE *pacqmode);
def DigitalInAcquisitionModeGet(hdwf: int) -> int:
    '''
    Retrieves the acquisition mode.
    '''
    out_acqmode = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInAcquisitionModeGet(ctypes.c_int(hdwf), ctypes.byref(out_acqmode)))
    return int(out_acqmode.value)

#------------------------------------------------------------------------------
# Trigger configuration:
#------------------------------------------------------------------------------

# DWFAPI int FDwfDigitalInTriggerSourceSet(HDWF hdwf, TRIGSRC trigsrc);
def DigitalInTriggerSourceSet(hdwf: int, trigger_source: int) -> None:
    '''
    Sets the trigger source for the instrument.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInTriggerSourceSet(ctypes.c_int(hdwf), ctypes.c_int(trigger_source)))

# DWFAPI int FDwfDigitalInTriggerSourceGet(HDWF hdwf, TRIGSRC *ptrigsrc);
def DigitalInTriggerSourceGet(hdwf: int) -> int:
    '''
    Gets the current trigger source setting for the instrument.
    '''
    out_trigger_source = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInTriggerSourceGet(ctypes.c_int(hdwf), ctypes.byref(out_trigger_source)))
    return int(out_trigger_source.value)

# DWFAPI int FDwfDigitalInTriggerSlopeSet(HDWF hdwf, DwfTriggerSlope slope);
def DigitalInTriggerSlopeSet(hdwf: int, slope: int) -> None:
    '''
    Sets the trigger slope for the instrument.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInTriggerSlopeSet(ctypes.c_int(hdwf), ctypes.c_int(slope)))

# DWFAPI int FDwfDigitalInTriggerSlopeGet(HDWF hdwf, DwfTriggerSlope *pslope);
def DigitalInTriggerSlopeGet(hdwf: int) -> int:
    '''
    Gets the current trigger source setting for the instrument.
    '''
    out_slope = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInTriggerSlopeGet(ctypes.c_int(hdwf), ctypes.byref(out_slope)))
    return int(out_slope.value)

# DWFAPI int FDwfDigitalInTriggerPositionInfo(HDWF hdwf, unsigned int *pnSamplesAfterTriggerMax);
def DigitalInTriggerPositionInfo(hdwf: int) -> int:
    '''
    Returns maximum values of the trigger position in samples. This can be
    greater than the specified buffer size.
    '''
    out_samples_after_trigger_max = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalInTriggerPositionInfo(ctypes.c_int(hdwf), ctypes.byref(out_samples_after_trigger_max)))
    return int(out_samples_after_trigger_max.value)

# DWFAPI int FDwfDigitalInTriggerPositionSet(HDWF hdwf, unsigned int cSamplesAfterTrigger);
def DigitalInTriggerPositionSet(hdwf: int, cSamplesAfterTrigger: int) -> None:
    '''
    Sets the number of samples to acquire after trigger.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInTriggerPositionSet(ctypes.c_int(hdwf), ctypes.c_uint(cSamplesAfterTrigger)))

# DWFAPI int FDwfDigitalInTriggerPositionGet(HDWF hdwf, unsigned int *pcSamplesAfterTrigger);
def DigitalInTriggerPositionGet(hdwf: int) -> int:
    '''
    Gets the configured trigger position.
    '''
    out_cSamplesAfterTrigger = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalInTriggerPositionGet(ctypes.c_int(hdwf), ctypes.byref(out_cSamplesAfterTrigger)))
    return int(out_cSamplesAfterTrigger.value)

# DWFAPI int FDwfDigitalInTriggerPrefillSet(HDWF hdwf, unsigned int cSamplesBeforeTrigger);
def DigitalInTriggerPrefillSet(hdwf: int, cSamplesBeforeTrigger: int) -> None:
    '''
    Sets the number of samples to acquire before arming in Record acquisition
    mode. The prefill is used for record with trigger to make sure at last the
    required number of samples are collected before arming, before looking for
    trigger event. With prefill 0 the recording process will stream data only
    after trigger event. With prefill more than zero the recording will stream
    until trigger occurs plus the samples specified by trigger position.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInTriggerPrefillSet(ctypes.c_int(hdwf), ctypes.c_uint(cSamplesBeforeTrigger)))

# DWFAPI int FDwfDigitalInTriggerPrefillGet(HDWF hdwf, unsigned int *pcSamplesBeforeTrigger);
def DigitalInTriggerPrefillGet(hdwf: int) -> int:
    '''
    Gets the configured trigger prefill.
    '''
    out_cSamplesBeforeTrigger = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalInTriggerPrefillGet(ctypes.c_int(hdwf), ctypes.byref(out_cSamplesBeforeTrigger)))
    return int(out_cSamplesBeforeTrigger.value)

# DWFAPI int FDwfDigitalInTriggerAutoTimeoutInfo(HDWF hdwf, double *psecMin, double *psecMax, double *pnSteps);
def DigitalInTriggerAutoTimeoutInfo(hdwf: int) -> (float, float, float):
    '''
    Returns the minimum and maximum auto trigger timeout values, and the number
    of adjustable steps.
    '''
    out_sec_min = ctypes.c_double(0.0)
    out_sec_max = ctypes.c_double(0.0)
    out_num_steps = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfDigitalInTriggerAutoTimeoutInfo(ctypes.c_int(hdwf), ctypes.byref(out_sec_min), ctypes.byref(out_sec_max), ctypes.byref(out_num_steps)))
    return float(out_sec_min.value), float(out_sec_max.value), float(out_num_steps.value)

# DWFAPI int FDwfDigitalInTriggerAutoTimeoutSet(HDWF hdwf, double secTimeout);
def DigitalInTriggerAutoTimeoutSet(hdwf: int, secTimeout: float) -> None:
    '''
    Configures the auto trigger timeout value in seconds.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInTriggerAutoTimeoutSet(ctypes.c_int(hdwf), ctypes.c_double(secTimeout)))

# DWFAPI int FDwfDigitalInTriggerAutoTimeoutGet(HDWF hdwf, double *psecTimeout);
def DigitalInTriggerAutoTimeoutGet(hdwf: int) -> float:
    '''
    Returns the configured auto trigger timeout value in seconds. The
    acquisition is auto triggered when the specified time elapses. With zero
    value the timeout is disabled, performing “Normal” acquisitions.
    '''
    out_secTimeout = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfDigitalInTriggerAutoTimeoutGet(ctypes.c_int(hdwf), ctypes.byref(out_secTimeout)))
    return float(out_secTimeout.value)

# DWFAPI int FDwfDigitalInTriggerInfo(HDWF hdwf, unsigned int *pfsLevelLow, unsigned int *pfsLevelHigh, unsigned int *pfsEdgeRise, unsigned int *pfsEdgeFall);
# Warning no docs found for FDwfDigitalInTriggerInfo
def DigitalInTriggerInfo(hdwf: int) -> (int, int, int, int):
    out_fsLevelLow = c_uint(0)
    out_fsLevelHigh = c_uint(0)
    out_fsEdgeRise = c_uint(0)
    out_fsEdgeFall = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalInTriggerInfo(ctypes.c_int(hdwf), ctypes.byref(out_fsLevelLow), ctypes.byref(out_fsLevelHigh), ctypes.byref(out_fsEdgeRise), ctypes.byref(out_fsEdgeFall)))
    return int(out_fsLevelLow.value), int(out_fsLevelHigh.value), int(out_fsEdgeRise.value), int(out_fsEdgeFall.value)

# DWFAPI int FDwfDigitalInTriggerSet(HDWF hdwf, unsigned int fsLevelLow, unsigned int fsLevelHigh, unsigned int fsEdgeRise, unsigned int fsEdgeFall);
def DigitalInTriggerSet(hdwf: int, fsLevelLow: int, fsLevelHigh: int, fsEdgeRise: int, fsEdgeFall: int) -> None:
    '''
    Configures the digital in trigger detector. The logic for the trigger bits
    is: Low and High and (Rise or Fall). Setting a bit in both rise and fall
    will trigger on any edge, any transition. For instance
    FDwfDigitalInTriggerInfo(hdwf, 1, 2, 4, 8) will generate trigger when DIO-0
    is low and DIO-1 is high and DIO-2 is rising or DIO-3 is falling.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInTriggerSet(ctypes.c_int(hdwf), ctypes.c_uint(fsLevelLow), ctypes.c_uint(fsLevelHigh), ctypes.c_uint(fsEdgeRise), ctypes.c_uint(fsEdgeFall)))

# DWFAPI int FDwfDigitalInTriggerGet(HDWF hdwf, unsigned int *pfsLevelLow, unsigned int *pfsLevelHigh, unsigned int *pfsEdgeRise, unsigned int *pfsEdgeFall);
def DigitalInTriggerGet(hdwf: int) -> (int, int, int, int):
    '''
    Returns the configured digital in trigger detector option.
    '''
    out_fsLevelLow = c_uint(0)
    out_fsLevelHigh = c_uint(0)
    out_fsEdgeRise = c_uint(0)
    out_fsEdgeFall = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalInTriggerGet(ctypes.c_int(hdwf), ctypes.byref(out_fsLevelLow), ctypes.byref(out_fsLevelHigh), ctypes.byref(out_fsEdgeRise), ctypes.byref(out_fsEdgeFall)))
    return int(out_fsLevelLow.value), int(out_fsLevelHigh.value), int(out_fsEdgeRise.value), int(out_fsEdgeFall.value)

# the logic for trigger bits: Low and High and (Rise or Fall)
# bits set in Rise and Fall means any edge

# DWFAPI int FDwfDigitalInTriggerResetSet(HDWF hdwf, unsigned int fsLevelLow, unsigned int fsLevelHigh, unsigned int fsEdgeRise, unsigned int fsEdgeFall);
def DigitalInTriggerResetSet(hdwf: int, fsLevelLow: int, fsLevelHigh: int, fsEdgeRise: int, fsEdgeFall: int) -> None:
    '''
    Configures the digital in trigger reset condition.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInTriggerResetSet(ctypes.c_int(hdwf), ctypes.c_uint(fsLevelLow), ctypes.c_uint(fsLevelHigh), ctypes.c_uint(fsEdgeRise), ctypes.c_uint(fsEdgeFall)))

# DWFAPI int FDwfDigitalInTriggerCountSet(HDWF hdwf, int cCount, int fRestart);
def DigitalInTriggerCountSet(hdwf: int, cCount: int, fRestart: int) -> None:
    '''
    Configures the trigger counter.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInTriggerCountSet(ctypes.c_int(hdwf), ctypes.c_int(cCount), ctypes.c_int(fRestart)))

# DWFAPI int FDwfDigitalInTriggerLengthSet(HDWF hdwf, double secMin, double secMax, int idxSync);
def DigitalInTriggerLengthSet(hdwf: int, sec_min: float, sec_max: float, idxSync: int) -> None:
    '''
    Configures the trigger timing. The synchronization modes are the following:
    0 – Normal
    1 – Timing: use for UART, CAN. The min length specifies bit length and max
        the timeout length.
    2 – PWM: use for 1-Wire. The min length specifies sampling time and max
        the timeout length.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInTriggerLengthSet(ctypes.c_int(hdwf), ctypes.c_double(sec_min), ctypes.c_double(sec_max), ctypes.c_int(idxSync)))

# DWFAPI int FDwfDigitalInTriggerMatchSet(HDWF hdwf, int iPin, unsigned int fsMask, unsigned int fsValue, int cBitStuffing);
def DigitalInTriggerMatchSet(hdwf: int, iPin: int, fsMask: int, fsValue: int, cBitStuffing: int) -> None:
    '''
    Configure the deserializer. The bits are left shifted. The mask and value
    should be specified according to this, in MSBit first order. Like to trigger
    on first to fourth bits received from a sequence of 8, b1010XXXX, set mask
    to 0x000000F0 and value to 0x000000A0.
    '''
    _ThrowIfError(_dwf.FDwfDigitalInTriggerMatchSet(ctypes.c_int(hdwf), ctypes.c_int(iPin), ctypes.c_uint(fsMask), ctypes.c_uint(fsValue), ctypes.c_int(cBitStuffing)))

###############################################################################
# DIGITAL OUT INSTRUMENT FUNCTIONS
###############################################################################

#------------------------------------------------------------------------------
# Control:
#------------------------------------------------------------------------------

# DWFAPI int FDwfDigitalOutReset(HDWF hdwf);
def DigitalOutReset(hdwf: int) -> None:
    '''
    Resets and configures (by default, having auto configure enabled) all the
    instrument parameters to default values.
    '''
    _ThrowIfError(_dwf.FDwfDigitalOutReset(ctypes.c_int(hdwf)))

# DWFAPI int FDwfDigitalOutConfigure(HDWF hdwf, int fStart);
def DigitalOutConfigure(hdwf: int, fStart: int) -> None:
    '''
    Starts or stops the instrument.
    '''
    _ThrowIfError(_dwf.FDwfDigitalOutConfigure(ctypes.c_int(hdwf), ctypes.c_int(fStart)))

# DWFAPI int FDwfDigitalOutStatus(HDWF hdwf, DwfState *psts);
def DigitalOutStatus(hdwf: int) -> int:
    '''
    Checks the state of the instrument.
    '''
    out_instrument_state = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalOutStatus(ctypes.c_int(hdwf), ctypes.byref(out_instrument_state)))
    return int(out_instrument_state.value)

#------------------------------------------------------------------------------
# Configuration:
#------------------------------------------------------------------------------

# DWFAPI int FDwfDigitalOutInternalClockInfo(HDWF hdwf, double *phzFreq);
def DigitalOutInternalClockInfo(hdwf: int) -> float:
    '''
    Retrieves the internal clock frequency.
    '''
    out_hzFreq = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfDigitalOutInternalClockInfo(ctypes.c_int(hdwf), ctypes.byref(out_hzFreq)))
    return float(out_hzFreq.value)

# DWFAPI int FDwfDigitalOutTriggerSourceSet(HDWF hdwf, TRIGSRC trigsrc);
def DigitalOutTriggerSourceSet(hdwf: int, trigger_source: int) -> None:
    '''
    Sets the trigger source for the instrument. Default setting is trigsrcNone.
    '''
    _ThrowIfError(_dwf.FDwfDigitalOutTriggerSourceSet(ctypes.c_int(hdwf), ctypes.c_int(trigger_source)))

# DWFAPI int FDwfDigitalOutTriggerSourceGet(HDWF hdwf, TRIGSRC *ptrigsrc);
def DigitalOutTriggerSourceGet(hdwf: int) -> int:
    '''
    Gets the current trigger source setting for the instrument.
    '''
    out_trigger_source = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalOutTriggerSourceGet(ctypes.c_int(hdwf), ctypes.byref(out_trigger_source)))
    return int(out_trigger_source.value)

# DWFAPI int FDwfDigitalOutRunInfo(HDWF hdwf, double *psecMin, double *psecMax);
def DigitalOutRunInfo(hdwf: int) -> (float, float):
    '''
    Returns the supported run length range for the instrument in seconds. Zero
    value (default) represent an infinite (or continuous) run.
    '''
    out_sec_min = ctypes.c_double(0.0)
    out_sec_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfDigitalOutRunInfo(ctypes.c_int(hdwf), ctypes.byref(out_sec_min), ctypes.byref(out_sec_max)))
    return float(out_sec_min.value), float(out_sec_max.value)

# DWFAPI int FDwfDigitalOutRunSet(HDWF hdwf, double secRun);
def DigitalOutRunSet(hdwf: int, secRun: float) -> None:
    '''
    Sets the run length for the instrument in seconds.
    '''
    _ThrowIfError(_dwf.FDwfDigitalOutRunSet(ctypes.c_int(hdwf), ctypes.c_double(secRun)))

# DWFAPI int FDwfDigitalOutRunGet(HDWF hdwf, double *psecRun);
def DigitalOutRunGet(hdwf: int) -> float:
    '''
    Reads the configured run length for the instrument in seconds.
    '''
    out_secRun = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfDigitalOutRunGet(ctypes.c_int(hdwf), ctypes.byref(out_secRun)))
    return float(out_secRun.value)

# DWFAPI int FDwfDigitalOutRunStatus(HDWF hdwf, double *psecRun);
def DigitalOutRunStatus(hdwf: int) -> float:
    '''
    Reads the remaining run length. It returns data from the last
    FDwfDigitalOutStatus call.
    '''
    out_secRun = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfDigitalOutRunStatus(ctypes.c_int(hdwf), ctypes.byref(out_secRun)))
    return float(out_secRun.value)

# DWFAPI int FDwfDigitalOutWaitInfo(HDWF hdwf, double *psecMin, double *psecMax);
def DigitalOutWaitInfo(hdwf: int) -> (float, float):
    '''
    Returns the supported wait length range in seconds. The wait length is how
    long the instrument waits after being triggered to generate the signal.
    Default value is zero.
    '''
    out_sec_min = ctypes.c_double(0.0)
    out_sec_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfDigitalOutWaitInfo(ctypes.c_int(hdwf), ctypes.byref(out_sec_min), ctypes.byref(out_sec_max)))
    return float(out_sec_min.value), float(out_sec_max.value)

# DWFAPI int FDwfDigitalOutWaitSet(HDWF hdwf, double secWait);
def DigitalOutWaitSet(hdwf: int, secWait: float) -> None:
    '''
    Sets the wait length.
    '''
    _ThrowIfError(_dwf.FDwfDigitalOutWaitSet(ctypes.c_int(hdwf), ctypes.c_double(secWait)))

# DWFAPI int FDwfDigitalOutWaitGet(HDWF hdwf, double *psecWait);
def DigitalOutWaitGet(hdwf: int) -> float:
    '''
    Gets the current wait length.
    '''
    out_secWait = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfDigitalOutWaitGet(ctypes.c_int(hdwf), ctypes.byref(out_secWait)))
    return float(out_secWait.value)

# DWFAPI int FDwfDigitalOutRepeatInfo(HDWF hdwf, unsigned int *pnMin, unsigned int *pnMax);
def DigitalOutRepeatInfo(hdwf: int) -> (int, int):
    '''
    Returns the supported repeat count range. This is how many times the
    generated signal will be repeated. Zero value represents infinite repeats.
    Default value is one.
    '''
    out_min = c_uint(0)
    out_max = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalOutRepeatInfo(ctypes.c_int(hdwf), ctypes.byref(out_min), ctypes.byref(out_max)))
    return int(out_min.value), int(out_max.value)

# DWFAPI int FDwfDigitalOutRepeatSet(HDWF hdwf, unsigned int cRepeat);
def DigitalOutRepeatSet(hdwf: int, cRepeat: int) -> None:
    '''
    Sets the repeat count.
    '''
    _ThrowIfError(_dwf.FDwfDigitalOutRepeatSet(ctypes.c_int(hdwf), ctypes.c_uint(cRepeat)))

# DWFAPI int FDwfDigitalOutRepeatGet(HDWF hdwf, unsigned int *pcRepeat);
def DigitalOutRepeatGet(hdwf: int) -> int:
    '''
    Reads the current repeat count.
    '''
    out_cRepeat = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalOutRepeatGet(ctypes.c_int(hdwf), ctypes.byref(out_cRepeat)))
    return int(out_cRepeat.value)

# DWFAPI int FDwfDigitalOutRepeatStatus(HDWF hdwf, unsigned int *pcRepeat);
def DigitalOutRepeatStatus(hdwf: int) -> int:
    '''
    Reads the remaining repeat counts. It only returns information from the last
    FDwfDigitalOutStatus function call, it does not read from the device.
    '''
    out_cRepeat = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalOutRepeatStatus(ctypes.c_int(hdwf), ctypes.byref(out_cRepeat)))
    return int(out_cRepeat.value)

# DWFAPI int FDwfDigitalOutTriggerSlopeSet(HDWF hdwf, DwfTriggerSlope slope);
def DigitalOutTriggerSlopeSet(hdwf: int, slope: int) -> None:
    '''
    Sets the trigger slope for the instrument.
    '''
    _ThrowIfError(_dwf.FDwfDigitalOutTriggerSlopeSet(ctypes.c_int(hdwf), ctypes.c_int(slope)))

# DWFAPI int FDwfDigitalOutTriggerSlopeGet(HDWF hdwf, DwfTriggerSlope *pslope);
def DigitalOutTriggerSlopeGet(hdwf: int) -> int:
    '''
    Gets the current trigger source setting for the instrument.
    '''
    out_slope = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalOutTriggerSlopeGet(ctypes.c_int(hdwf), ctypes.byref(out_slope)))
    return int(out_slope.value)

# DWFAPI int FDwfDigitalOutRepeatTriggerSet(HDWF hdwf, int fRepeatTrigger);
def DigitalOutRepeatTriggerSet(hdwf: int, fRepeatTrigger: int) -> None:
    '''
    Sets the repeat trigger option. To include the trigger in wait-run repeat
    cycles, set fRepeatTrigger to TRUE. It is disabled by default.
    '''
    _ThrowIfError(_dwf.FDwfDigitalOutRepeatTriggerSet(ctypes.c_int(hdwf), ctypes.c_int(fRepeatTrigger)))

# DWFAPI int FDwfDigitalOutRepeatTriggerGet(HDWF hdwf, int *pfRepeatTrigger);
def DigitalOutRepeatTriggerGet(hdwf: int) -> int:
    '''
    Verifies if the trigger has been included in wait-run repeat cycles.
    '''
    out_fRepeatTrigger = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalOutRepeatTriggerGet(ctypes.c_int(hdwf), ctypes.byref(out_fRepeatTrigger)))
    return int(out_fRepeatTrigger.value)

# DWFAPI int FDwfDigitalOutCount(HDWF hdwf, int *pcChannel);
def DigitalOutCount(hdwf: int) -> int:
    '''
    Returns the number of Digital Out channels by the device specified by hdwf.
    '''
    out_cChannel = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalOutCount(ctypes.c_int(hdwf), ctypes.byref(out_cChannel)))
    return int(out_cChannel.value)

# DWFAPI int FDwfDigitalOutEnableSet(HDWF hdwf, int idxChannel, int fEnable);
def DigitalOutEnableSet(hdwf: int, channel_index: int, enable: int) -> None:
    '''
    Enables or disables the channel specified by idxChannel.
    '''
    _ThrowIfError(_dwf.FDwfDigitalOutEnableSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(enable)))

# DWFAPI int FDwfDigitalOutEnableGet(HDWF hdwf, int idxChannel, int *pfEnable);
def DigitalOutEnableGet(hdwf: int, channel_index: int) -> int:
    '''
    Verifies if a specific channel is enabled or disabled.
    '''
    out_enable = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalOutEnableGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_enable)))
    return int(out_enable.value)

# DWFAPI int FDwfDigitalOutOutputInfo(HDWF hdwf, int idxChannel, int *pfsDwfDigitalOutOutput); // use IsBitSet
def DigitalOutOutputInfo(hdwf: int, channel_index: int) -> int:
    '''
    Returns the supported output modes of the channel. They are returned (by
    reference) as a bit field. This bit field can be parsed using the IsBitSet
    Macro. Individual bits are defined using the DwfDigitalOutOutput constants
    in DWF.h:
    '''
    out_fsDwfDigitalOutOutput = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalOutOutputInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_fsDwfDigitalOutOutput)))
    return int(out_fsDwfDigitalOutOutput.value)

# DWFAPI int FDwfDigitalOutOutputSet(HDWF hdwf, int idxChannel, DwfDigitalOutOutput v);
def DigitalOutOutputSet(hdwf: int, channel_index: int, v: int) -> None:
    '''
    Specifies output mode of the channel.
    '''
    _ThrowIfError(_dwf.FDwfDigitalOutOutputSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(v)))

# DWFAPI int FDwfDigitalOutOutputGet(HDWF hdwf, int idxChannel, DwfDigitalOutOutput *pv);
def DigitalOutOutputGet(hdwf: int, channel_index: int) -> int:
    '''
    Verifies if a specific channel output mode.
    '''
    out_v = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalOutOutputGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_v)))
    return int(out_v.value)

# DWFAPI int FDwfDigitalOutTypeInfo(HDWF hdwf, int idxChannel, int *pfsDwfDigitalOutType); // use IsBitSet
def DigitalOutTypeInfo(hdwf: int, channel_index: int) -> int:
    '''
    Returns the supported types of the channel. They are returned (by reference)
    as a bit field. This bit field can be parsed using the IsBitSet Macro.
    Individual bits are defined using the DwfDigitalOutType constants in dwf.h:
    '''
    out_fsDwfDigitalOutType = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalOutTypeInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_fsDwfDigitalOutType)))
    return int(out_fsDwfDigitalOutType.value)

# DWFAPI int FDwfDigitalOutTypeSet(HDWF hdwf, int idxChannel, DwfDigitalOutType v);
def DigitalOutTypeSet(hdwf: int, channel_index: int, v: int) -> None:
    '''
    Sets the output type of the specified channel.
    '''
    _ThrowIfError(_dwf.FDwfDigitalOutTypeSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(v)))

# DWFAPI int FDwfDigitalOutTypeGet(HDWF hdwf, int idxChannel, DwfDigitalOutType *pv);
def DigitalOutTypeGet(hdwf: int, channel_index: int) -> int:
    '''
    Verifies the type of a specific channel.
    '''
    out_v = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalOutTypeGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_v)))
    return int(out_v.value)

# DWFAPI int FDwfDigitalOutIdleInfo(HDWF hdwf, int idxChannel, int *pfsDwfDigitalOutIdle); // use IsBitSet
def DigitalOutIdleInfo(hdwf: int, channel_index: int) -> int:
    '''
    Returns the supported idle output types of the channel. They are returned
    (by reference) as a bit field. This bit field can be parsed using the
    IsBitSet Macro. Individual bits are defined using the DwfDigitalOutIdle
    constants in dwf.h. Output while not running:
    '''
    out_fsDwfDigitalOutIdle = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalOutIdleInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_fsDwfDigitalOutIdle)))
    return int(out_fsDwfDigitalOutIdle.value)

# DWFAPI int FDwfDigitalOutIdleSet(HDWF hdwf, int idxChannel, DwfDigitalOutIdle v);
def DigitalOutIdleSet(hdwf: int, channel_index: int, v: int) -> None:
    '''
    Sets the idle output of the specified channel.
    '''
    _ThrowIfError(_dwf.FDwfDigitalOutIdleSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(v)))

# DWFAPI int FDwfDigitalOutIdleGet(HDWF hdwf, int idxChannel, DwfDigitalOutIdle *pv);
def DigitalOutIdleGet(hdwf: int, channel_index: int) -> int:
    '''
    Verifies the idle output of a specific channel.
    '''
    out_v = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalOutIdleGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_v)))
    return int(out_v.value)

# DWFAPI int FDwfDigitalOutDividerInfo(HDWF hdwf, int idxChannel, unsigned int *vMin, unsigned int *vMax);
def DigitalOutDividerInfo(hdwf: int, channel_index: int) -> (int, int):
    '''
    Returns the supported clock divider value range.
    '''
    out_v_min = c_uint(0)
    out_v_max = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalOutDividerInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_v_min), ctypes.byref(out_v_max)))
    return int(out_v_min.value), int(out_v_max.value)

# DWFAPI int FDwfDigitalOutDividerInitSet(HDWF hdwf, int idxChannel, unsigned int v);
def DigitalOutDividerInitSet(hdwf: int, channel_index: int, v: int) -> None:
    '''
    Sets the initial divider value of the specified channel.
    '''
    _ThrowIfError(_dwf.FDwfDigitalOutDividerInitSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_uint(v)))

# DWFAPI int FDwfDigitalOutDividerInitGet(HDWF hdwf, int idxChannel, unsigned int *pv);
def DigitalOutDividerInitGet(hdwf: int, channel_index: int) -> int:
    '''
    Verifies the initial divider value of the specified channel.
    '''
    out_v = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalOutDividerInitGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_v)))
    return int(out_v.value)

# DWFAPI int FDwfDigitalOutDividerSet(HDWF hdwf, int idxChannel, unsigned int v);
def DigitalOutDividerSet(hdwf: int, channel_index: int, v: int) -> None:
    '''
    Sets the divider value of the specified channel.
    '''
    _ThrowIfError(_dwf.FDwfDigitalOutDividerSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_uint(v)))

# DWFAPI int FDwfDigitalOutDividerGet(HDWF hdwf, int idxChannel, unsigned int *pv);
def DigitalOutDividerGet(hdwf: int, channel_index: int) -> int:
    '''
    Verifies the divider value of the specified channel.
    '''
    out_v = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalOutDividerGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_v)))
    return int(out_v.value)

# DWFAPI int FDwfDigitalOutCounterInfo(HDWF hdwf, int idxChannel, unsigned int *vMin, unsigned int *vMax);
def DigitalOutCounterInfo(hdwf: int, channel_index: int) -> (int, int):
    '''
    Returns the supported counter value range.
    '''
    out_v_min = c_uint(0)
    out_v_max = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalOutCounterInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_v_min), ctypes.byref(out_v_max)))
    return int(out_v_min.value), int(out_v_max.value)

# DWFAPI int FDwfDigitalOutCounterInitSet(HDWF hdwf, int idxChannel, int fHigh, unsigned int v);
def DigitalOutCounterInitSet(hdwf: int, channel_index: int, fHigh: int, v: int) -> None:
    '''
    Sets the initial state and counter value of the specified channel.
    '''
    _ThrowIfError(_dwf.FDwfDigitalOutCounterInitSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(fHigh), ctypes.c_uint(v)))

# DWFAPI int FDwfDigitalOutCounterInitGet(HDWF hdwf, int idxChannel, int *pfHigh, unsigned int *pv);
def DigitalOutCounterInitGet(hdwf: int, channel_index: int) -> (int, int):
    '''
    Retrieves the initial state and counter value for the specified channel.
    '''
    out_fHigh = ctypes.c_int(0)
    out_v = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalOutCounterInitGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_fHigh), ctypes.byref(out_v)))
    return int(out_fHigh.value), int(out_v.value)

# DWFAPI int FDwfDigitalOutCounterSet(HDWF hdwf, int idxChannel, unsigned int vLow, unsigned int vHigh);
def DigitalOutCounterSet(hdwf: int, channel_index: int, vLow: int, vHigh: int) -> None:
    '''
    Sets the counter low and high values for the specified channel.
    '''
    _ThrowIfError(_dwf.FDwfDigitalOutCounterSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_uint(vLow), ctypes.c_uint(vHigh)))

# DWFAPI int FDwfDigitalOutCounterGet(HDWF hdwf, int idxChannel, unsigned int *pvLow, unsigned int *pvHigh);
def DigitalOutCounterGet(hdwf: int, channel_index: int) -> (int, int):
    '''
    Verifies the low and high counter value of the specified channel.
    '''
    out_vLow = c_uint(0)
    out_vHigh = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalOutCounterGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_vLow), ctypes.byref(out_vHigh)))
    return int(out_vLow.value), int(out_vHigh.value)

# DWFAPI int FDwfDigitalOutDataInfo(HDWF hdwf, int idxChannel, unsigned int *pcountOfBitsMax);
def DigitalOutDataInfo(hdwf: int, channel_index: int) -> int:
    '''
    Returns the maximum buffers size, the number of custom data bits.
    '''
    out_count_of_bits_max = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalOutDataInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_count_of_bits_max)))
    return int(out_count_of_bits_max.value)

# DWFAPI int FDwfDigitalOutDataSet(HDWF hdwf, int idxChannel, void *rgBits, unsigned int countOfBits);
def DigitalOutDataSet(hdwf: int, channel_index: int, countOfBits: int) -> int:
    '''
    Sets the custom data bits. The function also sets the counter initial, low
    and high value, according the number of bits. The data bits are sent out in
    LSB first order. For TS output, the count of bits is the total number of
    output value (I/O) and output enable (OE) bits, which should be an even
    number.
    '''
    out_rgBits = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalOutDataSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_uint(countOfBits), ctypes.byref(out_rgBits)))
    return int(out_rgBits.value)

# bits order is lsb first
# for TS output the count of bits its the total number of IO|OE bits, it should be an even number
# BYTE:   0                 |1     ...
# bit:    0 |1 |2 |3 |...|7 |0 |1 |...
# sample: IO|OE|IO|OE|...|OE|IO|OE|...

# DWFAPI int FDwfDigitalOutPlayDataSet(HDWF hdwf, unsigned char *rgBits, unsigned int bitPerSample, unsigned int countOfSamples);
def DigitalOutPlayDataSet(hdwf: int, bitPerSample: int, countOfSamples: int) -> int:
    '''
    Sets the divider value of the specified channel.
    '''
    out_rgBits = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalOutPlayDataSet(ctypes.c_int(hdwf), ctypes.c_uint(bitPerSample), ctypes.c_uint(countOfSamples), ctypes.byref(out_rgBits)))
    return int(out_rgBits.value)

# DWFAPI int FDwfDigitalOutPlayRateSet(HDWF hdwf, double hzRate);
def DigitalOutPlayRateSet(hdwf: int, hzRate: float) -> None:
    '''
    Sets the play rate.
    '''
    _ThrowIfError(_dwf.FDwfDigitalOutPlayRateSet(ctypes.c_int(hdwf), ctypes.c_double(hzRate)))

# DWFAPI int FDwfDigitalUartReset(HDWF hdwf);
def DigitalUartReset(hdwf: int) -> None:
    '''
    Resets the UART configuration to default value. Use FDwfDigitalOutReset to
    reset the output.
    '''
    _ThrowIfError(_dwf.FDwfDigitalUartReset(ctypes.c_int(hdwf)))

# DWFAPI int FDwfDigitalUartRateSet(HDWF hdwf, double hz);
def DigitalUartRateSet(hdwf: int, hz: float) -> None:
    '''
    Sets the data rate.
    '''
    _ThrowIfError(_dwf.FDwfDigitalUartRateSet(ctypes.c_int(hdwf), ctypes.c_double(hz)))

# DWFAPI int FDwfDigitalUartBitsSet(HDWF hdwf, int cBits);
def DigitalUartBitsSet(hdwf: int, cBits: int) -> None:
    '''
    Sets the character length, typically 8, 7, 6 or 5.
    '''
    _ThrowIfError(_dwf.FDwfDigitalUartBitsSet(ctypes.c_int(hdwf), ctypes.c_int(cBits)))

# DWFAPI int FDwfDigitalUartParitySet(HDWF hdwf, int parity); # 0 none, 1 odd, 2 even
def DigitalUartParitySet(hdwf: int, parity: int) -> None:
    '''
    Sets the parity bit: 0 for no parity, 1 for odd and 2 for even parity.
    '''
    _ThrowIfError(_dwf.FDwfDigitalUartParitySet(ctypes.c_int(hdwf), ctypes.c_int(parity)))

# DWFAPI int FDwfDigitalUartStopSet(HDWF hdwf, double cBit);
def DigitalUartStopSet(hdwf: int, cBit: float) -> None:
    '''
    Sets the stop length as number of bits.
    '''
    _ThrowIfError(_dwf.FDwfDigitalUartStopSet(ctypes.c_int(hdwf), ctypes.c_double(cBit)))

# DWFAPI int FDwfDigitalUartTxSet(HDWF hdwf, int idxChannel);
def DigitalUartTxSet(hdwf: int, channel_index: int) -> None:
    '''
    Specifies the DIO channel to use for transmission.
    '''
    _ThrowIfError(_dwf.FDwfDigitalUartTxSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index)))

# DWFAPI int FDwfDigitalUartRxSet(HDWF hdwf, int idxChannel);
def DigitalUartRxSet(hdwf: int, channel_index: int) -> None:
    '''
    Specifies the DIO channel to use for reception.
    '''
    _ThrowIfError(_dwf.FDwfDigitalUartRxSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index)))

# DWFAPI int FDwfDigitalUartTx(HDWF hdwf, char *szTx, int cTx);
def DigitalUartTx(hdwf: int, cTx: int) -> int:
    '''
    Transmits the specified characters.
    '''
    out_szTx = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalUartTx(ctypes.c_int(hdwf), ctypes.c_int(cTx), ctypes.byref(out_szTx)))
    return int(out_szTx.value)

# DWFAPI int FDwfDigitalUartRx(HDWF hdwf, char *szRx, int cRx, int *pcRx, int *pParity);
def DigitalUartRx(hdwf: int, cRx: int) -> (int, int, int):
    '''
    Initializes the reception with cRxMax zero. Otherwise returns the received
    characters since the last call.
    '''
    out_szRx = ctypes.c_int(0)
    out_cRx = ctypes.c_int(0)
    out_Parity = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalUartRx(ctypes.c_int(hdwf), ctypes.c_int(cRx), ctypes.byref(out_szRx), ctypes.byref(out_cRx), ctypes.byref(out_Parity)))
    return int(out_szRx.value), int(out_cRx.value), int(out_Parity.value)

# DWFAPI int FDwfDigitalSpiReset(HDWF hdwf);
def DigitalSpiReset(hdwf: int) -> None:
    '''
    Resets the SPI configuration to default value. Use FDwfDigitalOutReset to
    reset the outputs.
    '''
    _ThrowIfError(_dwf.FDwfDigitalSpiReset(ctypes.c_int(hdwf)))

# DWFAPI int FDwfDigitalSpiFrequencySet(HDWF hdwf, double hz);
def DigitalSpiFrequencySet(hdwf: int, hz: float) -> None:
    '''
    Sets the SPI frequency.
    '''
    _ThrowIfError(_dwf.FDwfDigitalSpiFrequencySet(ctypes.c_int(hdwf), ctypes.c_double(hz)))

# DWFAPI int FDwfDigitalSpiClockSet(HDWF hdwf, int idxChannel);
def DigitalSpiClockSet(hdwf: int, channel_index: int) -> None:
    '''
    Specifies the DIO channel to use for SPI clock.
    '''
    _ThrowIfError(_dwf.FDwfDigitalSpiClockSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index)))

# DWFAPI int FDwfDigitalSpiDataSet(HDWF hdwf, int idxDQ, int idxChannel); # 0 DQ0_MOSI_SISO, 1 DQ1_MISO, 2 DQ2, 3 DQ3
def DigitalSpiDataSet(hdwf: int, idxDQ: int, channel_index: int) -> None:
    '''
    Specifies the DIO channels to use for SPI data.
    '''
    _ThrowIfError(_dwf.FDwfDigitalSpiDataSet(ctypes.c_int(hdwf), ctypes.c_int(idxDQ), ctypes.c_int(channel_index)))

# DWFAPI int FDwfDigitalSpiIdleSet(HDWF hdwf, int idxDQ, DwfDigitalOutIdle idle);
def DigitalSpiIdleSet(hdwf: int, idxDQ: int, idle: int) -> None:
    '''
    Specifies the DIO channels to use for SPI data.
    '''
    _ThrowIfError(_dwf.FDwfDigitalSpiIdleSet(ctypes.c_int(hdwf), ctypes.c_int(idxDQ), ctypes.c_int(idle)))

# DWFAPI int FDwfDigitalSpiModeSet(HDWF hdwf, int iMode); # bit1 CPOL, bit0 CPHA
def DigitalSpiModeSet(hdwf: int, iMode: int) -> None:
    '''
    Sets the SPI mode
    '''
    _ThrowIfError(_dwf.FDwfDigitalSpiModeSet(ctypes.c_int(hdwf), ctypes.c_int(iMode)))

# DWFAPI int FDwfDigitalSpiOrderSet(HDWF hdwf, int fMSBFirst); # bit order: 1 MSB first, 0 LSB first
def DigitalSpiOrderSet(hdwf: int, fMSBFirst: int) -> None:
    '''
    Sets the bit order for SPI data.
    '''
    _ThrowIfError(_dwf.FDwfDigitalSpiOrderSet(ctypes.c_int(hdwf), ctypes.c_int(fMSBFirst)))

# DWFAPI int FDwfDigitalSpiSelect(HDWF hdwf, int idxChannel, int level); # 0 low, 1 high, -1 Z
def DigitalSpiSelect(hdwf: int, channel_index: int, level: int) -> None:
    '''
    Controls the SPI CS signal(s).
    '''
    _ThrowIfError(_dwf.FDwfDigitalSpiSelect(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(level)))

# cDQ 0 SISO, 1 MOSI/MISO, 2 dual, 4 quad, # 1-32 bits / word
# DWFAPI int FDwfDigitalSpiWriteRead(HDWF hdwf, int cDQ, int cBitPerWord, unsigned char *rgTX, int cTX, unsigned char *rgRX, int cRX);
def DigitalSpiWriteRead(hdwf: int, cDQ: int, cBitPerWord: int, cTX: int, cRX: int) -> (int, int):
    '''
    Performs SPI transfer of up to 8bit words. This function is intended for
    standard MOSI/MISO (cDQ 1) operations, but it can be used for other modes as
    long only write (rgTX/cTX) or read (rgRX/cRX) is specified. The number of
    clock signals generated is the maximum of cTX and cRX.
    '''
    out_rgTX = ctypes.c_int(0)
    out_rgRX = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalSpiWriteRead(ctypes.c_int(hdwf), ctypes.c_int(cDQ), ctypes.c_int(cBitPerWord), ctypes.c_int(cTX), ctypes.c_int(cRX), ctypes.byref(out_rgTX), ctypes.byref(out_rgRX)))
    return int(out_rgTX.value), int(out_rgRX.value)

# DWFAPI int FDwfDigitalSpiWriteRead16(HDWF hdwf, int cDQ, int cBitPerWord, unsigned short *rgTX, int cTX, unsigned short *rgRX, int cRX);
def DigitalSpiWriteRead16(hdwf: int, cDQ: int, cBitPerWord: int, cTX: int, cRX: int) -> (int, int):
    '''
    Performs SPI transfer of up to 16-bit words. See FDwfDigitalSpiWriteRead for
    more information.
    '''
    out_rgTX = ctypes.c_int(0)
    out_rgRX = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalSpiWriteRead16(ctypes.c_int(hdwf), ctypes.c_int(cDQ), ctypes.c_int(cBitPerWord), ctypes.c_int(cTX), ctypes.c_int(cRX), ctypes.byref(out_rgTX), ctypes.byref(out_rgRX)))
    return int(out_rgTX.value), int(out_rgRX.value)

# DWFAPI int FDwfDigitalSpiWriteRead32(HDWF hdwf, int cDQ, int cBitPerWord, unsigned int *rgTX, int cTX, unsigned int *rgRX, int cRX);
def DigitalSpiWriteRead32(hdwf: int, cDQ: int, cBitPerWord: int, cTX: int, cRX: int) -> (int, int):
    '''
    Performs SPI transfer of up to 32-bit words. See FDwfDigitalSpiWriteRead for
    more information.
    '''
    out_rgTX = c_uint(0)
    out_rgRX = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalSpiWriteRead32(ctypes.c_int(hdwf), ctypes.c_int(cDQ), ctypes.c_int(cBitPerWord), ctypes.c_int(cTX), ctypes.c_int(cRX), ctypes.byref(out_rgTX), ctypes.byref(out_rgRX)))
    return int(out_rgTX.value), int(out_rgRX.value)

# DWFAPI int FDwfDigitalSpiRead(HDWF hdwf, int cDQ, int cBitPerWord, unsigned char *rgRX, int cRX);
def DigitalSpiRead(hdwf: int, cDQ: int, cBitPerWord: int, cRX: int) -> int:
    '''
    Performs SPI reception of up to 8-bit words. See FDwfDigitalSpiWriteRead for
    more information.
    '''
    out_rgRX = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalSpiRead(ctypes.c_int(hdwf), ctypes.c_int(cDQ), ctypes.c_int(cBitPerWord), ctypes.c_int(cRX), ctypes.byref(out_rgRX)))
    return int(out_rgRX.value)

# DWFAPI int FDwfDigitalSpiReadOne(HDWF hdwf, int cDQ, int cBitPerWord, unsigned int *pRX);
def DigitalSpiReadOne(hdwf: int, cDQ: int, cBitPerWord: int) -> int:
    '''
    Performs SPI reception of up to 32 bits. See FDwfDigitalSpiWriteRead for
    more information.
    '''
    out_RX = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalSpiReadOne(ctypes.c_int(hdwf), ctypes.c_int(cDQ), ctypes.c_int(cBitPerWord), ctypes.byref(out_RX)))
    return int(out_RX.value)

# DWFAPI int FDwfDigitalSpiRead16(HDWF hdwf, int cDQ, int cBitPerWord, unsigned short *rgRX, int cRX);
def DigitalSpiRead16(hdwf: int, cDQ: int, cBitPerWord: int, cRX: int) -> int:
    '''
    Performs SPI read of up to 16-bit words. See FDwfDigitalSpiWriteRead for
    more information.
    '''
    out_rgRX = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalSpiRead16(ctypes.c_int(hdwf), ctypes.c_int(cDQ), ctypes.c_int(cBitPerWord), ctypes.c_int(cRX), ctypes.byref(out_rgRX)))
    return int(out_rgRX.value)

# DWFAPI int FDwfDigitalSpiRead32(HDWF hdwf, int cDQ, int cBitPerWord, unsigned int *rgRX, int cRX);
def DigitalSpiRead32(hdwf: int, cDQ: int, cBitPerWord: int, cRX: int) -> int:
    '''
    Performs SPI read of up to 32-bit words. See FDwfDigitalSpiWriteRead for
    more information.
    '''
    out_rgRX = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalSpiRead32(ctypes.c_int(hdwf), ctypes.c_int(cDQ), ctypes.c_int(cBitPerWord), ctypes.c_int(cRX), ctypes.byref(out_rgRX)))
    return int(out_rgRX.value)

# DWFAPI int FDwfDigitalSpiWrite(HDWF hdwf, int cDQ, int cBitPerWord, unsigned char *rgTX, int cTX);
def DigitalSpiWrite(hdwf: int, cDQ: int, cBitPerWord: int, cTX: int) -> int:
    '''
    Performs SPI transmission of up to 8-bit words. See FDwfDigitalSpiWriteRead
    for more information.
    '''
    out_rgTX = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalSpiWrite(ctypes.c_int(hdwf), ctypes.c_int(cDQ), ctypes.c_int(cBitPerWord), ctypes.c_int(cTX), ctypes.byref(out_rgTX)))
    return int(out_rgTX.value)

# DWFAPI int FDwfDigitalSpiWriteOne(HDWF hdwf, int cDQ, int cBits, unsigned int vTX);
def DigitalSpiWriteOne(hdwf: int, cDQ: int, cBits: int, vTX: int) -> None:
    '''
    Performs SPI transmit of up to 32 bits. See FDwfDigitalSpiWriteRead for more
    information.
    '''
    _ThrowIfError(_dwf.FDwfDigitalSpiWriteOne(ctypes.c_int(hdwf), ctypes.c_int(cDQ), ctypes.c_int(cBits), ctypes.c_uint(vTX)))

# DWFAPI int FDwfDigitalSpiWrite16(HDWF hdwf, int cDQ, int cBitPerWord, unsigned short *rgTX, int cTX);
def DigitalSpiWrite16(hdwf: int, cDQ: int, cBitPerWord: int, cTX: int) -> int:
    '''
    Performs SPI read of up to 16-bit words. See FDwfDigitalSpiWriteRead for
    more information.
    '''
    out_rgTX = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalSpiWrite16(ctypes.c_int(hdwf), ctypes.c_int(cDQ), ctypes.c_int(cBitPerWord), ctypes.c_int(cTX), ctypes.byref(out_rgTX)))
    return int(out_rgTX.value)

# DWFAPI int FDwfDigitalSpiWrite32(HDWF hdwf, int cDQ, int cBitPerWord, unsigned int *rgTX, int cTX);
def DigitalSpiWrite32(hdwf: int, cDQ: int, cBitPerWord: int, cTX: int) -> int:
    '''
    Performs SPI read of up to 32-bit words. See FDwfDigitalSpiWriteRead for
    more information.
    '''
    out_rgTX = c_uint(0)
    _ThrowIfError(_dwf.FDwfDigitalSpiWrite32(ctypes.c_int(hdwf), ctypes.c_int(cDQ), ctypes.c_int(cBitPerWord), ctypes.c_int(cTX), ctypes.byref(out_rgTX)))
    return int(out_rgTX.value)

# DWFAPI int FDwfDigitalI2cReset(HDWF hdwf);
def DigitalI2cReset(hdwf: int) -> None:
    '''
    Resets the I2C configuration to default value.
    '''
    _ThrowIfError(_dwf.FDwfDigitalI2cReset(ctypes.c_int(hdwf)))

# DWFAPI int FDwfDigitalI2cClear(HDWF hdwf, int *pfFree);
def DigitalI2cClear(hdwf: int) -> int:
    '''
    Verifies and tries to solve eventual bus lockup. The argument returns true,
    non-zero value if the bus is free.
    '''
    out_free = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalI2cClear(ctypes.c_int(hdwf), ctypes.byref(out_free)))
    return int(out_free.value)

# DWFAPI int FDwfDigitalI2cStretchSet(HDWF hdwf, int fEnable);
def DigitalI2cStretchSet(hdwf: int, enable: bool) -> None:
    '''
    Enables or disables clock stretching.
    '''
    _ThrowIfError(_dwf.FDwfDigitalI2cStretchSet(ctypes.c_int(hdwf), ctypes.c_int(enable)))

# DWFAPI int FDwfDigitalI2cRateSet(HDWF hdwf, double hz);
def DigitalI2cRateSet(hdwf: int, hz: float) -> None:
    '''
    Sets the data rate.
    '''
    _ThrowIfError(_dwf.FDwfDigitalI2cRateSet(ctypes.c_int(hdwf), ctypes.c_double(hz)))

# DWFAPI int FDwfDigitalI2cReadNakSet(HDWF hdwf, int fNakLastReadByte);
def DigitalI2cReadNakSet(hdwf: int, fNakLastReadByte: int) -> None:
    '''
    Specifies if the last read byte should be acknowledged or not. The I2C
    specifications require NAK, this parameter set to true.
    '''
    _ThrowIfError(_dwf.FDwfDigitalI2cReadNakSet(ctypes.c_int(hdwf), ctypes.c_int(fNakLastReadByte)))

# DWFAPI int FDwfDigitalI2cSclSet(HDWF hdwf, int idxChannel);
def DigitalI2cSclSet(hdwf: int, channel_index: int) -> None:
    '''
    Specifies the DIO channel to use for I2C clock.
    '''
    _ThrowIfError(_dwf.FDwfDigitalI2cSclSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index)))

# DWFAPI int FDwfDigitalI2cSdaSet(HDWF hdwf, int idxChannel);
def DigitalI2cSdaSet(hdwf: int, channel_index: int) -> None:
    '''
    Specifies the DIO channel to use for I2C data.
    '''
    _ThrowIfError(_dwf.FDwfDigitalI2cSdaSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index)))

# DWFAPI int FDwfDigitalI2cWriteRead(HDWF hdwf, unsigned char adr8bits, unsigned char *rgbTx, int cTx, unsigned char *rgRx, int cRx, int *pNak);
def DigitalI2cWriteRead(hdwf: int, address: int, write_data: List[int], read_data_size: int) -> (List[int], int):
    '''
    Performs I2C write, repeated start and read. In case zero bytes are
    specified for read (cRx) only write and for zero write (cTx) only read is
    performed. The read/write bit in the address is controlled by the function.
    The returned NAK index returns one based index of the first negative
    acknowledged transfer byte, zero when all the bytes where acknowledged. When
    the first address is acknowledged it returns 1. Returns negative value for
    other communication failures like timeout.
    '''
    read_data = []
    out_nak = ctypes.c_int(0)
    out_read_data = (ctypes.c_uint8 * read_data_size)()
    write_data_len = ctypes.c_int(len(write_data))
    local_write_data = (ctypes.c_uint8 * write_data_len.value)(*write_data)

    _ThrowIfError(_dwf.FDwfDigitalI2cWriteRead(ctypes.c_int(hdwf), ctypes.c_int(address<<1), local_write_data, write_data_len, ctypes.byref(out_read_data), ctypes.c_int(read_data_size), ctypes.byref(out_nak)))

    #if (out_nak.value != 0):
    #    print("Device Data NAK " + str(out_nak.value))
    for i in range(read_data_size): read_data.append(out_read_data[i])
    return (read_data, int(out_nak.value))

# DWFAPI int FDwfDigitalI2cRead(HDWF hdwf, unsigned char adr8bits, unsigned char *rgbRx, int cRx, int *pNak);
def DigitalI2cRead(hdwf: int, address: int, read_data_size: int) -> (int, int):
    '''
    Performs I2C read. See DwfDigitalI2cWriteRead function for more information.
    '''
    read_data = []
    out_nak = ctypes.c_int(0)
    out_read_data = (ctypes.c_uint8 * read_data_size)()
    _ThrowIfError(_dwf.FDwfDigitalI2cRead(ctypes.c_int(hdwf), ctypes.c_int(address<<1), ctypes.byref(out_read_data), ctypes.c_int(read_data_size), ctypes.byref(out_nak)))
    return (read_data, int(out_nak.value))

# DWFAPI int FDwfDigitalI2cWrite(HDWF hdwf, unsigned char adr8bits, unsigned char *rgbTx, int cTx, int *pNak);
def DigitalI2cWrite(hdwf: int, address: int, write_data: List[int]) -> int:
    '''
    Performs I2C write. See DwfDigitalI2cWriteRead function for more
    information.
    '''
    out_nak = ctypes.c_int(0)
    write_data_len = ctypes.c_int(len(write_data))
    local_write_data = (ctypes.c_uint8 * write_data_len.value)(*write_data)
    _ThrowIfError(_dwf.FDwfDigitalI2cWrite(ctypes.c_int(hdwf), ctypes.c_int(address<<1), local_write_data, write_data_len, ctypes.byref(out_nak)))
    return int(out_nak.value)

# DWFAPI int FDwfDigitalI2cWriteOne(HDWF hdwf, unsigned char adr8bits, unsigned char bTx, int *pNak);
def DigitalI2cWriteOne(hdwf: int, address: int, write_data: int) -> int:
    '''
    Performs I2C write of one byte. See DwfDigitalI2cWriteRead function for more
    information.
    '''
    out_nak = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalI2cWriteOne(ctypes.c_int(hdwf), ctypes.c_int(address<<1), ctypes.c_int(write_data), ctypes.byref(out_nak)))
    return int(out_nak.value)

# DWFAPI int FDwfDigitalCanReset(HDWF hdwf);
def DigitalCanReset(hdwf: int) -> None:
    '''
    Resets the CAN configuration to default value. Use FDwfDigitalOutReset to
    reset the output.
    '''
    _ThrowIfError(_dwf.FDwfDigitalCanReset(ctypes.c_int(hdwf)))

# DWFAPI int FDwfDigitalCanRateSet(HDWF hdwf, double hz);
def DigitalCanRateSet(hdwf: int, hz: float) -> None:
    '''
    Sets the data rate.
    '''
    _ThrowIfError(_dwf.FDwfDigitalCanRateSet(ctypes.c_int(hdwf), ctypes.c_double(hz)))

# DWFAPI int FDwfDigitalCanPolaritySet(HDWF hdwf, int fHigh); # 0 low, 1 high
def DigitalCanPolaritySet(hdwf: int, fHigh: int) -> None:
    '''
    Sets the signal polarity.
    '''
    _ThrowIfError(_dwf.FDwfDigitalCanPolaritySet(ctypes.c_int(hdwf), ctypes.c_int(fHigh)))

# DWFAPI int FDwfDigitalCanTxSet(HDWF hdwf, int idxChannel);
def DigitalCanTxSet(hdwf: int, channel_index: int) -> None:
    '''
    Specifies the DIO channel to use for transmission.
    '''
    _ThrowIfError(_dwf.FDwfDigitalCanTxSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index)))

# DWFAPI int FDwfDigitalCanRxSet(HDWF hdwf, int idxChannel);
def DigitalCanRxSet(hdwf: int, channel_index: int) -> None:
    '''
    Specifies the DIO channel to use for reception.
    '''
    _ThrowIfError(_dwf.FDwfDigitalCanRxSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index)))

# DWFAPI int FDwfDigitalCanTx(HDWF hdwf, int vID, int fExtended, int fRemote, int cDLC, unsigned char *rgTX);
def DigitalCanTx(hdwf: int, vID: int, fExtended: int, fRemote: int, cDLC: int) -> int:
    '''
    Performs a CAN transmission. Specifying -1 for vID it initializes the TX
    channel.
    '''
    out_rgTX = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalCanTx(ctypes.c_int(hdwf), ctypes.c_int(vID), ctypes.c_int(fExtended), ctypes.c_int(fRemote), ctypes.c_int(cDLC), ctypes.byref(out_rgTX)))
    return int(out_rgTX.value)

# DWFAPI int FDwfDigitalCanRx(HDWF hdwf, int *pvID, int *pfExtended, int *pfRemote, int *pcDLC, unsigned char *rgRX, int cRX, int *pvStatus);
def DigitalCanRx(hdwf: int, cRX: int) -> (int, int, int, int, int, int):
    '''
    Returns the received frames since the last call. With cRX zero initializes
    the reception.
    '''
    out_vID = ctypes.c_int(0)
    out_fExtended = ctypes.c_int(0)
    out_fRemote = ctypes.c_int(0)
    out_cDLC = ctypes.c_int(0)
    out_rgRX = ctypes.c_int(0)
    out_vStatus = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalCanRx(ctypes.c_int(hdwf), ctypes.c_int(cRX), ctypes.byref(out_vID), ctypes.byref(out_fExtended), ctypes.byref(out_fRemote), ctypes.byref(out_cDLC), ctypes.byref(out_rgRX), ctypes.byref(out_vStatus)))
    return int(out_vID.value), int(out_fExtended.value), int(out_fRemote.value), int(out_cDLC.value), int(out_rgRX.value), int(out_vStatus.value)

# DWFAPI int FDwfAnalogImpedanceReset(HDWF hdwf);
def AnalogImpedanceReset(hdwf: int) -> None:
    '''
    Resets the AI configuration to default value.
    '''
    _ThrowIfError(_dwf.FDwfAnalogImpedanceReset(ctypes.c_int(hdwf)))

# DWFAPI int FDwfAnalogImpedanceModeSet(HDWF hdwf, int mode); # 0 W1-C1-DUT-C2-R-GND, 1 W1-C1-R-C2-DUT-GND, 8 Impedance Analyzer for AD
def AnalogImpedanceModeSet(hdwf: int, mode: int) -> None:
    '''
    Specifies the circuit to be used.
    '''
    _ThrowIfError(_dwf.FDwfAnalogImpedanceModeSet(ctypes.c_int(hdwf), ctypes.c_int(mode)))

# DWFAPI int FDwfAnalogImpedanceModeGet(HDWF hdwf, int *mode);
def AnalogImpedanceModeGet(hdwf: int) -> int:
    '''
    Returns the selected circuit model.
    '''
    out_mode = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogImpedanceModeGet(ctypes.c_int(hdwf), ctypes.byref(out_mode)))
    return int(out_mode.value)

# DWFAPI int FDwfAnalogImpedanceReferenceSet(HDWF hdwf, double ohms);
def AnalogImpedanceReferenceSet(hdwf: int, ohms: float) -> None:
    '''
    Specifies the reference resistor to be used. For AD IA module the resistor
    is selected by relays controlled by power supplies and digital IOs.
    '''
    _ThrowIfError(_dwf.FDwfAnalogImpedanceReferenceSet(ctypes.c_int(hdwf), ctypes.c_double(ohms)))

# DWFAPI int FDwfAnalogImpedanceReferenceGet(HDWF hdwf, double *pohms);
def AnalogImpedanceReferenceGet(hdwf: int) -> float:
    '''
    Returns the reference resistor value.
    '''
    out_ohms = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogImpedanceReferenceGet(ctypes.c_int(hdwf), ctypes.byref(out_ohms)))
    return float(out_ohms.value)

# DWFAPI int FDwfAnalogImpedanceFrequencySet(HDWF hdwf, double hz);
def AnalogImpedanceFrequencySet(hdwf: int, hz: float) -> None:
    '''
    Configures the stimulus frequency.
    '''
    _ThrowIfError(_dwf.FDwfAnalogImpedanceFrequencySet(ctypes.c_int(hdwf), ctypes.c_double(hz)))

# DWFAPI int FDwfAnalogImpedanceFrequencyGet(HDWF hdwf, double *phz);
def AnalogImpedanceFrequencyGet(hdwf: int) -> float:
    '''
    Returns the frequency value.
    '''
    out_hz = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogImpedanceFrequencyGet(ctypes.c_int(hdwf), ctypes.byref(out_hz)))
    return float(out_hz.value)

# DWFAPI int FDwfAnalogImpedanceAmplitudeSet(HDWF hdwf, double volts);
def AnalogImpedanceAmplitudeSet(hdwf: int, volts: float) -> None:
    '''
    Configures the stimulus signal amplitude, half of the peak to peak value.
    '''
    _ThrowIfError(_dwf.FDwfAnalogImpedanceAmplitudeSet(ctypes.c_int(hdwf), ctypes.c_double(volts)))

# DWFAPI int FDwfAnalogImpedanceAmplitudeGet(HDWF hdwf, double *pvolts);
def AnalogImpedanceAmplitudeGet(hdwf: int) -> float:
    '''
    Returns the amplitude value.
    '''
    out_volts = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogImpedanceAmplitudeGet(ctypes.c_int(hdwf), ctypes.byref(out_volts)))
    return float(out_volts.value)

# DWFAPI int FDwfAnalogImpedanceOffsetSet(HDWF hdwf, double volts);
def AnalogImpedanceOffsetSet(hdwf: int, volts: float) -> None:
    '''
    Configures the stimulus signal offset.
    '''
    _ThrowIfError(_dwf.FDwfAnalogImpedanceOffsetSet(ctypes.c_int(hdwf), ctypes.c_double(volts)))

# DWFAPI int FDwfAnalogImpedanceOffsetGet(HDWF hdwf, double *pvolts);
def AnalogImpedanceOffsetGet(hdwf: int) -> float:
    '''
    Returns the offset value.
    '''
    out_volts = ctypes.c_double(0)
    _ThrowIfError(_dwf.FDwfAnalogImpedanceOffsetGet(ctypes.c_int(hdwf), ctypes.byref(out_volts)))
    return float(out_volts.value)

# DWFAPI int FDwfAnalogImpedanceProbeSet(HDWF hdwf, double ohmRes, double faradCap);
def AnalogImpedanceProbeSet(hdwf: int, ohmRes: float, faradCap: float) -> None:
    '''
    Specifies the probe impedance that will be taken in consideration for
    measurements. The default values are set specific for device when calling
    the FDwfAnalogImpedanceReset function.
    '''
    _ThrowIfError(_dwf.FDwfAnalogImpedanceProbeSet(ctypes.c_int(hdwf), ctypes.c_double(ohmRes), ctypes.c_double(faradCap)))

# DWFAPI int FDwfAnalogImpedanceProbeGet(HDWF hdwf, double *pohmRes, double *pfaradCap);
def AnalogImpedanceProbeGet(hdwf: int) -> (float, float):
    '''
    Returns the probe impedance.
    '''
    out_ohmRes = ctypes.c_double(0.0)
    out_faradCap = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogImpedanceProbeGet(ctypes.c_int(hdwf), ctypes.byref(out_ohmRes), ctypes.byref(out_faradCap)))
    return float(out_ohmRes.value), float(out_faradCap.value)

# DWFAPI int FDwfAnalogImpedancePeriodSet(HDWF hdwf, int cMinPeriods);
def AnalogImpedancePeriodSet(hdwf: int, min_period: int) -> None:
    '''
    Specifies the minimum number of periods to be captured.
    '''
    _ThrowIfError(_dwf.FDwfAnalogImpedancePeriodSet(ctypes.c_int(hdwf), ctypes.c_int(min_period)))

# DWFAPI int FDwfAnalogImpedancePeriodGet(HDWF hdwf, int *cMinPeriods);
def AnalogImpedancePeriodGet(hdwf: int) -> int:
    '''
    Returns the periods value.
    '''
    out_min_period = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogImpedancePeriodGet(ctypes.c_int(hdwf), ctypes.byref(out_min_period)))
    return int(out_min_period.value)

# DWFAPI int FDwfAnalogImpedanceCompReset(HDWF hdwf);
def AnalogImpedanceCompReset(hdwf: int) -> None:
    '''
    Resets the currently configured compensation parameters.
    '''
    _ThrowIfError(_dwf.FDwfAnalogImpedanceCompReset(ctypes.c_int(hdwf)))

# DWFAPI int FDwfAnalogImpedanceCompSet(HDWF hdwf, double ohmOpenResistance, double ohmOpenReactance, double ohmShortResistance, double ohmShortReactance);
def AnalogImpedanceCompSet(hdwf: int, ohmOpenResistance: float, ohmOpenReactance: float, ohmShortResistance: float, ohmShortReactance: float) -> None:
    '''
    Specifies the open and short compensation parameters. These values are
    specific for the circuit/adapter.
    '''
    _ThrowIfError(_dwf.FDwfAnalogImpedanceCompSet(ctypes.c_int(hdwf), ctypes.c_double(ohmOpenResistance), ctypes.c_double(ohmOpenReactance), ctypes.c_double(ohmShortResistance), ctypes.c_double(ohmShortReactance)))

# DWFAPI int FDwfAnalogImpedanceCompGet(HDWF hdwf, double *pohmOpenResistance, double *pohmOpenReactance, double *pohmShortResistance, double *pohmShortReactance);
def AnalogImpedanceCompGet(hdwf: int) -> (float, float, float, float):
    '''
    Returns the compensation parameters.
    '''
    out_ohmOpenResistance = ctypes.c_double(0.0)
    out_ohmOpenReactance = ctypes.c_double(0.0)
    out_ohmShortResistance = ctypes.c_double(0.0)
    out_ohmShortReactance = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogImpedanceCompGet(ctypes.c_int(hdwf), ctypes.byref(out_ohmOpenResistance), ctypes.byref(out_ohmOpenReactance), ctypes.byref(out_ohmShortResistance), ctypes.byref(out_ohmShortReactance)))
    return float(out_ohmOpenResistance.value), float(out_ohmOpenReactance.value), float(out_ohmShortResistance.value), float(out_ohmShortReactance.value)

# DWFAPI int FDwfAnalogImpedanceConfigure(HDWF hdwf, int fStart); # 1 start, 0 stop
# Warning no docs found for FDwfAnalogImpedanceConfigure
def AnalogImpedanceConfigure(hdwf: int, fStart: int) -> None:
    _ThrowIfError(_dwf.FDwfAnalogImpedanceConfigure(ctypes.c_int(hdwf), ctypes.c_int(fStart)))

# DWFAPI int FDwfAnalogImpedanceStatus(HDWF hdwf, DwfState *psts);
def AnalogImpedanceStatus(hdwf: int) -> int:
    '''
    Checks the state of the acquisition.
    '''
    out_instrument_state = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogImpedanceStatus(ctypes.c_int(hdwf), ctypes.byref(out_instrument_state)))
    return int(out_instrument_state.value)

# DWFAPI int FDwfAnalogImpedanceStatusInput(HDWF hdwf, int idxChannel, double *pgain, double *pradian);
def AnalogImpedanceStatusInput(hdwf: int, channel_index: int) -> (float, float):
    '''
    Read the raw input, for network analysis purpose. This returns the raw
    values without taking in consideration the probe characteristics or
    compensation parameters. For scope channel 1 (idxChannel = 0) the gain is
    relative to Wavegen amplitude (Ampltiude/Channel1) and the phase is zero.
    For further channels the gain and phase is relative to channel 1, gain =
    C1/C# The gain value is dimensionless, it represents the V/V ratio.
    '''
    out_gain = ctypes.c_double(0.0)
    out_radian = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogImpedanceStatusInput(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_gain), ctypes.byref(out_radian)))
    return float(out_gain.value), float(out_radian.value)

# DWFAPI int FDwfAnalogImpedanceStatusMeasure(HDWF hdwf, DwfAnalogImpedance measure, double *pvalue);
def AnalogImpedanceStatusMeasure(hdwf: int, measure: int) -> float:
    '''
    Read the DUT measurements. These take in account the scope probe
    characteristics and compensation parameters.
    '''
    out_value = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogImpedanceStatusMeasure(ctypes.c_int(hdwf), ctypes.c_int(measure), ctypes.byref(out_value)))
    return float(out_value.value)

# OBSOLETE but supported, avoid using the following in new projects:
#    KeepOnClose     = 1; # keep the device running after close, use DwfParamOnClose

# use FDwfDigitalInTriggerSourceSet trigsrcAnalogIn
# call FDwfDigitalInConfigure before FDwfAnalogInConfigure
# DWFAPI int FDwfDigitalInMixedSet(HDWF hdwf, int fEnable);
# Warning no docs found for FDwfDigitalInMixedSet
def DigitalInMixedSet(hdwf: int, enable: int) -> None:
    _ThrowIfError(_dwf.FDwfDigitalInMixedSet(ctypes.c_int(hdwf), ctypes.c_int(enable)))

# use DwfTriggerSlope
# typedef int TRIGCOND;
class TriggerCondition(IntEnum):
    RISING_POSITIVE    = 0
    FALLING_NEGATIVE   = 1
    def __str__(self):
        return self.name.replace("_", " ").title()

# use FDwfDeviceTriggerInfo(hdwf, ptrigsrcInfo);
# DWFAPI int FDwfAnalogInTriggerSourceInfo(HDWF hdwf, int *pfstrigsrc); # use IsBitSet
# Warning no docs found for FDwfAnalogInTriggerSourceInfo
def AnalogInTriggerSourceInfo(hdwf: int) -> int:
    out_fstrigsrc = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogInTriggerSourceInfo(ctypes.c_int(hdwf), ctypes.byref(out_fstrigsrc)))
    return int(out_fstrigsrc.value)

# DWFAPI int FDwfAnalogOutTriggerSourceInfo(HDWF hdwf, int idxChannel, int *pfstrigsrc); # use IsBitSet
# Warning no docs found for FDwfAnalogOutTriggerSourceInfo
def AnalogOutTriggerSourceInfo(hdwf: int, channel_index: int) -> int:
    out_fstrigsrc = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutTriggerSourceInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_fstrigsrc)))
    return int(out_fstrigsrc.value)

# DWFAPI int FDwfDigitalInTriggerSourceInfo(HDWF hdwf, int *pfstrigsrc); # use IsBitSet
# Warning no docs found for FDwfDigitalInTriggerSourceInfo
def DigitalInTriggerSourceInfo(hdwf: int) -> int:
    out_fstrigsrc = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalInTriggerSourceInfo(ctypes.c_int(hdwf), ctypes.byref(out_fstrigsrc)))
    return int(out_fstrigsrc.value)

# DWFAPI int FDwfDigitalOutTriggerSourceInfo(HDWF hdwf, int *pfstrigsrc); # use IsBitSet
# Warning no docs found for FDwfDigitalOutTriggerSourceInfo
def DigitalOutTriggerSourceInfo(hdwf: int) -> int:
    out_fstrigsrc = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfDigitalOutTriggerSourceInfo(ctypes.c_int(hdwf), ctypes.byref(out_fstrigsrc)))
    return int(out_fstrigsrc.value)

# use DwfState
# typedef unsigned char STS;
class Sts(IntEnum):
    READY      = 0
    ARM        = 1
    DONE       = 2
    TRIG       = 3
    CFG        = 4
    PREFILL    = 5
    NOTDONE    = 6
    TRIGDLY    = 7
    ERROR      = 8
    BUSY       = 9
    STOP       = 10
    def __str__(self):
        return self.name.replace("_", " ").title()

# use FDwfAnalogOutNode*
# DWFAPI int FDwfAnalogOutEnableSet(HDWF hdwf, int idxChannel, int fEnable);
def AnalogOutEnableSet(hdwf: int, channel_index: int, enable: int) -> None:
    '''
    Enables or disables the channel specified by idxChannel. With channel index
    -1, each Analog Out channel enable will be configured to use the same, new
    option.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutEnableSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(enable)))

# DWFAPI int FDwfAnalogOutEnableGet(HDWF hdwf, int idxChannel, int *pfEnable);
def AnalogOutEnableGet(hdwf: int, channel_index: int) -> int:
    '''
    Verifies if a specific channel is enabled or disabled.
    '''
    out_enable = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutEnableGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_enable)))
    return int(out_enable.value)

# DWFAPI int FDwfAnalogOutFunctionInfo(HDWF hdwf, int idxChannel, unsigned int *pfsfunc); # use IsBitSet
def AnalogOutFunctionInfo(hdwf: int, channel_index: int) -> int:
    '''
    Returns the supported generator function options. They are returned (by
    reference) as a bit field. This bit field can be parsed using the IsBitSet
    Macro. Individual bits are defined using the FUNC constants in dwf.h. These
    are:
    '''
    out_fsfunc = c_uint(0)
    _ThrowIfError(_dwf.FDwfAnalogOutFunctionInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_fsfunc)))
    return int(out_fsfunc.value)

# DWFAPI int FDwfAnalogOutFunctionSet(HDWF hdwf, int idxChannel, FUNC func);
def AnalogOutFunctionSet(hdwf: int, channel_index: int, func: int) -> None:
    '''
    Sets the generator output function for the specified instrument channel.
    With channel index -1, each enabled Analog Out channel function will be
    configured to use the same, new option.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutFunctionSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(func)))

# DWFAPI int FDwfAnalogOutFunctionGet(HDWF hdwf, int idxChannel, FUNC *pfunc);
def AnalogOutFunctionGet(hdwf: int, channel_index: int) -> int:
    '''
    Retrieves the current generator function option for the specified instrument
    channel.
    '''
    out_func = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutFunctionGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_func)))
    return int(out_func.value)

# DWFAPI int FDwfAnalogOutFrequencyInfo(HDWF hdwf, int idxChannel, double *phzMin, double *phzMax);
def AnalogOutFrequencyInfo(hdwf: int, channel_index: int) -> (float, float):
    '''
    Returns the supported frequency range for the instrument. The maximum value
    shows the DAC frequency. The frequency of the generated waveform: repetition
    frequency for standard types and custom data; DAC update for noise type;
    sample rate for play type.
    '''
    out_hz_min = ctypes.c_double(0.0)
    out_hz_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutFrequencyInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_hz_min), ctypes.byref(out_hz_max)))
    return float(out_hz_min.value), float(out_hz_max.value)

# DWFAPI int FDwfAnalogOutFrequencySet(HDWF hdwf, int idxChannel, double hzFrequency);
def AnalogOutFrequencySet(hdwf: int, channel_index: int, frequency_in_hz: float) -> None:
    '''
    Sets the frequency. With channel index -1, each enabled Analog Out channel
    frequency will be configured to use the same, new option.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutFrequencySet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_double(frequency_in_hz)))

# DWFAPI int FDwfAnalogOutFrequencyGet(HDWF hdwf, int idxChannel, double *phzFrequency);
def AnalogOutFrequencyGet(hdwf: int, channel_index: int) -> float:
    '''
    Gets the currently set frequency for the specified channel on the
    instrument.
    '''
    out_frequency_in_hz = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutFrequencyGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_frequency_in_hz)))
    return float(out_frequency_in_hz.value)

# DWFAPI int FDwfAnalogOutAmplitudeInfo(HDWF hdwf, int idxChannel, double *pvoltsMin, double *pvoltsMax);
def AnalogOutAmplitudeInfo(hdwf: int, channel_index: int) -> (float, float):
    '''
    Retrieves the amplitude range for the specified channel on the instrument.
    The amplitude is expressed in Volts units for carrier and in percentage
    units (modulation index) for AM/FM.
    '''
    out_volts_min = ctypes.c_double(0.0)
    out_volts_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutAmplitudeInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_volts_min), ctypes.byref(out_volts_max)))
    return float(out_volts_min.value), float(out_volts_max.value)

# DWFAPI int FDwfAnalogOutAmplitudeSet(HDWF hdwf, int idxChannel, double voltsAmplitude);
def AnalogOutAmplitudeSet(hdwf: int, channel_index: int, voltsAmplitude: float) -> None:
    '''
    Sets the amplitude or modulation index for the specified channel on the
    instrument. With channel index -1, each enabled Analog Out channel amplitude
    will be configured to use the same, new option.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutAmplitudeSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_double(voltsAmplitude)))

# DWFAPI int FDwfAnalogOutAmplitudeGet(HDWF hdwf, int idxChannel, double *pvoltsAmplitude);
def AnalogOutAmplitudeGet(hdwf: int, channel_index: int) -> float:
    '''
    Gets the currently set amplitude or modulation index for the specified
    channel on the instrument.
    '''
    out_voltsAmplitude = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutAmplitudeGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_voltsAmplitude)))
    return float(out_voltsAmplitude.value)

# DWFAPI int FDwfAnalogOutOffsetInfo(HDWF hdwf, int idxChannel, double *pvoltsMin, double *pvoltsMax);
def AnalogOutOffsetInfo(hdwf: int, channel_index: int) -> (float, float):
    '''
    Retrieves available the offset range in units of volts.
    '''
    out_volts_min = ctypes.c_double(0.0)
    out_volts_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutOffsetInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_volts_min), ctypes.byref(out_volts_max)))
    return float(out_volts_min.value), float(out_volts_max.value)

# DWFAPI int FDwfAnalogOutOffsetSet(HDWF hdwf, int idxChannel, double voltsOffset);
def AnalogOutOffsetSet(hdwf: int, channel_index: int, voltsOffset: float) -> None:
    '''
    Sets the offset value for the specified channel on the instrument. With
    channel index -1, each enabled Analog Out channel offset will be configured
    to use the same, new option.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutOffsetSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_double(voltsOffset)))

# DWFAPI int FDwfAnalogOutOffsetGet(HDWF hdwf, int idxChannel, double *pvoltsOffset);
def AnalogOutOffsetGet(hdwf: int, channel_index: int) -> float:
    '''
    Gets the current offset value for the specified channel on the instrument.
    '''
    out_voltsOffset = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutOffsetGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_voltsOffset)))
    return float(out_voltsOffset.value)

# DWFAPI int FDwfAnalogOutSymmetryInfo(HDWF hdwf, int idxChannel, double *ppercentageMin, double *ppercentageMax);
def AnalogOutSymmetryInfo(hdwf: int, channel_index: int) -> (float, float):
    '''
    Obtains the symmetry (or duty cycle) range (0..100). This symmetry is
    supported for standard signal types. It the pulse duration divided by the
    pulse period.
    '''
    out_percentage_min = ctypes.c_double(0.0)
    out_percentage_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutSymmetryInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_percentage_min), ctypes.byref(out_percentage_max)))
    return float(out_percentage_min.value), float(out_percentage_max.value)

# DWFAPI int FDwfAnalogOutSymmetrySet(HDWF hdwf, int idxChannel, double percentageSymmetry);
def AnalogOutSymmetrySet(hdwf: int, channel_index: int, percentage_symmetry: float) -> None:
    '''
    Sets the symmetry (or duty cycle) for the specified channel on the
    instrument. With channel index -1, each enabled Analog Out channel symmetry
    will be configured to use the same, new option.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutSymmetrySet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_double(percentage_symmetry)))

# DWFAPI int FDwfAnalogOutSymmetryGet(HDWF hdwf, int idxChannel, double *ppercentageSymmetry);
def AnalogOutSymmetryGet(hdwf: int, channel_index: int) -> float:
    '''
    Gets the currently set symmetry (or duty cycle) for the specified channel of
    the instrument.
    '''
    out_percentage_symmetry = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutSymmetryGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_percentage_symmetry)))
    return float(out_percentage_symmetry.value)

# DWFAPI int FDwfAnalogOutPhaseInfo(HDWF hdwf, int idxChannel, double *pdegreeMin, double *pdegreeMax);
def AnalogOutPhaseInfo(hdwf: int, channel_index: int) -> (float, float):
    '''
    Retrieves the phase range (in degrees 0…360) for the specified channel of
    the instrument.
    '''
    out_degree_min = ctypes.c_double(0.0)
    out_degree_max = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutPhaseInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_degree_min), ctypes.byref(out_degree_max)))
    return float(out_degree_min.value), float(out_degree_max.value)

# DWFAPI int FDwfAnalogOutPhaseSet(HDWF hdwf, int idxChannel, double degreePhase);
def AnalogOutPhaseSet(hdwf: int, channel_index: int, degree_phase: float) -> None:
    '''
    Sets the phase for the specified channel on the instrument. With channel
    index -1, each enabled Analog Out channel phase will be configured to use
    the same, new option.
    '''
    _ThrowIfError(_dwf.FDwfAnalogOutPhaseSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_double(degree_phase)))

# DWFAPI int FDwfAnalogOutPhaseGet(HDWF hdwf, int idxChannel, double *pdegreePhase);
def AnalogOutPhaseGet(hdwf: int, channel_index: int) -> float:
    '''
    Gets the current phase for the specified channel on the instrument.
    '''
    out_degree_phase = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutPhaseGet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_degree_phase)))
    return float(out_degree_phase.value)

# DWFAPI int FDwfAnalogOutDataInfo(HDWF hdwf, int idxChannel, int *pnSamplesMin, int *pnSamplesMax);
def AnalogOutDataInfo(hdwf: int, channel_index: int) -> (int, int):
    '''
    Retrieves the minimum and maximum number of samples allowed for custom data
    generation.
    '''
    out_samples_min = ctypes.c_int(0)
    out_samples_max = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutDataInfo(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_samples_min), ctypes.byref(out_samples_max)))
    return int(out_samples_min.value), int(out_samples_max.value)

# DWFAPI int FDwfAnalogOutDataSet(HDWF hdwf, int idxChannel, double *rgdData, int cdData);
def AnalogOutDataSet(hdwf: int, channel_index: int, cd_data: int) -> float:
    '''
    Sets the custom data or to prefill the buffer with play samples. The samples
    are double precision floating point values (rgdData) normalized to ±1.
    '''
    out_rgdData = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutDataSet(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(cd_data), ctypes.byref(out_rgdData)))
    return float(out_rgdData.value)

# DWFAPI int FDwfAnalogOutPlayStatus(HDWF hdwf, int idxChannel, int *cdDataFree, int *cdDataLost, int *cdDataCorrupted);
def AnalogOutPlayStatus(hdwf: int, channel_index: int) -> (int, int, int):
    '''
    Retrieves information about the play process. The data lost occurs when the
    device generator is faster than the sample send process from the PC. In this
    case, the device buffer gets emptied and generated samples are repeated.
    Corrupt samples are a warning that the buffer might have been emptied while
    samples were sent to the device. In this case, try optimizing the loop for
    faster execution; or reduce the frequency or run time to be less or equal to
    the device buffer size (run time <= buffer size/frequency).
    '''
    out_cdDataFree = ctypes.c_int(0)
    out_cdDataLost = ctypes.c_int(0)
    out_cdDataCorrupted = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfAnalogOutPlayStatus(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.byref(out_cdDataFree), ctypes.byref(out_cdDataLost), ctypes.byref(out_cdDataCorrupted)))
    return int(out_cdDataFree.value), int(out_cdDataLost.value), int(out_cdDataCorrupted.value)

# DWFAPI int FDwfAnalogOutPlayData(HDWF hdwf, int idxChannel, double *rgdData, int cdData);
def AnalogOutPlayData(hdwf: int, channel_index: int, cd_data: int) -> float:
    '''
    Sends new data samples for play mode. Before starting the Analog Out
    instrument, prefill the device buffer with the first set of samples using
    the AnalogOutDataSet function. In the loop of sending the following samples,
    first call AnalogOutStatus to read the information from the device, then
    AnalogOutPlayStatus to find out how many new samples can be sent, then send
    the samples with AnalogOutPlayData.
    '''
    out_rgdData = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfAnalogOutPlayData(ctypes.c_int(hdwf), ctypes.c_int(channel_index), ctypes.c_int(cd_data), ctypes.byref(out_rgdData)))
    return float(out_rgdData.value)

# DWFAPI int FDwfEnumAnalogInChannels(int idxDevice, int *pnChannels);
# Warning no docs found for FDwfEnumAnalogInChannels
def EnumAnalogInChannels(device_index: int) -> int:
    out_number_of_channels = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfEnumAnalogInChannels(ctypes.c_int(device_index), ctypes.byref(out_number_of_channels)))
    return int(out_number_of_channels.value)

# DWFAPI int FDwfEnumAnalogInBufferSize(int idxDevice, int *pnBufferSize);
# Warning no docs found for FDwfEnumAnalogInBufferSize
def EnumAnalogInBufferSize(device_index: int) -> int:
    out_buffer_size = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfEnumAnalogInBufferSize(ctypes.c_int(device_index), ctypes.byref(out_buffer_size)))
    return int(out_buffer_size.value)

# DWFAPI int FDwfEnumAnalogInBits(int idxDevice, int *pnBits);
# Warning no docs found for FDwfEnumAnalogInBits
def EnumAnalogInBits(device_index: int) -> int:
    out_number_of_bits = ctypes.c_int(0)
    _ThrowIfError(_dwf.FDwfEnumAnalogInBits(ctypes.c_int(device_index), ctypes.byref(out_number_of_bits)))
    return int(out_number_of_bits.value)

# DWFAPI int FDwfEnumAnalogInFrequency(int idxDevice, double *phzFrequency);
# Warning no docs found for FDwfEnumAnalogInFrequency
def EnumAnalogInFrequency(device_index: int) -> float:
    out_frequency_in_hz = ctypes.c_double(0.0)
    _ThrowIfError(_dwf.FDwfEnumAnalogInFrequency(ctypes.c_int(device_index), ctypes.byref(out_frequency_in_hz)))
    return float(out_frequency_in_hz.value)
