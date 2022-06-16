import googlemaps
from datetime import datetime
from config import g_maps_key


class Gmaps:
  	def __init__(self, key):
  		self.secret = key
  		self.gmaps = googlemaps.Client(key=self.secret)


	def travel_time(start, end):
		result = gmaps.directions(
			start,
			end,
			mode="transit",
			departure_time=now
		)
		return result

 

directions = Gmaps(g_maps_key)

directions.travel_time('West Kensington Station, North End Road, London','Oval Station, Kennington Park Road, London' )