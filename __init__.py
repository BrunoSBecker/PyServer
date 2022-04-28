#!./
import socket
import os

import handlers 
import views

def __init__(port):
    port = port
    host = '127.0.0.1'

    serverSocket = socket.socket()
    serverSocket.bind((host, port))
    print("Socket created")

    serverSocket.listen(5)
    print("Socket listening on http://{}:{}/".format(host, port))

    while True:
        conn, addr = serverSocket.accept()
        print("Connected with {} at port [{}]".format(addr[0], addr[1]))
        print("\n========\n")

        data = conn.recv(1024).decode('utf-8').splitlines()
        request = handlers.requestHandler(data)

        response = views.methods[request['headLine'][0]](request)

        conn.send(response)
        conn.close()

if __name__ == "__main__": 
    views.setRoute('/','index.html')
    views.setRoute('/test', 'about.html')

    __init__(8001)