""" This module implements the summary automaton for disjunctive time networks
    of the DTN^- class.

    !FIXME:
        - @PE rewrite this class for readability
"""

import time
import copy

from typing import Dict, Tuple, List

from dbm.bound import Bound, BoundType
from dbm.dbm import Constraint
from dbm.dbm_global import DBMG
from dtn.gta import GTA, GTATransition
from dtn.min_reach_time import get_min_reach_times


class DTNMinus:
    """DTNMinus implements the summary automaton construction for DTNs falling
    into the DTN^- class.

    Attributes:
        gta ("GTA"): The guarded timed automaton defining the DTN.
    """

    def __init__(self, gta: "GTA") -> None:
        """Initialize a DTNMinus.

        Args:
            gta ("GTA") : A guarded timed automaton that defines the DTN.
        """
        self.gta = gta

        self.max_clock_constr = gta.get_max_clock_guard()

        # Get the maximal reach time in the unguarded automaton
        max_reach_time: int = 0
        for b in get_min_reach_times(gta).values():
            if b.get_value_abs() > max_reach_time and not b.is_unbounded():
                max_reach_time = b.get_value_abs()

        # Compute exploration bound delta max
        self.delta_max = max_reach_time * (gta.get_n_location_guards() + 1)
        self.__executed = False

        self.__waiting_set: List[Tuple[str, DBMG]] = []
        self.__processing_set: List[Tuple[str, DBMG]] = []

        for s in gta.init_states:
            d = DBMG(copy.copy(gta.clocks))
            if s in gta.invariants:
                d.and_constr(gta.invariants[s])
            self.__waiting_set.append((s, copy.deepcopy(d)))
            self.__processing_set.append((s, d))

        self.min_reach: Dict[str, "Bound"] = {}
        self.visited: Dict[str, bool] = {}
        self.min_reach_zones: Dict[str, List["DBMG"]] = {}

        for q in self.gta.locations:
            self.min_reach[q] = Bound.unbounded()
            self.min_reach_zones[q] = []
            self.visited[q] = False
        self.min_reach["empty"] = Bound.leq(0)

    def get_min_reach_time(self) -> Dict[str, int]:
        """Returns the minimal reach time for each location, inf indicates an
        unreachable location.

        Returns:
            a dict mapping location name to minimal reachability times
        """
        if not self.__executed:
            self.__minreach_algorithm()
        min_reach_times: Dict[str, int] = {}
        for location in self.gta.locations:
            min_reach_times[location] = self.min_reach[location].get_value_abs()
        return min_reach_times

    def get_summary_automaton(self) -> Tuple["GTA", Dict[str, List["DBMG"]]]:
        """Returns the automaton where location guards are replaced by global
        clock guards

        Returns:
            an updated GTA without location guards and the zones
            corresponding to the minimal reach time
        """
        if not self.__executed:
            self.__minreach_algorithm()

        gta = copy.deepcopy(self.gta)

        # Replace location guards by a min reach constraint
        for _, trans in gta.transitions.items():
            if trans.loc_guard is not None:
                min_reach_constr = Constraint(
                    "0", "delta", self.min_reach[trans.loc_guard]
                )
                trans.clock_guard.append(min_reach_constr)
                trans.loc_guard = None

        return (gta, self.min_reach_zones)

    def get_execution_time(self) -> float:
        if not self.__executed:
            self.__minreach_algorithm()
        return self.execution_time

    def __dependent_transitions(self, loc_guard: str) -> List["GTATransition"]:
        """Computes the transitions that depend on the given location through a
        location guard

        Arg:
            loc_guard (str): location to find the dependent transitions for

        Returns:
            list of transition names
        """
        dependent_transition: List["GTATransition"] = []
        for _, trans in self.gta.transitions.items():
            if trans.loc_guard == loc_guard:
                dependent_transition.append(trans)

        return dependent_transition

    def __successor(self, zone: "DBMG", transition: "GTATransition") -> "DBMG":
        """Computes the successor of a transition

        Attr:
            zone ("DBMGlobal"): current zone
            transition ("GTATransition): transition fo which to compute
                the successor

        Returns:
            successor zone
        """
        replacement_constr = []
        if transition.loc_guard in self.gta.locations:
            replacement_constr = [
                Constraint("0", "delta", self.min_reach[transition.loc_guard])
            ]

        successor_zone = self.gta.successor(zone, transition, replacement_constr)
        successor_zone.extrapolate(self.max_clock_constr, self.delta_max)
        return successor_zone

    def __update_information(self, loc: str, new_min_reach_time: "Bound") -> None:
        """Updates reachability for all given locations that have a location
        guard depending on the given location

        Attr:
            loc (str): location for which the new min reach time has been
                found
            new_min_reach_time ("Bound"): new bound on minimal reach time
        """
        self.min_reach[loc] = new_min_reach_time

        for trans in self.__dependent_transitions(loc):
            for index in range(len(self.__processing_set)):
                source_loc = self.__processing_set[index][0]
                source_zone = self.__processing_set[index][1]

                if source_loc == trans.source_loc:
                    successor_zone = self.__successor(source_zone, trans)
                    successor_node = (trans.target_loc, successor_zone)
                    if successor_node not in self.__processing_set:
                        self.__waiting_set.append(successor_node)
                        self.__processing_set.append(successor_node)
                        # sort by minimum global reach time
                        self.__waiting_set = sorted(
                            self.__waiting_set, key=lambda x: x[1]
                        )
                        self.__processing_set = sorted(
                            self.__processing_set, key=lambda x: x[1]
                        )

    def __add_successors(self, source_loc: str, source_zone: "DBMG") -> None:
        """Computes and adds all possible successors for a given location and
        adds them to the wait sets

        Attr:
            source_loc (str): location for which to compute all successors
            source_zone ("DBMGlobal"): zone with which location has been
                reached
        """
        source_zone.canonicalize()
        for _, trans in self.gta.transitions.items():
            if trans.source_loc == source_loc:
                if trans.loc_guard is not None:
                    if not self.visited[trans.loc_guard]:
                        continue

                successor_zone = self.__successor(source_zone, trans)

                successor_node = (trans.target_loc, successor_zone)

                if successor_node not in self.__processing_set:
                    self.__processing_set.append(successor_node)
                    self.__waiting_set.append(successor_node)
                    # sort by minimum global reach time
                    self.__waiting_set = sorted(self.__waiting_set, key=lambda x: x[1])
                    self.__processing_set = sorted(
                        self.__processing_set, key=lambda x: x[1]
                    )

    def __minreach_algorithm(self) -> None:
        """This is the main algorithm loop for computing MINREACH as described
        in the paper (Algorithm 1)
        """
        start_time = time.process_time()
        self.__executed = True
        while len(self.__waiting_set) != 0:
            (location, zone) = self.__waiting_set.pop(0)

            if zone is not None and zone.is_not_empty():
                self.visited[location] = True
                new_min_reach_bound = zone.get_min_global_bound()

                if new_min_reach_bound == self.min_reach[location]:
                    self.min_reach_zones[location].append(copy.deepcopy(zone))

                # Update if we have a smaller global minimum reach time
                if self.min_reach[location] == Bound.unbounded() or (
                    self.min_reach[location].get_value_abs()
                    > new_min_reach_bound.get_value_abs()
                ):
                    self.min_reach_zones[location] = [copy.deepcopy(zone)]
                    self.__update_information(location, new_min_reach_bound)

                self.__add_successors(location, zone)

        end_time = time.process_time()
        self.execution_time = end_time - start_time
        print(f"\t Summary automaton construction took {self.execution_time}")

    def print_min_reach_times(self) -> None:
        """Prints the computed minimal global time to reach each location"""

        if not self.__executed:
            self.__minreach_algorithm()

        print("\t MINREACH results: ")
        for loc_name, bound in self.min_reach.items():
            if loc_name == "empty":
                # TODO: fix this by removing all occurrences, should not be
                # needed anymore
                continue

            if bound.ty == BoundType.LEQ:
                print(f"\t\t{loc_name} : ≥ {bound.get_value_abs()}")
            else:
                print(f"\t\t{loc_name} : ≥ {bound.get_value_abs()}")
