from datetime import datetime

class Request(object):
	
	def __init__(self,latitude,longitude,dateS,dateE):
		self.latitude 	= latitude
		self.longitude 	= longitude
		self.dateS 		= dateS
		self.dateE 		= dateE
		self.time		= datetime.utcnow()
		self.id			= hex(hash(tuple([latitude,longitude,dateS,self.time])))
	
	def __repr__(self):
		return ''''Coordinates: 
 		latitude: %s' longitude: %s''' % (self.latitude,self.longitude)

class AirportStation(object):
	
	def __init__(self,city,icao,latitude,longitude):
		self.city = city
		self.icao = icao
		self.latitude = latitude
		self.longitude = longitude
	
	def __repr__(self):
		return ''''Coordinates: 
		city: %s' ICAO code: %s''' % (self.city,self.icao)

class PersonalStation(object):

	def __init__(self,stationid,distance):
		self.stationid = stationid
		self.distance = distance

	def __repr__(self):
		return ''''Coordinates: 
		station id: %s' distance (km): %s''' % (self.stationid,self.distance)