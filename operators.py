from solutions import Solution, BerthAssignment


def move(starting_sol, vessel_id, new_berth_id, bap):
    # create copy of solution
    candidate_solution = eval(repr(starting_sol))
    # remove vessel from current berth
    for berth in candidate_solution.assignment:
        if berth.contains_vessel(vessel_id):
            berth.remove_vessel(vessel_id)

    # Get duration of vessel in new berth
    duration = bap.vessels[vessel_id].handling_time[new_berth_id]
    # Get arrival time of vessel
    arrival_time = bap.vessels[vessel_id].arrival_time

    placement_times = candidate_solution.assignment[new_berth_id].get_available(arrival_time, duration, bap)
    if len(placement_times) == 0:
        return False
    placement_time = placement_times[0]
    candidate_solution.assignment[new_berth_id].add_vessel(vessel_id, placement_time, duration)
    return candidate_solution

def swap(starting_sol, vessel_1_id, vessel_2_id, bap):
    placement_1 = -1
    placement_2 = -1
    new_berth_id_1 = starting_sol.find_vessel(vessel_2_id)
    new_berth_id_2 =  starting_sol.find_vessel(vessel_1_id)
    # create copy of solution
    candidate_solution = eval(repr(starting_sol))
    # remove vessel from current berth
    for berth in candidate_solution.assignment:            
        for (v_id, v_start, v_duration) in berth.vessels:
            if v_id == vessel_1_id:
               placement_1 = v_start
               berth.remove_vessel(vessel_1_id)
            if v_id == vessel_2_id:
                placement_2 = v_start 
                berth.remove_vessel(vessel_2_id)
    # Get duration of vessel in new berth
    duration_1 = bap.vessels[vessel_1_id].handling_time[new_berth_id_2]
    # Get arrival time of vessel
    arrival_time_1 = bap.vessels[vessel_1_id].arrival_time

        # Get duration of vessel in new berth
    duration_2 = bap.vessels[vessel_2_id].handling_time[new_berth_id_1]
    # Get arrival time of vessel
    arrival_time_2 = bap.vessels[vessel_2_id].arrival_time

    if duration_1 == 200 or duration_2 == 200:
        return False

    moving_vessels = []
    durations_vessels = []
    for (v_id, v_start, v_duration) in eval(repr(candidate_solution)).assignment[new_berth_id_1].vessels:
        if v_id == vessel_2_id:
            continue
        if v_start >= min(arrival_time_1, arrival_time_2):
            moving_vessels.append(v_id)
            durations_vessels.append(v_duration)
            candidate_solution.assignment[new_berth_id_1].remove_vessel(v_id)
        

    candidate_solution.assignment[new_berth_id_1].add_vessel(vessel_1_id, max(bap.berths[new_berth_id_1].opening_time, max(arrival_time_1, placement_2)), duration_1)

    for ind, vessel_move in enumerate(moving_vessels):
        placement_times = candidate_solution.assignment[new_berth_id_1].get_available(max(arrival_time_1, placement_2), durations_vessels[ind], bap)
        if len(placement_times) == 0:
            return False

        candidate_solution.assignment[new_berth_id_1].add_vessel(vessel_move, max(bap.vessels[vessel_move].arrival_time, placement_times[0]), durations_vessels[ind])

    moving_vessels = []
    durations_vessels = []
    for (v_id, v_start, v_duration) in eval(repr(candidate_solution)).assignment[new_berth_id_2].vessels:
        if v_id == vessel_1_id:
            continue
        if v_start >=  min(arrival_time_1, arrival_time_2):
            moving_vessels.append(v_id)
            durations_vessels.append(v_duration)
            candidate_solution.assignment[new_berth_id_2].remove_vessel(v_id)

    candidate_solution.assignment[new_berth_id_2].add_vessel(vessel_2_id, max(bap.berths[new_berth_id_2].opening_time, max(arrival_time_2, placement_1)), duration_2)

    for ind, vessel_move in enumerate(moving_vessels):
        placement_times = candidate_solution.assignment[new_berth_id_2].get_available(max(arrival_time_2, placement_1), durations_vessels[ind], bap)
        if len(placement_times) == 0:
            return False

        candidate_solution.assignment[new_berth_id_2].add_vessel(vessel_move, max(bap.vessels[vessel_move].arrival_time, placement_times[0]), durations_vessels[ind])

    return candidate_solution



