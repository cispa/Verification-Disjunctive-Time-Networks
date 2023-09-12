""" This module performs the minimal time computation on the unguarded automaton
"""

import copy
import time
import math

from dtn.gta import GTA
from dbm.dbm_global import DBMG, Bound


def get_min_reach_times(gta: "GTA"):
    """Computes the minimal reachability for each state in the *unguarded*
    automaton
    """
    start_time = time.process_time()
    min_reach = {}
    for loc in gta.locations:
        min_reach[loc] = Bound.unbounded()

    visited = []
    waiting = []
    for i in gta.init_states:
        d = DBMG(copy.deepcopy(gta.clocks))
        if i in gta.invariants:
            d.and_constr(gta.invariants[i])
        waiting.append((i, d))

    not_visited = set(gta.locations)

    m = gta.get_max_clock_guard()

    while (len(not_visited) > 0) and (len(waiting) > 0):
        (loc, zone) = waiting.pop(0)
        visited.append((loc, zone.get_dbm()))

        if loc in not_visited:
            not_visited.remove(loc)

        if zone.get_min_global_bound().get_value_abs() < min_reach[loc].get_value_abs():
            min_reach[loc] = zone.get_min_global_bound()

        for t in gta.get_transitions_for_state(loc):
            zone = gta.successor(zone, gta.transitions[t])
            zone.extrapolate(m, math.inf)  # type: ignore
            loc = gta.transitions[t].target_loc
            if (loc, zone.get_dbm()) not in visited:
                waiting.append((loc, zone))

        waiting = sorted(waiting, key=lambda x: x[1])

    end_time = time.process_time()
    print(f" \t Finding delta max took {end_time - start_time}s")
    return min_reach
