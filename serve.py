<<<<<<< HEAD
import os
from textual_serve.server import Server

port = int(os.environ.get("PORT", 8000))
server = Server("python app_render.py", host="0.0.0.0", port=port)
=======
from textual_serve.server import Server

server = Server("python main.py")  # el comando que lanza tu app
>>>>>>> a5a4cdd (v1)
server.serve()
