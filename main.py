import socket
import os

class Server():

    def __init__(self, port, host):
        self.port = port
        self.host = host
        self.serverSocket = socket.socket()
        self.serverSocket.bind((host, port))
        self.routes = {}

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
            self.routerCheck()

            
                file = open('.'+request['headLine'][1],'r')

                responseBody = ''.join([x+'\n' for x in file.readlines()])
                print(responseBody)
                respondeHeadLine = "HTTP/1.1 200 ok\n"
                respondeHeaders = "server: pyserver\n content-type: text/html\n connection: close\n\n"

                conn.send(''.join([respondeHeadLine, respondeHeaders, responseBody]).encode())
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

    def routerCheck(self, request):
        pass

    class router():

        def __init__(self):
            self.routes = {}

        def set_route(self, method, path):
            self.routes[path] = method

        def routeHandler(self, path, method):
            if self.routes[path] and self.routes[path] == method:
                return path
            else: 
                return False

"""
Request 
        GET /
          |
          |
    Check Routes()
          |
        Router
          |
          |
    route handler()
          |
          |
    route exists:
    |           |
  True        False
    |           |
send Path   send Error
"""

if __name__ == "__main__": 
    pyServer = Server(8000, '127.0.0.1')
    router = pyServer.router()

    router.set_route('GET', '/') 