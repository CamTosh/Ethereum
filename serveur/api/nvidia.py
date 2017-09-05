from gpu import GPU


class Nvidia(GPU):


	def __init__(self):
		super(GPU, self).__init__()


		self.commands = {
			"list": ["nvidia-smi", "-L"],
			"stats": ["gpustat", "--json"],
			"lsmod": ["lsmod"],
		}
		self.encoding = "utf-8"
		self.isNvidiaLoaded()


	def isNvidiaLoaded(self):
		
		type = self.getType()
		if type == "NVIDIA":
			return True
		sys.exit(1)


	def getJson(self):
		gpu_query_columns = ('index', 'name', 'temperature.gpu',
					'utilization.gpu', 'memory.used', 'memory.total')
		gpu_list = []

		smi_output = self.execute_process(
			r'nvidia-smi --query-gpu={query_cols} --format=csv,noheader,nounits'.format(
			query_cols=','.join(gpu_query_columns)
		))
		lines = smi_output.split("\n")
		
		gpus = []

		for line in lines:
			l = line.split(",")
			infos = {}

			infos['index'] = l[0]
			infos['name'] = l[1]
			infos['temperature'] = l[2]
			infos['utilization'] = l[3] if l[3] != " [Not Supported]" else "False"
			
			memory = {}
			memory['used'] = l[4]
			memory['total'] = l[5]

			infos['memory'] = memory


			gpus.append(infos)

		return gpus