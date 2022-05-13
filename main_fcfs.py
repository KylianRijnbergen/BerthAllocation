from solutions import BerthAllocationProblem
from fitness_functions import get_total_cost, get_makespan, get_utilizations
from pareto_local_search import ParetoLocalSearch
import random
#import matplotlib.pyplot

#Define scenario
scenario = "scenario05.txt"
iterations = 500
seed = 1
random.seed(1)
#Initiate the problem instance
bap = BerthAllocationProblem.from_file(scenario)


fcfs_solution = bap.fcfs()
print(get_utilizations(fcfs_solution, bap))
print(fcfs_solution)
print(get_total_cost(fcfs_solution, bap), get_makespan(fcfs_solution, bap))
fcfs_solution.visualize(scen="fcfs"+scenario, seed=seed, its=iterations, save=True)

PS = ParetoLocalSearch(fcfs_solution, [get_total_cost, get_makespan], bap, iters=iterations)
PS.search()
PS.best_solution.visualize(scen="fcfsAfter"+scenario, seed=seed, its=iterations, save=True)
print(get_total_cost(PS.best_solution, bap), get_makespan(PS.best_solution, bap))
PS.pareto_frontier.visualize(scenario, seed, iterations)
print(get_utilizations(fcfs_solution, bap))
print(fcfs_solution)
