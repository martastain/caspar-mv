from pyosc import OSCServer

from .common import *

__all__ = ["OSC"]

class OSC(object):
    def __init__(self, parent):
        self.parent = parent
        self.server = OSCServer((self.parent.osc_host, self.parent.osc_port))
        self.server.addMsgHandler("default", self.message_handler)
        logging.info("Starting osc server")
        thread.start_new_thread(self.server.serve_forever, ())

    def message_handler(self, address, *args):
        if not address.startswith("/channel"):
            return
        elements = address.lstrip("/").split("/")
        id_channel = int(elements[1])

        if len(elements) == 6 and elements[2] == "mixer" and elements[3] == "audio" and elements[5] == "pFS":
            val = int(args[1][0]*100)**1.6
            self.parent.set_vu(id_channel, elements[4], val)
