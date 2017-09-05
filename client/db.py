from tinydb import TinyDB, Query

class DB(object):

	def __init__(self):
		self.db = TinyDB('config.json')

	def get(type, value):
		return self.db.search(type == value)

	def getAll():
		return self.db.all()

if __name__ == '__main__':
	d = DB()
	print(d.getAll())