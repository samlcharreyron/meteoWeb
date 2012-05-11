#!/usr/bin/env python
import os,sys,pickle
import cherrypy

from genshi.filters import HTMLFormFiller

from formencode import Invalid
from model import Request,AirportStation
from form  import RequestForm
from lib import template
from geolookup import GeoLookup

class Root(object):
	
	def __init__(self,data):
		self.data = data
		
	@cherrypy.expose
	@template.output('index.html')
	def index(self):
		return template.render(title="Weather Scraper")
		
	@cherrypy.expose
	@template.output('submit.html')
	def submit(self, cancel=False, **data):
		if cherrypy.request.method == 'POST':
			if cancel:
				raise cherrypy.HTTPRedirect('/')
			form = RequestForm()
			try:
				
				#store request digest in pickle file
				data = form.to_python(data)
				request = Request(**data)
				self.data[request.id] = request
				
				#lookup request
				GeoLookup(request.latitude,request.longitude).writeData()
				
				raise cherrypy.HTTPRedirect('/station')
			except Invalid, e:
				errors = e.unpack_errors()
		else:
			errors = {}
			
		return template.render(errors=errors) | HTMLFormFiller(data=data)
	
	@cherrypy.expose
	@template.output('station.html')
	def station(selfcancel=False, **data):pass
		

def main(filename):
				
	#load data from pickle file or initialize as empty list
	if os.path.exists(os.getcwd()+'/'+filename):
		fileobj = open(filename,'rb')
		try:
			data = pickle.load(fileobj)
		finally:
			fileobj.close()
	else:
		data = {}
	
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
		        '/media': {
		            'tools.staticdir.on': True,
		            'tools.staticdir.dir': 'static'
		        }
		})
		
if __name__ == '__main__':
	main(sys.argv[1])
		
