import sys
import random
from operators import move, swap
from solutions import Solution, BerthAssignment
import matplotlib.pyplot as plt



class ParetoLocalSearch:
    def __init__(self, solution, fitness_function, bap, move_tabu=60, swap_tabu=50, iters=100):
        self.tabu_move = []
        self.tabu_swap = []
        self.best_solution = solution
        self.current_solution = solution
        self.fitness_function = fitness_function
        self.operators = [move, swap]
        self.bap = bap
        self.swap_tabu = swap_tabu
        self.move_tabu = move_tabu
        self.iters = iters
        self.performed_its = 0
        self.best_fitness = [ffcn(self.best_solution, self.bap) for ffcn in self.fitness_function]
        self.pareto_frontier = ParetoFront()
        self.pareto_frontier.front.append(self.best_fitness)

    def get_best_fitness(self):
        return [ffcn(self.best_solution, self.bap) for ffcn in self.fitness_function]

    def get_neighbour(self):
        #We first generate all move neighbours
        neighbourhood = []

        #First, we generate all moves:
        # create a list that checks which berths a vessel may be moved to.
        vessel_allowed_berths = []
        # Loop over all vessels such that we can determine which berths are allowed for that vessel
        for vessel_id in range(len(self.bap.vessels)):
            berth_id = -1
            for berth in self.current_solution.assignment:
                if berth.contains_vessel(vessel_id):
                    berth_id = berth.berth_id
            allowed_berths = []
            for x in range(len(self.bap.berths)):
                if self.bap.vessels[vessel_id].handling_time[x] == 200 \
                    or x == berth_id \
                    or self.operators[0](self.current_solution, vessel_id, x, self.bap) == False:
                    continue
                else:
                    allowed_berths.append(x)
            vessel_allowed_berths.append(allowed_berths)

        for v_id, vessels_to_move in enumerate(vessel_allowed_berths):
            for candidate_berth in vessels_to_move:
                new_soln = self.operators[0](self.current_solution, v_id, candidate_berth, self.bap)
                if new_soln != False:
                    new_sol_fitness = [ffcn(new_soln, self.bap) for ffcn in self.fitness_function]
                    neighbourhood.append(MoveNeighbour(v_id, candidate_berth, new_soln, new_sol_fitness))


        #We then generate all swap neighbouurs:
        for v_id_1 in range(len(self.bap.vessels)):
            for v_id_2 in range(len(self.bap.vessels)):
                #Skip moves with self
                if v_id_1 == v_id_2:
                    continue
                #Get berths of vessels, so that we can see if a swap is allowed
                og_berth_1 = self.current_solution.find_vessel(v_id_1)
                og_berth_2 = self.current_solution.find_vessel(v_id_2)

                #Check if swap is allowed
                if og_berth_2 in vessel_allowed_berths[v_id_1] and og_berth_1 in vessel_allowed_berths[v_id_2]:
                    new_sol = self.operators[1](eval(repr(self.current_solution)), v_id_1, v_id_2, self.bap)
                    if new_sol != False:
                        new_sol_fitness = [ffcn(new_soln, self.bap) for ffcn in self.fitness_function]
                        neighbourhood.append(SwapNeighbour(v_id_1, v_id_2 , new_sol, new_sol_fitness))


        sorted_neighbours = sorted(neighbourhood, key = lambda x: x.solution_fitness[0])
        placement_done = False

        while not placement_done:
            cand_move = sorted_neighbours.pop(0)

            if isinstance(cand_move, MoveNeighbour):

                #Neighbour is found by moving.
                v_id = cand_move.v_id
                b_id = cand_move.n_b_id

                if (v_id, b_id) not in self.tabu_move:
                    self.tabu_move.append((v_id, b_id))
                    self.current_solution = eval(repr(cand_move.solution))

                    if len(self.tabu_move) > self.move_tabu:
                        self.tabu_move = self.tabu_move[1:]

                    if cand_move.solution_fitness[0] <= self.best_fitness[0] and cand_move.solution_fitness[1] <= self.best_fitness[1]:
                        self.best_fitness = [ffcn(cand_move.solution, self.bap) for ffcn in self.fitness_function]
                        self.best_solution = eval(repr(cand_move.solution))
                        self.pareto_frontier.front.append([cand_move.solution_fitness[0], cand_move.solution_fitness[1]])


                    #Update the iterations
                    self.performed_its += 1
                    placement_done = True

            elif isinstance(cand_move, SwapNeighbour):
                #Neighbour is found by swapping
                v_id_1 = cand_move.v_id_1
                v_id_2 = cand_move.v_id_2

                if (v_id_1, v_id_2) not in self.tabu_swap:
                    self.tabu_swap.append((v_id_1, v_id_2))
                    self.current_solution = eval(repr(cand_move.solution))

                    if len(self.tabu_swap) > self.swap_tabu:
                        self.tabu_swap = self.tabu_swap[1:]

                    #Update best if it is better
                    if cand_move.solution_fitness[0] <= self.best_fitness[0] and cand_move.solution_fitness[1] <= self.best_fitness[1]:
                        self.best_fitness = [ffcn(cand_move.solution, self.bap) for ffcn in self.fitness_function]
                        self.best_solution = eval(repr(cand_move.solution))
                        self.pareto_frontier.front.append([cand_move.solution_fitness[0], cand_move.solution_fitness[1]])

                    #Update the iterations
                    self.performed_its += 1
                    placement_done = True

            else:
                raise Exception("Incorrect neighbour found")

    def search(self):
        while self.performed_its < self.iters:
            self.get_neighbour()

#Class for moving neighbours
class MoveNeighbour:
    def __init__(self, v_id, n_b_id, solution, solution_fitness):
        self.v_id = v_id
        self.n_b_id = n_b_id
        self.solution = solution
        self.solution_fitness = solution_fitness

    def __str__(self):
        return f"({self.v_id}, {self.n_b_id_2}, {self.solution_fitness})."
    
#Class for swapping neighbours
class SwapNeighbour:
    __new_id = 0
    def __init__(self, v_id_1, v_id_2, solution, solution_fitness):
        self.v_id_1 = v_id_1
        self.v_id_2 = v_id_2
        self.solution = solution
        self.solution_fitness = solution_fitness
        self.id = SwapNeighbour.__new_id = 0
        SwapNeighbour.__new_id += 1

    def __str__(self):
        return f"({self.v_id_1}, {self.v_id_2}, {self.solution_fitness})."
    
    
class ParetoFront:
    def __init__(self):
        self.front = []
    
    def visualize(self, scen="NoScen", seed="NoSeed", its="NoIters"):
        plt.figure(figsize=(5, 5), dpi=250)
        for coord in self.front:
            plt.plot(coord[0], coord[1], marker = "o", markersize = 20)
        plt.title("Pareto efficiency Frontier")
        plt.xlabel("Total cost")
        plt.ylabel("Makespan")
        plt.savefig(fname=f"figures/pareto_front_scn_{scen}_seed_{seed}_its_{its}.png", dpi=250)
