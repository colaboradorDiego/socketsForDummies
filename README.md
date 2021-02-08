# Difference entre socket and websocket?
	-> https://stackoverflow.com/questions/4973622/difference-between-socket-and-websocket
	
# How to Work with TCP Sockets in Python (with Select Example)”
	-> https://steelkiwi.com/blog/working-tcp-sockets/

# Difference entre REST vs WebSocket?
	1. REST vs WebSocket for dummies -> https://www.itdo.com/blog/rest-vs-websocket-que-diferencia-hay/
	2. GET and POST requests using Python -> https://www.geeksforgeeks.org/get-post-requests-using-python/
	
	3. REST vs WebSocket for sysAdmins -> https://www.baeldung.com/rest-vs-websockets
	
# Difference between persistence and durability in messaging?
	 1. https://developers.redhat.com/blog/2018/06/14/stomp-with-activemq-artemis-python/
	 
# websocket-client. All APIs are the synchronous functions.

	Antes que nada vamos a separar el estudio en 3 capetas
	Tenga presente que websockets (con s final) lo tratamos por completo en el repo asyncWebSockets
	
	Requerimiento previo: entender python Thread
		What Is a Thread?
			https://realpython.com/intro-to-python-threading/#what-is-a-thread
			https://realpython.com/python-concurrency/

	websocket
		estudiamos los modulos websocket y websocket-client
		Importante:
			. All APIs are the synchronous functions.
			. Supports only hybi-13 (ping/pong)
		
		https://pypi.org/project/websocket_client/
		doc's -> https://websocket-client.readthedocs.io/en/latest/

		
		Heartbeat:
			Cuando manejamos datos en tiempo real es nesesario que el  cliente chequee que la 
			conexión con el servidor sigue siendo válida.
			Por lo general el servidor ​enviará requests al cliente cada 10 seg y esperará uno de respuesta cada 20
			seg​. En tanto que para el cliente los valores de heartbeat son enviar a lo sumo cada 20 seg 
			esperar uno a lo sumo cada 10 seg.
			
			https://github.com/BitMEX/api-connectors/issues/397
			
		
		Reconecion y salir
			https://github.com/websocket-client/websocket-client/issues/580
			https://stackoverflow.com/questions/38995640/how-to-stop-python-websocket-client-ws-run-forever
			
			
		Sending custom headers in websocket handshake
			https://stackoverflow.com/questions/15381414/sending-custom-headers-in-websocket-handshake
		
					
	autobahn
		Open-source (MIT) real-time framework for Web, Mobile & Internet of Things.
		home -> https://pypi.org/project/autobahn/
			You can use Autobahn to create clients speaking just plain WebSocket protocol
			for Python 3.6+ and running on Twisted and asyncio.
			
		WebSocket Programming -> https://autobahn.readthedocs.io/en/latest/websocket/programming.html
		Creating Clients, Servers & examples
			https://github.com/crossbario/autobahn-python/tree/master/examples/asyncio/websocket/echo
			
		Arranquemos estudiando el codigo del server -> websocket/serverAutoBahn.py
		y dos clientes bien basicos -> websocket/clienteOtraLib.py & clienteAutoBahn.py
		
		mas avanzado -> https://autobahn.readthedocs.io/en/latest/websocket/examples.html
		entre estos recomiendo leer.
		Slow Square -> shows a WebSocket server that will receive a JSON & co-routines inside WebSocket handlers.
		Secure WebSocket - > How to run WebSocket over TLS (“wss”). 
							 El ejemplo esta para Twisted y nosotros estamos trabajando con asyncio, upsss, hay q laburar el bocho
							 
		
		Mas info q aun no lei
		
		Reconection -> https://stackoverflow.com/questions/37500945/autobahn-asyncio-reconnectingclientfactory
		
		autobahn.twisted.websocket -> https://codesuche.com/python-examples/autobahn.twisted.websocket.connectWS/
		autobahn.asyncio.websocket -> https://codesuche.com/python-examples/?api=autobahn.asyncio.websocket
		
	socket
		socket genericos
		
	
# Ni idea de esto
	-> Using a websocket client as a class in python https://stackoverflow.com/questions/26980966/using-a-websocket-client-as-a-class-in-python
	-> IKE websocket https://www.kite.com/python/docs/websocket
	
