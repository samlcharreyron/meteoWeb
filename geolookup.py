#!/usr/bin/env python
import json,urllib2,os,csv

class GeoLookup:
	
	def __init__(self,latitude,longitude):
		self.latitude = float(latitude)
		self.longitude = float(longitude)
		#self.fileName = fileName
		self.data = self.getData()	#dict containing airport and personal stations
		
	def getData(self):
		lookupUrl = 'http://api.wunderground.com/api/9e513f497c5753b0/geolookup/q/%f,%f.json' %(self.latitude,self.longitude)
		lookupPage = urllib2.urlopen(lookupUrl)
		json_string = lookupPage.read()
		parsed_json = json.loads(json_string)
		
		airportStations = parsed_json['location']['nearby_weather_stations']['airport']['station']
		personalStations = parsed_json['location']['nearby_weather_stations']['pws']['station']
		
		return {"airportStations": airportStations,"personalStations": personalStations}
		
	def writeData(self):
		
		# Writing airport data to CSV
		try:
			f1 = open(os.getcwd()+'''/airports.csv''','wt')
			airportWriter = csv.writer(f1)
			airportWriter.writerow(('City','ICAO','Latitude','Longitude'))
			for airport in self.data["airportStations"]:
				airportWriter.writerow((airport['city'],airport['icao'],airport['lat'],airport['lon']))
		finally:
			f1.close()
		
		# Writing pws data to CSV
		try:
			f2 = open(os.getcwd()+'''/pws.csv''','wt')
			pwsWriter = csv.writer(f2)
			pwsWriter.writerow(('ID','Distance'))
			for pws in self.data["personalStations"]:
				pwsWriter.writerow((pws['id'],pws['distance_km']))
		finally:
			f2.close()
	
if __name__ == '__main__':
	#latitude = float(raw_input("Enter latitude:"))
	#longitude = float(raw_input("Enter longitude:"))
	
	latitude = 37.776289
	longitude = -122.395234
	#fileName = str(raw_input("Enter filename:"))
	
	#Initialize lookup class
	
	lookup1 = GeoLookup(latitude,longitude)
	lookup1.writeData()
