import asyncio
import json

from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory

"""
1. Server Protocol 
    To create a WebSocket server, you need to write a protocol class to specify the behavior of the server.
    
2. Receiving Messages
    We override a callbacks which is called by Autobahn whenever the callback related event happens.
    In case of onMessage, the callback will be called whenever a new WebSocket message was received.
    Also onMessage the core WebSocket interface autobahn.websocket.interfaces.IWebSocketChannel provides the following callbacks:
        .onConnect()
        .onConnecting()
        .onOpen()
        .onMessage()
        .onClose()
    
    The payload is always a Python byte string.
    Since WebSocket is able to transmit text (UTF8) and binary payload, the actual payload type is signaled via the isBinary flag.
    When the payload is text (isBinary == False), the bytes received will be an UTF8 encoded string.
    To process text payloads, the first thing you often will do is decoding the UTF8 payload into a text

3. Sending Messages
    Utilizamos los metodos del Server Protocol WebSocketServerProtocol para enviar msg

"""


# Simple EchoServer protocol class
class MyServerProtocol(WebSocketServerProtocol):

    # Whenever a new client connects to the server, a new protocol instance will be created.
    # and onConnect() callback fires as soon as the WebSocket opening handshake is begun by the client.
    #
    # For a WebSocket server protocol, onConnect() will fire with autobahn.websocket.protocol.ConnectionRequest
    # providing information on the client wishing to connect via WebSocket.
    def onConnect(self, request):
        print("onConnect:", request)
        print()

    def onOpen(self):
        print("onOpen: WebSocket connection open.")
        print()

    def onMessage(self, payload, isBinary):
        print("onMessage: Message received")
        if isBinary:
            print("Binary message received bytes:", len(payload))
            self.sendMessage(payload, isBinary=True)

        else:
            print('Text message received:', payload)

            textPayload = payload.decode('utf8')
            print("payload decoded:", textPayload)

            byteStringPayload = textPayload.encode('utf8')
            print('payload encoded to byte string again:', byteStringPayload)
            self.sendMessage(byteStringPayload, isBinary=False)

        print()

    def onClose(self, wasClean, code, reason):
        print("onClose: WebSocket connection closed:", reason)
        print()



# Running a Server
if __name__ == '__main__':

    # 1. Create a Factory for producing instances of our protocol class
    factory = WebSocketServerFactory("ws://localhost:8765")

    # 2. Create a TCP listening server using the former Factory
    factory.protocol = MyServerProtocol

    # 3. Start a server using the factory, listening on TCP port 8765
    loop = asyncio.get_event_loop()
    echoServer = loop.create_server(factory, 'localhost', 8765)
    server = loop.run_until_complete(echoServer)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print()
        print('closind server ....')
        print()
        server.close()
        loop.close()
