import api

import wsgiref.simple_server
from wsgiref.simple_server import ServerHandler

ServerHandler.server_software = ''

def main():
    httpd = wsgiref.simple_server.make_server('0.0.0.0', 8833, application)
    httpd.serve_forever()

def application(environ, startResponse):
    return api.application(environ, startResponse)

if __name__ == '__main__':
    main()
