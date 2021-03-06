import time
import numpy as np
import csv
import sys


num_readings = 2000;
osr = 10


try:
	class_val = sys.argv[1]
except:
	print("Provide a CLASS VAL!")
	sys.exit(69)

import gatt, json
#import struct

manager = gatt.DeviceManager(adapter_name='hci0')

class AnyDevice(gatt.Device):
	
	def services_resolved(self):
		super().services_resolved()

		self.posture_service = next(
		s for s in self.services
			if s.uuid == '64a15170-33f2-c6b6-f740-9985e07962c7')

		self.back_characteristic = next(
		c for c in self.posture_service.characteristics
			if c.uuid == '64a15171-33f2-c6b6-f740-9985e07962c7')
		
		self.butt_characteristic = next(
		c for c in self.posture_service.characteristics
			if c.uuid == '64a15172-33f2-c6b6-f740-9985e07962c7')

		#back_characteristic.read_value()
		self.butt_characteristic.enable_notifications()
		self.back_characteristic.enable_notifications()

	def characteristic_value_updated(self, characteristic, value):
		value = bytes(self.back_characteristic.read_value())
		data = []
		data_fix_back = []
		for z in value:
			data.append(int(z))
		const = 10
		for z in range(0, int(len(data)/2)):
			
			data_fix_back.append((int(data[2*z+1])<<8 | int(data[2*z]))*const)
			
			
		value = bytes(self.butt_characteristic.read_value())
		data = []
		data_fix_butt = []
		for z in value:
			data.append(int(z))
		const = 10
		for z in range(0, int(len(data)/2)):
			data_fix_butt.append((int(data[2*z+1])<<8 | int(data[2*z]))*const)
		
		print(data_fix_butt+data_fix_back)
		with open('bledata.json', 'w') as outfile:
			s = data_fix_butt+data_fix_back
			json.dump(s, outfile)
			s.append(class_val)
			csvwriter.writerow(s)
			
		
logfile_fn = "Logger%s.csv" % int(time.time())

logfile = open(logfile_fn, 'w', newline='')
#csvwriter = csv.writer(logfile, quoting=csv.QUOTE_ALL)
csvwriter = csv.writer(logfile)

# device = AnyDevice(mac_address='C3:22:AC:A0:80:34', manager=manager)
device = AnyDevice(mac_address='D6:6B:78:47:61:B5', manager=manager)
device.connect()

manager.run()
