from flask import Flask, Response, render_template, request, redirect, url_for

from pymongo import MongoClient
import time

mongo_client = MongoClient("mongodb://localhost:27017/")

db = mongo_client['sensor']
collection = db.motor

raw_data = collection.find().sort("_id", -1).limit(1)[0]
for key in raw_data.keys():
	if key != "_id":
		print(key + " " + str(raw_data[key]))

print(time.strftime('%Y%m%d %X', time.localtime()) )
