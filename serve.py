import os
from textual_serve.server import Server

port = int(os.environ.get("PORT", 10000))
cmd = "python -m biblia_cli.main"
server = Server(cmd, host="0.0.0.0", port=port)
server.serve()
