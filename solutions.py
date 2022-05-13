import numpy as np
from vessel import Vessel
from berth import Berth
import operator
import matplotlib.pyplot as plt
import random


class BerthAssignment:
    def __init__(self, berth_id, vessels=None):
        self.berth_id = berth_id
        if vessels is None:
            self.vessels = []
        else:
            self.vessels = vessels

    def contains_vessel(self, vessel_id):
        for (v, *_) in self.vessels:
            if v == vessel_id:
                return True
        return False

    def remove_vessel(self, vessel_id):
        if not self.contains_vessel(vessel_id):
            raise Exception("Vessel not found in berth assignment.")
        for v in self.vessels:
            if v[0] == vessel_id:
                self.vessels.remove(v)

    def add_vessel(self, vessel_id, starting_time, duration):
        if self.contains_vessel(vessel_id):
            raise Exception("Vessel already in berth assignment.")
        self.vessels.append((vessel_id, starting_time, duration))


    def get_available(self, arrival_time, duration, bap, debug=False):
        opening_time_berth = bap.berths[self.berth_id].opening_time
        closing_time_berth = bap.berths[self.berth_id].closing_time

        # set the first vessel start variable to either the closing time or the time the
        # first vessel arrives at this berth
        if len(self.vessels) == 0:  # and max(arrival_time, opening_time_berth) + duration <= closing_time_berth:
            return [max(arrival_time, opening_time_berth)]
        if duration > 199:
            return []

        times_set = set(range(max(arrival_time, opening_time_berth), closing_time_berth))
        sorted_vessels = sorted(self.vessels, key=lambda x: x[1])
        _, v_1_start_, _ = sorted_vessels[0]
        if max(arrival_time, opening_time_berth) + duration < v_1_start_:
            return [max(arrival_time, opening_time_berth)]

        for i in range(len(sorted_vessels)):
            y = i
            if i < len(sorted_vessels) - 1:
                y = i + 1
            (v_1_id, v_1_start, v_1_duration) = sorted_vessels[i]
            (v_2_id, v_2_start, v_2_duration) = sorted_vessels[y]
            # Check if we can fit in front
            v_occupied = set(range(v_1_start, v_1_start + v_1_duration))
            times_set = times_set.difference(v_occupied)
            if arrival_time + duration > v_1_start:
                v_occupied = set(range(arrival_time, v_1_start + v_1_duration))
                times_set = times_set.difference(v_occupied)

            if arrival_time < v_1_start + v_1_duration:
                v_occupied = set(range(arrival_time, v_1_start + v_1_duration))
                times_set = times_set.difference(v_occupied)

            if v_2_start - v_1_start - v_1_duration < duration:
                v_occupied = set(range(arrival_time, v_2_start + v_2_duration))
                times_set = times_set.difference(v_occupied)

        return list(times_set)

    def __str__(self):
        return str(self.vessels)

    def __repr__(self):
        return f"BerthAssignment({self.berth_id}, {self.vessels})"


class Solution:
    __new_id = 0

    def __init__(self, nr_berths, assignment=None):
        if assignment is None:
            self.assignment = [BerthAssignment(i) for i in range(nr_berths)]
        else:
            self.assignment = assignment
        self.id = Solution.__new_id
        Solution.__new_id += 1

    def find_vessel(self, vessel_id):
        for berth in self.assignment:
            if berth.contains_vessel(vessel_id):
                return berth.berth_id
        raise Exception("Vessel not found in solution")

    def __str__(self):
        returnstr = ""
        for berth in self.assignment:
            returnstr += str(berth.vessels) + "\n"
        return returnstr

    def __repr__(self):
        return f"Solution(nr_berths={len(self.assignment)}, assignment={[eval(repr(ba)) for ba in self.assignment]})"

    def __hash__(self):
        solstr = ""
        for ba in self.assignment:
            solstr += str(ba)
        return 31 * hash(solstr)

    def visualize(self, scen="NoScen", seed="NoSeed", its="NoIters", save=False):
        plt.figure(figsize=(5, 5), dpi=250)
        for y, berth in enumerate(self.assignment):
            for (id_, start, duration) in berth.vessels:
                plt.plot((start, start + duration), (y, y))
                plt.annotate(id_, (start, y + 0.1))
        plt.title("Vessel allocation per berth.")
        plt.xlabel("Time")
        plt.ylabel("Berth")
        plt.xlim((0, 250))
        plt.ylim((-1, 13))
        if save:
            plt.savefig(fname=f"figures/scn_{scen}_seed_{seed}_its_{its}.png", dpi=250)


