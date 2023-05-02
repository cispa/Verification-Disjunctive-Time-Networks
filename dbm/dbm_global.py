from dbm.dbm import *

DELTA = "delta"


class DBMGlobal(DBM):
    """DBMGlobal is a DBM with an additional global clock delta intended to track global time"""

    def __init__(self, clocks: List[str], m=None) -> None:
        assert not (DELTA in clocks)
        clocks.append(DELTA)
        super().__init__(clocks, m)

    def __str__(self) -> str:
        return "DBMGlobal\n" + super().__str__()

    def __repr__(self) -> str:
        return self.__str__()

    def extrapolate(self, max: int, max_delta: int) -> None:
        """This extrapolation extrapolates the delta clock with a different maximal value"""
        delta_ind = self.clocks[DELTA]

        for i in range(len(self.m)):
            for j in range(len(self.m)):
                if (i != delta_ind) and j != (delta_ind):
                    if self.m[i][j].get_value() > max:
                        self.m[i][j] = Bound.unbounded()
                    if self.m[i][j].get_value() < -max:
                        self.m[i][j] = Bound.less(-max)
                else:
                    if self.m[i][j].get_value() > max_delta:
                        self.m[i][j] = Bound.unbounded()
                    if self.m[i][j].get_value() < -max_delta:
                        self.m[i][j] = Bound.less(-max_delta)

    def __lt__(self, other: 'DBMGlobal') -> bool:
        """< is defined on the minimum global clock value"""
        return self.get_min_global_bound().get_value_abs() < other.get_min_global_bound().get_value_abs()

    def get_dbm(self) -> 'DBM':
        """get_dbm returns a copy of the inner dbm without the delta clock"""
        m = copy.deepcopy(self.m)
        for l in m:
            del l[self.clocks[DELTA]]
        del m[self.clocks[DELTA]]

        clocks = list(self.clocks.keys())
        clocks.remove(DELTA)
        clocks.remove(ZERO)

        return DBM(clocks, m)

    def get_min_bound_on_clock(self, clock) -> 'Bound':
        self.canonicalize()
        ind_clock = self.clocks[clock]
        ind_0 = self.clocks[ZERO]
        return self.m[ind_0][ind_clock]

    def get_max_bound_on_clock(self, clock) -> 'Bound':
        self.canonicalize()
        ind_clock = self.clocks[clock]
        ind_0 = self.clocks[ZERO]
        return self.m[ind_clock][ind_0]

    def get_min_global(self) -> 'Constraint':
        """get_min_global returns a constraint that corresponds to the minimum global time required by the DBM."""
        return Constraint("0", DELTA, self.get_min_global_bound())

    def get_min_global_bound(self) -> 'Bound':
        """get_min_global_bound returns the Bound on the minimum global of the DBM."""
        self.canonicalize()
        ind_delta = self.clocks[DELTA]
        ind_0 = self.clocks[ZERO]
        return self.m[ind_0][ind_delta]

    def get_max_global(self) -> 'Constraint':
        """get_max_global returns a constraint that corresponds to the maximal global time required by the DBM."""
        return Constraint(DELTA, "0", self.get_max_global_bound())

    def get_max_global_bound(self) -> 'Bound':
        """get_max_global_bound returns the Bound on the maximum global of the DBM."""
        self.canonicalize()
        ind_delta = self.clocks[DELTA]
        ind_0 = self.clocks[ZERO]
        return self.m[ind_delta][ind_0]
