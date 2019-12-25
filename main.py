import time
import sys
import serial

# initialize serial port
# this must be 115200 baud to support scope data output
# the USB must be unlinked form the CIV port on the radio
# TODO: read port definition from config file
ser = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate = 115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_TWO,
	bytesize=serial.EIGHTBITS,
	timeout=0
)

# log serial status
print(ser.is_open)

# we must enable both the scope display (\x27\x10 state)
# and the scope data output (\x27\x11 state)
# to get data output

def interface_off():
	# turn scope off
	ser.write("\xfe\xfe\x94\xe0\x27\x10\x00\xfd")
	time.sleep(.2)
	# turn data out off
	ser.write("\xfe\xfe\x94\xe0\x27\x11\x00\xfd")
	time.sleep(.2)

def interface_on():
	# turn the scope display on
	ser.write("\xfe\xfe\x94\xe0\x27\x10\x01\xfd")
	time.sleep(.2)
	# turn on data output mode
	ser.write("\xfe\xfe\x94\xe0\x27\x11\x01\xfd")
	time.sleep(.2)

def init_interface():
	interface_off()
	interface_on()

init_interface()

# main loop
header = 0x00
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
			print(' '.join("{:02X}".format(ord(i)) for i in pkt))
			buffer = ''
		else:
			buffer += rd
	data.append(pkt)
  #line = ser.read(8)
	#if len(line) > 0:
	#	print(' '.join("{:02X}".format(ord(i)) for i in line))
	#time.sleep(.005)
