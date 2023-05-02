import unittest
from examples.example_tns import *
from tn.ta import *
from tn.dtn_with_inv import *
from dbm.constraint import *
from dbm.bound import *
from dbm.dbm_global import *


class TestDTNWithInv(unittest.TestCase):

    def test_compute_T(self):
        test_cases = [
            (TA(["q0", "q1", "q2", "q3"],
                ["q0"],
                {
                    "t0": {"source_loc": "q0", "clock_guard": [Constraint("0", "x", Bound.less_equal(-5))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q1"},
                    "t1": {"source_loc": "q1", "clock_guard": [], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q0"},
            }, {}),
                ["t0", "t1"],
                math.inf),
            (TA(["q0", "q1", "q2", "q3"],
                ["q0"],
                {
                    "t0": {"source_loc": "q0", "clock_guard": [Constraint("x", "0", Bound.less_equal(5))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q1"},
                    "t1": {"source_loc": "q1", "clock_guard": [], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q0"},
            },
                {"q0": Constraint("x", "0", Bound.less_equal(5))}),
                ["t0", "t1"], 5)
        ]
        # TODO: coverage
        for (ta, psi, expected) in test_cases:
            lc = DTNWithInv(ta)
            got = lc._DTNWithInv__compute_T(psi)
            self.assertEqual(got, expected)

    def test_split_trail(self):
        test_cases = [
            ({"t1": {"source_loc": "a", "target_loc": "b", "reset_clocks": ["x"], "clock_guard": []},
              "t2": {"source_loc": "b", "target_loc": "a", "clock_guard": []}},
             ["t1", "t2"], (["t1"], [], ["t2"])),
            ({"t1": {"source_loc": "a", "target_loc": "b", "reset_clocks": ["x"], "clock_guard": []},
              "t2": {"source_loc": "b", "target_loc": "c", "reset_clocks": ["x"], "clock_guard": []},
              "t3": {"source_loc": "c", "target_loc": "a", "clock_guard": []}},
             ["t1", "t2", "t3"], (["t1"], ["t2"], ["t3"]))
        ]
        for (transitions, trail, expected_psis) in test_cases:
            lc = DTNWithInv(TA({}, [], transitions, {}))
            got = lc._DTNWithInv__split_trail(trail)
            self.assertEqual(got, expected_psis)

    def test_check_valid_summary_automaton_luca_3(self):
        alg = DTNWithInv(example_3_ta)
        self.assertEqual(alg.check_valid_summary_automaton(), True)
        self.assertEqual(alg.cutoff, 7)

    def test_check_valid_summary_automaton_luca_4(self):
        alg = DTNWithInv(example_4_ta)
        self.assertEqual(alg.check_valid_summary_automaton(), True)
        self.assertEqual(alg.cutoff, 9)
