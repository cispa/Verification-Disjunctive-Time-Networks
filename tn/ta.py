from typing import List

from dbm.dbm import *


class TA:
    """TA represents a timed automaton"""

    def __init__(self, locations, init_states, transitions, invariants, clocks=["x"]) -> None:
        self.transitions = transitions  # see transition dict in on_the_fly_algo
        self.locations = locations
        self.invariants = invariants
        self.init_states = init_states
        # TODO: infer clocks from above
        self.clocks = clocks
        self.__transition_index = None

    def successor(self, zone: 'DBM', transition, additional_constraints=None) -> 'DBM':
        """Computes the successor DBM for a given DBM. The parameter additonalConstraint can currently be used to pass an inferred replacement clock guard."""
        zone = copy.deepcopy(zone)

        constraints = transition["clock_guard"]
        if additional_constraints is not None:
            constraints += additional_constraints

        for constraint in constraints:
            zone.and_constr(constraint)

        zone.canonicalize()

        zone.reset(transition["reset_clocks"])
        zone.delay()

        if transition["target_loc"] in self.invariants:
            zone.and_constr(self.invariants[transition["target_loc"]])

        zone.canonicalize()

        return zone

    def get_transitions_for_state(self, state: str):
        self.___index_transitions()

        if state in self.__transition_index:
            return self.__transition_index[state]
        else:
            return []

    def get_trails_for_state(self, l: str) -> List[str]:
        """get_trails_for_state returns all trails starting in location l."""
        self.___index_transitions()
        trails = []

        if l not in self.__transition_index:
            return []

        for t_name in self.__transition_index[l]:
            trails += self.__compute_trail(
                t_name, self.transitions[t_name], l, {t_name})

        for x in trails:
            x.reverse()

        return trails

    def get_extrapolation_m(self) -> int:
        """get_extrapolation_m returns the maximal constant appearing on a clock guard in the automaton"""
        max = 0

        for t in self.transitions:
            for guard in self.transitions[t]["clock_guard"]:
                if guard.get_bound().get_value_abs() > max \
                        and guard.get_bound().get_value_abs() != math.inf:
                    max = guard.get_bound().get_value_abs()

        for guard in self.invariants.values():
            if guard.get_bound().get_value_abs() > max \
                    and guard.get_bound().get_value_abs() != math.inf:
                max = guard.get_bound().get_value_abs()
        return max

    def get_guarding_locations(self) -> List[str]:
        """get_guarding_locations returns the locations that are part of location guards"""
        state = set([])
        for (_, t) in self.transitions.items():
            if "loc_guard" in t:
                if t["loc_guard"] != "empty":
                    state.add(t["loc_guard"])
        return state

    def get_n_location_guards(self) -> int:
        """Returns the number of location guards"""
        guard_locations = set([])
        for t in self.transitions.values():
            if "loc_guard" in t:
                guard_locations.add(t["loc_guard"])
        return len(guard_locations)

    def ___index_transitions(self) -> None:
        """index all transitions by source location"""
        if self.__transition_index is None:
            transition_index = {}
            for (name, t) in self.transitions.items():
                if t["source_loc"] in transition_index:
                    transition_index[t["source_loc"]].append(name)
                else:
                    transition_index[t["source_loc"]] = [name]
            self.__transition_index = transition_index

    def __compute_trail(self, transition_name, transition, starting_state, visited):
        # part of trail computation
        if transition["target_loc"] == starting_state:
            return [[transition_name]]

        visited = visited.union({transition_name})
        possible_transitions = filter(
            lambda x: x not in visited,
            self.__transition_index[transition["target_loc"]]
        )

        trails = []
        for t_name in possible_transitions:
            trail_suffix = self.__compute_trail(
                t_name, self.transitions[t_name], starting_state, visited)

            for t in trail_suffix:
                t.append(transition_name)

            trails += trail_suffix

        return trails
