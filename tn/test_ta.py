import unittest

from tn.ta import TA


class TestTA(unittest.TestCase):

    def test_compute_trails(self):
        # TODO : coverage
        test_cases = [
            (TA(["a", "b", "c"], ["a"],
                {"t0": {"source_loc": "a", "target_loc": "a"},
                "t1": {"source_loc": "a", "target_loc": "b"},
                 "t2": {"source_loc": "b", "target_loc": "a"}},
                {}),
             "a",
             [["t0"], ["t1", "t2"]]
             ),
            (TA(["a", "b", "c"], ["a"],
                {"t0": {"source_loc": "a", "target_loc": "a"},
                 "t1": {"source_loc": "a", "target_loc": "b"},
                 "t2": {"source_loc": "b", "target_loc": "a"}},
                {}),
             "b",
             [["t2", "t0", "t1"], ["t2", "t1"]]
             ),
            (TA(["a", "b", "c"], ["a"],
                {"t0": {"source_loc": "a", "target_loc": "a"},
                 "t1": {"source_loc": "a", "target_loc": "b"},
                 "t2": {"source_loc": "b", "target_loc": "a"}},
                {}),
             "c",
             []
             ),
            (TA(["a", "b", "c"], ["a"],
                {"t0": {"source_loc": "a", "target_loc": "b"},
                 "t1": {"source_loc": "b", "target_loc": "c"},
                 "t2": {"source_loc": "c", "target_loc": "c"}},
                {}),
             "a",
             []
             )
        ]
        for (ta, state, expected_trails) in test_cases:
            ta.get_trails_for_state("a")
            self.assertEqual(ta.get_trails_for_state(state), expected_trails)
