import csv
import time
import json


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
	
	return json.dumps(data)
	

print(get_JSON_hist('longhistory.csv', 566969))