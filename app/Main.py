import json
import logging

import HwVendors
from Parser import Parser

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info("test")

    ti = Parser(HwVendors.Teleinfo3())
    print(json.dumps(ti.get_frame(), indent=2, separators=(',', ':')))
