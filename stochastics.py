from solutions import BerthAllocationProblem
from fitness_functions import get_total_cost_with_penalty, get_makespan, get_utilizations
from tabu_search import TabuSearch
import random
import matplotlib.pyplot as plt
from timeit import default_timer as timer

scenario = "scenario05.txt"
iterations = 1000
#Initiate the problem instance

scores_list = []
begin = timer()
for seed in range(iterations):
    print(seed)
    bap = BerthAllocationProblem.from_file(scenario)
    random.seed(seed)
    fcfs_solution = bap.fcfs()
    #TS = TabuSearch(fcfs_solution, get_total_cost_with_penalty, bap, iters=20)
    #TS.search()
    scores_list.append(get_total_cost_with_penalty(fcfs_solution, bap))
    

plt.figure(figsize=(5, 5), dpi=250)
plt.boxplot(scores_list)
plt.title("Box plot of stochastic arrival and handling times")
plt.xlabel("Scenario 5")
plt.ylabel("Cost with penalty")
plt.show()
print(timer()-begin)