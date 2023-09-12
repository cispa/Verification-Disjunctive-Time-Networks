# type: ignore
""" Tests for DTN with invariants"""

# pylint: disable=protected-access

import unittest
import math

from examples.examples_dtns import example_3_ta, example_4_ta
from dtn.gta import GTA, to_gta_transitions
from dtn.dtn_with_inv import DTNWithInv
from dbm.constraint import Constraint
from dbm.bound import Bound


class TestDTNWithInv(unittest.TestCase):
    """Tests for DTNWithInv"""

    def test_compute_t(self):
        test_cases = [
            (
                GTA(
                    ["q0", "q1", "q2", "q3"],
                    ["q0"],
                    to_gta_transitions(
                        {
                            "t0": {
                                "source_loc": "q0",
                                "clock_guard": [Constraint("0", "x", Bound.leq(-5))],
                                "reset_clocks": [],
                                "loc_guard": "empty",
                                "target_loc": "q1",
                            },
                            "t1": {
                                "source_loc": "q1",
                                "clock_guard": [],
                                "reset_clocks": ["x"],
                                "loc_guard": "empty",
                                "target_loc": "q0",
                            },
                        }
                    ),
                    {},
                ),
                ["t0", "t1"],
                math.inf,
            ),
            (
                GTA(
                    ["q0", "q1", "q2", "q3"],
                    ["q0"],
                    to_gta_transitions(
                        {
                            "t0": {
                                "source_loc": "q0",
                                "clock_guard": [Constraint("x", "0", Bound.leq(5))],
                                "reset_clocks": [],
                                "loc_guard": "empty",
                                "target_loc": "q1",
                            },
                            "t1": {
                                "source_loc": "q1",
                                "clock_guard": [],
                                "reset_clocks": ["x"],
                                "loc_guard": "empty",
                                "target_loc": "q0",
                            },
                        }
                    ),
                    {"q0": Constraint("x", "0", Bound.leq(5))},
                ),
                ["t0", "t1"],
                5,
            ),
        ]
        # TODO: coverage
        for ta, psi, expected in test_cases:
            lc = DTNWithInv(ta)
            got = lc._DTNWithInv__compute_t(psi)
            self.assertEqual(got, expected)

    def test_split_trail(self):
        test_cases = [
            (
                {
                    "t1": {
                        "source_loc": "a",
                        "target_loc": "b",
                        "reset_clocks": ["x"],
                        "clock_guard": [],
                    },
                    "t2": {"source_loc": "b", "target_loc": "a", "clock_guard": []},
                },
                ["t1", "t2"],
                (["t1"], [], ["t2"]),
            ),
            (
                {
                    "t1": {
                        "source_loc": "a",
                        "target_loc": "b",
                        "reset_clocks": ["x"],
                        "clock_guard": [],
                    },
                    "t2": {
                        "source_loc": "b",
                        "target_loc": "c",
                        "reset_clocks": ["x"],
                        "clock_guard": [],
                    },
                    "t3": {"source_loc": "c", "target_loc": "a", "clock_guard": []},
                },
                ["t1", "t2", "t3"],
                (["t1"], ["t2"], ["t3"]),
            ),
        ]
        for transitions, trail, expected_psis in test_cases:
            lc = DTNWithInv(GTA({}, [], to_gta_transitions(transitions), {}))
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
