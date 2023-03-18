#!/usr/bin/env python

import serial
import time
import os
from abc import ABCMeta, abstractmethod
from BaseVendor import BaseVendor


class HW_serial_based(BaseVendor):
    __metaclass__ = ABCMeta

    PARITY = serial.PARITY_EVEN
    STOP_BITS = serial.STOPBITS_ONE
    BYTE_SIZE = serial.SEVENBITS

    def __init__(self, port, baudrate):
        self._serial_port = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=self.PARITY,
            stopbits=self.STOP_BITS,
            bytesize=self.BYTE_SIZE)


class RpiDom(HW_serial_based):
    CHANNEL_TELEINFO1 = 'A'
    CHANNEL_TELEINFO2 = 'B'

    def __init__(self, port='/dev/ttyAMA0', baudrate=1200, *args, **kwargs):
        super(RpiDom, self).__init__(port, baudrate, *args, **kwargs)
        self.select_channel(self.CHANNEL_TELEINFO1)

    def read_char(self):
        return self._serial_port.read(1)

    def select_channel(self, channel):
        assert channel in [self.CHANNEL_TELEINFO1, self.CHANNEL_TELEINFO2]
        self._serial_port.write(channel)
        time.sleep(1)


class SolarBox_USB(HW_serial_based):
    def __init__(self, port="/dev/ttyUSB0", baudrate=1200, *args, **kwargs):
        super(SolarBox_USB, self).__init__(port, baudrate, *args, **kwargs)
        raise NotImplementedError()


class UTInfo2(HW_serial_based):
    def __init__(self, port="/dev/ttyUSB0", baudrate=1200, *args, **kwargs):
        ports = os.listdir('/dev/serial/by-id/')
        for uport in ports:
            if 'TINFO-' in uport:
                port = '/dev/serial/by-id/' + uport
        super(UTInfo2, self).__init__(port, baudrate, *args, **kwargs)

    def read_char(self):
        return self._serial_port.read(1)


class PITInfo(HW_serial_based):
    def __init__(self, port="/dev/ttyAMA0", baudrate=1200, *args, **kwargs):
        super(PITInfo, self).__init__(port, baudrate, *args, **kwargs)

    def read_char(self):
        return self._serial_port.read(1)


class UTInfo3(HW_serial_based):
    def __init__(self, port="/dev/ttyACM0", baudrate=1200, *args, **kwargs):
        ports = os.listdir('/dev/serial/by-id/')
        for uport in ports:
            if 'uTinfo-V3' in uport:
                port = '/dev/serial/by-id/' + uport
        super(UTInfo3, self).__init__(port, baudrate, *args, **kwargs)

    def read_char(self):
        return self._serial_port.read(1)


class Teleinfo3(HW_serial_based):
    def __init__(self, port="/dev/ttyACM0", baudrate=1200):
        super(Teleinfo3, self).__init__(port, baudrate)

    def read_char(self):
        return self._serial_port.read(1)
