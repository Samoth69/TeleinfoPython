from abc import ABCMeta, abstractmethod


class BaseVendor:
    __metaclass__ = ABCMeta

    @abstractmethod
    def read_char(self):
        pass

    def __iter__(self):
        while True:
            yield self.read_char()
