import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from math import radians, cos, sin, asin, sqrt
from networkx.algorithms import approximation as ax

class Map:

	def __init__(self):
		# load data
		self.lines = self.get_data()["lines"]
		self.stations = self.get_data()["stations"]
		self.connections = self.get_data()["connections"]
		# make graph
		self.graph = self.make_graph()

	def get_data(self):
		# get the data from csv files
		lines = pd.read_csv('data/london.lines.csv', index_col=0)
		stations = pd.read_csv('data/london.stations.csv', index_col=0)
		connections = pd.read_csv('data/london.connections.csv')
		# Get rid of ugly column
		stations.drop('display_name', axis=1, inplace=True)
		# Create nice dictionary
		data = thisdict = {
				  "lines":lines,
				  "stations": stations,
				  "connections": connections
				}
		return data

	def make_graph(self):
		graph = nx.Graph()
		# Add connections
		for connection_id, connection in self.connections.iterrows():
			station1_name = self.stations.loc[connection['station1']]['name']
			station1_coords = {
				"x" : self.stations.loc[connection['station1']]['latitude'],
				"y" : self.stations.loc[connection['station1']]['longitude']
				}

			station2_name = self.stations.loc[connection['station2']]['name']
			station2_coords = {
				"x" : self.stations.loc[connection['station2']]['latitude'],
				"y" : self.stations.loc[connection['station2']]['longitude']
				}
			graph.add_node(station1_name, pos=(station1_coords['x'],station1_coords['y']))
			graph.add_node(station2_name, pos=(station2_coords['x'],station2_coords['y']))
			graph.add_edge(station1_name, station2_name, time = connection['time'])
		# Add Bank to Monument manually
		# TODO: this will be replaced by using the API to check close stations
		graph.add_edge('Bank', 'Monument', time = 1)
		return graph

	def draw_graph(self):
		pos = nx.get_node_attributes(self.graph,'pos')
		nx.draw(self.graph, pos, node_size=10, with_labels = False)
		plt.show()

	def get_close_stations(self, station, radius):
		pos = nx.get_node_attributes(self.graph,'pos')

		station_pos = pos[station]

		close_stations = [(station, self.distance(station_pos[1], pos[station][1], station_pos[0], pos[station][0])) 
			for station in pos if self.distance(station_pos[1], pos[station][1], station_pos[0], pos[station][0]) <= radius
			]

		return close_stations


	def distance(self, lat1, lat2, lon1, lon2): 
		# The math module contains a function named
		# radians which converts from degrees to radians.
		lon1 = radians(lon1)
		lon2 = radians(lon2)
		lat1 = radians(lat1)
		lat2 = radians(lat2)

		# Haversine formula
		dlon = lon2 - lon1
		dlat = lat2 - lat1
		a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2	
		c = 2 * asin(sqrt(a))
		
		# Radius of earth in kilometers. Use 3956 for miles
		r = 6371
		
		# calculate the result
		return(c * r)


def main():
	underground = Map()

	# Example of all stations within a 3 km radius of bank
	print(underground.get_close_stations("Bank", 3))

	# underground.draw_graph()


if __name__ == '__main__':
	main()