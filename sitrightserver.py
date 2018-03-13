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
import requests, json

import numpy as np

import NNWorkFn

#import serial
#ser = serial.Serial('/dev/ttyACM0', 115200, timeout=10)  # open serial port
#print("Opened port:", ser.name) # check which port was really used

KEY = 6769

def get_buf_fromserial(ser, buffer_len, buffer_width):
    buf = np.zeros((buffer_width, buffer_len), dtype=float)
    for i in range(0, buffer_len):
        line = ser.readline()   # read a '\n' terminated line
        print(line)
        line = line.decode("utf-8") 
        line = line.strip('\n')
        line_str = line.split(",")
        line_int = []
        for j in range(0, len(line_str)):
            line_int.append(int(line_str[j]))
        # #line_int = map(int, line_str)
        line_arr = np.asarray(line_int)
        #print("Shapes", line_arr.shape, buf.shape)
        buf[:,i] = line_arr
    return buf

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        if self.path == "/":
            f=open("data.json")
            print("###### GET Request ##########")
            data = f.read()
            f.close()
            self.wfile.write(data.encode('utf-8'))
        #elif self.path == "/serial":
            #print("###### SERIAL GET Request ##########")
            #while True:
                #try:
                    #buf = get_buf_fromserial(ser, 200, 13)
                    #buf = np.mean(buf, axis=1)
                    #break
                #except ValueError:
                    #print("Value Error")
            #print("Got buffer")
            #buf_dict = {}
            #buf_dict['data'] = buf.tolist()
            #buf_dict['key'] = KEY
            #buf_json = json.dumps(buf_dict)
            #NNWorkFn.work_function_POST(buf_json.encode('utf-8'))
            #self._set_headers()
            #f=open("data.json")
            #data = f.read()
            #f.close()
            #self.wfile.write(data.encode('utf-8'))
        elif self.path == "/ble":
            print("###### BLE GET Request ##########")
            f=open("bledata.json")
            bledata = f.read()
            f.close()
            bledata = json.loads(bledata)
            print("Got buffer")
            buf_dict = {}
            buf_dict['data'] = bledata### from BLE
            buf_dict['key'] = KEY
            buf_json = json.dumps(buf_dict)
            NNWorkFn.work_function_POST(buf_json.encode('utf-8'))
            self._set_headers()
            f=open("data.json")
            data = f.read()
            f.close()
            self.wfile.write(data.encode('utf-8'))

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print(self.path)
        if self.path == "/":
            NNWorkFn.work_function_POST(post_data)
            self._set_headers()
            f=open("data.json")
            print("###### POST Request ##########")
            data = f.read()
            f.close()
            self.wfile.write(data.encode('utf-8'))
        elif self.path == "/history":
            post_data = post_data.decode('utf-8')
            print(post_data)
            jsondata = json.loads(post_data)
            key = jsondata['key']
            tmp = NNWorkFn.get_JSON_hist('longhistory.csv', key)
            self.wfile.write(tmp.encode('utf-8'))
        
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

