#!/usr/bin/env python
import os,sys,pickle
import cherrypy

from genshi.filters import HTMLFormFiller

from formencode import Invalid
from model import Request,AirportStation,PersonalStation
from form  import RequestForm
from lib import template
from geolookup import GeoLookup,GeoLookupError

class Root(object):
	
	def __init__(self,data):
		self.data = data
		self.response = {}		
		
	@cherrypy.expose
	@template.output('index.html')
	def index(self, cancel=False, **data):
		if cherrypy.request.method == 'POST':
			if cancel:
				raise cherrypy.HTTPRedirect('/')
			form = RequestForm()
			try:
				
				#store request digest in pickle file
				data = form.to_python(data)
				request = Request(**data)
				self.data['request'][request.id] = request
				
				#geolookup request
				try:
					self.data['response'] = GeoLookup(request.latitude,request.longitude).toModel()
					raise cherrypy.HTTPRedirect('/station')
				except Exception as ers:
					flasherrors = str(ers)
					errors = {}
					#raise cherrypy.HTTPRedirect('/')
				
			except Invalid, e:
				errors = e.unpack_errors()
		else:
			errors = {}
			flasherrors = ''
			
		return template.render(errors=errors,flasherrors=flasherrors) | HTMLFormFiller(data=data)
	
	@cherrypy.expose
	@template.output('station.html')
	def station(self,cancel=False):
		return template.render(airports=self.data['response']['airports'],pwstations=self.data['response']['pwstations'])
		

def main(filename):
				
	#load data from pickle file or initialize as empty list
	if os.path.exists(os.getcwd()+'/'+filename):
		fileobj = open(filename,'rb')
		try:
			data = pickle.load(fileobj)
		finally:
			fileobj.close()
	else:
		data = {'request':{},'response':{}}
	
	def _save_data():
		fileobj = open(filename,'wb')
		try:
			pickle.dump(data, fileobj)
		finally:
			fileobj.close()
		
	cherrypy.engine.subscribe('stop',_save_data)
	
	cherrypy.config.update({
	        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
	        'tools.decode.on': True,
	        'tools.trailing_slash.on': True,
	        'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
	    })
	
	cherrypy.quickstart(Root(data), '/', {
		        '/static/css': {
		            'tools.staticdir.on': True,
		            'tools.staticdir.dir': 'static/css'
		        }
		})
		
if __name__ == '__main__':
	main(sys.argv[1])
		
