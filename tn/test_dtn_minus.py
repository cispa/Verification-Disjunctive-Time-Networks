import unittest
import math
from tn.ta import *
from tn.dtn_minus import *
from examples.example_tns import *
from examples.minreach_examples import *


class TestDTNMinus(unittest.TestCase):

    def test_algorithm(self):
        locations = ["q1", "q2", "q3", "q4", "q5", "q6", "q7"]
        init_states = ["q1"]
        invariants = {"q1": Constraint("x", "0", Bound.unbounded()),
                      "q2": Constraint("x", "0", Bound.unbounded()),
                      "q3": Constraint("x", "0", Bound.unbounded()),
                      "q4": Constraint("x", "0", Bound.unbounded()),
                      "q5": Constraint("x", "0", Bound.unbounded()),
                      "q6": Constraint("x", "0", Bound.unbounded()),
                      "q7": Constraint("x", "0", Bound.unbounded())}
        transitions = {"t1": {"source_loc": "q1", "clock_guard": [Constraint("0", "x", Bound.less_equal(-5))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q7"},
                       "t2": {"source_loc": "q1", "clock_guard": [Constraint("0", "x", Bound.less_equal(-3))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q2"},
                       "t3": {"source_loc": "q2", "clock_guard": [Constraint("0", "x", Bound.less_equal(-2))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q7"},
                       "t4": {"source_loc": "q1", "clock_guard": [Constraint("0", "x", Bound.less_equal(-2))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q3"},
                       "t5": {"source_loc": "q3", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "x", Bound.less_equal(-1))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q7"},
                       "t6": {"source_loc": "q3", "clock_guard": [Constraint("x", "0", Bound.unbounded())], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q4"},
                       "t7": {"source_loc": "q4", "clock_guard": [Constraint("0", "x", Bound.less_equal(-2))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q5"},
                       "t8": {"source_loc": "q5", "clock_guard": [Constraint("0", "x", Bound.unbounded())], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q3"},
                       "t9": {"source_loc": "q1", "clock_guard": [Constraint("x", "0", Bound.less_equal(4))], "reset_clocks": [], "loc_guard": "q7", "target_loc": "q6"}, }
        ta = TA(locations, init_states, transitions, invariants)
        algo = DTNMinus(ta)
        algo._DTNMinus__on_the_fly_algo()
        self.assertEqual(algo.get_min_reach_time(), {
                         "q1": 0, "q2": 3, "q3": 2, "q4": 2, "q5": 4,
                         "q6": math.inf, "q7": 5})

    def test_algorithm_example_1(self):
        algo = DTNMinus(example_1_ta)
        algo._DTNMinus__on_the_fly_algo()
        self.assertEqual(algo.get_min_reach_time(), {
                         "q1": 0, "q2": 5, "q3": 5, "q4": math.inf})

    def test_algorithm_example_2(self):
        algo = DTNMinus(example_2_ta)
        algo._DTNMinus__on_the_fly_algo()
        self.assertEqual(algo.get_min_reach_time(), {
                         "q1": 0, "q2": 0, "q3": 2, "q4": 5, "q5": 10, "q6": 10})

    def test_algorithm_example_3(self):
        algo = DTNMinus(example_3_ta)
        algo._DTNMinus__on_the_fly_algo()
        self.assertEqual(algo.get_min_reach_time(), {
                         "syH": 0, "syL": 2, "0H": 0, "1H": 2, "2H": 4, "0L": 2, "1L": 0, "2L": 1})

    def test_algorithm_example_4(self):
        algo = DTNMinus(example_4_ta)
        algo._DTNMinus__on_the_fly_algo()
        self.assertEqual(algo.get_min_reach_time(), {
                         "syH": 0, "syL": 3, "0H": 0, "1H": 2, "2H": 4, "3H": 6, "3L": 2,  "0L": 3, "1L": 0, "2L": 1})

    def test_example5(self):
        algo = DTNMinus(ta_example_5)
        algo._DTNMinus__on_the_fly_algo()
        self.assertEqual(algo.get_min_reach_time(),
                         {"q1": 0, "q2": 3, "q3": 5})

    def test_example6(self):
        algo = DTNMinus(example_6_ta)
        algo._DTNMinus__on_the_fly_algo()
        self.assertEqual(algo.get_min_reach_time(),
                         {"q1": 0, "q2": 3, "q3": 2, "q4": 2, "q5": 4, "q6": math.inf, "q7": 5})

    def test_min_reach_3(self):
        algo = DTNMinus(star_4)
        algo._DTNMinus__on_the_fly_algo()
        self.maxDiff = None
        self.assertEqual(algo.get_min_reach_time(),
                         {"q_hat": 0, "q_final": 10,
                          "q0": 10, "q0_pre": 1, "q0_loc": 0, "q0_loc_suc": 10,
                          "q1": 10, "q1_pre": 1, "q1_loc": 10, "q1_loc_suc": 10,
                          "q2": 10, "q2_pre": 1, "q2_loc": 10, "q2_loc_suc": 10,
                          "q3": 10, "q3_pre": 1, "q3_loc": 10, })

    def test_min_reach_5(self):
        algo = DTNMinus(star_5)
        algo._DTNMinus__on_the_fly_algo()
        self.maxDiff = None
        self.assertEqual(algo.get_min_reach_time(),
                         {"q_hat": 0, "q_final": 10,
                          "q0": 10, "q0_pre": 1, "q0_loc": 0, "q0_loc_suc": 10,
                          "q1": 10, "q1_pre": 1, "q1_loc": 10, "q1_loc_suc": 10,
                          "q2": 10, "q2_pre": 1, "q2_loc": 10, "q2_loc_suc": 10,
                          "q3": 10, "q3_pre": 1, "q3_loc": 10, "q3_loc_suc": 10,
                          "q4": 10, "q4_pre": 1, "q4_loc": 10, })

    def test_min_reach_5(self):
        algo = DTNMinus(star_6)
        algo._DTNMinus__on_the_fly_algo()
        self.maxDiff = None
        self.assertEqual(algo.get_min_reach_time(),
                         {"q_hat": 0, "q_final": 10,
                          "q0": 10, "q0_pre": 1, "q0_loc": 0, "q0_loc_suc": 10,
                          "q1": 10, "q1_pre": 1, "q1_loc": 10, "q1_loc_suc": 10,
                          "q2": 10, "q2_pre": 1, "q2_loc": 10, "q2_loc_suc": 10,
                          "q3": 10, "q3_pre": 1, "q3_loc": 10, "q3_loc_suc": 10,
                          "q4": 10, "q4_pre": 1, "q4_loc": 10, "q4_loc_suc": 10,
                          "q5": 10, "q5_pre": 1, "q5_loc": 10, })

    def test_min_reach_6(self):
        algo = DTNMinus(star_7)
        algo._DTNMinus__on_the_fly_algo()
        self.maxDiff = None
        self.assertEqual(algo.get_min_reach_time(),
                         {"q_hat": 0, "q_final": 10,
                          "q0": 10, "q0_pre": 1, "q0_loc": 0, "q0_loc_suc": 10,
                          "q1": 10, "q1_pre": 1, "q1_loc": 10, "q1_loc_suc": 10,
                          "q2": 10, "q2_pre": 1, "q2_loc": 10, "q2_loc_suc": 10,
                          "q3": 10, "q3_pre": 1, "q3_loc": 10, "q3_loc_suc": 10,
                          "q4": 10, "q4_pre": 1, "q4_loc": 10, "q4_loc_suc": 10,
                          "q5": 10, "q5_pre": 1, "q5_loc": 10, "q5_loc_suc": 10,
                          "q6": 10, "q6_pre": 1, "q6_loc": 10})
