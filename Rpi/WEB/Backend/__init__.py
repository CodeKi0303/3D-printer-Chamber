from flask import Flask, Response, render_template, request

from pymongo import MongoClient
from time import sleep

import socket
import os
import time
import json
import cv2

app = Flask(__name__)
mongo_client = MongoClient("mongodb://localhost:27017/")

db = mongo_client['sensor']
col_sensor = db.sensor
col_motor =  db.motor
col_mode = db.mode
col_cutoff = db.cutoff

camera = cv2.VideoCapture(1)

def generate_frame():
	while True:
		success, frame = camera.read()
		if not success:
			print("camera failed")
			continue
		else:
			ret, buffer = cv2.imencode('.jpg',frame)
			frame = buffer.tobytes()
			yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
@app.route("/Main", methods=["GET","POST"])
def main():
	return render_template('Main.html')

@app.route("/video")
def video():
	return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/motor", methods=["GET","POST"])
def motor():
	if request.method == 'POST':
		speed = request.form["speed"]
	def add_motor_speed(speed):
		col_motor.insert_one({"speed": speed})
		print(speed)
	return Response(add_motor_speed(speed), mimetype='text/event-stream')

@app.route('/mode', methods=["GET", "POST"])
def mode():
	def get_mode():
		return col_mode.find().sort("_id", -1).limit(1)[0]['mode']

	def change_mode(post_mode):
		col_mode.insert_one({"mode": post_mode})
		print("stop_mode: " + post_mode)

	if request.method == 'GET':
		return Response(get_mode(), mimetype='text/event-stream')

	if request.method == 'POST':
		post_mode = request.form["mode"]
		return Response(change_mode(post_mode), mimetype='text/event-stream')
	

@app.route('/deadline', methods=["GET", "POST"])
def deadline():
	def get_cutoff():
		return col_cutoff.find().sort("_id", -1).limit(1)[0]['cutoff']

	def change_cutoff(post_cutoff):
		col_cutoff.insert_one({"cutoff": post_cutoff })
		print("cutoff: " + post_cutoff)

	if request.method == 'GET':
		return Response(get_cutoff(), mimetype='text/event-stream')
	if request.method == 'POST':
		post_cutoff = request.form["cutoff"]
		return Response(change_cutoff(post_cutoff), mimetype='text/event-stream')

@app.route('/graph')
def chart_data():
	def generate_raw_data():
		while True:
			raw_data = col_sensor.find().sort("_id", -1).limit(1)[0]
			speed_data = col_motor.find().sort("_id", -1).limit(1)[0]
			mode = col_mode.find().sort("_id", -1).limit(1)[0]['mode']
			cutoff = int(col_cutoff.find().sort("_id", -1).limit(1)[0]['cutoff'])
			key_value_data = {}
			key_value_data['TIME'] = time.strftime('%Y%m%d %X', time.localtime())
			key_value_data['speed'] = speed_data['speed']
			 
			for key in raw_data.keys():
				if key != "_id":
					key_value_data[key] = raw_data[key]
			
			pm = int(key_value_data['PM1P0'])
			if mode == '1':
				if pm > cutoff:
					key_value_data['speed'] = '100'
					col_motor.insert_one({"speed": '100'})
				else:
					key_value_data['speed'] = '0'
					col_motor.insert_one({"speed": '0'})
			key_value_data['mode'] = mode
			key_value_data['cutoff'] = str(cutoff)
			
			json_data = json.dumps(key_value_data)
			print(key_value_data)
			yield f"data:{json_data}\n\n"	
			time.sleep(1)

	return Response(generate_raw_data(), mimetype='text/event-stream')

