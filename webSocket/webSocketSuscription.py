import websocket
import threading
import time
import sys
import ssl
import os
import json

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


def on_ping(payload):
    print('on_ping:', payload)

def on_pong(payload):
    print('on_pong:', payload)


# es recomendable tener a conectar como una funcion para que en caso de desconexion
# la podamos voler a llamar
def conectar(endPoint, myHeader):
    ws = websocket.WebSocketApp(url=endPoint,
                                header=myHeader,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_ping=on_ping,
                                on_pong=on_pong)

    # bound method
    ws.on_open = on_open

    return ws



def main(argv):

    # loads JSON from a file.
    parametros = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'appOmsApi.ini'))
    with open(parametros, 'r') as f:
        conArgs = json.load(f)

    showConf(conArgs)

    # Ping cada 20seg
    """
    Cuando manejamos datos en tiempo real es nesesario que el cliente chequee que la
    conexión con el servidor sea valida en todo momento. Este proceso lo hace manteniendo ping/pong
    El servidor envia pings al cliente y el cliente envia pongs al servidor. Por lo general los
    tiempo de envio son entre 10 y 30 segundos.
    Asi de esta manera ambos saben que el otro esta en linea y funcionando    
    """
    heartbeat = (10000, 20000)
    pingInterval = heartbeat[1]/1000

    # ssl
    sslOpt={"cert_reqs": ssl.CERT_NONE, "check_hostname": True, "ssl_version": ssl.PROTOCOL_TLSv1}

    # auth
    token = 'd501ae04-48d4-4a8d-9cd6-16465277d441'
    header = {"Authorization": "Bearer " + token}

    endPoint = 'wss://' + conArgs['login']['host'] + conArgs['stomp']['service']
    print('endPoint:', endPoint)
    print()

    # websocket.enableTrace(True)
    ws = conectar(endPoint, header)


    try:
        ws.run_forever(ping_interval=pingInterval, sslopt=sslOpt)

    except KeyboardInterrupt:
        pass

    finally:
        ws.close()



def init():
    if __name__ == '__main__':
        sys.exit(main(sys.argv))

init()
