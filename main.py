import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

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
			station2_name = self.stations.loc[connection['station2']]['name']
			graph.add_edge(station1_name, station2_name, time = connection['time'])
			# Add Bank to Monument manually
			# TODO: this will be replaced by using the API to check close stations
		graph.add_edge('Bank', 'Monument', time = 1)
		return graph

	def draw_graph(self):
		nx.draw(self.graph,node_size=15)
		plt.show()


def main():
	underground = Map()
	underground.draw_graph()


if __name__ == '__main__':
	main()