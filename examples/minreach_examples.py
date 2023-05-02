from dbm.bound import *
from dbm.constraint import *
from tn.ta import TA
# MinReach - 3 -----------------------------------------------------------------
clocks = ["x", "y"]
locations = ["q_hat", "q_final",
             "q0", "q0_pre", "q0_loc", "q0_loc_suc",
             "q1", "q1_pre", "q1_loc", "q1_loc_suc",
             "q2", "q2_pre", "q2_loc", "q2_loc_suc",
             "q3", "q3_pre", "q3_loc",
             ]
init_states = ["q_hat"]
invariants = {
    "q_hat": Constraint("x", "0", Bound.unbounded()),
    "q_final": Constraint("x", "0", Bound.unbounded()),
    #
    "q0": Constraint("x", "0", Bound.unbounded()),
    "q0_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q0_loc": Constraint("x", "0", Bound.unbounded()),
    "q0_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q1": Constraint("x", "0", Bound.unbounded()),
    "q1_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q1_loc": Constraint("x", "0", Bound.unbounded()),
    "q1_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q2": Constraint("x", "0", Bound.unbounded()),
    "q2_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q2_loc": Constraint("x", "0", Bound.unbounded()),
    "q2_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q3": Constraint("x", "0", Bound.unbounded()),
    "q3_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q3_loc": Constraint("x", "0", Bound.unbounded()),

}

