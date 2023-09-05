""" Unit tests for GTA functionality"""

import unittest

from dtn.gta import GTA, to_gta_transitions


class TestGTA(unittest.TestCase):
    """Unit tests for GTA class"""

    def test_compute_trails(self):
        # TODO : coverage
        test_cases = [
            (
                GTA(
                    ["a", "b", "c"],
                    ["a"],
                    to_gta_transitions(
                        {
                            "t0": {"source_loc": "a", "target_loc": "a"},
                            "t1": {"source_loc": "a", "target_loc": "b"},
                            "t2": {"source_loc": "b", "target_loc": "a"},
                        }
                    ),
                    {},
                ),
                "a",
                [["t0"], ["t1", "t2"]],
            ),
            (
                GTA(
                    ["a", "b", "c"],
                    ["a"],
                    to_gta_transitions(
                        {
                            "t0": {"source_loc": "a", "target_loc": "a"},
                            "t1": {"source_loc": "a", "target_loc": "b"},
                            "t2": {"source_loc": "b", "target_loc": "a"},
                        }
                    ),
                    {},
                ),
                "b",
                [["t2", "t0", "t1"], ["t2", "t1"]],
            ),
            (
                GTA(
                    ["a", "b", "c"],
                    ["a"],
                    to_gta_transitions(
                        {
                            "t0": {"source_loc": "a", "target_loc": "a"},
                            "t1": {"source_loc": "a", "target_loc": "b"},
                            "t2": {"source_loc": "b", "target_loc": "a"},
                        }
                    ),
                    {},
                ),
                "c",
                [],
            ),
            (
                GTA(
                    ["a", "b", "c"],
                    ["a"],
                    to_gta_transitions(
                        {
                            "t0": {"source_loc": "a", "target_loc": "b"},
                            "t1": {"source_loc": "b", "target_loc": "c"},
                            "t2": {"source_loc": "c", "target_loc": "c"},
                        }
                    ),
                    {},
                ),
                "a",
                [],
            ),
        ]
        for ta, state, expected_trails in test_cases:
            ta.get_trails_for_state("a")
            self.assertEqual(ta.get_trails_for_state(state), expected_trails)
