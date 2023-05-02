import unittest
from dbm.bound import *


class TestBound(unittest.TestCase):
    def test_eq(self):

        test_cases = [
            {
                "name": "true_two_bounded_leq",
                "bound_1": Bound.less_equal(1),
                "bound_2": Bound.less_equal(1),
                "expected": True
            },
            {
                "name": "true_two_unbounded",
                "bound_1": Bound.unbounded(),
                "bound_2": Bound.unbounded(),
                "expected": True
            },
            {
                "name": "false_two_bounded_leq",
                "bound_1": Bound.less_equal(1),
                "bound_2": Bound.less_equal(2),
                "expected": False
            },
            {
                "name": "false_bounded_one_leq_one_less",
                "bound_1": Bound.less_equal(1),
                "bound_2": Bound.less(1),
                "expected": False
            },
        ]

        for tc in test_cases:
            self.assertEqual(
                tc["bound_1"] == tc["bound_2"],
                tc["expected"],
                "failed test case {}: expected {} == {} to be {}".format(
                    tc["name"],
                    tc["bound_1"],
                    tc["bound_2"],
                    tc["expected"])
            )

    def test_lt(self):
        test_cases = [
            {
                "name": "two_bound_leq_greater_n",
                "bound_1": Bound.less_equal(1),
                "bound_2": Bound.less_equal(2),
                "expected": True
            },
            {
                "name": "two_bound_leq_equal_n",
                "bound_1": Bound.less_equal(1),
                "bound_2": Bound.less_equal(1),
                "expected": False
            },
            {
                "name": "two_bound_leq_smaller_n",
                "bound_1": Bound.less_equal(2),
                "bound_2": Bound.less_equal(2),
                "expected": False
            },
            {
                "name": "two_bound_one_less_one_leq_greater_n",
                "bound_1": Bound.less_equal(1),
                "bound_2": Bound.less_equal(2),
                "expected": True
            },
            {
                "name": "two_bound_one_less_one_leq_greater_n",
                "bound_1": Bound.less_equal(1),
                "bound_2": Bound.less(2),
                "expected": True
            },
            {
                "name": "one_leq_one_unbounded",
                "bound_1": Bound.less_equal(1),
                "bound_2": Bound.unbounded(),
                "expected": True
            },
            {
                "name": "one_leq_one_unbounded",
                "bound_1": Bound.less(1),
                "bound_2": Bound.unbounded(),
                "expected": True
            },
            {
                "name": "one_unbounded_one_leq_bounded",
                "bound_1": Bound.unbounded(),
                "bound_2": Bound.less_equal(1),
                "expected": False
            },
            {
                "name": "one_unbounded_one_less_bounded",
                "bound_1": Bound.unbounded(),
                "bound_2": Bound.less(1),
                "expected": False
            },
            {
                "name": "two_bound_one_less_one_leq_equal_n",
                "bound_1": Bound.less(1),
                "bound_2": Bound.less_equal(1),
                "expected": True
            },
            {
                "name": "two_bound_one_leq_one_less_equal_n",
                "bound_1": Bound.less_equal(1),
                "bound_2": Bound.less(1),
                "expected": False
            },
            {
                "name": "two_bound_one_leq_one_less_equal_n",
                "bound_1": Bound.less(1),
                "bound_2": Bound.less_equal(1),
                "expected": True
            },
        ]

        for tc in test_cases:
            self.assertEqual(
                tc["bound_1"] < tc["bound_2"],
                tc["expected"],
                "failed test case {}: expected {} < {} to be {}".format(
                    tc["name"],
                    tc["bound_1"],
                    tc["bound_2"],
                    tc["expected"])
            )

    def test_add(self):
        test_cases = [
            {
                "name": "two_bounded_leq",
                "bound_1": Bound.less_equal(1),
                "bound_2": Bound.less_equal(2),
                "expected": Bound.less_equal(3)
            },
            {
                "name": "two_bounded_less",
                "bound_1": Bound.less(1),
                "bound_2": Bound.less(2),
                "expected": Bound.less(3)
            },
            {
                "name": "one_bounded_less_one_bounded_less_eq",
                "bound_1": Bound.less_equal(1),
                "bound_2": Bound.less(2),
                "expected": Bound.less(3)
            },
            {
                "name": "one_bounded_leq_one_unbounded",
                "bound_1": Bound.less_equal(1),
                "bound_2": Bound.unbounded(),
                "expected": Bound.unbounded()
            },
            {
                "name": "one_bounded_less_one_unbounded",
                "bound_1": Bound.unbounded(),
                "bound_2": Bound.less(1),
                "expected": Bound.unbounded()
            },
        ]

        for tc in test_cases:
            self.assertEqual(
                tc["bound_1"] + tc["bound_2"],
                tc["expected"],
                "failed test case {}: expected {} + {} to be {}".format(
                    tc["name"],
                    tc["bound_1"],
                    tc["bound_2"],
                    tc["expected"])
            )
