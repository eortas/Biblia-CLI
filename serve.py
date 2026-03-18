import os
import sys
from textual_serve.server import Server

port = int(os.environ.get("PORT", 10000))
cmd = f"{sys.executable} app_render.py"
server = Server(cmd, host="0.0.0.0", port=port)
server.serve()
