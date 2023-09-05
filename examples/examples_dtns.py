# type: ignore

""" Examples & Benchmarks

    This module contains the manually encoded examples from the paper.
    The current input format still is very rudimentary and needs to be changed
    as it involves much manual labor. However, we encoded these examples so that
    you don't have to.

    We plan to add support for text based input formats that are easier to write
    and check and possibly make it compatible with other tools such as Upaal.
"""

from dbm.bound import Bound
from dbm.constraint import Constraint
from dtn.gta import GTA, to_gta_transitions


# Example 1 --------------------------------------------------------------------
locations = ["q1", "q2", "q3", "q4"]
init_states = ["q1"]
invariants = {
    "q1": Constraint("x", "0", Bound.leq(1)),
    "q2": Constraint("y", "0", Bound.unbounded()),
    "q3": Constraint("x", "0", Bound.unbounded()),
    "q4": Constraint("x", "0", Bound.unbounded()),
}

transitions = {
    "t1": {
        "source_loc": "q1",
        "clock_guard": [Constraint("0", "x", Bound.leq(-1))],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "q1",
    },
    "t2": {
        "source_loc": "q1",
        "clock_guard": [Constraint("0", "y", Bound.leq(-5))],
        "reset_clocks": ["y"],
        "loc_guard": "empty",
        "target_loc": "q2",
    },
    "t3": {
        "source_loc": "q1",
        "clock_guard": [Constraint("y", "0", Bound.unbounded())],
        "reset_clocks": [],
        "loc_guard": "q2",
        "target_loc": "q3",
    },
}
example_1_ta = GTA(
    locations, init_states, to_gta_transitions(transitions), invariants, ["x", "y"]
)


# Example 2 --------------------------------------------------------------------
locations = ["q1", "q2", "q3", "q4", "q5", "q6"]
init_states = ["q1"]
invariants = {
    "q1": Constraint("x", "0", Bound.unbounded()),
    "q2": Constraint("x", "0", Bound.leq(2)),
    "q3": Constraint("x", "0", Bound.leq(2)),
    "q4": Constraint("x", "0", Bound.unbounded()),
    "q5": Constraint("x", "0", Bound.unbounded()),
    "q6": Constraint("x", "0", Bound.unbounded()),
}
transitions = {
    "t1": {
        "source_loc": "q1",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": [],
        "loc_guard": "empty",
        "target_loc": "q2",
    },
    "t2": {
        "source_loc": "q2",
        "clock_guard": [Constraint("0", "x", Bound.leq(-2))],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "q3",
    },
    "t3": {
        "source_loc": "q3",
        "clock_guard": [Constraint("0", "x", Bound.leq(-1))],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "q2",
    },
    "t4": {
        "source_loc": "q1",
        "clock_guard": [Constraint("0", "x", Bound.leq(-5))],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "q4",
    },
    "t5": {
        "source_loc": "q4",
        "clock_guard": [Constraint("0", "x", Bound.leq(-5))],
        "reset_clocks": [],
        "loc_guard": "empty",
        "target_loc": "q5",
    },
    "t6": {
        "source_loc": "q2",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": [],
        "loc_guard": "q5",
        "target_loc": "q6",
    },
}
example_2_ta = GTA(locations, init_states, to_gta_transitions(transitions), invariants)


