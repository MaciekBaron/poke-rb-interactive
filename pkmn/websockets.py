from pkmn.config import PORTS
import asyncio
import websockets
import time
from threading import Thread

PORT = 8765

# There will be only one connection so we only have to worry about one queue
message_queue = []

def _start_loop(loop, server):
    loop.run_until_complete(server)
    loop.run_forever()

async def on_ready(websocket, path):
    # @TODO: Improve handling to follow standards
    from pkmn.voting import VoteManager
    start_time = time.time()
    vote_manager = VoteManager.Instance()
    vote_manager.send_poll_state()
    # Do a loop instead of a producer
    while True:
        if len(message_queue) > 0:
            await websocket.send(message_queue.pop())
        if time.time() - start_time > 1:
            # Send "alive" signal every second
            start_time = time.time()
            try:
                await websocket.send('alive')
            except:
                print("Websocket connection closed, reconnecting.")
                break
        # Doesn't need to be instant
        time.sleep(.1)

def start_web_sockets():
    new_loop = asyncio.new_event_loop()
    start_server = websockets.serve(on_ready, "localhost", PORT, loop=new_loop)
    t = Thread(target=_start_loop, args=(new_loop, start_server))
    t.start()
    print("Websockets layer ready")

def add_message(msg):
    message_queue.append(msg)
