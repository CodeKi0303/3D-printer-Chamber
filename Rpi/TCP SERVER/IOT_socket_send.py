from pymongo import MongoClient, DESCENDING
from time import sleep

import socket
import os
import time
import subprocess

def bind_loop(ip, port):
	try:
		server_socket.bind((ip,port))
	except socket.error:
		print('Bind failed')
		time.sleep(1)
		bind_loop(ip,port)

#port init
while True:
	os.system("fuser -l 54322/tcp")
	
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	print("bind...")
	bind_loop('192.168.0.21', 54322)

	print("listen...")
	server_socket.listen(0)
	
	client_socket, addr = server_socket.accept()
	print("IP: " + str(client_socket))
	print("Address: " + str(addr))

	mongo_client = MongoClient("mongodb://localhost:27017/")
	my_db = mongo_client['sensor']
	collection = my_db.motor
	while True:
		sleep(3)
		raw_data = collection.find().sort("_id", -1).limit(1)[0]
		speed = int(int(raw_data['speed']) * 1.55 + 100)
		try:
			client_socket.send(str(speed).encode())
		except:
			print('tcp disconnected')
			break
		print("send data: " + str(speed))
	


