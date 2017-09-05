import netifaces as ni
from datetime import datetime, timedelta
import socket
import json
from nvidia import Nvidia
from amd import Amd


class Rig(object):

	def __init__(self):
		self.encoding = "utf-8"


	def getUptime(self):

		with open('/proc/uptime', 'r') as f:
			uptime_seconds = float(f.readline().split()[0])
			uptime_string = str(timedelta(seconds = uptime_seconds))

			return uptime_string


	def getName(self):
		return socket.gethostname()


	def getQueryTime(self):
		return datetime.now().__str__()


	def execute_process(self, command_shell):
		stdout = check_output(command_shell, shell=True).strip()
		if not isinstance(stdout, (str)):
			stdout = stdout.decode()
			
		return stdout


	def getIp(self):

		try:
			ni.ifaddresses('eth0')
			ip = ni.ifaddresses('eth0')[2][0]['addr'] 
			return str(ip)

		except Exception as e:
			return "localhost"


	def getJson(self, g):
		      
		type = g.getType()
		
		if type == "AMD":
			card = Amd()
		elif type == "NVIDIA":
			card = Nvidia()
		else:
			sys.exit(1)
		
		data = {}
		data['ip'] = self.getIp()
		data['name'] = self.getName()
		data['query'] = self.getQueryTime()
		data['uptime'] = self.getUptime()
		data['type'] = type
		data['gpus'] = card.getJson()

		arr = {}
		arr['data'] = data

		return json.dumps(arr)