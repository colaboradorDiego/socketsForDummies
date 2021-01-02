"""

IP + PORT = socket
In practice all IP traffic is done using 'sockets'
	https://stackoverflow.com/questions/4782105/understanding-socket-basics

No voy a profundizar, por ahora solo puedo decir que todo el trafico de aplicaciones por internet (Internet Layer) es
mediante socket programing, conectando servers con clients

Disponemos de estos modulos para programar

	socket:
		Low-level networking interface
		https://docs.python.org/3.6/library/socket.html

	ssl:
		A TLS/SSL wrapper for socket objects.
		https://docs.python.org/3.6/library/ssl.html#module-ssl

"""
import logging
import sys
import socket


print("Socket Client Demo")


def startclient(paises):
	log = logging.getLogger(__name__)
	log.info(paises)

	host, port = "localhost", 1234

	for pais in paises:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.connect((host, port))

			log.info("HostName: {}, Full qualified name: {} ".format(socket.gethostname(), socket.getfqdn()))

			# sock.send returns the number of bytes sent and msg debe ser en bytes
			bytes_send = sock.send(pais)

			# sock.recv return value is a bytes type.
			# The maximum amount of data to be received at once is specified by bufsize
			received = str(sock.recv(1024), 'utf-8')

			log.info("Bytes send: {} and msg received: {}".format(bytes_send, received))


def main(argv):
	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s")

	path = 'C:/Users/usuario/bitBucket/docpython/dataTest/algunosPaises.txt'
	with open(path, 'r') as fHandle:
		paises = [bytes(pais.strip(), 'utf-8') for pais in fHandle.readlines()]
		startclient(paises)


def init():
	if __name__ == '__main__':
		sys.exit(main(sys.argv))


init()
