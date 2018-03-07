#!/usr/bin/env python
"""
Very simple HTTP server in python.

Usage::
    ./dummy-web-server.py [<port>]

Send a GET request::
    curl http://localhost

Send a HEAD request::
    curl -I http://localhost

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

"""
from http.server import BaseHTTPRequestHandler, HTTPServer
#import SocketServer
import requests

import NNWorkFn

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        f=open("data.json")
        print("###### GET Request ##########")
        data = f.read()
        f.close()
        self.wfile.write(data.encode('utf-8'))
		

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        NNWorkFn.work_function_POST(post_data)
        self._set_headers()
        f=open("data.json")
        print("###### POST Request ##########")
        data = f.read()
        f.close()
        self.wfile.write(data.encode('utf-8'))
        
def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    r = requests.get('http://sync.afraid.org/u/f8pJnAJazhOSZW0N9evL8Ora/ ')

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
