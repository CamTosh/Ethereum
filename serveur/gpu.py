#!/bin/env python
from subprocess import check_output
import locale
import re
import requests
import sys
from time import sleep
import os
from bottle import route, run, request, response
import json
import socket
import netifaces as ni
from datetime import timedelta


class GPUInfo(object):


	commands = {
		"odgc": ["aticonfig", "--adapter={0}", "--odgc"],
		"odgt": ["aticonfig", "--adapter={0}", "--odgt"],
		"fan":  ["aticonfig", "--pplib-cmd", "get fanspeed {0}"],
		"lsmod": ["lsmod"],
	}

	gpu_mem_posit = {
		"gpu": 0,
		"mem": 0,
	}


	def __init__(self):
		
		self.encoding = "utf-8"
		self.isCatalystLoaded()


	def isCatalystLoaded(self):
		
		info = self.getInformation("lsmod")
		if "fglrx" in info:
			return True
		sys.exit(1)


	def getInformation(self, source, adapter=0):
		
		command = [part.format(adapter) for part in self.commands[source]] 
		
		try:
			info = check_output(command)
		except OSError:
			sys.exit(1)
		
		return info.decode(self.encoding)


	def getLoad(self, adapter=0):
		
		info = self.getInformation("odgc", adapter).split("\n")
		
		for line in info:
			try:
				load_match = re.search(r"GPU load\D+(\d+)%", line)
				if load_match:
					return load_match.group(1)
			except IndexError:
				sys.exit(1)


	def getFanspeed(self, adapter=0):
		
		info = self.getInformation("fan", adapter)
		try:
			fan_match = re.search("(\d{1,3})%", info)
			return fan_match.group(1)
		except IndexError:
			sys.exit(1)


	def getCurrentClock(self, gpu_or_mem, adapter=0):
		
		if gpu_or_mem not in self.gpu_mem_posit:
			sys.exit(1)
		info = self.getInformation("odgc").split("\n")
		current_clock_regex = re.compile(r'Current Clocks\D+(\d+)\s+(\d+)')
		
		for line in info:
			current_clock_match = current_clock_regex.search(line)
			if current_clock_match:
				return current_clock_match.group(self.gpu_mem_posit[gpu_or_mem])
	

	def getMaxClock(self, gpu_or_mem, adapter=0):
		
		if gpu_or_mem not in self.gpu_mem_posit:
			sys.exit(1)
		info = self.getInformation("odgc", adapter).split("\n")
		max_clock_regex = re.compile(r'Current Peak\D+(\d+)\s+(\d+)')
		
		for line in info:
			max_clock_match = max_clock_regex.search(line)
			if max_clock_match:
				return max_clock_match.group(self.gpu_mem_posit[gpu_or_mem])

	
	def getTemperature(self, adapter=0):
		
		info = self.getInformation("odgt", adapter)
		try:
			temp_match = re.search(r'(\d{2,3})\.\d{2} C', info)
			return temp_match.group(1)
		except IndexError:
			sys.exit(1)


def get_uptime():

	with open('/proc/uptime', 'r') as f:
	    uptime_seconds = float(f.readline().split()[0])
	    uptime_string = str(timedelta(seconds = uptime_seconds))

	    return uptime_string

def get_name():
	return socket.gethostname()


def get_ip():
	ni.ifaddresses('eth0')
	ip = ni.ifaddresses('eth0')[2][0]['addr'] 

	return ip


