import json
import logging
import time

import paho.mqtt.client as mqtt

from Parser import Parser

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("starting")

    ti = Parser()
    client = mqtt.Client("teleinfo", clean_session=False)
    client.connect("192.168.0.7")
    # print(json.dumps(ti.get_frame(), indent=2, separators=(',', ':')))
    while True:
        dic = ti.get_frame()
        dic["_time"] = int(time.time())  # epoch
        client.publish("homeassistant/sensor/teleinfo/linky", payload=json.dumps(dic), retain=True)
