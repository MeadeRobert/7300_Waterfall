import wx
import thread
import time
import Queue
from Tkinter import Tk, Canvas, Frame, BOTH

from serial_interface import SerialInterface

ser = SerialInterface("/dev/ttyUSB0")

packets = Queue.Queue()
commands = Queue.Queue()


root = Tk()



# FE FE E0 94 27 00 00 02 11 
# 		3D 41 3E 39 40 47 4B 3D 32 3A 3E 34 31 40 3B 4D 4A 48 38 3A 43 52 4D 38 2C 
#		33 3D 3C 2E 24 40 33 25 11 31 3C 3E 3F 33 2D 48 5E 6D 5E 3B 27 41 3C 42 47 FD
def task():
	canvas.delete("all")
	root.after(1000, task)
	#print "frame"
	while(not packets.empty()):
		pkt = packets.get()
		print(' '.join("{:02X}".format(ord(i)) for i in pkt))
		
		if(pkt[0:4] == "\xfe\xe0\x94\x27"):
			if pkt[6] != chr(0x01):
				a = pkt.split(chr(0x11))[1]
				values = [ord(i) for i in a]
				
				for i in range(0, len(values)-1):
					canvas.create_line(50*(ord(pkt[6])-2)+i, 0, 50*(ord(pkt[6])-2)+i, values[i], fill="Green")
				#	print i
				
				
				#print(' '.join("{:02X}".format(ord(i)) for i in a))
		else:
			pass
			#print(' '.join("{:02X}".format(ord(i)) for i in pkt))
	
	#print(' '.join("{:02X}".format(ord(i)) for i in pkt))
	canvas.update()
def process_serial(ser):
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
		packets.put(pkt)

thread.start_new_thread( process_serial, (ser,) )

canvas = Canvas(root)
canvas.pack()
root.after(1000, task)
root.mainloop()
	
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

'''
ex = wx.App()
Mywin(None, 'asdf')
ex.MainLoop()
'''
