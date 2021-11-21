import serial
import time

if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyS0', 115200, timeout = 1)
	ser.flush()

	while True:
		ser.write(b"Hello form Raspberry Pi!\n")
		line = ser.readline().decode('utf-8').rstrip()
		print(line)
		time.sleep(1)
		#if ser.in_waiting > 0:
		#	line = ser.readline().decode('utf-8').rstrip()
		#	print(line)
