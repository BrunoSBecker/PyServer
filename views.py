
routes = {}

def setRoute(route, path):
    global routes 
    routes[route] = path

def get(request):
    global routes

    requestRoute = request['headLine'][1]

    if requestRoute not in list(routes.keys()):
        return '''HTTP/1.1 404 not-found\n 
                        server: pyserver\n 
                        content-type: text/html\n 
                        connection: close\n\n'''.encode()
    else:
        path = routes[requestRoute]

        try:
            file = open('./src/'+path,'r')

        except: 
            return '''HTTP/1.1 404 not-found\n 
                        server: pyserver\n 
                        content-type: text/html\n 
                        connection: close\n\n'''.encode()
                        
        respondeHeadLine = "HTTP/1.1 200 ok\n"
        respondeHeaders = "server: pyserver\n content-type: text/html\n connection: close\n\n"
        responseBody = ''.join([x+'\n' for x in file.readlines()])

        return ''.join([respondeHeadLine, respondeHeaders, responseBody]).encode()

    print(request['headLine'][1])

methods = {'GET': get, 'POST': 'post'}
