# coding: utf-8
import requests
import re
import json
from bottle import route, request, run


class Chart(object):

	def __init__(self):
		pass


	def avg(self, l):
		return int(sum(l) / len(l))


	def getIp(self):
		
		with open("config.json") as dataJson:
			data = json.load(dataJson)
		
		l = []

		for d in data['worker']:
			l.append(d['ip'])

		return l


	def getHeat(self, ip):
		r = requests.get("http://" + ip)
		data = r.json()
		l = []

		for d in data['data']['gpu']:
			l.append(int(d['Heat']))

		return self.avg(l)


	def avgHeatWorker(self):
		ip = self.getIp()
		l = []

		for i in ip:
			print(i + " " + str(self.getHeat(i)))
			l.append(self.getHeat(i))

		return self.avg(l)


@route('/')
def home():
	"""
	Todo :
		- template graph
		- fix GPU api timeout
	"""
	pass

if __name__ == '__main__':
	c = Chart()
	print(c.avgHeatWorker())

	run(host='localhost', port=8080, debug=False)
