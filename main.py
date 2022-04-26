import socket
import os

class Server():

    def __init__(self, port, host):
        self.port = port
        self.host = host

        self.serverSocket = socket.socket()
        self.serverSocket.bind((host, port))
        print("Socket created")

        self.routes = {'root': '.'}

    def start(self):
        self.serverSocket.listen(5)

        print("Socket listening on http://{}:{}/".format(self.host, self.port))

        while True:
            conn, addr = self.serverSocket.accept()
            print("Connected with {} at port [{}]".format(addr[0], addr[1]))
            print("\n========\n")

            data = conn.recv(1024).decode('utf-8').splitlines()
            request = self.requestHandler(data)

            try:
                path = self.routes[request['headLine'][1]][1]
                file = open(self.routes['root']+path,'r')

                respondeHeadLine = "HTTP/1.1 200 ok\n"
                respondeHeaders = "server: pyserver\n content-type: text/html\n connection: close\n\n"
                responseBody = ''.join([x+'\n' for x in file.readlines()])

                conn.send(''.join([respondeHeadLine, respondeHeaders, responseBody]).encode())
                conn.close()
            except:
                conn.send('''HTTP/1.1 404 not-found\n 
                            server: pyserver\n 
                            content-type: text/html\n 
                            connection: close\n\n'''.encode())
                conn.close()

            print(request['headLine'][1])

    def requestHandler(self, req):
            request = ''.join((line + '\n') for line in req) 
            print(request)
            requestHead, requestBody = request.split('\n\n', 1)
            requestHead = requestHead.splitlines()

            requestHeadline = requestHead[0]
            requestHeadline = requestHeadline.split()

            requestHeaders = dict(x.split(': ', 1) for x in requestHead[1:])

            return {'headLine': requestHeadline, 'headers': requestHeaders, 'body': requestBody}

    def setRoute(self, method, route, path):
        self.routes[route] = [method, path]

    def setRoot(self, path):
        self.routes['root'] = path

if __name__ == "__main__": 
    pyServer = Server(8000, '127.0.0.1')

    pyServer.setRoot('./src')

    pyServer.setRoute('GET', '/', '/index.html') 
    pyServer.setRoute('GET', '/about-us', '/about.html')
    pyServer.start()