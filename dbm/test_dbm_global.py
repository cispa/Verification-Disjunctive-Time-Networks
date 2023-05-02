import unittest

from dbm.dbm_global import *
from dbm.bound import *
from dbm.constraint import *


class TestDBMGlobal(unittest.TestCase):

    def test_init(self):
        d = DBMGlobal(["x"])
        clocks = set([key for key in d.clocks.keys()])
        self.assertEqual(clocks, set(
            ["x", ZERO, DELTA]), "failed initialization DBMGlobal")

    def test_min_global_time(self):
        test_cases = [
            ("single_clock",
                ["x"],
                [[Bound.less_equal(0), Bound.less_equal(0), Bound.less_equal(0)],
                 [Bound.unbounded(), Bound.less_equal(0), Bound.less_equal(0)],
                 [Bound.unbounded(), Bound.less_equal(0), Bound.less_equal(0)]],
                Bound.less_equal(0),
             )
        ]

        for (test_name, clocks, m_init, expected_min) in test_cases:
            d = DBMGlobal(clocks, m=m_init)
            self.assertEqual(d.get_min_global_bound(), expected_min)

    def test_le(self):
        # TODO: test coverage
        d_1 = DBMGlobal(["x"],
                        m=[[Bound.less_equal(0), Bound.unbounded(), Bound.less_equal(-10)],
                            [Bound.unbounded(), Bound.less_equal(0),
                             Bound.unbounded()],
                            [Bound.unbounded(), Bound.unbounded(), Bound.less_equal(0)]]
                        )
        d_2 = DBMGlobal(["x"],
                        m=[[Bound.less_equal(0), Bound.less_equal(0), Bound.less_equal(0)],
                            [Bound.unbounded(), Bound.less_equal(0),
                             Bound.less_equal(0)],
                            [Bound.unbounded(), Bound.less_equal(0), Bound.less_equal(0)]]
                        )
        self.assertGreater(d_1, d_2)
