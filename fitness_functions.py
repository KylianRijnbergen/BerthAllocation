import sys


def get_total_cost(solution, bap):
    cost = 0
    if isinstance(solution, bool):
        return sys.maxsize
    for berth in solution.assignment:
        for vessel in berth.vessels:
            (id_, start, duration) = vessel
            arrival = bap.vessels[id_].arrival_time
            time_cost = bap.vessels[id_].cost_unit_time
            cost += time_cost * (start + duration - arrival)
    return cost


def get_total_cost_with_penalty(solution, bap):
    cost = 0
    if isinstance(solution, bool):
        return sys.maxsize
    for berth in solution.assignment:
        for vessel in berth.vessels:
            (id_, start, duration) = vessel
            if start + duration > bap.vessels[id_].closing_time:
                arrival = bap.vessels[id_].arrival_time
                time_cost = bap.vessels[id_].cost_unit_time
                cost += time_cost * (start + duration - arrival) + 25 * (
                            start + duration - bap.vessels[id_].closing_time) + 450
            else:
                arrival = bap.vessels[id_].arrival_time
                time_cost = bap.vessels[id_].cost_unit_time
                cost += time_cost * (start + duration - arrival)
    return cost


def get_makespan(solution, bap):
    highest_makespan = -1
    for berth in solution.assignment:
        for vessel in berth.vessels:
            (v_id, v_start, v_duration) = vessel
            if v_start + v_duration > highest_makespan:
                highest_makespan = v_start + v_duration
    return highest_makespan


def get_utilizations(solution, bap):
    utilizations = []
    for berth in solution.assignment:
        open_window = bap.berths[berth.berth_id].closing_time - bap.berths[berth.berth_id].opening_time
        used_window = 0
        for vessel in berth.vessels:
            (v_id, v_start, v_duration) = vessel
            used_window += v_duration
        utilizations.append(used_window / open_window)
    return utilizations
