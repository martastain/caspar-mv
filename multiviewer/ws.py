from websockets import *

from .common import *

__all__ = ["WebSockets"]

class WebSockets(object):
    def __init__(self, parent):
        self.parent = parent
        self.server = WebsocketServer(host=self.parent.ws_host, port=self.parent.ws_port)
        thread.start_new_thread(self.server.run_forever, ())

    def send(self, message):
        self.server.send_message_to_all(message)
