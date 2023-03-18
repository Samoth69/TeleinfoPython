from BaseVendor import BaseVendor
import itertools
import logging

logger = logging.getLogger(__name__)


# https://github.com/hallard/python-teleinfo/blob/master/teleinfo/parser.py
class Parser:
    MARKER_START_FRAME = chr(2)
    MARKER_STOP_FRAME = chr(3)
    MARKER_END_LINE = '\r\n'

    def __init__(self, hw=None):
        assert hw is not None and isinstance(hw, BaseVendor)
        self._hw = hw
        self._synchro_debut_trame()

    def __iter__(self):
        while True:
            yield self.get_frame()

    def get_frame(self):
        logging.debug("get frame start")
        raw = self._get_raw_frame().strip(self.MARKER_END_LINE)
        try:
            groups = [line.split(" ", 2) for line in raw.split(self.MARKER_END_LINE)]
            frame = dict([
                (k, v) for k, v, chksum in groups if chksum == self._checksum(k, v)
            ])
            if len(frame) != len(groups):
                logger.info("Discarded fields because of bad checksum: {}".format(
                    [f for f in itertools.ifilterfalse(lambda g: g[2] == self._checksum(g[0], g[1]), groups)]
                ))
        except Exception as e:
            logger.error("Caught exception while parsing teleinfo frame: {}".format(e))
            frame = {}
        logging.debug("get frame done")
        return frame

    def _synchro_debut_trame(self):
        logging.debug("synchro début trame")
        while self._hw.read_char() != self.MARKER_START_FRAME:
            pass
        logging.debug("synchro début trame done")

    def _get_raw_frame(self):
        logging.debug("get raw frame start")
        self._synchro_debut_trame()
        frame = ''.join(itertools.takewhile(
            lambda c: c != self.MARKER_STOP_FRAME,
            self._hw)
        )
        logging.debug("get raw frame done")
        return frame

    def _checksum(self, key, value):
        chksum = 32
        chksum += sum([ord(c) for c in key])
        chksum += sum([ord(c) for c in value])
        chksum = (chksum & 63) + 32
        return chr(chksum)