transitions = {
    "t-q_hat-q0_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q0_pre"},
    "t-q0_pre-q_hat": {"source_loc": "q0_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q0_pre-q0": {"source_loc": "q0_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q0"},
    "t-q_hat-q0_loc": {"source_loc": "q_hat", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q0_loc"},
    "t-q0_loc-q0_loc_suc": {"source_loc": "q0_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q0", "target_loc": "q0_loc_suc"},
    #
    "t-q_hat-q1_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q1_pre"},
    "t-q1_pre-q_hat": {"source_loc": "q1_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q1_pre-q1": {"source_loc": "q1_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q1"},
    "t-q0_loc_suc-q1_loc": {"source_loc": "q0_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q1_loc"},
    "t-q1_loc-q1_loc_suc": {"source_loc": "q1_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q1", "target_loc": "q1_loc_suc"},
    #
    "t-q_hat-q2_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q2_pre"},
    "t-q2_pre-q_hat": {"source_loc": "q2_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q2_pre-q2": {"source_loc": "q2_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q2"},
    "t-q1_loc_suc-q2_loc": {"source_loc": "q1_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q2_loc"},
    "t-q2_loc-q2_loc_suc": {"source_loc": "q2_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q2", "target_loc": "q2_loc_suc"},
    #
    "t-q_hat-q3_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q3_pre"},
    "t-q3_pre-q_hat": {"source_loc": "q3_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q3_pre-q3": {"source_loc": "q3_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q3"},
    "t-q2_loc_suc-q3_loc": {"source_loc": "q2_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q3_loc"},
    "t-q3_loc-q_final": {"source_loc": "q3_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q3", "target_loc": "q_final"},
}
star_4 = TA(locations, init_states, transitions, invariants, clocks=clocks)

# MinReach - 4 -----------------------------------------------------------------
clocks = ["x", "y"]
locations = ["q_hat", "q_final",
             "q0", "q0_pre", "q0_loc", "q0_loc_suc",
             "q1", "q1_pre", "q1_loc", "q1_loc_suc",
             "q2", "q2_pre", "q2_loc", "q2_loc_suc",
             "q3", "q3_pre", "q3_loc", "q3_loc_suc",
             "q4", "q4_pre", "q4_loc",
             ]
init_states = ["q_hat"]
invariants = {
    "q_hat": Constraint("x", "0", Bound.unbounded()),
    "q_final": Constraint("x", "0", Bound.unbounded()),
    #
    "q0": Constraint("x", "0", Bound.unbounded()),
    "q0_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q0_loc": Constraint("x", "0", Bound.unbounded()),
    "q0_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q1": Constraint("x", "0", Bound.unbounded()),
    "q1_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q1_loc": Constraint("x", "0", Bound.unbounded()),
    "q1_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q2": Constraint("x", "0", Bound.unbounded()),
    "q2_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q2_loc": Constraint("x", "0", Bound.unbounded()),
    "q2_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q3": Constraint("x", "0", Bound.unbounded()),
    "q3_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q3_loc": Constraint("x", "0", Bound.unbounded()),
    "q3_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q4": Constraint("x", "0", Bound.unbounded()),
    "q4_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q4_loc": Constraint("x", "0", Bound.unbounded()),

}

transitions = {
    "t-q_hat-q0_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q0_pre"},
    "t-q0_pre-q_hat": {"source_loc": "q0_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q0_pre-q0": {"source_loc": "q0_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q0"},
    "t-q_hat-q0_loc": {"source_loc": "q_hat", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q0_loc"},
    "t-q0_loc-q0_loc_suc": {"source_loc": "q0_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q0", "target_loc": "q0_loc_suc"},
    #
    "t-q_hat-q1_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q1_pre"},
    "t-q1_pre-q_hat": {"source_loc": "q1_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q1_pre-q1": {"source_loc": "q1_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q1"},
    "t-q0_loc_suc-q1_loc": {"source_loc": "q0_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q1_loc"},
    "t-q1_loc-q1_loc_suc": {"source_loc": "q1_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q1", "target_loc": "q1_loc_suc"},
    #
    "t-q_hat-q2_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q2_pre"},
    "t-q2_pre-q_hat": {"source_loc": "q2_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q2_pre-q2": {"source_loc": "q2_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q2"},
    "t-q1_loc_suc-q2_loc": {"source_loc": "q1_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q2_loc"},
    "t-q2_loc-q2_loc_suc": {"source_loc": "q2_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q2", "target_loc": "q2_loc_suc"},
    #
    "t-q_hat-q3_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q3_pre"},
    "t-q3_pre-q_hat": {"source_loc": "q3_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q3_pre-q3": {"source_loc": "q3_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q3"},
    "t-q2_loc_suc-q3_loc": {"source_loc": "q2_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q3_loc"},
    "t-q3_loc-q3_loc_suc": {"source_loc": "q3_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q3", "target_loc": "q3_loc_suc"},
    #
    "t-q_hat-q4_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q4_pre"},
    "t-q4_pre-q_hat": {"source_loc": "q4_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q4_pre-q4": {"source_loc": "q4_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q4"},
    "t-q3_loc_suc-q4_loc": {"source_loc": "q3_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q4_loc"},
    "t-q4_loc-q_final": {"source_loc": "q4_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q4", "target_loc": "q_final"},
}
star_5 = TA(locations, init_states, transitions, invariants, clocks=clocks)


# MinReach - 5 -----------------------------------------------------------------
clocks = ["x", "y"]
locations = ["q_hat", "q_final",
             "q0", "q0_pre", "q0_loc", "q0_loc_suc",
             "q1", "q1_pre", "q1_loc", "q1_loc_suc",
             "q2", "q2_pre", "q2_loc", "q2_loc_suc",
             "q3", "q3_pre", "q3_loc", "q3_loc_suc",
             "q4", "q4_pre", "q4_loc", "q4_loc_suc",
             "q5", "q5_pre", "q5_loc",
             ]
init_states = ["q_hat"]
invariants = {
    "q_hat": Constraint("x", "0", Bound.unbounded()),
    "q_final": Constraint("x", "0", Bound.unbounded()),
    #
    "q0": Constraint("x", "0", Bound.unbounded()),
    "q0_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q0_loc": Constraint("x", "0", Bound.unbounded()),
    "q0_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q1": Constraint("x", "0", Bound.unbounded()),
    "q1_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q1_loc": Constraint("x", "0", Bound.unbounded()),
    "q1_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q2": Constraint("x", "0", Bound.unbounded()),
    "q2_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q2_loc": Constraint("x", "0", Bound.unbounded()),
    "q2_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q3": Constraint("x", "0", Bound.unbounded()),
    "q3_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q3_loc": Constraint("x", "0", Bound.unbounded()),
    "q3_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q4": Constraint("x", "0", Bound.unbounded()),
    "q4_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q4_loc": Constraint("x", "0", Bound.unbounded()),
    "q4_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q5": Constraint("x", "0", Bound.unbounded()),
    "q5_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q5_loc": Constraint("x", "0", Bound.unbounded()),
}

transitions = {
    "t-q_hat-q0_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q0_pre"},
    "t-q0_pre-q_hat": {"source_loc": "q0_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q0_pre-q0": {"source_loc": "q0_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q0"},
    "t-q_hat-q0_loc": {"source_loc": "q_hat", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q0_loc"},
    "t-q0_loc-q0_loc_suc": {"source_loc": "q0_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q0", "target_loc": "q0_loc_suc"},
    #
    "t-q_hat-q1_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q1_pre"},
    "t-q1_pre-q_hat": {"source_loc": "q1_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q1_pre-q1": {"source_loc": "q1_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q1"},
    "t-q0_loc_suc-q1_loc": {"source_loc": "q0_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q1_loc"},
    "t-q1_loc-q1_loc_suc": {"source_loc": "q1_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q1", "target_loc": "q1_loc_suc"},
    #
    "t-q_hat-q2_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q2_pre"},
    "t-q2_pre-q_hat": {"source_loc": "q2_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q2_pre-q2": {"source_loc": "q2_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q2"},
    "t-q1_loc_suc-q2_loc": {"source_loc": "q1_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q2_loc"},
    "t-q2_loc-q2_loc_suc": {"source_loc": "q2_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q2", "target_loc": "q2_loc_suc"},
    #
    "t-q_hat-q3_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q3_pre"},
    "t-q3_pre-q_hat": {"source_loc": "q3_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q3_pre-q3": {"source_loc": "q3_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q3"},
    "t-q2_loc_suc-q3_loc": {"source_loc": "q2_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q3_loc"},
    "t-q3_loc-q3_loc_suc": {"source_loc": "q3_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q3", "target_loc": "q3_loc_suc"},
    #
    "t-q_hat-q4_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q4_pre"},
    "t-q4_pre-q_hat": {"source_loc": "q4_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q4_pre-q4": {"source_loc": "q4_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q4"},
    "t-q3_loc_suc-q4_loc": {"source_loc": "q3_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q4_loc"},
    "t-q4_loc-q4_loc_suc": {"source_loc": "q4_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q4", "target_loc": "q4_loc_suc"},
    #
    "t-q_hat-q5_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q5_pre"},
    "t-q5_pre-q_hat": {"source_loc": "q5_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q5_pre-q5": {"source_loc": "q5_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q5"},
    "t-q4_loc_suc-q5_loc": {"source_loc": "q4_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q5_loc"},
    "t-q5_loc-q_final": {"source_loc": "q5_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q5", "target_loc": "q_final"},
}
star_6 = TA(locations, init_states, transitions, invariants, clocks=clocks)


# MinReach - 6 -----------------------------------------------------------------
clocks = ["x", "y"]
locations = ["q_hat", "q_final",
             "q0", "q0_pre", "q0_loc", "q0_loc_suc",
             "q1", "q1_pre", "q1_loc", "q1_loc_suc",
             "q2", "q2_pre", "q2_loc", "q2_loc_suc",
             "q3", "q3_pre", "q3_loc", "q3_loc_suc",
             "q4", "q4_pre", "q4_loc", "q4_loc_suc",
             "q5", "q5_pre", "q5_loc", "q5_loc_suc",
             "q6", "q6_pre", "q6_loc",
             ]
init_states = ["q_hat"]
invariants = {
    "q_hat": Constraint("x", "0", Bound.unbounded()),
    "q_final": Constraint("x", "0", Bound.unbounded()),
    #
    "q0": Constraint("x", "0", Bound.unbounded()),
    "q0_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q0_loc": Constraint("x", "0", Bound.unbounded()),
    "q0_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q1": Constraint("x", "0", Bound.unbounded()),
    "q1_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q1_loc": Constraint("x", "0", Bound.unbounded()),
    "q1_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q2": Constraint("x", "0", Bound.unbounded()),
    "q2_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q2_loc": Constraint("x", "0", Bound.unbounded()),
    "q2_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q3": Constraint("x", "0", Bound.unbounded()),
    "q3_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q3_loc": Constraint("x", "0", Bound.unbounded()),
    "q3_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q4": Constraint("x", "0", Bound.unbounded()),
    "q4_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q4_loc": Constraint("x", "0", Bound.unbounded()),
    "q4_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q5": Constraint("x", "0", Bound.unbounded()),
    "q5_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q5_loc": Constraint("x", "0", Bound.unbounded()),
    "q5_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q6": Constraint("x", "0", Bound.unbounded()),
    "q6_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q6_loc": Constraint("x", "0", Bound.unbounded()),
}

transitions = {
    "t-q_hat-q0_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q0_pre"},
    "t-q0_pre-q_hat": {"source_loc": "q0_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q0_pre-q0": {"source_loc": "q0_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q0"},
    "t-q_hat-q0_loc": {"source_loc": "q_hat", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q0_loc"},
    "t-q0_loc-q0_loc_suc": {"source_loc": "q0_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q0", "target_loc": "q0_loc_suc"},
    #
    "t-q_hat-q1_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q1_pre"},
    "t-q1_pre-q_hat": {"source_loc": "q1_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q1_pre-q1": {"source_loc": "q1_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q1"},
    "t-q0_loc_suc-q1_loc": {"source_loc": "q0_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q1_loc"},
    "t-q1_loc-q1_loc_suc": {"source_loc": "q1_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q1", "target_loc": "q1_loc_suc"},
    #
    "t-q_hat-q2_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q2_pre"},
    "t-q2_pre-q_hat": {"source_loc": "q2_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q2_pre-q2": {"source_loc": "q2_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q2"},
    "t-q1_loc_suc-q2_loc": {"source_loc": "q1_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q2_loc"},
    "t-q2_loc-q2_loc_suc": {"source_loc": "q2_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q2", "target_loc": "q2_loc_suc"},
    #
    "t-q_hat-q3_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q3_pre"},
    "t-q3_pre-q_hat": {"source_loc": "q3_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q3_pre-q3": {"source_loc": "q3_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q3"},
    "t-q2_loc_suc-q3_loc": {"source_loc": "q2_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q3_loc"},
    "t-q3_loc-q3_loc_suc": {"source_loc": "q3_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q3", "target_loc": "q3_loc_suc"},
    #
    "t-q_hat-q4_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q4_pre"},
    "t-q4_pre-q_hat": {"source_loc": "q4_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q4_pre-q4": {"source_loc": "q4_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q4"},
    "t-q3_loc_suc-q4_loc": {"source_loc": "q3_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q4_loc"},
    "t-q4_loc-q4_loc_suc": {"source_loc": "q4_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q4", "target_loc": "q4_loc_suc"},
    #
    "t-q_hat-q5_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q5_pre"},
    "t-q5_pre-q_hat": {"source_loc": "q5_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q5_pre-q5": {"source_loc": "q5_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q5"},
    "t-q4_loc_suc-q5_loc": {"source_loc": "q4_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q5_loc"},
    "t-q5_loc-q5_loc_suc": {"source_loc": "q5_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q5", "target_loc": "q5_loc_suc"},
    #
    "t-q_hat-q6_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q6_pre"},
    "t-q6_pre-q_hat": {"source_loc": "q6_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q6_pre-q6": {"source_loc": "q6_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q6"},
    "t-q5_loc_suc-q6_loc": {"source_loc": "q5_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q6_loc"},
    "t-q6_loc-q_final": {"source_loc": "q6_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q6", "target_loc": "q_final"},
}
star_7 = TA(locations, init_states, transitions, invariants, clocks=clocks)

# MinReach - 7 -----------------------------------------------------------------
clocks = ["x", "y"]
locations = ["q_hat", "q_final",
             "q0", "q0_pre", "q0_loc", "q0_loc_suc",
             "q1", "q1_pre", "q1_loc", "q1_loc_suc",
             "q2", "q2_pre", "q2_loc", "q2_loc_suc",
             "q3", "q3_pre", "q3_loc", "q3_loc_suc",
             "q4", "q4_pre", "q4_loc", "q4_loc_suc",
             "q5", "q5_pre", "q5_loc", "q5_loc_suc",
             "q6", "q6_pre", "q6_loc", "q6_loc_suc",
             "q7", "q7_pre", "q7_loc",
             ]
init_states = ["q_hat"]
invariants = {
    "q_hat": Constraint("x", "0", Bound.unbounded()),
    "q_final": Constraint("x", "0", Bound.unbounded()),
    #
    "q0": Constraint("x", "0", Bound.unbounded()),
    "q0_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q0_loc": Constraint("x", "0", Bound.unbounded()),
    "q0_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q1": Constraint("x", "0", Bound.unbounded()),
    "q1_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q1_loc": Constraint("x", "0", Bound.unbounded()),
    "q1_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q2": Constraint("x", "0", Bound.unbounded()),
    "q2_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q2_loc": Constraint("x", "0", Bound.unbounded()),
    "q2_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q3": Constraint("x", "0", Bound.unbounded()),
    "q3_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q3_loc": Constraint("x", "0", Bound.unbounded()),
    "q3_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q4": Constraint("x", "0", Bound.unbounded()),
    "q4_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q4_loc": Constraint("x", "0", Bound.unbounded()),
    "q4_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q5": Constraint("x", "0", Bound.unbounded()),
    "q5_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q5_loc": Constraint("x", "0", Bound.unbounded()),
    "q5_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q6": Constraint("x", "0", Bound.unbounded()),
    "q6_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q6_loc": Constraint("x", "0", Bound.unbounded()),
    "q6_loc_suc": Constraint("x", "0", Bound.unbounded()),
    #
    "q7": Constraint("x", "0", Bound.unbounded()),
    "q7_pre": Constraint("x", "0", Bound.less_equal(1)),
    "q7_loc": Constraint("x", "0", Bound.unbounded()),
}

transitions = {
    "t-q_hat-q0_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q0_pre"},
    "t-q0_pre-q_hat": {"source_loc": "q0_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q0_pre-q0": {"source_loc": "q0_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q0"},
    "t-q_hat-q0_loc": {"source_loc": "q_hat", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q0_loc"},
    "t-q0_loc-q0_loc_suc": {"source_loc": "q0_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q0", "target_loc": "q0_loc_suc"},
    #
    "t-q_hat-q1_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q1_pre"},
    "t-q1_pre-q_hat": {"source_loc": "q1_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q1_pre-q1": {"source_loc": "q1_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q1"},
    "t-q0_loc_suc-q1_loc": {"source_loc": "q0_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q1_loc"},
    "t-q1_loc-q1_loc_suc": {"source_loc": "q1_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q1", "target_loc": "q1_loc_suc"},
    #
    "t-q_hat-q2_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q2_pre"},
    "t-q2_pre-q_hat": {"source_loc": "q2_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q2_pre-q2": {"source_loc": "q2_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q2"},
    "t-q1_loc_suc-q2_loc": {"source_loc": "q1_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q2_loc"},
    "t-q2_loc-q2_loc_suc": {"source_loc": "q2_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q2", "target_loc": "q2_loc_suc"},
    #
    "t-q_hat-q3_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q3_pre"},
    "t-q3_pre-q_hat": {"source_loc": "q3_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q3_pre-q3": {"source_loc": "q3_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q3"},
    "t-q2_loc_suc-q3_loc": {"source_loc": "q2_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q3_loc"},
    "t-q3_loc-q3_loc_suc": {"source_loc": "q3_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q3", "target_loc": "q3_loc_suc"},
    #
    "t-q_hat-q4_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q4_pre"},
    "t-q4_pre-q_hat": {"source_loc": "q4_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q4_pre-q4": {"source_loc": "q4_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q4"},
    "t-q3_loc_suc-q4_loc": {"source_loc": "q3_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q4_loc"},
    "t-q4_loc-q4_loc_suc": {"source_loc": "q4_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q4", "target_loc": "q4_loc_suc"},
    #
    "t-q_hat-q5_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q5_pre"},
    "t-q5_pre-q_hat": {"source_loc": "q5_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q5_pre-q5": {"source_loc": "q5_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q5"},
    "t-q4_loc_suc-q5_loc": {"source_loc": "q4_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q5_loc"},
    "t-q5_loc-q5_loc_suc": {"source_loc": "q5_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q5", "target_loc": "q5_loc_suc"},
    #
    "t-q_hat-q6_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q6_pre"},
    "t-q6_pre-q_hat": {"source_loc": "q6_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q6_pre-q6": {"source_loc": "q6_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q6"},
    "t-q5_loc_suc-q6_loc": {"source_loc": "q5_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q6_loc"},
    "t-q6_loc-q6_loc_suc": {"source_loc": "q6_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q6", "target_loc": "q6_loc_suc"},
    #
    "t-q_hat-q7_pre": {"source_loc": "q_hat", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q7_pre"},
    "t-q7_pre-q_hat": {"source_loc": "q7_pre", "clock_guard": [Constraint("0", "x", Bound.less_equal(-1)), Constraint("x", "0", Bound.less_equal(1))], "reset_clocks": ["x"], "loc_guard": "empty", "target_loc": "q_hat"},
    "t-q7_pre-q7": {"source_loc": "q7_pre", "clock_guard": [Constraint("x", "0", Bound.less_equal(1)), Constraint("0", "y", Bound.less_equal(-10))], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q7"},
    "t-q6_loc_suc-q7_loc": {"source_loc": "q6_loc_suc", "clock_guard": [], "reset_clocks": [], "loc_guard": "empty", "target_loc": "q7_loc"},
    "t-q7_loc-q_final": {"source_loc": "q7_loc", "clock_guard": [], "reset_clocks": [], "loc_guard": "q7", "target_loc": "q_final"},
}
star_8 = TA(locations, init_states, transitions, invariants, clocks=clocks)
