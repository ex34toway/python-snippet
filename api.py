import json
import random

def application(environ, startResponse):
    path = environ['PATH_INFO']
    if path == '/':
        json_content = '{"result": "ok"}'
        bytes = str.encode(json_content)
        headers = []
        headers.append(('Content-Type', 'application/json; charset=utf-8'))
        headers.append(('Content-Length', str(len(bytes))))
        startResponse('401 Unauthorized', headers)
        return [bytes];
    startResponse('404 Not Found', [])
    return [('Path %s not found' % path).encode('utf-8')]
