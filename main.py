import socket
import os

class Server():

    def __init__(self, port, host):
        self.port = port
        self.host = host
        self.serverSocket = socket.socket()
        self.serverSocket.bind((host, port))
        print("Socket created")

        self.connectionHandler()

    def connectionHandler(self):
        self.serverSocket.listen(5)

        print("Socket listening on http://{}:{}/".format(self.host, self.port))

        while True:
            conn, addr = self.serverSocket.accept()
            print("Connected with {} at port [{}]".format(addr[0], addr[1]))
            print("\n========\n")

            request = self.requestHandler(conn.recv(1024).decode('utf-8').splitlines())

            try:
                file = open('.'+request['headLine'][1],'r')

                responseBody = ''.join([x+'\n' for x in file.readlines()])
                print(responseBody)
                respondeHead = "HTTP/1.1 200 ok\n server: pyserver\n content-type: text/html\n connection: close\n\n"

                conn.send(''.join([respondeHead,responseBody]).encode())
                conn.close()
            except:
                conn.send('404 not found'.encode())
                conn.close()

            print(request['headLine'][1])

    def requestHandler(self, req):
            request = ''.join((line + '\n') for line in req) 

            requestHead, requestBody = request.split('\n\n', 1)
            requestHead = requestHead.splitlines()

            requestHeadline = requestHead[0]
            requestHeadline = requestHeadline.split()

            requestHeaders = dict(x.split(': ', 1) for x in requestHead[1:])

            return {'headLine': requestHeadline, 'headers': requestHeaders, 'body': requestBody}

#soc = socket.socket()
#
#soc.bind(('', 8080))
#soc.listen(5)
#
#while True:
#    conn, addr = soc.accept()
#
#    print("Connected with: ",addr)
#
#    print(conn.recv(1024).decode('utf-8'))
#
#    conn.send("HTTP/1.1 200 ok;\n Connection: close; \nContent-Type: text/html; charset=utf-8; \nServer: Linux; \n\n<h1>Hello World!</h1>".encode())
#
#    conn.close()

if __name__ == "__main__": 
    serverObj = Server(8000, '127.0.0.1')