import asyncio
import websockets

# simple echo server
async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

        # force stop afeter the first message received
        asyncio.get_event_loop().stop()

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
