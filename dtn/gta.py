""" This module contains all functionality of for guarded timed automata
"""

# !FIXME:
#   - less redundancy in input parameters
#   - rework the transition / invariant format
#   - check all implicit assertions between lists (e.g. name of
#     locations in a transition exist)
#   - parse transitions from a file based representation (similar to
#     UPPAAL ?)

import math
import copy

from typing import List, Dict, Optional, Union
from dataclasses import dataclass

from dbm.dbm import Constraint
from dbm.dbm_global import DBMG


@dataclass
class GTATransition:
    """
    Representation of a transition in a GTA.
    """

    source_loc: str
    target_loc: str
    reset_clocks: List[str]
    clock_guard: List["Constraint"]
    loc_guard: Optional[str]


def to_gta_transitions(
    trans_dict: Dict[str, Dict[str, Union[str, List[str], List["Constraint"]]]]
) -> Dict[str, GTATransition]:
    """Conversion function from Dict representation"""
    parsed_transitions = {}
    for name, trans in trans_dict.items():
        source_loc = trans["source_loc"]
        assert isinstance(source_loc, str)

        target_loc = trans["target_loc"]
        assert isinstance(target_loc, str)

        reset_clocks: List[str] = trans.get("reset_clocks", [])  # type: ignore

        clock_guard: List["Constraint"] = trans.get("clock_guard", [])  # type: ignore

        loc_guard = trans.get("loc_guard", None)
        if loc_guard in ["empty", ""]:
            loc_guard = None

        parsed_transitions[name] = GTATransition(
            source_loc,
            target_loc,
            reset_clocks,  # type: ignore
            clock_guard,  # type: ignore
            loc_guard,  # type: ignore
        )
    return parsed_transitions


class GTA:
    """Guarded Timed Automaton (GTA) represents a guarded timed automaton
    template.

    Attributes:
        locations (List[str]): The list of locations of the GTA
        init_states (List[str]): The list of initial states of the GTA (must
            be contained in `locations`)
        transitions (Dict[str, "GTATransition"]):
            A Dict containing all transitions of the GTA with a unique name
        invariants (Dict[str, "Constraint"]): specifies possible location
            invariants. Format:
                Key (str): location name
                Value ("Constraint"): clock constraint
    """

    def __init__(
        self,
        locations: List[str],
        init_states: List[str],
        transitions: Dict[str, "GTATransition"],
        invariants: Dict[str, "Constraint"],
        clocks: Optional[List[str]] = None,
    ):
        """Initialize a guarded timed automaton (GTA)

        Args:
            locations (List[str]): The list of locations of the GTA
            inti_states (List[str]): The list of initial states of the GTA
                (must be contained in `locations`)
            transitions (Dict[str, GTATransition]):
                    A Dict containing all transitions of the GTA
            invariants (Dict[str, "Constraint"]): specifies possible
                location invariants
            Format:
                Key (str): location name
                Value ("Constraint"): clock constraint
        """
        self.transitions = transitions
        self.locations = locations
        self.invariants = invariants
        self.init_states = init_states

        if clocks:
            self.clocks = clocks
        else:
            # Default: single clock "x"
            self.clocks = ["x"]
        # index for transitions because of legacy input format
        self.__transition_index: Optional[Dict[str, List[str]]] = None

    def successor(
        self,
        zone: "DBMG",
        transition: "GTATransition",
        add_constr: Optional[List["Constraint"]] = None,
    ) -> "DBMG":
        """Computes the successor DBM for a given DBM.

        Args:
            zone ("DBM"): The current zone for which to compute the
                successor
            transition ("Dict[str, Union[str,
                List[str], List["Constraint"]]]"):
                    The transition that is taken.
            add_constr (Optional[List["Constraint"]] ): Can currently be
                used to pass an inferred replacement clock guard.

        Returns:
            successor zone
        """
        # TODO: better handling of zone copies
        zone = copy.deepcopy(zone)

        constraints = transition.clock_guard
        if add_constr is not None:
            assert isinstance(constraints, List)
            constraints += add_constr

        for constraint in constraints:
            zone.and_constr(constraint)

        zone.canonicalize()

        zone.reset(transition.reset_clocks)
        zone.delay()

        if transition.target_loc in self.invariants:
            zone.and_constr(self.invariants[transition.target_loc])

        zone.canonicalize()

        return zone

    def get_transitions_for_state(self, loc: str) -> List[str]:
        """Returns the names of all transitions from the given location

        Args:
            loc (str): The location to get the transitions for.
        """
        self.__index_transitions()
        assert isinstance(self.__transition_index, Dict)

        if loc in self.__transition_index:
            return self.__transition_index[loc]
        else:
            return []

    def get_trails_for_state(self, loc: str) -> List[List[str]]:
        """Returns all trails starting in location loc.

        A trail is a cycle which only contains a repetition of the first
        and last state. They are used to check the existence of a flooding
        path.

        Args:
            loc (str): location to get the transitions for

        Returns:
            list of trails
        """
        self.__index_transitions()
        assert isinstance(self.__transition_index, Dict)
        trails: List[List[str]] = []

        if loc not in self.__transition_index:
            return trails

        for t_name in self.__transition_index[loc]:
            trails += self.__compute_trail(
                t_name, self.transitions[t_name], loc, {t_name}
            )

        for x in trails:
            x.reverse()

        return trails

    def get_max_clock_guard(self) -> int:
        """Returns the maximal constant appearing on a clock guard in the
        automaton

        Returns:
            maximal value appearing in a clock guard
        """
        curr_max = 0

        for trans in self.transitions:
            for guard in self.transitions[trans].clock_guard:
                if (
                    guard.get_bound().get_value_abs() > curr_max
                    and guard.get_bound().get_value_abs() != math.inf
                ):
                    curr_max = guard.get_bound().get_value_abs()

        for guard in self.invariants.values():
            if (
                guard.get_bound().get_value_abs() > curr_max
                and guard.get_bound().get_value_abs() != math.inf
            ):
                curr_max = guard.get_bound().get_value_abs()
        return curr_max

    def get_guarding_locations(self) -> set[str]:
        """Returns the locations that appear in a location guards

        Returns:
            set of locations appearing in a location guard
        """
        state = set([])
        for _, trans in self.transitions.items():
            if trans.loc_guard is not None:
                state.add(trans.loc_guard)

        return state

    def get_n_location_guards(self) -> int:
        """Returns the number of location guards

        Returns:
            number of location guards
        """
        return len(self.get_guarding_locations())

    def __index_transitions(self) -> None:
        """index all transitions by source location"""
        if self.__transition_index is None:
            transition_index: Dict[str, List[str]] = {}
            for name, trans in self.transitions.items():
                if trans.source_loc in transition_index:
                    transition_index[trans.source_loc].append(name)
                else:
                    transition_index[trans.source_loc] = [name]
            self.__transition_index = transition_index

    def __compute_trail(
        self,
        transition_name: str,
        transition: GTATransition,
        starting_state: str,
        visited: set[str],
    ) -> List[List[str]]:
        """compute all possible trails"""
        self.__index_transitions()
        assert isinstance(self.__transition_index, Dict)

        if transition.target_loc == starting_state:
            return [[transition_name]]

        visited = visited.union({transition_name})
        possible_transitions = filter(
            lambda x: x not in visited, self.__transition_index[transition.target_loc]
        )

        trails = []
        for t_name in possible_transitions:
            trail_suffix = self.__compute_trail(
                t_name, self.transitions[t_name], starting_state, visited
            )

            for t in trail_suffix:
                t.append(transition_name)

            trails += trail_suffix

        return trails
