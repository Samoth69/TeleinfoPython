from typing import List, Optional

import serial
import itertools
import logging

logger = logging.getLogger(__name__)


# https://github.com/hallard/python-teleinfo/blob/master/teleinfo/parser.py
class Parser:
    MARKER_START_FRAME = b'\x02'
    MARKER_STOP_FRAME = b'\x03'
    MARKER_START_LINE = chr(10)  # LF (\n)
    MARKER_END_LINE = chr(13)  # CR (\r)

    def __init__(self):
        self._serial_port = serial.Serial(
            port="/dev/ttyACM0",
            baudrate=1200,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.SEVENBITS)
        self._synchro_debut_trame()

    def __iter__(self):
        while True:
            yield self.get_frame()

    def get_frame(self):
        logging.debug("get frame start")
        raw = self._get_raw_frame()
        try:
            groups = [line.split(" ", 2) for line in raw.split(self.MARKER_END_LINE)]
            groups.pop()  # enlève le \x03 qui représente la fin de la trame
            logger.debug(groups)
            frame = {}
            for line in groups:
                try:
                    ret = self._process_line(line)
                    if ret is not None:
                        frame[ret[0]] = ret[1]
                except Exception as e:
                    logger.error(f"processing line {line} failed: ", e)
        except Exception as e:
            logger.error("Caught exception while parsing teleinfo frame: ", e)
            frame = {}
        logging.debug("get frame done")
        return frame

    def _process_line(self, line: str) -> Optional[List]:
        line = line.lstrip(self.MARKER_START_LINE).rstrip(self.MARKER_END_LINE)
        group = line.split(" ", 2)
        if group[2] == self._checksum(group[0], group[1]):
            return group
        else:
            logger.error("Checksum error on field ", group[0])
        return None

    def _synchro_debut_trame(self):
        logging.debug("synchro début trame")
        while self._serial_port.read(1) != self.MARKER_START_FRAME:
            pass
        logging.debug("synchro début trame done")

    def _get_raw_frame(self):
        logging.debug("get raw frame start")
        self._synchro_debut_trame()
        frame = self._serial_port.read_until(self.MARKER_STOP_FRAME)
        logging.debug("get raw frame done")
        return frame.decode(encoding="ascii")

    def _checksum(self, key, value):
        chksum = 32
        chksum += sum([ord(c) for c in key])
        chksum += sum([ord(c) for c in value])
        chksum = (chksum & 63) + 32
        return chr(chksum)
