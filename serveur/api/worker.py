#!/bin/env python
import locale
import re
import requests
import sys
from time import sleep
import os
from bottle import route, run, request, response
import json
import socket
from datetime import timedelta
from gpu import GPU
from rig import Rig


@route('/', method='get')
def api():
	response['Access-Control-Allow-Origin'] = '*'
	response['Access-Control-Allow-Methods'] = 'GET'
	response['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'

	g = GPU()
	r = Rig()

	return r.getJson(g) 

if __name__ == '__main__':

	#ip = get_ip()
	run(host="localhost", port=6969)