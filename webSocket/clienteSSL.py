# WSS (WS over TLS) client example, with a self-signed certificate

import asyncio
import pathlib
import ssl
import websockets
import os

"""
para que el cliente y server funcionaran funcionara me lei todo esto, mira
https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate
"""


#ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_verify_locations(localhost_pem)


async def hello():
    uri = "wss://localhost:8765"
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        await websocket.send("Hello world!")
        respuesta = await websocket.recv()
        print(respuesta)

asyncio.get_event_loop().run_until_complete(hello())