from solutions import BerthAllocationProblem
from fitness_functions import get_total_cost, get_makespan, get_utilizations
from pareto_local_search import ParetoLocalSearch
import random
#import matplotlib.pyplot

#Define scenario
scenario = "scenario04.txt"
iterations = 500
seed = 1
random.seed(1)
#Initiate the problem instance
bap = BerthAllocationProblem.from_file(scenario)


pr_solution = bap.pr_time_window()
print(get_utilizations(pr_solution, bap))
print(pr_solution)
print(get_total_cost(pr_solution, bap), get_makespan(pr_solution, bap))
pr_solution.visualize(scen="PR"+scenario, seed=seed, its=iterations, save=True)

PS = ParetoLocalSearch(pr_solution, [get_total_cost, get_makespan], bap, iters=iterations)
PS.search()
PS.best_solution.visualize(scen="PRAfter"+scenario, seed=seed, its=iterations, save=True)
print(get_total_cost(PS.best_solution, bap), get_makespan(PS.best_solution, bap))
PS.pareto_frontier.visualize(scenario, seed, iterations)
print(get_utilizations(pr_solution, bap))
print(pr_solution)