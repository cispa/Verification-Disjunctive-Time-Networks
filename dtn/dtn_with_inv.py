""" This module implements the summary automaton for general disjunctive time
    networks.
"""

import time
import math

from typing import Dict, Tuple, List, Optional

from dtn.gta import GTA, DBMG
from dtn.dtn_minus import DTNMinus


class DTNWithInv:
    """DTNWithInvariants implements the summary automaton construction and
    validity check for general DTNs
    """

    def __init__(self, gta: "GTA") -> None:
        assert len(gta.clocks) == 1, "DTNWithInv only supports a single clock!"
        self.locations_to_check = gta.get_guarding_locations()
        self.summary_a = DTNMinus(gta)
        self.gta, self.min_reach_zones = self.summary_a.get_summary_automaton()
        self.summary_construction_time = self.summary_a.get_execution_time()
        self.w_q: Dict[str, int] = {}
        self.cutoff = math.inf
        self.checked = False
        self.summary_valid = True

    def get_min_reach_time(self) -> Optional[Dict[str, int]]:
        """Returns the minimal reach time for each location, if a lasso could
        not be found for any location it returns None

        Returns:
            minimal reach time if lassos could be found, else None
        """
        if self.check_valid_summary_automaton():
            return self.summary_a.get_min_reach_time()

        return None

    def get_summary_automaton(self) -> Optional[Tuple["GTA", Dict[str, List["DBMG"]]]]:
        """Returns the automaton where location guards are replaced by global
        clock guards.  If a lasso could not be found for a location it
        returns None

        Returns:
            summary TA if lassos could be found, else None
        """
        if self.check_valid_summary_automaton():
            return self.summary_a.get_summary_automaton()

        return None

    def check_valid_summary_automaton(self):
        """This function will first create a summary automaton and then check
        whether all locations that need to be flooded are indeed floodable
        """
        if self.checked:
            return self.summary_valid

        start_time = time.process_time()

        to_check = self.locations_to_check

        for l in to_check:
            if not self.__can_be_flooded(l):
                print(
                    f"Could not find lasso for location {l}. Summary \
                    automaton is not valid!"
                )
                self.summary_valid = False
                return False

        cutoff = 1
        for w in self.w_q.values():
            cutoff += w
        self.cutoff = cutoff

        print(f"\t Cutoff {cutoff}")

        end_time = time.process_time()
        self.lasso_check_t = end_time - start_time
        print(f"\t Checking for lassos in summary automaton took {self.lasso_check_t}.")

        self.summary_valid = True
        return True

    def get_execution_time(self) -> float:
        return self.summary_construction_time + self.lasso_check_t

    def __can_be_flooded(self, state: str) -> bool:
        """Checks whether state state can be flooded

        Args:
            state (str): state fo which to check whether a lasso exists
        """
        trails = self.gta.get_trails_for_state(state)
        for trail in trails:
            psi_1, psi_2, psi_3 = self.__split_trail(trail)
            big_t = self.__compute_t(psi_1)

            for zone in self.min_reach_zones[state]:
                v_x_before = zone.get_min_bound_on_clock("x").get_value_abs()
                # clock valuations from prefix
                (d, d_1) = self.__compute_delta(psi_1, zone)
                (d, d_2) = self.__compute_delta(psi_2, d)
                (d, d_3) = self.__compute_delta(psi_3, zone)

                v_x = zone.get_min_bound_on_clock("x").get_value_abs()

                if (
                    (big_t >= (d_1 + d_2 + d_3 + v_x))
                    and (big_t > d_3)
                    and (v_x == v_x_before)
                ):
                    # Check if lasso was a valid automaton run
                    if d.is_not_empty():
                        self.w_q[state] = max(
                            math.ceil((big_t + d_2) / (big_t - d_3)), 2
                        )
                        return True
        return False

    def __split_trail(self, trail: List[str]) -> Tuple[List[str], List[str], List[str]]:
        """Splits a trail into ψ_1, ψ_2 and ψ_3

        Args:
            trails (List[str]): the trail to split

        Returns:
            tuple (ψ_1, ψ_2, ψ_3)
        """
        psi_1 = []
        i = 0
        for t in trail:
            i += 1
            psi_1.append(t)
            if len(self.gta.transitions[t].reset_clocks) > 0:
                break

        trail = trail[i:]

        psi_3 = []
        j = len(trail)
        for t in reversed(trail):
            if len(self.gta.transitions[t].reset_clocks) > 0:
                break
            j -= 1
            psi_3.append(t)

        psi_2 = trail[:j]

        return (psi_1, psi_2, psi_3)

    def __compute_t(self, psi_1: List[str]) -> int:
        """compute T based of ψ_1

        Returns
            T
        """
        min_t = math.inf
        for t in psi_1:
            source = self.gta.transitions[t].source_loc
            if source in self.gta.invariants:
                constr = self.gta.invariants[source]
                ok = constr.is_upper_bound()
                if ok:
                    if constr.get_bound().get_value() < min_t:
                        min_t = constr.get_bound().get_value()
        return min_t  # type: ignore

    def __compute_delta(self, psi: List[str], start_zone: "DBMG"):
        """compute minimal δ(ψ) provided that the initial state can be reached
        with zone start_zone
        """
        start_d = start_zone.get_min_global_bound().get_value_abs()
        zone = start_zone

        for t in psi:
            zone = self.gta.successor(zone, self.gta.transitions[t])
            if not zone.is_not_empty():
                break

        end_d = zone.get_min_global_bound().get_value_abs()

        return zone, (end_d - start_d)

    def print_min_reach_times(self) -> None:
        """Prints the computed minimal global time to reach each location"""

        if not self.check_valid_summary_automaton():
            print("Flooding construction failed. Results invalid!")
            return

        self.summary_a.print_min_reach_times()
