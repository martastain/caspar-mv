#!/usr/bin/env python

from __future__ import print_function

import sys
import time
import json

import rex

from multiviewer import *

#
# First argument of MultiViewerChannel constructor is capar channel id.
# Other keyword arguments are optional:
#
# source - The part of AMCP command after "PLAY X-Y " i
#          Just for debugging - should be handled by broadcast automation
# title -  Title displayed in HTML overlay.
#          Defaults to "Channel X", where X is caspar channel id

channel_setup = [
        MultiViewerChannel(1, title="Demo 2",      source="d1 LOOP"),
        MultiViewerChannel(2, title="Demo 2",      source="d2 LOOP"),
        MultiViewerChannel(3, title="Demo 3",      source="d3 LOOP"),
        MultiViewerChannel(4, title="Demo 4",      source="d4 LOOP"),
        MultiViewerChannel(5, title="Demo 5",      source="d5 LOOP"),
        MultiViewerChannel(6, title="Demo 6",      source="d6 LOOP"),
        MultiViewerChannel(7, title="Red color",   source="#cc0000"),
        MultiViewerChannel(8, title="Green color", source="#00cc00"),
        MultiViewerChannel(9, title="Blue color",  source="#0000cc"),
    ]

# Caspar channel ID of the multiviewer output
# In this demo, we have first 9 channels configured as sources,
# Channel ID 10 has its decklink output

mv_channel = 10

try:
    settings = json.load(open("settings.json"))
except:
    settings = {}


if __name__ == "__main__":
    mv = MultiViewer(
            mv_channel,
            channel_setup,
            **settings
        )
    mv.reset()

    # Enter infinite loop
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print ()
        logging.warning("Shutting down")
        sys.exit(0)
