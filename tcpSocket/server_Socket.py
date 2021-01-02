import logging
import sys
import socket

print("Socket Server Demo")


def startserver(argv):
    log = logging.getLogger(__name__)
    log.info(argv)

    host, port = "localhost", 1234

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                log.info("El cliente: {} wrote: {}".format(addr[0], str(data, 'utf-8')))
                conn.send(bytes(data))



def main(argv):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s")

    startserver(argv)


def init():
    if __name__ == '__main__':
        sys.exit(main(sys.argv))


init()
