import serial
import time
from threading import Thread, Lock

###########################
######## serial ###########
###########################
ser = serial.Serial("/dev/ttyS0") 
ser.baudrate = 115200
#ser.xonxoff = True
#ser.rtscts = True
#ser.dsrdtr = True
ser.timeout = 1
exitThread = False
ser.flush()

def run_serial(ser):
	global exitThread, isSetting, esp_OK

	print("Thread Start!")
	while not exitThread:
		try:
			if ser.isOpen():
				if ser.in_waiting > 0:
					line = ser.readline().decode('utf-8').rstrip()
					print("serial:" + line)
			else:
				ser.open()
		except Exception as ex:
			print(ex)
		time.sleep(0.25)
	print("Thread  exit")

def send_serial(data):
	if ser.isOpen():
		print(data)
		for my_chr in data:
			ser.write(my_chr)

run_serial(ser)
#serial_thread = Thread(target=run_serial, args=(ser,))
#serial_thread.daemon = True
#serial_thread.start()

