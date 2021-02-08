import websocket
import threading
import time
import sys


def on_message(ws, message):
    print('on_message:', message)
    print()


def on_error(ws, err):
    print('on_error:', err)
    print()


def on_close(ws):
    print('on_close:', 'Connection Closed!')


def on_open(ws):
    print('on_open:', 'Connection opened!')

    # enviarMsg running on secondary thread
    def enviarMsg(arg):
        for i in range(arg):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)

    x = threading.Thread(target=enviarMsg, args=(3,))
    x.start()


# es recomendable tener a conectar como una funcion para que en caso de desconexion
# la podamos voler a llamar
def conectar():
    ws = websocket.WebSocketApp("ws://localhost:8765",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    # bound methods
    ws.on_open = on_open

    return ws



def main(argv):
    # websocket.enableTrace(True)
    ws = conectar()

    """
    Aqui es donde precisas entender q es un thread

    There's always going to be a thread dedicated to listening to the socket.
    In this case the main thread that enters a loop inside the run_forever waiting for messages.
    If you want to have some other thing going ON you'll need another thread, here, enviarMsg.
    """

    # Ping cada 20seg
    heartbeat = (10000, 20000)
    pingInterval = heartbeat[1]/1000
    sslOpt={"cert_reqs": ssl.CERT_NONE, "check_hostname": True, "ssl_version": ssl.PROTOCOL_TLSv1}

    try:
        # https://www.kite.com/python/docs/websocket.WebSocketApp.run_forever
        # run_forever running on main thread
        ws.run_forever(ping_interval=pingInterval, sslopt=sslOpt)
        print('por aca solo pasa cuando salimos del loop infinito')

    except KeyboardInterrupt:
        pass

    finally:
        ws.close()



def init():
    if __name__ == '__main__':
        sys.exit(main(sys.argv))

init()
