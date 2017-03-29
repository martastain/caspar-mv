import os

from nxtools import *
from .osd_templates import *

if PYTHON_VERSION < 3:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
else:
    from http.server import BaseHTTPRequestHandler, HTTPServer

__all__ = ["OSDHTTPServer"]


#
# HTTP REQUEST HANDLER
#

MIME_TYPES = {
        ".css" : "text/css",
        ".js" :  "text/javascript"
    }

class OSDRequestHandler(BaseHTTPRequestHandler):
    def log_request(self, code='-', size='-'):
        pass

    def do_headers(self, response=200, mime="application/json", headers=[]):
        self.send_response(response)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header('Content-type', mime)
        for key, value in headers:
            handler.send_header(key, value)
        self.end_headers()

    def echo(self, string):
        self.wfile.write(encode_if_py3(string))

    def result(self, response, data, mime="application/json"):
        self.do_headers(response=response, mime=mime)
        self.echo(data)

    def do_GET(self):
        path = self.path.lstrip("/")
        if not path:
            self.render_index()
            return

        if path == "js/main.js":
            self.do_headers(response=200, mime="text/javascript")
            self.echo(MAIN_JS_TPL.format(
                    ws_host=self.server.parent.ws_host,
                    ws_port=self.server.parent.ws_port,
                ))
            return

        ext = os.path.splitext(path)[1]
        if not ext in MIME_TYPES:
            self.render_error(404, "bad request: {}".format(path))
            return
        fpath = os.path.join("osd", path)
        with open(fpath) as f:
            self.result(200, f.read(), MIME_TYPES.get(ext, "text/txt"))


    def render_error(self, code=500, message="error"):
        self.result(code, message, mime="text/txt")

    def render_index(self):
        mv = self.server.parent
        result = HTML_HEADER
        for channel in mv.channels:
            result += CHANNEL_TPL.format(
                        channel_id=channel.caspar_id,
                        channel_label=channel.title,
                        width=mv.channel_scale*100,
                        height=mv.channel_scale*100
                    )
        result += HTML_FOOTER
        self.result(200, result, mime="text/html")


class OSDHTTPServer(HTTPServer):
    def __init__(self, parent, host, port):
        self.parent = parent
        HTTPServer.__init__(self, (host, port),  OSDRequestHandler)
