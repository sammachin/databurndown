from __future__ import division
import datetime
from calendar import monthrange
import random
import requests 
from bs4 import BeautifulSoup
import pickle
import string
import json
import cherrypy

global aauser
global aapass
aauser = 'xx99@a' # Update this to your clueless user
aapass = 'xxxxxxx' # Update this to your clueless pass



def getUsage(user, password):
	r = requests.get('http://localhost:8080/usage.html')
	soup = BeautifulSoup(r.text)
	qstring = soup.find_all('table')[4].find('tr').findNext('tr').find_all('td')[4].string
	usage = float(qstring)
	return usage


def getQuota(user, password):
	r = requests.get('http://localhost:8080/usage.html')
	soup = BeautifulSoup(r.text)
	topup =  soup.find_all('table')[4].find('tr').findNext('tr').find_all('td')[5].string
	cfwd =  soup.find_all('table')[4].find('tr').findNext('tr').find_all('td')[3].string
	quota = float(topup) + float(cfwd.lstrip('\n').rstrip('\n'))
	return quota


def newMonth():
	d = datetime.datetime.now()
	daysinmonth = monthrange(d.year, d.month)[1]
	hoursinmonth = daysinmonth * 24
	t = datetime.datetime(d.year, d.month, 1, 00, 00, 0)
	weekdays = 0
	for i in range(1, daysinmonth+1):
    	try:
			thisdate = datetime.date(d.year, d.month, i)
		except(ValueError):
			break
		if thisdate.weekday() < 5: 
			weekdays += 1
	peakhours = weekdays * 9
	ophours = hoursinmonth - peakhours
	steps = 0
	for i in range(1, hoursinmonth):
		t += datetime.timedelta(hours=1)
		if t.weekday() < 5 and 9<= int(t.strftime('%H')) <= 18:
			steps +=  20
		else:
			steps +=  1
	vals = {}
	vals['steps'] = steps
	t = datetime.datetime(d.year, d.month, 1, 00, 00, 0)
	arr = []
	data = ['Date', 'Target']
	arr.append(data)
	data = [t.strftime('%d-%b-%Y %H:00'), quota, None]
	arr.append(data)
	for i in range(1, hoursinmonth):
		t += datetime.timedelta(hours=1)
		if t.weekday() < 5 and 9<= int(t.strftime('%H')) <= 18:
			steps -=  20
		else:
			steps -=  1
		data = [t.strftime('%d-%b-%Y %H:00'), steps, None]
		arr.append(data)
	vals['quota'] = getQuota(aauser, aapass)
	vals['factor'] = vals['steps'] / vals['quota']
	month = d.strftime('%Y%b')
	pickle.dump( month, open(month+"_val.pkl", "wb"))
	pickle.dump( arr, open(month+".pkl", "wb"))

def update(usage):
	d = datetime.date.now()
	month = d.strftime('%Y%b')
	arr = pickle.load(open(month+".pkl", "rb"))
	vals = pickle.load(open(month+"_val.pkl", "rb"))
	for x in arr:
		if x[0] == d.strftime('%d-%b-%Y %H:00'):
			x[2] = usage * vals['factor']
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
		usage = getUsage(aauser, aapass)
		update(usage)
		return  "ok"
	index.exposed = True
	newmonth.exposed = True
	update.exposed = True

cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(Start())
		
		
		
	

	