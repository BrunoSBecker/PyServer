def requestHandler(req):
        request = ''.join((line + '\n') for line in req) 
        print(request)
        requestHead, requestBody = request.split('\n\n', 1)
        requestHead = requestHead.splitlines()

        requestHeadline = requestHead[0]
        requestHeadline = requestHeadline.split()

        requestHeaders = dict(x.split(': ', 1) for x in requestHead[1:])

        return {'headLine': requestHeadline, 'headers': requestHeaders, 'body': requestBody}