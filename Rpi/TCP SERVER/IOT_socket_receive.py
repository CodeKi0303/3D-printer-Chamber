from pymongo import MongoClient
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


def make_json(data_received):
	PM_1P0 = data_received.split(' ')[1]
	PM_2P5 = data_received.split(' ')[3]
	PM_10 = data_received.split(' ')[5]
	HUMID = data_received.split(' ')[7]
	TEMP = data_received.split(' ')[9]
	var ={
		"PM1P0": int(PM_1P0),
		"PM2P5": int(PM_2P5),
		"PM10" : int(PM_10),
		"HUMID": float(HUMID),
		"TEMP" : float(TEMP)
	}
	return var
	
while True:
	#port init
	os.system("fuser -l 54321/tcp")
	
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	print("bind...")
	bind_loop('192.168.0.21', 54321)
	
	print("listen...")
	server_socket.listen(0)
	
	client_socket, addr = server_socket.accept()
	print("IP: " + str(client_socket))
	print("Address: " + str(addr))
	
	mongo_client = MongoClient("mongodb://localhost:27017/")
	my_db = mongo_client['sensor']
	collection = my_db.sensor
	while True:
		try:
			data_received = client_socket.recv(1024).decode()
			client_socket.send("get".encode())
		except:
			print("TCP disconnected");
			break;
		data_json = make_json(data_received)
		collection.insert_one(data_json)
		print(data_json)


