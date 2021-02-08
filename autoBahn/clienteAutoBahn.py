import asyncio

from autobahn.asyncio.websocket import WebSocketClientProtocol, WebSocketClientFactory

# protocol class
class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("onConnect - Server connected:", response)
        print()

    def onConnecting(self, transport_details):
        print("onConnecting - Connecting transport details:", transport_details)
        print()
        return None  # ask for defaults

    def onOpen(self):
        print("onOpen - WebSocket connection open")

        def hello():
            self.sendMessage("Hello, world!".encode('utf8'))
            self.sendMessage(b"\x00\x01\x03\x04", isBinary=True)
            self.factory.loop.call_later(1, hello)

        # start sending messages every second ..
        hello()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary payload message", payload)

        else:
            print("Text payload message", payload.decode('utf8'))

        print()

    def onClose(self, wasClean, code, reason):
        print("onClose -  WebSocket connection closed:", reason)
        print()


if __name__ == '__main__':
    factory = WebSocketClientFactory("ws://localhost:8765")
    factory.protocol = MyClientProtocol

    loop = asyncio.get_event_loop()
    cliente = loop.create_connection(factory, 'localhost', 8765)
    loop.run_until_complete(cliente)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print()
        print('closind cliente ....')
        print()
        cliente.close()
        loop.close()