def dico():
	
	grosTableau = {}
	data = {}
	gpu = []
	gpu0 = {}
	gpu1 = {}
	gpu2 = {}
	gpu3 = {}
	gpu4 = {}
	gpu5 = {}

	g = GPUInfo()	
	ip = get_ip()

	data['Uptime'] = get_uptime()
	data['Name'] = get_name()
	data['Ip'] = get_ip()
	
	gpu0['Load'] = str(g.getLoad())
	gpu0['Heat'] = str(g.getTemperature(adapter = 0))
	gpu0['FanSpeed'] = str(g.getFanspeed(adapter = 0))	
	gpu0['MaxClock'] = str(g.getMaxClock("gpu", adapter = 0))
	gpu0['CurrentClock'] = g.getCurrentClock("gpu", adapter = 0)
	gpu0['MaxMem'] = str(g.getMaxClock("mem", adapter = 0))
	gpu0['CurrentMem'] = g.getCurrentClock("mem", adapter = 0)
	#gpu0['Information'] = str(g.getInformation("odgc", adapter = 0))

	gpu1['Load'] = str(g.getLoad())
	gpu1['Heat'] = str(g.getTemperature(adapter = 1))
	gpu1['FanSpeed'] = str(g.getFanspeed(adapter = 1))	
	gpu1['MaxClock'] = str(g.getMaxClock("gpu", adapter = 1))
	gpu1['CurrentClock'] = g.getCurrentClock("gpu", adapter = 1)
	gpu1['MaxMem'] = str(g.getMaxClock("mem", adapter = 1))
	gpu1['CurrentMem'] = g.getCurrentClock("mem", adapter = 1)
	#gpu1['Information'] = str(g.getInformation("odgc", adapter = 1))
	
	gpu2['Load'] = str(g.getLoad())
	gpu2['Heat'] = str(g.getTemperature(adapter = 2))
	gpu2['FanSpeed'] = str(g.getFanspeed(adapter = 2))	
	gpu2['MaxClock'] = str(g.getMaxClock("gpu", adapter = 2))
	gpu2['CurrentClock'] = g.getCurrentClock("gpu", adapter = 2)
	gpu2['MaxMem'] = str(g.getMaxClock("mem", adapter = 2))
	gpu2['CurrentMem'] = g.getCurrentClock("mem", adapter = 2)
	#gpu2['Information'] = str(g.getInformation("odgc", adapter = 2))

	gpu3['Load'] = str(g.getLoad())
	gpu3['Heat'] = str(g.getTemperature(adapter = 3))
	gpu3['FanSpeed'] = str(g.getFanspeed(adapter = 3))	
	gpu3['MaxClock'] = str(g.getMaxClock("gpu", adapter = 3))
	gpu3['CurrentClock'] = g.getCurrentClock("gpu", adapter = 3)
	gpu3['MaxMem'] = str(g.getMaxClock("mem", adapter = 3))
	gpu3['CurrentMem'] = g.getCurrentClock("mem", adapter = 3)
	#gpu3['Information'] = str(g.getInformation("odgc", adapter = 3))
	"""
	gpu4['Load'] = str(g.getLoad())
	gpu4['Heat'] = str(g.getTemperature(adapter = 4))
	gpu4['FanSpeed'] = str(g.getFanspeed(adapter = 4))	
	gpu4['MaxClock'] = str(g.getMaxClock("gpu", adapter = 4))
	gpu4['CurrentClock'] = g.getCurrentClock("gpu", adapter = 4)
	gpu4['MaxMem'] = str(g.getMaxClock("mem", adapter = 4))
	gpu4['CurrentMem'] = g.getCurrentClock("mem", adapter = 4)
	#gpu4['Information'] = str(g.getInformation("odgc", adapter = 4))

	gpu5['Load'] = str(g.getLoad())
	gpu5['Heat'] = str(g.getTemperature(adapter = 5))
	gpu5['FanSpeed'] = str(g.getFanspeed(adapter = 5))	
	gpu5['MaxClock'] = str(g.getMaxClock("gpu", adapter = 5))
	gpu5['CurrentClock'] = g.getCurrentClock("gpu", adapter = 5)
	gpu5['MaxMem'] = str(g.getMaxClock("mem", adapter = 5))
	gpu5['CurrentMem'] = g.getCurrentClock("mem", adapter = 5)
	#gpu5['Information'] = str(g.getInformation("odgc", adapter = 5))
	"""
	gpu.append(gpu0)
	gpu.append(gpu1)
	gpu.append(gpu2)
	gpu.append(gpu3)
	#gpu.append(gpu4)
	#gpu.append(gpu5)

	data['gpu'] = gpu
	grosTableau['data'] = data
	return grosTableau


@route('/', method='get')
def api():
	response['Access-Control-Allow-Origin'] = '*'
	response['Access-Control-Allow-Methods'] = 'GET'
	response['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
	d = dico()
	
	return json.dumps(d)

if __name__ == '__main__':

	ip = get_ip()
	run(host=ip, port=6969)