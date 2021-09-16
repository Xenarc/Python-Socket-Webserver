from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
#SERVER
from socket import *

def datestring(date):
	stamp = mktime(date.timetuple())
	return format_date_time(stamp)

def HandleRequest(route):
	route = f".{route}"
	if(route == "./"): route = "./index.html"
	
	contentType = "css" if route.split('.')[-1] == "css" else "html"
	
	try:
		content = open(route, "r").read()
	except OSError as e:
		print(f'[ERROR] File not found: "{route}"')
	response = """HTTP/1.1 200 OK
Date: """ + datestring(datetime.now()) + """
Server: SIT202Homebrew/0.0.1 (Win32)
Last-Modified: """ + datestring(datetime.now()) + """
Content-Length: """ + str(len(content)) + """
Content-Type: text/""" + contentType + """
Connection: Closed\r\n\r\n""" + content;
	return response

def decodeRoute(message):
	if(message[0:3] == "GET"):
		print("[INFO] GET request")
		route = message.split(' ')[1]
		print(f"[INFO] Route = {route}")
		return route

def main():
	serverPort = 11500
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.bind(('', serverPort))
	serverSocket.listen(1)
	
	message = " "
	print("[INFO] Server listening\n---------------------")
	while len(message) != 0:
		serverSocket.settimeout(1)
	
		try:
			recieveSocket, addr = serverSocket.accept()
			recieveSocket.settimeout(1)
			message, clientAddress = recieveSocket.recvfrom(4096)
		except timeout: continue
		
		try:
			route = decodeRoute(message.decode())
			response = HandleRequest(route)
		except Exception as ex:
			response = str(f"HTTP/1.1 400 \r\n\r\n {repr(ex)}")
		
		recieveSocket.sendall(response.encode());
		recieveSocket.close()

main()
