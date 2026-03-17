from textual_serve.server import Server

server = Server("python main.py")  # el comando que lanza tu app
server.serve()
