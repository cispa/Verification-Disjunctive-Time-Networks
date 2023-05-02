from tn.ta import *
from dbm.dbm_global import *
import copy
import time


def get_min_reach_times(ta: 'TA'):
    """Computes the minimal reachability for each state in the *unguarded* automaton"""
    start_time = time.process_time()
    min_reach = {}
    for loc in ta.locations:
        min_reach[loc] = Bound.unbounded()

    visited = []
    waiting = []
    for i in ta.init_states:
        d = DBMGlobal(copy.deepcopy(ta.clocks))
        if i in ta.invariants:
            d.and_constr(ta.invariants[i])
        waiting.append((i, d))

    not_visited = set(ta.locations)

    m = ta.get_extrapolation_m()

    while (len(not_visited) > 0) and (len(waiting) > 0):
        (loc, zone) = waiting.pop(0)
        visited.append((loc, zone.get_dbm()))

        if loc in not_visited:
            not_visited.remove(loc)

        if zone.get_min_global_bound().get_value_abs() < min_reach[loc].get_value_abs():
            min_reach[loc] = zone.get_min_global_bound()

        for t in ta.get_transitions_for_state(loc):
            zone = ta.successor(zone, ta.transitions[t])
            zone.extrapolate(m, math.inf)
            loc = ta.transitions[t]["target_loc"]
            if (loc, zone.get_dbm()) not in visited:
                waiting.append((loc, zone))

        waiting = sorted(waiting, key=lambda x: x[1])

    end_time = time.process_time()
    print(" \t Finding delta max took {}s".format(end_time - start_time))
    return min_reach
