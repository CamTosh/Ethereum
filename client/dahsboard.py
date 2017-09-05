#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template
import json
import requests
import subprocess as sp
import os
import sys
import time
from 
app = Flask(__name__)

def openJson():
	f = open("config.json", "r")
	return json.loads(f.read())

def getIP(index):
	j = openJson()
	
	for i in j['worker']:
		for k in i['rig']:
			if k['index'] == index:
				return "http://" + k['ip']

def ping(ip):
	ip = ip.split(":")[0]
	# Do the ping function
	return True


@app.context_processor
def my_utility_processor():
	return dict(ping=ping)


@app.route("/")
def home():
	return render_template('index.html', json=openJson())


@app.route("/list")
def list():
	return "Hello World!"


@app.route("/dashboard")
def dashboard():
	return "Hello World!"

@app.route("/chart")
def chart():
	return render_template('chart.html', json=openJson()['charts'])


@app.route("/detail/<id>")
def detail(id):
	id = id.replace("%", " ")
	ip = getIP(id)

	return render_template('detail.html', ip=ip)


if __name__ == "__main__":
	app.run(debug=True)
