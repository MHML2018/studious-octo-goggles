import socket
import threading
import json
import sys
import numpy as np

import serial

from keras.models import model_from_json

## Starting code from:
## https://gist.github.com/tuxmartin/e7c85f84153ba15576c5

## Lots of help from:
## https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/
# and
## https://machinelearningmastery.com/save-load-keras-deep-learning-models/


## Set up TCP Server
bind_ip = '127.0.0.1' # Use localhost for now - replace with '' for global connections
bind_port = 5025

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print('Listening on ', bind_ip, bind_port)


## This is the function that does the classification
def work_function(input_data):
    print("Work function working on work stuff of length %i" % (len(input_data)))
    np_input = np.asmatrix(input_data, dtype = np.float)
    X = np.mean(np_input, 0)
    
    # We need to load the nnet into memory in each thread (to make it thread safe)
    json_file = open('model.nn', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")

    # evaluate loaded model on test data
    #loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    
    print("Data Shape:", X.shape)
    prediction = loaded_model.predict(X)
    prediction = prediction.flat[0]
    print(prediction)
    return prediction


buffer_len = 100
buffer_width = 4

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=10)  # open serial port
print("Opened port:", ser.name)         # check which port was really used
while True:
	buf = np.zeros(buffer_width, buffer_len)
	for i in buffer_len:
		line = ser.readline()   # read a '\n' terminated line
		line_str = line.split(",")
		line_int = []
		for j in range(0, len(line_str)):
			line_int.append(int(line_str[j]))
		#line_int = map(int, line_str)
		line_arr = np.asarray(line_int)
		buf[:,i] = line_arr
	
	
	

# ## Handle request and pass data to work function
# def handle_client_connection(client_socket):
    # print("Listening for data")
    # request = client_socket.recv(2097152)
    # print('Received len()', len(request))
    
    # rx_size = sys.getsizeof(request)
   
    # request_decode = json.loads(request.decode())
    
    # work_output = work_function(request_decode)
    
    # response = "This is my response! I recieved %i bytes. Work output: %f" % (rx_size, work_output)
    # client_socket.send(response.encode())
    
    # client_socket.close()


# ## Main loop
# while True:
    # client_sock, address = server.accept()
    # print('Accepted connection from', address[0], address[1])
    # client_handler = threading.Thread(
        # target=handle_client_connection,
        # args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    # )
    # client_handler.start()
