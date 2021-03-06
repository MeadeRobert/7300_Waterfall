import time
import sys
import serial

class SerialInterface:

	port = ""
	ser = None

	# we must enable both the scope display (\x27\x10 state)
	# and the scope data output (\x27\x11 state)
	# to get data output
	def interface_on(self):
		# turn the scope display on
		self.ser.write("\xfe\xfe\x94\xe0\x27\x10\x01\xfd")
		time.sleep(.2)
		# turn on data output mode
		self.ser.write("\xfe\xfe\x94\xe0\x27\x11\x01\xfd")
		time.sleep(.2)
		
	def interface_off(self):
		# turn scope off
		self.ser.write("\xfe\xfe\x94\xe0\x27\x10\x00\xfd")
		time.sleep(.2)
		# turn data out off
		self.ser.write("\xfe\xfe\x94\xe0\x27\x11\x00\xfd")
		time.sleep(.2)

	def init_interface(self):
		self.interface_off()
		self.interface_on()

	def __init__(self, port):
		self.port = port
		
		# initialize serial port
		# this must be 115200 baud to support scope data output
		# the USB must be unlinked form the CIV port on the radio
		# TODO: read port definition from config file
		self.ser = serial.Serial(
			port=self.port,
			baudrate = 115200,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_TWO,
			bytesize=serial.EIGHTBITS,
			timeout=0
		)
		
		# log serial status
		print(self.ser.is_open)
		self.init_interface()

# main loop
'''
data = []
pkt = ""
buffer = ""
while 1:
	found = False
	while not found:
		rd = ser.read()
		sp = buffer.split(chr(0xfe), 1)
		if len(sp) == 2:
			pkt = chr(0xfe) + sp[1]
			while pkt[-1] != chr(0xfd):
				rd = ser.read()
				pkt += rd
			found = True
			#print(' '.join("{:02X}".format(ord(i)) for i in pkt))
			buffer = ''
		else:
			buffer += rd
	data.append(pkt)
  #line = ser.read(8)
	#if len(line) > 0:
	#	print(' '.join("{:02X}".format(ord(i)) for i in line))
	#time.sleep(.005)
'''
