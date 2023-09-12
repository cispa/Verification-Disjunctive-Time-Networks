""" Unit tests for DBM functionality"""

# pylint: disable=protected-access

import unittest

from dbm.dbm import DBM
from dbm.bound import Bound
from dbm.constraint import Constraint


class TestDBM(unittest.TestCase):
    """Unit tests for DBM class"""

    def test_init(self):
        test_cases = [
            ("n_clocks 0", [], [[Bound.leq(0)]]),
            (
                "n_clocks 2",
                ["x", "y"],
                [
                    [Bound.leq(0), Bound.leq(0), Bound.leq(0)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                ],
            ),
            (
                "n_clocks 4",
                ["x", "y", "z", "delta"],
                [
                    [
                        Bound.leq(0),
                        Bound.leq(0),
                        Bound.leq(0),
                        Bound.leq(0),
                        Bound.leq(0),
                    ],
                    [
                        Bound.unbounded(),
                        Bound.leq(0),
                        Bound.leq(0),
                        Bound.leq(0),
                        Bound.leq(0),
                    ],
                    [
                        Bound.unbounded(),
                        Bound.leq(0),
                        Bound.leq(0),
                        Bound.leq(0),
                        Bound.leq(0),
                    ],
                    [
                        Bound.unbounded(),
                        Bound.leq(0),
                        Bound.leq(0),
                        Bound.leq(0),
                        Bound.leq(0),
                    ],
                    [
                        Bound.unbounded(),
                        Bound.leq(0),
                        Bound.leq(0),
                        Bound.leq(0),
                        Bound.leq(0),
                    ],
                ],
            ),
        ]
        for test_name, n_clock, expected in test_cases:
            self.assertEqual(DBM(n_clock).m, expected, f"failed test case {test_name}")

    def test_canonicalize_non_empty(self):
        # TODO: coverage !
        test_cases = [
            (
                "simple_two_clocks_first_one_downward_bounded",
                ["x", "y"],
                [
                    [Bound.leq(0), Bound.leq(-1), Bound.leq(0)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                ],
                [
                    [Bound.leq(0), Bound.leq(-1), Bound.leq(-1)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                ],
            ),
            (
                "simple_two_clocks_first_one_upward_bounded",
                ["x", "y"],
                [
                    [Bound.leq(0), Bound.leq(0), Bound.leq(0)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                    [Bound.leq(10), Bound.leq(0), Bound.leq(0)],
                ],
                [
                    [Bound.leq(0), Bound.leq(0), Bound.leq(0)],
                    [Bound.leq(10), Bound.leq(0), Bound.leq(0)],
                    [Bound.leq(10), Bound.leq(0), Bound.leq(0)],
                ],
            ),
        ]
        for test_name, clocks, m_init, m_expected in test_cases:
            d = DBM(clocks, m=m_init)
            ok = d.canonicalize()
            self.assertTrue(ok)
            self.assertEqual(
                d.m,
                m_expected,
                f"failed test canonicalize non-empty test \
                                case {test_name}",
            )

    def test_is_not_empty(self):
        # TODO: coverage !
        test_cases = [
            (
                "contradicting_constraints_1",
                ["x", "y"],
                [
                    [Bound.leq(0), Bound.leq(-3), Bound.leq(0)],
                    [Bound.le(2), Bound.leq(0), Bound.leq(0)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                ],
            ),
            (
                "contradicting_constraints_2",
                ["x", "y"],
                [
                    [Bound.leq(0), Bound.leq(-1), Bound.leq(0)],
                    [Bound.le(1), Bound.leq(0), Bound.leq(0)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                ],
            ),
            (
                "negative_cycle_1",
                ["x", "y"],
                [
                    [Bound.leq(0), Bound.leq(-1), Bound.leq(0)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(1)],
                    [Bound.leq(-2), Bound.leq(0), Bound.leq(0)],
                ],
            ),
            (
                "negative_cycle_2",
                ["x", "y"],
                [
                    [Bound.leq(0), Bound.leq(-1), Bound.unbounded()],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(1)],
                    [Bound.leq(-2), Bound.unbounded(), Bound.leq(0)],
                ],
            ),
            (
                "negative_cycle_3",
                ["x", "y"],
                [
                    [Bound.leq(0), Bound.le(-1), Bound.leq(0)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                    [Bound.leq(-1), Bound.leq(0), Bound.leq(0)],
                ],
            ),
        ]

        for test_name, clocks, m_init in test_cases:
            d = DBM(clocks, m=m_init)
            ok = d.is_not_empty()
            self.assertFalse(
                ok,
                f"failed is_not_empty() test test case\
                                {test_name} without prior canonicalization",
            )
            d = DBM(clocks, m=m_init)
            ok = d.canonicalize()
            self.assertFalse(
                ok,
                f"failed emptiness test, test case {test_name} \
                                returned by canonicalize",
            )
            ok = d.is_not_empty()
            self.assertFalse(
                ok,
                f"failed is_not_empty() test test case {test_name}\
                                after prior canonicalization",
            )

    def test_reset(self):
        test_cases = [
            (
                "one_clock_one_reset",
                ["x"],
                ["x"],
                [
                    [Bound.leq(0), Bound.leq(-1)],
                    [Bound.unbounded(), Bound.leq(0)],
                ],
                [
                    [Bound.leq(0), Bound.leq(0)],
                    [Bound.leq(0), Bound.leq(0)],
                ],
            ),
            (
                "two_clocks_one_reset_1",
                ["x", "y"],
                ["x"],
                [
                    [Bound.leq(0), Bound.leq(-1), Bound.leq(-1)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                ],
                [
                    [Bound.leq(0), Bound.leq(0), Bound.leq(-1)],
                    [Bound.leq(0), Bound.leq(0), Bound.leq(-1)],
                    [Bound.unbounded(), Bound.unbounded(), Bound.leq(0)],
                ],
            ),
            (
                "two_clocks_one_reset_2",
                ["x", "y"],
                ["x"],
                [
                    [Bound.leq(0), Bound.leq(-2), Bound.leq(-2)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                ],
                [
                    [Bound.leq(0), Bound.leq(0), Bound.leq(-2)],
                    [Bound.leq(0), Bound.leq(0), Bound.leq(-2)],
                    [Bound.unbounded(), Bound.unbounded(), Bound.leq(0)],
                ],
            ),
            (
                "two_clocks_two_reset",
                ["x", "y"],
                ["x", "y"],
                [
                    [Bound.leq(0), Bound.leq(-1), Bound.leq(-1)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                ],
                [
                    [Bound.leq(0), Bound.leq(0), Bound.leq(0)],
                    [Bound.leq(0), Bound.leq(0), Bound.leq(0)],
                    [Bound.leq(0), Bound.leq(0), Bound.leq(0)],
                ],
            ),
        ]

        for test_name, clocks, reset_clocks, m_init, m_expected in test_cases:
            d = DBM(clocks, m=m_init)
            d.reset(reset_clocks)
            self.assertEqual(
                d.m, m_expected, f"failed test reset test case {test_name}"
            )

    def test_delay(self):
        test_cases = [
            (
                "one_clock",
                ["x"],
                [
                    [Bound.leq(0), Bound.leq(-1)],
                    [Bound.leq(4), Bound.leq(0)],
                ],
                [
                    [Bound.leq(0), Bound.leq(-1)],
                    [Bound.unbounded(), Bound.leq(0)],
                ],
            ),
            (
                "two_clocks",
                ["x", "y"],
                [
                    [Bound.leq(0), Bound.leq(-1), Bound.leq(-1)],
                    [Bound.leq(42), Bound.leq(0), Bound.leq(0)],
                    [Bound.leq(42), Bound.leq(0), Bound.leq(0)],
                ],
                [
                    [Bound.leq(0), Bound.leq(-1), Bound.leq(-1)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                ],
            ),
        ]

        for test_name, clocks, m_init, m_expected in test_cases:
            d = DBM(clocks, m=m_init)
            d.delay()
            self.assertEqual(
                d.m, m_expected, f"failed test delay test case {test_name}"
            )

    def test_and_constr(self):
        # TODO: coverage
        test_cases = [
            (
                "one_clock_true",
                ["x"],
                Constraint("0", "x", Bound.leq(-2)),
                True,
                [
                    [Bound.leq(0), Bound.leq(-1)],
                    [Bound.leq(4), Bound.leq(0)],
                ],
                [
                    [Bound.leq(0), Bound.leq(-2)],
                    [Bound.leq(4), Bound.leq(0)],
                ],
            ),
            (
                "one_clock_false",
                ["x"],
                Constraint("0", "x", Bound.leq(-10)),
                False,
                [
                    [Bound.leq(0), Bound.leq(-1)],
                    [Bound.leq(4), Bound.leq(0)],
                ],
                [],
            ),
            (
                "two_clocks",
                ["x", "y"],
                Constraint("x", "y", Bound.leq(-1)),
                False,
                [
                    [Bound.leq(0), Bound.leq(-1), Bound.leq(-1)],
                    [Bound.leq(42), Bound.leq(0), Bound.leq(0)],
                    [Bound.leq(42), Bound.leq(0), Bound.leq(0)],
                ],
                [
                    [Bound.leq(0), Bound.leq(-1), Bound.leq(-1)],
                    [Bound.leq(42), Bound.leq(0), Bound.leq(-1)],
                    [Bound.leq(42), Bound.leq(0), Bound.leq(0)],
                ],
            ),
            (
                "two_clocks",
                ["x", "y"],
                Constraint("x", "y", Bound.leq(10)),
                True,
                [
                    [Bound.leq(0), Bound.leq(-1), Bound.leq(-1)],
                    [Bound.leq(42), Bound.leq(0), Bound.leq(0)],
                    [Bound.leq(42), Bound.leq(0), Bound.leq(0)],
                ],
                [
                    [Bound.leq(0), Bound.leq(-1), Bound.leq(-1)],
                    [Bound.leq(42), Bound.leq(0), Bound.leq(0)],
                    [Bound.leq(42), Bound.leq(0), Bound.leq(0)],
                ],
            ),
        ]

        for (
            test_name,
            clocks_init,
            constr,
            is_canon,
            dbm_m_init,
            m_expected,
        ) in test_cases:
            d = DBM(clocks_init, m=dbm_m_init)
            d.and_constr(constr)

            self.assertEqual(
                is_canon,
                d.canonicalize(),
                f"failed test and_constraint test case {test_name}",
            )
            if is_canon:
                self.assertEqual(
                    d.m,
                    m_expected,
                    f"failed test and_constraint test case \
                                    {test_name}",
                )


def test_intersection(self):
    # TODO: coverage
    test_cases = [
        (
            "simple_dbms_with_one_clock",
            DBM(["x"], [[Bound.leq(0), Bound.leq(-1)], [Bound.leq(2), Bound.leq(0)]]),
            DBM(["x"], [[Bound.leq(0), Bound.leq(-1)], [Bound.leq(1), Bound.leq(0)]]),
            [[Bound.leq(0), Bound.leq(-1)], [Bound.leq(1), Bound.leq(0)]],
        ),
        (
            "simple_dbms_with_two_clocks",
            DBM(
                ["x", "y"],
                [
                    [Bound.leq(0), Bound.leq(-1), Bound.leq(-1)],
                    [Bound.leq(42), Bound.leq(0), Bound.leq(0)],
                    [Bound.leq(42), Bound.leq(0), Bound.leq(0)],
                ],
            ),
            DBM(
                ["x", "y"],
                [
                    [Bound.leq(0), Bound.leq(-3), Bound.leq(-3)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                    [Bound.unbounded(), Bound.leq(0), Bound.leq(0)],
                ],
            ),
            [
                [Bound.leq(0), Bound.leq(-3), Bound.leq(-3)],
                [Bound.leq(42), Bound.leq(0), Bound.leq(0)],
                [Bound.leq(42), Bound.leq(0), Bound.leq(0)],
            ],
        ),
    ]
    for test_name, dbm_1, dbm_2, m_expected in test_cases:
        d = dbm_1.intersect(dbm_2)
        self.assertEqual(
            d.m, m_expected, f"failed test intersect test case {test_name}"
        )


def test_check_constraints_emptiness(self):
    dbm = DBM(
        ["x", "y"],
        [
            [Bound.le(0), Bound.le(-1), Bound.le(-1)],
            [Bound.le(1), Bound.le(0), Bound.le(0)],
            [Bound.le(1), Bound.le(0), Bound.le(0)],
        ],
    )
    self.assertEqual(dbm._DBM__check_constraints_satisfiable(), False)
