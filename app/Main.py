import json
import logging

from Parser import Parser

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info("test")

    ti = Parser()
    print(json.dumps(ti.get_frame(), indent=2, separators=(',', ':')))
