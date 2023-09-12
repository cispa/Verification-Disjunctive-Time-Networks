""" Unit tests for Bound functionality
"""

import unittest
from dbm.bound import Bound


class TestBound(unittest.TestCase):
    """Unit tests for Bound class"""

    def test_eq(self):
        test_cases = [
            {
                "name": "true_two_bounded_leq",
                "bound_1": Bound.leq(1),
                "bound_2": Bound.leq(1),
                "expected": True,
            },
            {
                "name": "true_two_unbounded",
                "bound_1": Bound.unbounded(),
                "bound_2": Bound.unbounded(),
                "expected": True,
            },
            {
                "name": "false_two_bounded_leq",
                "bound_1": Bound.leq(1),
                "bound_2": Bound.leq(2),
                "expected": False,
            },
            {
                "name": "false_bounded_one_leq_one_less",
                "bound_1": Bound.leq(1),
                "bound_2": Bound.le(1),
                "expected": False,
            },
        ]

        for tc in test_cases:
            self.assertEqual(
                tc["bound_1"] == tc["bound_2"],
                tc["expected"],
                f"failed test case {tc['name']}: expected {tc['bound_1']} == \
                    {tc['bound_2']} to be {tc['expected']}",
            )

    def test_lt(self):
        test_cases = [
            {
                "name": "two_bound_leq_greater_n",
                "bound_1": Bound.leq(1),
                "bound_2": Bound.leq(2),
                "expected": True,
            },
            {
                "name": "two_bound_leq_equal_n",
                "bound_1": Bound.leq(1),
                "bound_2": Bound.leq(1),
                "expected": False,
            },
            {
                "name": "two_bound_leq_smaller_n",
                "bound_1": Bound.leq(2),
                "bound_2": Bound.leq(2),
                "expected": False,
            },
            {
                "name": "two_bound_one_less_one_leq_greater_n",
                "bound_1": Bound.leq(1),
                "bound_2": Bound.leq(2),
                "expected": True,
            },
            {
                "name": "two_bound_one_less_one_leq_greater_n",
                "bound_1": Bound.leq(1),
                "bound_2": Bound.le(2),
                "expected": True,
            },
            {
                "name": "one_leq_one_unbounded",
                "bound_1": Bound.leq(1),
                "bound_2": Bound.unbounded(),
                "expected": True,
            },
            {
                "name": "one_leq_one_unbounded",
                "bound_1": Bound.le(1),
                "bound_2": Bound.unbounded(),
                "expected": True,
            },
            {
                "name": "one_unbounded_one_leq_bounded",
                "bound_1": Bound.unbounded(),
                "bound_2": Bound.leq(1),
                "expected": False,
            },
            {
                "name": "one_unbounded_one_less_bounded",
                "bound_1": Bound.unbounded(),
                "bound_2": Bound.le(1),
                "expected": False,
            },
            {
                "name": "two_bound_one_less_one_leq_equal_n",
                "bound_1": Bound.le(1),
                "bound_2": Bound.leq(1),
                "expected": True,
            },
            {
                "name": "two_bound_one_leq_one_less_equal_n",
                "bound_1": Bound.leq(1),
                "bound_2": Bound.le(1),
                "expected": False,
            },
            {
                "name": "two_bound_one_leq_one_less_equal_n",
                "bound_1": Bound.le(1),
                "bound_2": Bound.leq(1),
                "expected": True,
            },
        ]

        for tc in test_cases:
            self.assertEqual(
                tc["bound_1"] < tc["bound_2"],
                tc["expected"],
                f"failed test case {tc['name']}: expected {tc['bound_1']} < \
                    {tc['bound_2']} to equal {tc['expected']}",
            )

    def test_add(self):
        test_cases = [
            {
                "name": "two_bounded_leq",
                "bound_1": Bound.leq(1),
                "bound_2": Bound.leq(2),
                "expected": Bound.leq(3),
            },
            {
                "name": "two_bounded_less",
                "bound_1": Bound.le(1),
                "bound_2": Bound.le(2),
                "expected": Bound.le(3),
            },
            {
                "name": "one_bounded_less_one_bounded_less_eq",
                "bound_1": Bound.leq(1),
                "bound_2": Bound.le(2),
                "expected": Bound.le(3),
            },
            {
                "name": "one_bounded_leq_one_unbounded",
                "bound_1": Bound.leq(1),
                "bound_2": Bound.unbounded(),
                "expected": Bound.unbounded(),
            },
            {
                "name": "one_bounded_less_one_unbounded",
                "bound_1": Bound.unbounded(),
                "bound_2": Bound.le(1),
                "expected": Bound.unbounded(),
            },
        ]

        for tc in test_cases:
            self.assertEqual(
                tc["bound_1"] + tc["bound_2"],
                tc["expected"],
                f"failed test case {tc['name']}: expected {tc['bound_1']} + \
                    {tc['bound_2']} to equal {tc['expected']}",
            )