# Example 3 - GCS(3) -----------------------------------------------------------
locations = ["syH", "syL", "0H", "1H", "2H", "0L", "1L", "2L"]
init_states = ["0H"]
invariants = {
    "syH": Constraint("x", "0", Bound.unbounded()),
    "syL": Constraint("x", "0", Bound.unbounded()),
    "0H": Constraint("x", "0", Bound.leq(2)),
    "1H": Constraint("x", "0", Bound.leq(2)),
    "2H": Constraint("x", "0", Bound.leq(2)),
    "0L": Constraint("x", "0", Bound.leq(4)),
    "1L": Constraint("x", "0", Bound.leq(4)),
    "2L": Constraint("x", "0", Bound.leq(4)),
}
transitions = {
    # Green tag
    "tsyH-0Hu": {
        "source_loc": "syH",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": [],
        "loc_guard": "empty",
        "target_loc": "0H",
    },
    "t0H-syHu": {
        "source_loc": "0H",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": [],
        "loc_guard": "empty",
        "target_loc": "syH",
    },
    # Orange tag
    "tsyH-0Hg": {
        "source_loc": "syH",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "0H",
    },
    "tsyH-1Hg": {
        "source_loc": "syH",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "1H",
    },
    "tsyH-2Hg": {
        "source_loc": "syH",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "2H",
    },
    # black tag
    "t0H-1H": {
        "source_loc": "0H",
        "clock_guard": [
            Constraint("x", "0", Bound.leq(2)),
            Constraint("0", "x", Bound.leq(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "1H",
    },
    "t1H-2H": {
        "source_loc": "1H",
        "clock_guard": [
            Constraint("x", "0", Bound.leq(2)),
            Constraint("0", "x", Bound.leq(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "2H",
    },
    "t2H-0H": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("x", "0", Bound.leq(2)),
            Constraint("0", "x", Bound.leq(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "0H",
    },
    # red tag
    "tsyL-0H": {
        "source_loc": "syL",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "0H",
    },
    "tsyL-1H": {
        "source_loc": "syL",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "1H",
    },
    "tsyL-2H": {
        "source_loc": "syL",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "2H",
    },
    # blue tag
    "t0H-1LgOHless": {
        "source_loc": "0H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "1L",
    },
    "t0H-1Lg1Hless": {
        "source_loc": "0H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "1L",
    },
    "t0H-1Lg2Hless": {
        "source_loc": "0H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "1L",
    },
    "t0H-1Lg0Hgreat": {
        "source_loc": "0H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "1L",
    },
    "t0H-1Lg1Hgreat": {
        "source_loc": "0H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "1L",
    },
    "t0H-1Lg2Hgreat": {
        "source_loc": "0H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "1L",
    },
    "t1H-2Lg0Hless": {
        "source_loc": "1H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "2L",
    },
    "t1H-2Lg1Hless": {
        "source_loc": "1H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "2L",
    },
    "t1H-2Lg2Hless": {
        "source_loc": "1H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "2L",
    },
    "t1H-2Lg0Hgreat": {
        "source_loc": "1H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "2L",
    },
    "t1H-2Lg1Hgreat": {
        "source_loc": "1H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "2L",
    },
    "t1H-2Lg2Hgreat": {
        "source_loc": "1H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "2L",
    },
    "t2H-0Lg0Hless": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "0L",
    },
    "t2H-0Lg1Hless": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "0L",
    },
    "t2H-0Lg2Hless": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "0L",
    },
    "t2H-0Lg0Hgreat": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "0L",
    },
    "t2H-0Lg1Hgreat": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "0L",
    },
    "t2H-0Lg2Hgreat": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "0L",
    },
    # purple tag
    "tsyL-0L": {
        "source_loc": "syL",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": [],
        "loc_guard": "empty",
        "target_loc": "0L",
    },
    "t0L-syL": {
        "source_loc": "0L",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": [],
        "loc_guard": "empty",
        "target_loc": "syL",
    },
    # brown tag
    "t0L-1L": {
        "source_loc": "0L",
        "clock_guard": [Constraint("0", "x", Bound.leq(-1))],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "1L",
    },
    "t1L-2L": {
        "source_loc": "1L",
        "clock_guard": [Constraint("0", "x", Bound.leq(-1))],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "2L",
    },
    "t2L-0L": {
        "source_loc": "2L",
        "clock_guard": [Constraint("0", "x", Bound.leq(-1))],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "0L",
    },
}

example_3_ta = GTA(locations, init_states, to_gta_transitions(transitions), invariants)
gcs_3 = example_3_ta

# Example 4 - GCS(4) -----------------------------------------------------------

locations = ["syH", "syL", "0H", "1H", "2H", "3H", "0L", "1L", "2L", "3L"]
init_states = ["0H"]
invariants = {
    "syH": Constraint("x", "0", Bound.unbounded()),
    "syL": Constraint("x", "0", Bound.unbounded()),
    "0H": Constraint("x", "0", Bound.leq(2)),
    "1H": Constraint("x", "0", Bound.leq(2)),
    "2H": Constraint("x", "0", Bound.leq(2)),
    "3H": Constraint("x", "0", Bound.leq(2)),
    "0L": Constraint("x", "0", Bound.leq(4)),
    "1L": Constraint("x", "0", Bound.leq(4)),
    "2L": Constraint("x", "0", Bound.leq(4)),
    "3L": Constraint("x", "0", Bound.leq(4)),
}
transitions = {
    # Green tag
    "tsyH-0Hu": {
        "source_loc": "syH",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": [],
        "loc_guard": "empty",
        "target_loc": "0H",
    },
    "t0H-syHu": {
        "source_loc": "0H",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": [],
        "loc_guard": "empty",
        "target_loc": "syH",
    },
    # Orange tag
    "tsyH-0Hg": {
        "source_loc": "syH",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "0H",
    },
    "tsyH-1Hg": {
        "source_loc": "syH",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "1H",
    },
    "tsyH-2Hg": {
        "source_loc": "syH",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "2H",
    },
    "tsyH-3Hg": {
        "source_loc": "syH",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": ["x"],
        "loc_guard": "3H",
        "target_loc": "3H",
    },
    # black tag
    "t0H-1H": {
        "source_loc": "0H",
        "clock_guard": [
            Constraint("x", "0", Bound.leq(2)),
            Constraint("0", "x", Bound.leq(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "1H",
    },
    "t1H-2H": {
        "source_loc": "1H",
        "clock_guard": [
            Constraint("x", "0", Bound.leq(2)),
            Constraint("0", "x", Bound.leq(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "2H",
    },
    "t2H-3H": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("x", "0", Bound.leq(2)),
            Constraint("0", "x", Bound.leq(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "3H",
    },
    "t3H-0H": {
        "source_loc": "3H",
        "clock_guard": [
            Constraint("x", "0", Bound.leq(2)),
            Constraint("0", "x", Bound.leq(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "0H",
    },
    # red tag
    "tsyL-0H": {
        "source_loc": "syL",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "0H",
    },
    "tsyL-1H": {
        "source_loc": "syL",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "1H",
    },
    "tsyL-2H": {
        "source_loc": "syL",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "2H",
    },
    "tsyL-3H": {
        "source_loc": "syL",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": ["x"],
        "loc_guard": "3H",
        "target_loc": "3H",
    },
    # blue tag
    "t0H-1LgOHless": {
        "source_loc": "0H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "1L",
    },
    "t0H-1Lg1Hless": {
        "source_loc": "0H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "1L",
    },
    "t0H-1Lg2Hless": {
        "source_loc": "0H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "1L",
    },
    "t0H-1Lg3Hless": {
        "source_loc": "0H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "3H",
        "target_loc": "1L",
    },
    "t0H-1Lg0Hgreat": {
        "source_loc": "0H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "1L",
    },
    "t0H-1Lg1Hgreat": {
        "source_loc": "0H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "1L",
    },
    "t0H-1Lg2Hgreat": {
        "source_loc": "0H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "1L",
    },
    "t0H-1Lg3Hgreat": {
        "source_loc": "0H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "3H",
        "target_loc": "1L",
    },
    "t1H-2Lg0Hless": {
        "source_loc": "1H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "2L",
    },
    "t1H-2Lg1Hless": {
        "source_loc": "1H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "2L",
    },
    "t1H-2Lg2Hless": {
        "source_loc": "1H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "2L",
    },
    "t1H-2Lg3Hless": {
        "source_loc": "1H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "3H",
        "target_loc": "2L",
    },
    "t1H-2Lg0Hgreat": {
        "source_loc": "1H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "2L",
    },
    "t1H-2Lg1Hgreat": {
        "source_loc": "1H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "2L",
    },
    "t1H-2Lg2Hgreat": {
        "source_loc": "1H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "2L",
    },
    "t1H-2Lg3Hgreat": {
        "source_loc": "1H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "3H",
        "target_loc": "2L",
    },
    ########## 2H to 3L new transition start ############
    "t2H-3Lg0Hless": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "3L",
    },
    "t2H-3Lg1Hless": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "3L",
    },
    "t2H-3Lg2Hless": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "3L",
    },
    "t2H-3Lg3Hless": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "3H",
        "target_loc": "3L",
    },
    "t2H-3Lg0Hgreat": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "3L",
    },
    "t2H-3Lg1Hgreat": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "3L",
    },
    "t2H-3Lg2Hgreat": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "3L",
    },
    "t2H-3Lg3Hgreat": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "3H",
        "target_loc": "3L",
    },
    ########## 2H to 3L new transition end ############
    ########## 3H to 0L new transition start ############
    "t3H-0Lg0Hless": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "0L",
    },
    "t3H-0Lg1Hless": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "0L",
    },
    "t3H-0Lg2Hless": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "0L",
    },
    "t3H-0Lg3Hless": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("x", "0", Bound.le(2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "3H",
        "target_loc": "0L",
    },
    "t3H-0Lg0Hgreat": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "0H",
        "target_loc": "0L",
    },
    "t3H-0Lg1Hgreat": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "1H",
        "target_loc": "0L",
    },
    "t3H-0Lg2Hgreat": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "2H",
        "target_loc": "0L",
    },
    "t3H-0Lg3Hgreat": {
        "source_loc": "2H",
        "clock_guard": [
            Constraint("0", "x", Bound.le(-2)),
        ],
        "reset_clocks": ["x"],
        "loc_guard": "3H",
        "target_loc": "0L",
    },
    ########## 3H to 0L new transition end ############
    # purple tag
    "tsyL-0L": {
        "source_loc": "syL",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": [],
        "loc_guard": "empty",
        "target_loc": "0L",
    },
    "t0L-syL": {
        "source_loc": "0L",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": [],
        "loc_guard": "empty",
        "target_loc": "syL",
    },
    # brown tag
    "t0L-1L": {
        "source_loc": "0L",
        "clock_guard": [Constraint("0", "x", Bound.leq(-1))],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "1L",
    },
    "t1L-2L-1": {
        "source_loc": "1L",
        "clock_guard": [Constraint("0", "x", Bound.leq(-1))],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "2L",
    },
    "t1L-2L": {
        "source_loc": "2L",
        "clock_guard": [Constraint("0", "x", Bound.leq(-1))],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "3L",
    },
    "t3L-0L": {
        "source_loc": "3L",
        "clock_guard": [Constraint("0", "x", Bound.leq(-1))],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "0L",
    },
}

