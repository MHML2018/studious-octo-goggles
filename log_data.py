import serial
import time
import numpy as np
import csv
import sys

ser = serial.Serial('COM3', 115200, timeout=10)  # open serial port
print("Opened port:", ser.name)         # check which port was really used

logfile_fn = "Logger%s.csv" % int(time.time())

logfile = open(logfile_fn, 'w', newline='')
#csvwriter = csv.writer(logfile, quoting=csv.QUOTE_ALL)
csvwriter = csv.writer(logfile)

num_readings = 2000;
osr = 10


try:
	class_val = sys.argv[1]
except:
	print("Provide a CLASS VAL!")
	sys.exit(69)

def get_buf_fromserial(ser, buffer_len, buffer_width):
	buf = np.zeros((buffer_width, buffer_len), dtype=float)
	for i in range(0, buffer_len):
		line = ser.readline()   # read a '\n' terminated line
		line = line.decode("utf-8") 
		line = line.strip('\n')
		line_str = line.split(",")
		line_int = []
		for j in range(0, len(line_str)):
			line_int.append(int(line_str[j]))
		# #line_int = map(int, line_str)
		line_arr = np.asarray(line_int)
		#print(line_int)
		#print("Shapes", line_arr.shape, buf.shape)
		buf[:,i] = line_arr
	return buf



for i in range(0, num_readings+1):
	try:
		buf = get_buf_fromserial(ser, osr, 13)
		#print(buf)
		line = np.mean(buf, axis = 1)
		print(i/num_readings * 100, "%\t", int(time.time()), "\t",np.mean(line))
		data_line = line.tolist()
		data_line.append(class_val)
		csvwriter.writerow(data_line)
	except KeyboardInterrupt:
		print("Interrupted")
	except ValueError:
		print("Value Error")
		continue
print("Finished")
logfile.close()