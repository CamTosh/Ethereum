from subprocess import check_output

class GPU(object):


	def __init__(self):

		self.commands = {
			"lsmod": ["lsmod"]
		}

		self.encoding = "utf-8"


	def execute_process(self, command_shell):
		stdout = check_output(command_shell, shell=True).strip()
		if not isinstance(stdout, (str)):
			stdout = stdout.decode()
			
		return stdout


	def getInformation(self, source, adapter=0):
		
		command = [part.format(adapter) for part in self.commands[source]] 
		
		try:
			info = check_output(command)
		except OSError:
			sys.exit(1)
		
		return info.decode(self.encoding)



	def getType(self):
		
		info = self.getInformation("lsmod")

		if "fglrx" in info:
			return "AMD"
		elif "nvidia" in info:
			return "NVIDIA"
		else:
			return Falses