example_4_ta = GTA(locations, init_states, to_gta_transitions(transitions), invariants)
gcs_4 = example_4_ta

# Example 5 --------------------------------------------------------------------
locations = ["q1", "q2", "q3"]
init_states = ["q1"]
invariants = {
    "q1": Constraint("x", "0", Bound.unbounded()),
    "q2": Constraint("x", "0", Bound.unbounded()),
    "q3": Constraint("x", "0", Bound.unbounded()),
}
transitions = {
    "t1": {
        "source_loc": "q1",
        "clock_guard": [Constraint("0", "x", Bound.leq(-5))],
        "reset_clocks": [],
        "loc_guard": "empty",
        "target_loc": "q3",
    },
    "t2": {
        "source_loc": "q1",
        "clock_guard": [Constraint("0", "x", Bound.leq(-3))],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "q2",
    },
    "t3": {
        "source_loc": "q2",
        "clock_guard": [Constraint("0", "x", Bound.leq(-2))],
        "reset_clocks": [],
        "loc_guard": "empty",
        "target_loc": "q3",
    },
}

ta_example_5 = GTA(locations, init_states, to_gta_transitions(transitions), invariants)

# Example 6 --------------------------------------------------------------------
locations = ["q1", "q2", "q3", "q4", "q5", "q6", "q7"]
init_states = ["q1"]
invariants = {
    "q1": Constraint("x", "0", Bound.unbounded()),
    "q2": Constraint("x", "0", Bound.unbounded()),
    "q3": Constraint("x", "0", Bound.unbounded()),
    "q4": Constraint("x", "0", Bound.unbounded()),
    "q5": Constraint("x", "0", Bound.unbounded()),
    "q6": Constraint("x", "0", Bound.unbounded()),
    "q7": Constraint("x", "0", Bound.unbounded()),
}
transitions = {
    "t1": {
        "source_loc": "q1",
        "clock_guard": [Constraint("0", "x", Bound.leq(-5))],
        "reset_clocks": [],
        "loc_guard": "empty",
        "target_loc": "q7",
    },
    "t2": {
        "source_loc": "q1",
        "clock_guard": [Constraint("0", "x", Bound.leq(-3))],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "q2",
    },
    "t3": {
        "source_loc": "q2",
        "clock_guard": [Constraint("0", "x", Bound.leq(-2))],
        "reset_clocks": [],
        "loc_guard": "empty",
        "target_loc": "q7",
    },
    "t4": {
        "source_loc": "q1",
        "clock_guard": [Constraint("0", "x", Bound.leq(-2))],
        "reset_clocks": [],
        "loc_guard": "empty",
        "target_loc": "q3",
    },
    "t5": {
        "source_loc": "q3",
        "clock_guard": [
            Constraint("x", "0", Bound.leq(1)),
            Constraint("0", "x", Bound.leq(-1)),
        ],
        "reset_clocks": [],
        "loc_guard": "empty",
        "target_loc": "q7",
    },
    "t6": {
        "source_loc": "q3",
        "clock_guard": [Constraint("x", "0", Bound.unbounded())],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "q4",
    },
    "t7": {
        "source_loc": "q4",
        "clock_guard": [Constraint("0", "x", Bound.leq(-2))],
        "reset_clocks": ["x"],
        "loc_guard": "empty",
        "target_loc": "q5",
    },
    "t8": {
        "source_loc": "q5",
        "clock_guard": [Constraint("0", "x", Bound.unbounded())],
        "reset_clocks": [],
        "loc_guard": "empty",
        "target_loc": "q3",
    },
    "t9": {
        "source_loc": "q1",
        "clock_guard": [Constraint("x", "0", Bound.leq(4))],
        "reset_clocks": [],
        "loc_guard": "q7",
        "target_loc": "q6",
    },
}

example_6_ta = GTA(locations, init_states, to_gta_transitions(transitions), invariants)
