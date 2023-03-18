import json
import logging
import paho.mqtt.client as mqtt

from Parser import Parser

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info("test")

    ti = Parser()
    client = mqtt.Client("teleinfo", clean_session=False)
    client.connect("192.168.0.7")
    # print(json.dumps(ti.get_frame(), indent=2, separators=(',', ':')))
    while True:
        data = json.dumps(ti.get_frame())
        client.publish("teleinfo", payload=data, retain=True)
