import gatt, json, sys, os
#import struct



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
			try:
				value = bytes(self.back_characteristic.read_value())
			except TypeError:
				os.execl(sys.executable, sys.executable, *sys.argv)

			data = []
			data_fix_back = []
			for z in value:
				data.append(int(z))
			const = 10
			for z in range(0, int(len(data)/2)):
				
				data_fix_back.append((int(data[2*z+1])<<8 | int(data[2*z]))*const)
				
			try:
				value = bytes(self.butt_characteristic.read_value())
			except TypeError:
				os.execl(sys.executable, sys.executable, *sys.argv)
				
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
		#except:
			#print("Cannot get chair data!")


manager = gatt.DeviceManager(adapter_name='hci0')
# device = AnyDevice(mac_address='C3:22:AC:A0:80:34', manager=manager)
device = AnyDevice(mac_address='D6:6B:78:47:61:B5', manager=manager)
device.connect()

manager.run()
	

