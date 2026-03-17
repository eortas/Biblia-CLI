import os
from textual_serve.server import Server

port = int(os.environ.get("PORT", 8000))
server = Server("python main.py", host="0.0.0.0", port=port)
server.serve()
