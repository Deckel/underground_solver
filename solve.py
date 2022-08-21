import random

import pandas as pd
import pyomo.environ as pyo
import networkx

from main import *


def solve(graph):
	# UTILITY
	friends = {n: [e for e in graph.edges if n in e] for n in graph.nodes}
	min_degree = {n: min(d, 2) for n, d in graph.degree()}

	# MODEL
	model = pyo.ConcreteModel()

	# SETS
	model.nodes = pyo.Set(initialize=list(graph.nodes))
	model.edges = pyo.Set(within=model.nodes * model.nodes, dimen=2, initialize=list(graph.edges))

	# PARAMETERS
	def time_init(m, start, end):
		return graph.edges[(start, end)]['time']
	model.time = pyo.Param(model.edges, initialize=time_init)

	# VARIABLES
	model.weight = pyo.Var(model.edges, within=pyo.NonNegativeIntegers)
	model.used = pyo.Var(model.edges, within=pyo.Binary)
	model.halfweight = pyo.Var(model.nodes, within=pyo.NonNegativeIntegers)

	# CONSTRAINTS
	def total_weight_ge_1_rule(m, node):
		return sum(m.weight[edge] for edge in friends[node]) >= 1
	model.total_weight_ge_1 = pyo.Constraint(model.nodes, rule=total_weight_ge_1_rule)

	def total_weight_even_rule(m, node):
		return sum(m.weight[edge] for edge in friends[node]) == 2 * model.halfweight[node]
	model.total_weight_even = pyo.Constraint(model.nodes, rule=total_weight_even_rule)

	def used_lt_weight_rule(m, start, end):
		return m.weight[(start, end)] >= m.used[(start, end)]
	model.used_lt_weight = pyo.Constraint(model.edges, rule=used_lt_weight_rule)

	def min_friends_rule(m, node):
		return sum(m.used[edge] for edge in friends[node]) >= min_degree[node]
	model.min_friends = pyo.Constraint(model.nodes, rule=min_friends_rule)

	# OBJECTIVE
	def minimise_total_weight(m):
		return sum(m.weight[edge] * m.time[edge] for edge in m.edges)
	model.objective = pyo.Objective(rule=minimise_total_weight, sense=pyo.minimize)

	# SOLVE
	opt = pyo.SolverFactory('cbc')#, executable='solver/bin/cbc')
	sln = opt.solve(model, tee=True)
	model.display() 

	return model, sln


biggraph = get_biggraph()
model, sln = solve(biggraph.graph)

# xx = networkx.complete_graph(4)
# for a, b, d in xx.edges(data=True):
# 	d['time'] = random.randint(1, 10)
# model, sln = solve(xx)

edges = pd.read_csv('output.csv')

g = networkx.Graph()


if __name__ == '__main__':
	test()
