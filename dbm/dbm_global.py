""" This file contains all functionality for DBMs with an additional "global
    clock".

    This "global clock" is an additional clock added to a zone which can be
    never reset through a transition. Therefore such a clock can be used how
    much global time has passed.
"""

import copy

from typing import List, Optional

from dbm.dbm import DBM, ZERO
from dbm.bound import Bound
from dbm.constraint import Constraint

# Name of the global clock
DELTA = "delta"


class DBMG(DBM):
    """DBMGlobal is a special for of a DBM with an additional global clock
    named as defined in the constant DELTA intended to track the global time
    that has passed.
    """

    def __init__(
        self, clocks: List[str], m: Optional[List[List["Bound"]]] = None
    ) -> None:
        assert DELTA not in clocks
        clocks.append(DELTA)
        super().__init__(clocks, m)

    def __str__(self) -> str:
        return "DBMG\n" + super().__str__()

    def __repr__(self) -> str:
        return self.__str__()

    def extrapolate(self, max_clock: int, max_delta: int) -> None:
        """This function extrapolates the regular clocks with constant
        `max_clock` and the delta clock with `max_delta`.

        I.e. if the difference between any two clocks is larger than
        `max clock` or the difference between a regular clock and the global
        clock is greater than `max_delta` it will be replaced by an
        unbounded difference.

        Args:
            max_clock (int): maximal clock valuation of regular clock
                constraints
            max_delta (int): maximal clock valuation of clock constraints on
                the global clock
        """
        delta_ind = self.clocks[DELTA]

        for i in range(len(self.m)):
            for j in range(len(self.m)):
                if delta_ind not in (i, j):
                    if self.m[i][j].get_value() > max_clock:
                        self.m[i][j] = Bound.unbounded()
                    if self.m[i][j].get_value() < -max_clock:
                        self.m[i][j] = Bound.le(-max_clock)
                else:
                    if self.m[i][j].get_value() > max_delta:
                        self.m[i][j] = Bound.unbounded()
                    if self.m[i][j].get_value() < -max_delta:
                        self.m[i][j] = Bound.le(-max_delta)

    def __lt__(self, other: "DBMG") -> bool:
        """< is defined on the lower bound of the global clock value"""
        return (
            self.get_min_global_bound().get_value_abs()
            < other.get_min_global_bound().get_value_abs()
        )

    def get_dbm(self) -> "DBM":
        """Returns a copy of the inner dbm without the global clock"""
        m = copy.deepcopy(self.m)
        for l in m:
            del l[self.clocks[DELTA]]
        del m[self.clocks[DELTA]]

        clocks = list(self.clocks.keys())
        clocks.remove(DELTA)
        clocks.remove(ZERO)

        return DBM(clocks, m)

    def get_min_bound_on_clock(self, clock: str) -> "Bound":
        self.canonicalize()
        ind_clock = self.clocks[clock]
        ind_0 = self.clocks[ZERO]
        return self.m[ind_0][ind_clock]

    def get_max_bound_on_clock(self, clock: str) -> "Bound":
        self.canonicalize()
        ind_clock = self.clocks[clock]
        ind_0 = self.clocks[ZERO]
        return self.m[ind_clock][ind_0]

    def get_min_global(self) -> "Constraint":
        """Returns a constraint representing the lower bound on the global time
        in this DBM
        """
        return Constraint("0", DELTA, self.get_min_global_bound())

    def get_min_global_bound(self) -> "Bound":
        """Returns the Bound on the minimum global time of the DBM"""
        self.canonicalize()
        ind_delta = self.clocks[DELTA]
        ind_0 = self.clocks[ZERO]
        return self.m[ind_0][ind_delta]

    def get_max_global(self) -> "Constraint":
        """Returns a constraint representing the upper bound on the global time
        in this DBM
        """
        return Constraint(DELTA, "0", self.get_max_global_bound())

    def get_max_global_bound(self) -> "Bound":
        """Returns the Bound on the maximal global time of the DBM"""
        self.canonicalize()
        ind_delta = self.clocks[DELTA]
        ind_0 = self.clocks[ZERO]
        return self.m[ind_delta][ind_0]
