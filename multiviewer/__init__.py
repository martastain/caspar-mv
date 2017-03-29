import json

from nxtools.caspar import CasparCG

from .common import *

from .osc import *
from .osd import *
from .ws import *


class MultiViewerChannel(object):
    def __init__(self, caspar_id, **kwargs):
        self.caspar_id = caspar_id
        self.params = kwargs

    @property
    def title(self):
        return self.params.get("title", "Channel {}".format(self.caspar_id))

    @property
    def source(self):
        return self.params.get("source", False)

    def __repr__(self):
        return self.title


class MultiViewer(object):
    def __init__(self, mv_channel, channels, **kwargs):
        self.mv_channel = mv_channel
        self.caspar_host = kwargs.get("caspar_host", "localhost")
        self.caspar_port = kwargs.get("caspar_port", 5250)
        self.osc_host = kwargs.get("osc_host", "localhost")
        self.osc_port = kwargs.get("osc_port", 5253)
        self.osd_host = kwargs.get("osd_host", "")
        self.osd_port = kwargs.get("osd_port", 8081)
        self.osd_layer = kwargs.get("osd_layer", 100)
        self.osd_template = kwargs.get("osd_template", "mvboot")
        self.ws_host = kwargs.get("ws_host", "")
        self.ws_port = kwargs.get("ws_port", 9001)

        assert type(channels) == list
        self.channels = []
        for i, channel in enumerate(channels):
            if not isinstance(channel, MultiViewerChannel):
                logging.warning("Unexpected type of channel {}. Skipping.".format(i))
            else:
                self.channels.append(channel)

        if len(channels) <= 4:
            self.grid_size = 2
        elif len(channels) <= 9:
            self.grid_size = 3
        else:
            self.grid_size = 4
        self.channel_scale = 1.0 / self.grid_size

        # CasparCG client
        self.caspar = CasparCG(self.caspar_host, self.caspar_port)

        # HTML OSD Layer server
        self.osd = OSDHTTPServer(self, self.osd_host, self.osd_port)
        thread.start_new_thread(self.osd.serve_forever, ())


        # OSC server (caspar -> service)
        self.osc = OSC(self)

        # Websockets server (service -> html)
        self.ws = WebSockets(self)


    def set_vu(self, id_channel, audio_channel, value):
        id = "#channel-{}-vu-{}".format(id_channel, audio_channel)
        self.ws.send(json.dumps({"vuid" : id, "value": value}))

    def query(self, query):
        return self.caspar.query(query)

    def reset(self):
        self.query("CLEAR {}".format(self.mv_channel))
        self.query("PLAY {}-{} {}".format(self.mv_channel, self.osd_layer, self.osd_template))

        for i, channel in enumerate(self.channels):
            self.query("CLEAR {}".format(channel.caspar_id))
            source = channel.source
            if source:
                self.query("PLAY {}-1 {}".format(channel.caspar_id, source))

            self.query("MIXER {}-{} VOLUME 0".format(self.mv_channel, i))

            x = (i%3) * self.channel_scale
            y = int(i/3) * self.channel_scale

            self.query("MIXER {}-{} FILL {} {} {} {}".format(self.mv_channel, i, x, y, self.channel_scale, self.channel_scale))
            self.query("PLAY {}-{} route://{}".format(self.mv_channel, i, channel.caspar_id))
