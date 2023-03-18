import json

import HwVendors
from Parser import Parser

if __name__ == "__main__":
    ti = Parser(HwVendors.Teleinfo3())
    print(json.dumps(ti.get_frame(), indent=2, separators=(',', ':')))
