#!/bin/env python
from eth_rpc_client import Client
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


class GPUInfo(object):


	commands = {
		"odgc": ["aticonfig", "--adapter={0}", "--odgc"],
		"odgt": ["aticonfig", "--adapter={0}", "--odgt"],
		"fan":  ["aticonfig", "--pplib-cmd", "get fanspeed {0}"],
		"lsmod": ["lsmod"],
	}

	gpu_mem_posit = {
		"gpu": 1,
		"mem": 2,
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
		current_clock_regex = re.compile(r'Current Clocks\D+(\d+)\s+(\d+)') # J'ai corrigé le soucis.
		
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


class RpcJson(object):

	def __init__(self, ip, port):
		self.ip = ip
		self.port = port


	def json (self, command, args = []):
		payload = {
			"method": command,
			"params": args,
			"jsonrpc": "2.0",
			"id": 0,
		}
		r = requests.post('http://' + self.ip + ':' + str(self.port) + '/', data=json.dumps(payload), headers={'content-type': 'application/json'})
		res = r.json()
		return res['result']


	def getEuroBalance(self):

		r = requests.get("https://www.cryptocompare.com/api/data/price?fsym=ETH&tsyms=EUR")
		res = r.json()

		for i in res['Data']:
			i['Price']

		b = self.getBalance()

		return str(b / 1000000000000000000 * i['Price'])[:5]


	def getCoinbase(self):
		c = self.json('eth_coinbase', 'ether')
		return c


	def getHashrate(self):

		h = self.json('eth_hashrate')
		return int(h, 16)


	def getBalance(self):
		c = self.getCoinbase()
		l = (c, 'latest')
		b = self.json('eth_getBalance', l)
		return int(b, 16)


	def getAccounts(self):

		a = self.json('eth_getAccounts')
		return a



def get_name():
	return socket.gethostname()


def get_ip():
	ni.ifaddresses('eth0')
	ip = ni.ifaddresses('eth0')[2][0]['addr'] 

	return ip


def dico():
	d = {}
	ip = get_ip()
	g = GPUInfo()
	r = RpcJson(ip, 8008) # mettre le port de Geth

	d['Hash'] = r.getHashrate()
	d['Balance'] = r.getBalance()
	#d['Accounts'] = r.getAccounts()
	d['Name'] = get_name()
	d['Ip'] = get_ip()
	d['Load'] = str(g.getLoad())
	d['Heat'] = str(g.getTemperature())
	d['FanSpeed'] = str(g.getFanspeed())	
	d['MaxClock'] = str(g.getMaxClock("gpu"))
	d['CurrentClock'] = g.getCurrentClock("gpu")
	d['MaxMem'] = str(g.getMaxClock("mem"))
	d['CurrentMem'] = g.getCurrentClock("mem")
	d['Information'] = str(g.getInformation("odgc"))

	return d


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

