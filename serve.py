from textual_serve.server import Server

import os
from textual_serve.server import Server

port = int(os.environ.get("PORT", 8000))
server = Server("python main.py", port=port)
server.serve()

