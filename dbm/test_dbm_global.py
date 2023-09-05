""" Unit tests for DBMs with global clocks"""

import unittest

from dbm.dbm_global import DBMG, DELTA
from dbm.bound import Bound
from dbm.constraint import ZERO


class TestDBMG(unittest.TestCase):
    """Unit tests for class DBMG"""

    def test_init(self):
        d = DBMG(["x"])
        clocks = set(d.clocks)
        self.assertEqual(
            clocks, set(["x", ZERO, DELTA]), "failed initialization DBMGlobal"
        )

    def test_min_global_time(self):
        test_cases = [
            (
                "single_clock",
                ["x"],
                [
                    [Bound.leq(0), Bound.leq(0), Bound.leq(0)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                ],
                Bound.leq(0),
            )
        ]

        for _, clocks, m_init, expected_min in test_cases:
            d = DBMG(clocks, m=m_init)
            self.assertEqual(d.get_min_global_bound(), expected_min)

    def test_le(self):
        # TODO: test coverage
        d_1 = DBMG(
            ["x"],
            m=[
                [Bound.leq(0), Bound.unbounded(), Bound.leq(-10)],
                [Bound.unbounded(), Bound.leq(0), Bound.unbounded()],
                [Bound.unbounded(), Bound.unbounded(), Bound.leq(0)],
            ],
        )
        d_2 = DBMG(
            ["x"],
            m=[
                [Bound.leq(0), Bound.leq(0), Bound.leq(0)],
                [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
            ],
        )
        self.assertGreater(d_1, d_2)
