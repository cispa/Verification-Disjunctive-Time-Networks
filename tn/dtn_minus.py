import time

from typing import Dict, Tuple, List
from dbm.bound import *
from dbm.dbm import *
from dbm.dbm_global import *
from tn.ta import *
from tn.min_reach_time import *


class DTNMinus:
    def __init__(self, ta: 'TA') -> None:
        self.ta = ta

        self.extra_m = ta.get_extrapolation_m()

        max = 0
        for b in get_min_reach_times(ta).values():
            if b.get_value_abs() > max and not b.is_unbounded():
                max = b.get_value_abs()

        self.extra_delta = max * (ta.get_n_location_guards() + 1)
        self.__executed = False

        self.W = []
        self.P = []

        for s in ta.init_states:
            d = DBMGlobal(copy.copy(ta.clocks))
            if s in ta.invariants:
                d.and_constr(ta.invariants[s])
            self.W.append((s, copy.deepcopy(d)))
            self.P.append((s, d))

        self.min_reach = {}
        self.visited = {}
        self.min_reach_zones = {}

        for q in self.ta.locations:
            self.min_reach[q] = Bound.unbounded()
            self.min_reach_zones[q] = []
            self.visited[q] = False
        self.min_reach["empty"] = Bound.less_equal(0)

    def get_min_reach_time(self) -> Dict[str, int]:
        """get_min_reach_time returns the minimal reach time for each location. inf indicates an unreachable location."""
        if not self.__executed:
            self.__on_the_fly_algo()
        min = {}
        for location in self.ta.locations:
            min[location] = self.min_reach[location].get_value_abs()
        return min

    def get_summary_automaton(self) -> Tuple['TA', Dict[str, 'DBMGlobal']]:
        """get_summary_automaton returns the automaton where location guards are replaced by global clock guards"""
        if not self.__executed:
            self.__on_the_fly_algo()

        ta = copy.deepcopy(self.ta)
        transitions = ta.transitions

        for t in transitions:
            if ("loc_guard" in t) and (t["loc_guard"] != "empty"):
                t["clock_guard"].append(Constraint(
                    "0", "delta", self.min_reach[t["loc_guard"]]))
                t["loc_guard"] = "empty"

        ta.transitions = transitions

        return (ta, self.min_reach_zones)

    def get_execution_time(self) -> float:
        if not self.__executed:
            self.__on_the_fly_algo()
        return self.execution_time

    def __dependent_transitions(self, locationGuard: str) -> List[str]:
        """dependent_transitions returns the transitions that depend on the \
            given location through a guard"""
        dependent_transition = []
        for key in self.ta.transitions.keys():
            transition = self.ta.transitions[key]

            if (transition["loc_guard"] == locationGuard):
                dependent_transition.append(transition)
        return dependent_transition

    def __successor(self, zone: 'DBMGlobal',  transition: Dict[str, str]) -> 'DBMGlobal':
        """successor computes the successor of a transition"""
        loc_guard = transition["loc_guard"]

        replacement_constr = []
        if loc_guard in self.ta.locations:
            replacement_constr = [Constraint(
                "0", "delta", self.min_reach[loc_guard])]

        successor_zone = self.ta.successor(
            zone, transition, replacement_constr)
        successor_zone.extrapolate(self.extra_m, self.extra_delta)
        return successor_zone

    def __updateInformation(self, locationGuard: str, newMinReachTime: 'Bound') -> None:
        """updateInformation updates reachability for all given locations that \
            have a location guard depending on the given location"""
        self.min_reach[locationGuard] = newMinReachTime

        for transition in self.__dependent_transitions(locationGuard):

            for index in range(len(self.P)):
                source_location = self.P[index][0]
                source_zone = self.P[index][1]

                if source_location == transition["source_loc"]:
                    successor_zone = self.__successor(
                        source_zone, transition)
                    successor_node = (
                        transition["target_loc"], successor_zone)
                    if successor_node not in self.P:
                        self.W.append(successor_node)
                        self.P.append(successor_node)
                        # sort by minimum global reach time
                        self.W = sorted(self.W, key=lambda x: x[1])
                        self.P = sorted(self.P, key=lambda x: x[1])

    def __add_successors(self, sourceLocation: str, sourceZone: 'DBMGlobal') -> None:
        """addSuccessors computes and adds all possible successors for a given """
        sourceZone.canonicalize()
        for (_, t) in self.ta.transitions.items():
            t_source_loc = t["source_loc"]
            t_target_location = t["target_loc"]

            if t_source_loc == sourceLocation:
                loc_guard = t["loc_guard"]

                if loc_guard != "empty" and self.visited[loc_guard] == False:
                    continue
                else:
                    successor_zone = self.__successor(
                        sourceZone, t)

                    successor_node = (t_target_location, successor_zone)

                    if successor_node not in self.P:
                        self.P.append(successor_node)
                        self.W.append(successor_node)
                        # sort by minimum global reach time
                        self.W = sorted(self.W, key=lambda x: x[1])
                        self.P = sorted(self.P, key=lambda x: x[1])

    def __on_the_fly_algo(self) -> None:
        start_time = time.process_time()
        self.__executed = True
        while len(self.W) != 0:
            (location, zone) = self.W.pop(0)

            if zone is not None and zone.is_not_empty():
                self.visited[location] = True
                new_min_reach_bound = zone.get_min_global_bound()

                if new_min_reach_bound == self.min_reach[location]:
                    self.min_reach_zones[location].append(copy.deepcopy(zone))

                # Update if we have a smaller global minimum reach time
                if self.min_reach[location] == Bound.unbounded() \
                        or (self.min_reach[location].get_value_abs() > new_min_reach_bound.get_value_abs()):
                    self.min_reach_zones[location] = [copy.deepcopy(zone)]
                    self.__updateInformation(location, new_min_reach_bound)

                self.__add_successors(location, zone)

        end_time = time.process_time()
        self.execution_time = end_time - start_time
        print("\t Summary automaton construction took {}".format(self.execution_time))
