"""
PLAN (in my head at least)

1 Populate directed graph of tube stations with mean travel times and standard deviations (based on train frequency)
  - Each station has an 'Upstairs-Downstairs' split to account for platform-to-surface travel

2 Solve:
  minimize sum of (arc * arc visits) for each arc in the digraph, subject to:
  for downstairs nodes, we require sum(INWARD arc visits) == sum(OUTWARD arc visits)
  (i.e. We travel to the station as many times as we travel from it)

  This is a MILP and can be solved with the open-source CBC solver.

3 By making 'cuts', establish the top N routes to compare.

4 Solve many times, using the standard deviations to randomly vary the travel times.

5 Use all of the above to work out the most robust route.

"""