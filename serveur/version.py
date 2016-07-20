#!/bin/env python
import requests

def get_version():
	v = requests.get("https://raw.githubusercontent.com/CamTosh/Ethereum/master/version")
	version = open("../version", 'r').read()
	if int(v.json()) == int(version):
		print("Software up to date")
	else:
		print("Update your software please")

if __name__ == '__main__':
	get_version()
		