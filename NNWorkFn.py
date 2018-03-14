import socket
import threading
import json
import sys
import numpy as np
import csv
import serial
import time

from keras.models import model_from_json

## Starting code from:
## https://gist.github.com/tuxmartin/e7c85f84153ba15576c5

## Lots of help from:
## https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/
# and
## https://machinelearningmastery.com/save-load-keras-deep-learning-models/


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
	
def work_function_single_thread(input_data, loaded_model):
    print("Work function working on work stuff of length %i" % (len(input_data)))
    X = np.asarray(input_data, dtype=np.float32)
    #np_input = np.asmatrix(input_data, dtype = np.float)
    #X = np.mean(np.asarray(input_data, dtype=np.float), axis=1)
    meanz = 111334.06928537242
    maxz = 500000.0
    minz = 920
    
    X = X - meanz
    X = X/(maxz-minz)
    # We need to load the nnet into memory in each thread (to make it thread safe)
    print(X)

    # evaluate loaded model on test data
    #loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])


    print("Data Shape:", X.shape)
    X = np.array([X])
    prediction = loaded_model.predict(X)
    #prediction = prediction.flat[0]
    print(prediction)
    return prediction


def dump_JSON(_posture, _occupied, _data_list, _confidence = None,  _score = None, _x = None, _y = None, _z = None, _ui = "Please consult the NHS guidelines"):
	data = {}
	data["occupied"] = _occupied
	data["posture"] = _posture
	data["confidence"] = _confidence
	data["score"] = _score
	data["x"] = _x
	data["y"] = _y
	data["z"] = _z
	data["ui"] = _ui
	data["raw"] = _data_list
	
	with open('data.json','w') as outfile:
		json.dump(data, outfile)


json_file = open('model.nn', 'r')
loaded_model_json = json_file.read()
json_file.close()

loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

history_len = 200
i = 0
score_guide = 0.4
thresh = 300000
with open('history.json', 'w') as fp:
	data = {}
	history = np.zeros(history_len)
	for i in range(0, history_len):
		if i%2:
			history[i] = 1
	
	data['hist'] = history.tolist()
	data['i'] = i
	data['score_guide'] = score_guide
	data['thresh'] = thresh
	
	json.dump(data, fp)
	

def work_function_POST(buf):
	buf = buf.decode('utf-8')
	print(buf)
	with open('history.json', 'r') as fp:
		history_dict = json.load(fp)
		history = history_dict['hist']
		history_len = len(history)
		i = history_dict['i']
		score_guide = history_dict['score_guide']
		thresh = history_dict['thresh']
	
	#try: 
	jsondata = json.loads(buf)
	cert = work_function_single_thread(jsondata['data'], loaded_model) 
	
	meanval = np.mean(jsondata['data'])
	print("Abs Val:", meanval)
	if (meanval < thresh):
		occ = True
		print("SOMEONE IS SITTING HERE")
	else:
		occ = False
		print("NO ONE IS SITTING HERE")
	
	pos = int(np.argmax(cert))
	
	if pos == 0:
		print("GOOD")
	elif pos == 1:
		print("Leaning Back")
	elif pos == 2:
		print("Leaning Forward")
	elif pos == 3:
		print("Leaning Left")
	elif pos == 4:
		print("Leaning Right")
	elif pos == 5:
		print("Crossed Legs")
	else:
		print("Invalid Class")
		
		
	#except ValueError:
		#print("Excepted Value Error")
	
	
	if i>history_len-1:
		i = 0
	
	if occ:
		if pos == 0:
			history[int(i)]=1
		else:
			history[int(i)]=0
	i = i + 1
	score = np.mean(np.asarray(history, dtype=np.float32))
	print('@@@@@@@@@@@@@ SCORE = %f @@@@@@@@@@@' % (score))
	#print(history)
	#score = 0 
	#delta = 0.02
	#if occ: 
		#for z in history:
			#if z != 0:
				#score = score + delta
			#elif z != 0:
				#score = score + delta
	
	#if score < 0:
		#score = 0
	#elif score > 1:
		#score = 1
	
	if score > score_guide:
		ui = "Good job!"
	else:
		ui = "Please consult the NHS guidelines"
		
	with open('history.json', 'w') as fp:
		history_dict['hist'] = history
		history_dict['i'] = i
		
		json.dump(history_dict, fp)
	
	fields=[jsondata['key'],time.time(),float(score)]
	with open('longhistory.csv', 'a', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(fields)
	dump_JSON(pos, occ, jsondata['data'], _score = float(score), _ui = ui)
	
	
def get_JSON_hist(fname, key):
	key = int(key)
	tmp = []

	with open(fname, newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			if int(row[0]) == key:
				tmp.append(row)
	data = []
	for i in tmp:
		tmpdict = {}
		tmpdict['x'] = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(float(i[1])))
		tmpdict['y'] = i[2]
		data.append(tmpdict)
	jsonout = {};
	jsonout['data'] = data;
	return json.dumps(jsonout)
	

