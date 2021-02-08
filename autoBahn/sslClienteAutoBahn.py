"""
bueno estoy tranado en el error:
    TypeError: 'MyClientProtocol' object is not callable

googleando encontre esto pero es muy complejo por ahora, lo dejo registrado pero paso a buscar otra solucion.
. Callbacks from autobahn WebSocketClientProtocol to another object
    https://stackoverflow.com/questions/34676565/callbacks-from-autobahn-websocketclientprotocol-to-another-object

. SSL context stuff
    https://github.com/crossbario/autobahn-python/issues/393
    https://docs.python.org/3/library/asyncio-eventloop.html?highlight=create_connection#opening-network-connections



"""

import asyncio
import sys
import json
import os
import ssl
import stomper


from autobahn.asyncio.websocket import WebSocketClientProtocol, WebSocketClientFactory


# Stuff
def showConf(connDATA):
    print()
    print('Setup from json conf file')
    print('Loading connection parameters')
    print()
    print("User credentials & Stuff")
    print('... Login.host', connDATA['login']['host'])
    print('... Login.user', connDATA['login']['user'])
    print('... Login.pass', connDATA['login']['pass'])
    print()
    print("API credentials & Stuff")
    print('... API.name', connDATA['api']['name'])
    print('... API.user', connDATA['api']['user'])
    print('... API.pass', connDATA['api']['pass'])
    print('... API.tokenUrl', connDATA['api']['tokenUrl'])
    print()
    print("Stomper data")
    print('... Stomp.service', connDATA['stomp']['service'])
    print('... Stomp.port', connDATA['stomp']['port'])
    print()
    print("Endpoints")
    for data in connDATA['endpoint']:
        print('... Enpoints.' + data, connDATA['endpoint'][data])
    print()
    print()


def showToken(conn):
    print()
    # print(conn)
    print("Connection Status")
    print('... access_token', conn['access_token'])
    print('... token_type', conn['token_type'])
    print('... refresh_token', conn['refresh_token'])
    print('... expires_in', conn['expires_in'])
    print('... scope', conn['scope'])
    print('... expires_at', conn['expires_at'])
    print()











# Client



# protocol class
class MyClientProtocol(WebSocketClientProtocol):

    def __init__(self, connArgs):
        self.conArgs = connArgs

    def onConnect(self, response):
        print("onConnect - Server connected:", response)
        print()

    def onConnecting(self, transport_details):
        print("onConnecting - Connecting transport details:", transport_details)
        print()
        return None  # ask for defaults

        # print("onConnecting - Connecting transport details:", transport_details)
        # print()
        # heartbeat = (10000, 20000)
        # connect_msg = stomper.connect(self.conArgs['login']['user'], 'DUMMY_PW', 'WebSocketApp-' + self.conArgs['login']['user'], heartbeat)
        # print('stomp MSG:', connect_msg)
        # print()
        # self.sendMessage(connect_msg)

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
            print("onMessage - Binary payload message", payload)

        else:
            print("onMessage - Text payload message", payload.decode('utf8'))

        print()

    def onClose(self, wasClean, code, reason):
        print("onClose -  WebSocket connection closed:", reason)
        print()


def main(argv):

    # loads JSON from a file.
    parametros = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'appOmsApi.ini'))
    with open(parametros, 'r') as f:
        conArgs = json.load(f)

    showConf(conArgs)

    # serviceUrl = 'ws://localhost:8765'
    serviceUrl='wss://' + conArgs['login']['host'] + ':' + conArgs['stomp']['port'] + conArgs['stomp']['service']
    print('serviceUrl: ', serviceUrl)
    print()

    token='a5a1dd5d-3dad-4949-8439-bff0ad2179b5'
    wssHeader = {
        'Authorization': 'Bearer ' + token
    }

    factory = WebSocketClientFactory(serviceUrl, headers=wssHeader)
    factory.protocol = MyClientProtocol(conArgs)

    # SSL client context: default
    if factory.isSecure:
        print('Secure Server')
        print()
        contextFactory = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        contextFactory.check_hostname=False
        contextFactory.verify_mode=ssl.CERT_NONE
    else:
        print('WARNING!!!! NOT Secure Server')
        print()
        contextFactory = False

    loop = asyncio.get_event_loop()
    # cliente = loop.create_connection(factory, 'localhost', 8765)
    cliente = loop.create_connection(factory, host=conArgs['login']['host'] , port=conArgs['stomp']['port'], ssl=contextFactory)
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



def init():
    if __name__ == '__main__':
        sys.exit(main(sys.argv))

init()
