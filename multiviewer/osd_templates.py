#
# HTML INDEX TEMPLATE
#

HTML_HEADER = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Multiviewer</title>
    <link rel="stylesheet" href="/css/main.css">
</head>
<body>
"""

HTML_FOOTER= """
    <script src="/js/jquery.min.js"></script>
    <script src="/js/main.js"></script>
</body>
</html>"""


CHANNEL_TPL = """
    <div id="channel-{channel_id}" class="channel-wrapper" style="width:{width}%; height:{height}%">
        <div class="channel-vu">
        </div>
        <div class="channel-label">
            <span id="channel-{channel_id}-label">{channel_label}</span>
        </div>
        <div class="channel-vu-left">
            <div class="vu-bar-container">
                <div id="channel-{channel_id}-vu-1" class="vu-bar"></div>
            </div>
            <div class="vu-bar-container">
                <div id="channel-{channel_id}-vu-2" class="vu-bar"></div>
            </div>
        </div>
        <div class="channel-vu-right">
            <div class="vu-bar-container">
                <div id="channel={channel_id}-vu-3" class="vu-bar"></div>
            </div>
            <div class="vu-bar-container">
                <div id="channel={channel_id}-vu-4" class="vu-bar"></div>
            </div>
        </div>
    </div>"""


#
# boot javascript
#

MAIN_JS_TPL = """
var ws;
function init() {{
    ws = new WebSocket("ws://{ws_host}:{ws_port}/");
    ws.onmessage = function(e) {{
        var data = JSON.parse(e.data);
        $(data["vuid"]).css("height", data["value"]);
    }};
}}
$(document).ready(function() {{
    init();
}});
"""


