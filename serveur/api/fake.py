#!/bin/env python
import locale
import re
import requests
import sys
from time import sleep
import os
from bottle import route, run, request, response
import json
import socket
import random

def getRandom(list):
	return random.choice(list)

def getJson():

	data = {}
	data['name'] 	= "GPUSRV00" + str(random.randint(1, 9))
	data['type'] 	= getRandom(["NVIDIA", "AMD"])
	data['ip'] 	 	= ".".join(map(str, (random.randint(0, 255) 
                        for _ in range(4))))
	data['uptime'] 	= "0:43:23.730000"
	
	gpus = []

	for i in range(4):
		g 	 = {}
		g['temperature']  = str(random.randint(20, 90))		

		memory = {}
		memory['used']	  = str(random.randint(1400, 2000))
		memory['total']	  = "2000"
		g['memory'] 	  = memory

		clock = {}
		clock['used']	  = str(random.randint(1200, 1800))
		clock['total']	  = "1800"
		g['clock'] 	 	  = clock


		g['index'] 	      = str(i)
		g['utilization']  = str(True)
		g['load'] 		  = str(random.randint(20, 100))
		g['fan'] 		  = str(random.randint(20, 100))

		gpus.append(g)
	data['gpus'] 	= gpus
	data['query'] 	= "2017-06-15 20:17:30.720493"

	d = {}
	d['data'] = data
	return str(json.dumps(d))


@route('/', method='get')
def api():
	response['Access-Control-Allow-Origin'] = '*'
	response['Access-Control-Allow-Methods'] = 'GET'
	response['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'

	return getJson() 

if __name__ == '__main__':

	#ip = get_ip()
	run(host="localhost", port=4242)