class BerthAllocationProblem:
    def __init__(self, vessels, berths):
        self.vessels = vessels
        self.berths = berths

    @classmethod
    def from_file(cls, filename):
        scenario = []
        with open(filename) as inputFile:
            lines = inputFile.readlines()
            for line in lines:
                b = np.fromstring(line, dtype=float, sep=' ')
                scenario.append(b.tolist())

        nr_vessels = int(scenario[0][0])
        nr_berths = int(scenario[1][0])
        arrival_times_vessels = scenario[2]
        opening_times_berths = scenario[3]
        handling_times_vessels = scenario[4:4 + nr_vessels]
        closing_times_berths = scenario[4 + nr_vessels]
        closing_time_vessels = scenario[5 + nr_vessels]
        cost_per_unit_vessel = scenario[6 + nr_vessels]

        st_arr = False
        st_hand = False

        if st_arr:
            for id_, vessel in enumerate(arrival_times_vessels):
                arrival_times_vessels[id_] += random.randint(2, 5)

        if st_hand:
            for berth in range(nr_berths):
                for vessel in range(len(handling_times_vessels)):
                    if handling_times_vessels[vessel][berth] != 200:
                        handling_times_vessels[vessel][berth] += random.randint(1, 7)

        vessels = [Vessel(arrival_time=int(arrival_times_vessels[vessel]),
                          handling_time=[int(time) for time in handling_times_vessels[vessel]],
                          closing_time=int(closing_time_vessels[vessel]),
                          cost_unit_time=float(cost_per_unit_vessel[vessel])) for vessel in range(nr_vessels)]
        berths = [Berth(opening_time=int(opening_times_berths[berth]), closing_time=int(closing_times_berths[berth]))
                  for berth in range(nr_berths)]

        return cls(vessels, berths)

    def fcfs(self):
        sorted_vessels = sorted(self.vessels, key=operator.attrgetter("arrival_time"))
        sol = Solution(len(self.berths))
        for vessel in sorted_vessels:
            times_berths = []
            earliest_time = 999999
            for berth in sol.assignment:
                if vessel.handling_time[berth.berth_id] >= 200:
                    times_berths.append(99999)
                    continue
                earliest_time = berth.get_available(arrival_time=vessel.arrival_time,
                                                    duration=vessel.handling_time[berth.berth_id], bap=self)

                if len(earliest_time) == 0:
                    earliest_time = 9999
                    times_berths.append(earliest_time)
                else:
                    earliest_time = earliest_time[0]
                    times_berths.append(earliest_time)
            best_berth = times_berths.index(min(times_berths))
            best_time = min(times_berths)

            sol.assignment[best_berth].add_vessel(vessel_id=vessel.id, starting_time=best_time,
                                                  duration=vessel.handling_time[best_berth])
        return sol

    def pr_time_window(self):
        sorted_vessels = sorted(self.vessels, key=operator.attrgetter("time_window"))
        sol = Solution(len(self.berths))
        num_vessels = len(sorted_vessels)
        for _ in range(num_vessels):
            if len(sorted_vessels) >= 10:
                rnd = random.randint(0, 9)
            elif len(sorted_vessels) >= 2:
                rnd = random.randint(0, 1)
            else:
                rnd = 0

            selected_vessel = sorted_vessels.pop(rnd)

            times_berths = []
            earliest_time = 999999
            for berth in sol.assignment:
                if selected_vessel.handling_time[berth.berth_id] >= 200:
                    times_berths.append(9999)
                    continue
                earliest_time = berth.get_available(arrival_time=selected_vessel.arrival_time,
                                                    duration=selected_vessel.handling_time[berth.berth_id], bap=self)

                if len(earliest_time) == 0:
                    earliest_time = 9999
                    times_berths.append(earliest_time)
                else:
                    earliest_time = earliest_time[0]
                    times_berths.append(earliest_time)

            best_berth = times_berths.index(min(times_berths))
            best_time = min(times_berths)
            sol.assignment[best_berth].add_vessel(vessel_id=selected_vessel.id, starting_time=best_time,
                                                  duration=selected_vessel.handling_time[best_berth])
        return sol

    def __str__(self):
        vessels_str = [str(vessel) for vessel in self.vessels]
        berths_str = [str(berth) for berth in self.berths]
        return f"Vessels: {vessels_str} \n Berths: {berths_str}"


if __name__ == "__main__":
    sol = Solution(13)
    print(sol)
    print(hash(sol))
