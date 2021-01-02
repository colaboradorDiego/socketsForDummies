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

	socketserver:
		Classes that simplify writing network servers.
		https://docs.python.org/3.6/library/socketserver.html#module-socketserver

	ssl:
		A TLS/SSL wrapper for socket objects.
		https://docs.python.org/3.6/library/ssl.html#module-ssl


Problema Importante con socketserver
	Python SocketServer close the socket after each call to handle

El problema que se me presento al utilizar socketserver en mis primeros pasos con python fue que
el metodo handle() me cerraba la conexion tras la primer llamada desde el cliente y obviamente en la
segunta me tiraba el siguiente error:

	"ConnectionAbortedError: [WinError 10053] Se ha anulado una conexión establecida por el software en su equipo host"

Esto me obligaba a abrir una nueva conexion para cada request desde el cliente.
Googleando esto es normal y asi fuinciona, parece el metodo handle cierra las los clientes. No hay mucho mas que hacer



"""
import logging
import sys
import socketserver


print("Socket Server Demo")


"""
Request handler
handle:
. do all the work required to service a request
. several instance attributes are available to it:
	request         = self.request
	client address  = self.client_address
	server instance = self.server
	
	https://www.programcreek.com/python/example/73643/SocketServer.BaseRequestHandler
"""


class MyServer(socketserver.StreamRequestHandler):

	def handle(self):
		log = logging.getLogger(__name__)

		# self.request is the TCP socket connected to the client
		data = self.request.recv(1024)
		log.info("El cliente: {} wrote: {}".format(self.client_address[0], str(data, 'utf-8')))

		# just send back the same data, but upper-cased
		self.request.send(bytes(data))


"""
concrete socketserver.TCPServer class
This process requests synchronously; each request must be completed before the next request can be started.
	1. create a request handler, derive a class from BaseRequestHandler. 
	2. instantiate TCPServer, passing it the server’s address and the request handler class. Recommended to use a with statement.
	3. call the handle_request() or serve_forever() method of the server object to process one or many requests.
	4. finally, call server_close() to close the socket (unless you used a with statement). 
"""
def startserver(argv):
	log = logging.getLogger(__name__)
	log.info(argv)

	host, port = "localhost", 1234

	"""
	the constructor automatically attempts to invoke:
		server_bind()
		server_activate()
		The other parameters are passed to the BaseServer base class.
	"""
	with socketserver.TCPServer((host, port), MyServer) as server:
		# 1 = poll_interval seconds
		server.serve_forever(1)


def main(argv):
	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s")

	startserver(argv)


def init():
	if __name__ == '__main__':
		sys.exit(main(sys.argv))


init()
