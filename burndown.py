#! /usr/bin/env python

from __future__ import division
import datetime
from calendar import monthrange
import random
import requests 
import pickle
import string
import json
import cherrypy

global quota
global aauser
global aapass
aauser = 'xx99@a' # Update this to your clueless user
aapass = 'xxxxxxx' # Update this to your clueless pass
quota = 100 # Update this to your quota in GB 100 is for std Home::1



def getQuota(user, password):
	payload = {'JSON': 0}
	r = requests.get('https://chaos.aa.net.uk/info', auth=(user, password), params=payload)
	data= json.loads(r.text)
	usage = float(int(data['login'][0]['broadband'][0]['quota_left'])/10000000)/100
	return usage

def newMonth(quota):
	d = datetime.date.today()
	file = d.strftime('%Y%b.pkl')
	day = datetime.date(d.year, d.month, 1)
	daysinmonth = monthrange(d.year, d.month)[1]
	dayquota = quota/daysinmonth
	arr = []
	data = ['Date', 'Target', 'Actual']
	arr.append(data)
	data = [day.strftime('%d-%b-%Y'), quota, quota]
	arr.append(data)
	for i in range(1, daysinmonth):
		day += datetime.timedelta(days=1)
		quota = quota - dayquota
		data = [day.strftime('%d-%b-%Y'), quota, None]
		arr.append(data)
	pickle.dump( arr, open(file, "wb"))

def update(usage):
	d = datetime.date.today()
	file = d.strftime('%Y%b.pkl')
	arr = pickle.load(open(file, "rb"))
	for x in arr:
		if x[0] == d.strftime('%d-%b-%Y'):
			x[2] = usage
	pickle.dump( arr, open(file, "wb"))
	

def getPage():
	d = datetime.date.today()
	file = d.strftime('%Y%b.pkl')
	arr = pickle.load(open(file, "rb"))
	data={ 'data':json.dumps(arr)}
	filein = open('index.html')
	src = string.Template(filein.read())
	page = src.substitute(data)
	return page

class Start(object):
	def index(self):
		return getPage()
	def newmonth(self):
		newMonth(quota)
		return "ok"
	def update(self):
		usage = getQuota(aauser, aapass)
		update(usage)
		return  "ok"
	index.exposed = True
	newmonth.exposed = True
	update.exposed = True

cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(Start())

	

