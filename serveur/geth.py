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
from datetime import timedelta


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
	d = {}
	ip = get_ip()
	r = RpcJson("localhost", 8008)

	d['Uptime'] = get_uptime()
	d['Hash'] = r.getHashrate()
	d['Balance'] = r.getBalance()
	d['Euro'] = r.getEuroBalance()
	
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