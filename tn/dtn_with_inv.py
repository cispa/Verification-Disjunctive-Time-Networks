import time
import math

from dbm.dbm_global import DELTA
from tn.ta import *
from tn.dtn_minus import *


class DTNWithInv:
    """DTNWithInvariants checks whether all """

    def __init__(self, ta: 'TA') -> None:
        assert len(ta.clocks) == 1, "DTNWithInv only supports a single clock!"
        self.locations_to_check = ta.get_guarding_locations()
        self.summary_a = DTNMinus(ta)
        ta, minZone = self.summary_a.get_summary_automaton()
        self.summary_construction_time = self.summary_a.get_execution_time()
        self.ta = ta
        self.minZone = minZone
        self.w_q = {}
        self.cutoff = math.inf
        self.checked = False
        self.summary_valid = True

    def get_min_reach_time(self) -> Dict[str, int]:
        """get_min_reach_time returns the minimal reach time for each location, if a lasso could not be found for a location it returns None"""
        if self.check_valid_summary_automaton():
            return self.summary_a.get_min_reach_time()
        else:
            None

    def get_summary_automaton(self) -> Tuple['TA', Dict[str, 'DBMGlobal']]:
        """get_summary_automaton returns the automaton where location guards are replaced by global clock guards.  If a lasso could not be found for a location it returns None"""
        if self.check_valid_summary_automaton():
            return self.summary_a.get_summary_automaton()
        else:
            None

    def check_valid_summary_automaton(self):
        """check_valid_summary_automaton will first create a summary automaton \
            and then check whether all locations that need to be flooded are \
            indeed floodable"""
        if self.checked:
            return self.summary_valid

        start_time = time.process_time()

        to_check = self.locations_to_check

        for l in to_check:
            if not self.__can_be_flooded(l):
                print(
                    "Could not find lasso for location {}.\
                        Summary Automaton is invalid!".format(l))
                self.summary_valid = False
                return False

        cutoff = 1
        for w in self.w_q.values():
            cutoff += w
        self.cutoff = cutoff

        print("\t Cutoff {}".format(cutoff))

        end_time = time.process_time()
        self.lasso_check_time = end_time - start_time
        print("\t Checking for lassos in the summary automaton took {}".format(
            self.lasso_check_time))

        self.summary_valid = True
        return True

    def get_execution_time(self) -> float:
        return self.summary_construction_time + self.lasso_check_time

    def __can_be_flooded(self, state: str):
        """can_be_flooded checks whether state state can be flooded"""
        trails = self.ta.get_trails_for_state(state)
        for trail in trails:
            psi_1, psi_2, psi_3 = self.__split_trail(trail)
            T = self.__compute_T(psi_1)

            for zone in self.minZone[state]:
                v_x_before = zone.get_min_bound_on_clock("x").get_value_abs()
                # clock valuations from prefix
                (d, t_1) = self.__compute_delta(psi_1, zone)
                (d, t_2) = self.__compute_delta(psi_2, d)
                (d, t_3) = self.__compute_delta(psi_3, zone)

                v_x = zone.get_min_bound_on_clock("x").get_value_abs()

                if (T >= (t_1 + t_2 + t_3 + v_x)) and (T > t_3) and (v_x == v_x_before):
                    # Check if lasso was a valid automaton run
                    if d.is_not_empty():
                        self.w_q[state] = max(
                            math.ceil((T + t_2) / (T - t_3)), 2)
                        return True
        return False

    def __split_trail(self, trail: List[str]):
        """split_trail splits a trail into ψ_1, ψ_2 and ψ_3"""
        psi_1 = []
        i = 0
        for t in trail:
            i += 1
            psi_1.append(t)
            if "reset_clocks" in self.ta.transitions[t]:
                break

        trail = trail[i:]

        psi_3 = []
        j = len(trail)
        for t in reversed(trail):
            if "reset_clocks" in self.ta.transitions[t]:
                break
            j -= 1
            psi_3.append(t)

        psi_2 = trail[:j]

        return (psi_1, psi_2, psi_3)

    def __compute_T(self, psi_1: List[str]):
        """compute T based of ψ_1"""
        min = math.inf
        for t in psi_1:
            source = self.ta.transitions[t]["source_loc"]
            if source in self.ta.invariants:
                constr = self.ta.invariants[source]
                ok = constr.is_upper_bound()
                if ok:
                    if constr.get_bound().get_value() < min:
                        min = constr.get_bound().get_value()
        return min

    def __compute_delta(self, psi: List[str], start_zone: 'DBM'):
        """compute minimal δ(ψ) provided that the initial state can be reached \
            with zone start_zone"""
        start_d = start_zone.get_min_global_bound().get_value_abs()
        zone = start_zone

        for t in psi:
            zone = self.ta.successor(zone, self.ta.transitions[t])
            if not zone.is_not_empty:
                break

        end_d = zone.get_min_global_bound().get_value_abs()

        return zone, (end_d - start_d)
