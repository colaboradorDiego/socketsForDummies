from websocket import create_connection

ws = create_connection("ws://localhost:8765")

ws.send("Hola Mundo!")
resultado = ws.recv()
print(resultado)

ws.close()
