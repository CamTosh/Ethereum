from gpu import GPU
from subprocess import check_output


class Amd(GPU):


	commands = {
		"odgc": ["aticonfig", "--adapter={0}", "--odgc"],
		"odgt": ["aticonfig", "--adapter={0}", "--odgt"],
		"fan":  ["aticonfig", "--pplib-cmd", "get fanspeed {0}"]
		}

	gpu_mem_posit = {
		"gpu": 1,
		"mem": 2,
	}


	def __init__(self):
		super(GPU, self).__init__()
		self.isCatalystLoaded()


	def isCatalystLoaded(self):
		
		type = self.getType()
		if type == "AMD":
			return True
		sys.exit(1)


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


	def getAdapter(self):

		s = check_output(["aticonfig", "--list-adapters"])
		
		for l in s.splitlines():
			n = l[:2].replace(" ", "").replace("*", "")
		
		return int(n) 


	def getJson(self):

		nbr = self.getAdapter()
		gpus = []

		for i in range(0, nbr):
			infos = {}

			infos['index'] = i
			infos['utilization'] = str(self.getLoad())
			infos['temperature'] = str(self.getTemperature(adapter = i))
			infos['fanSpeed'] = str(self.getFanspeed(adapter = i))	
			
			clock = {}
			clock['used'] = self.getCurrentClock("gpu", adapter = i)
			clock['total'] = str(self.getMaxClock("gpu", adapter = i))
			infos['clock'] = clock

			memory = {}
			memory['used'] = self.getCurrentClock("mem", adapter = i)
			memory['total'] = str(self.getMaxClock("mem", adapter = i))
			infos['memory'] = memory

			gpus.append(infos)

		return gpus