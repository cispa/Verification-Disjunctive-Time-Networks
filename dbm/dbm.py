import copy
from typing import List
from dbm.bound import *
from dbm.constraint import *

# Possible improvements:
#   Currently, canonicalization will always execute the full Floyd Warshall
#   algorithm rather than checking for which entries that might be necessary.
#   More can be found in
#       https://www.seas.upenn.edu/~lee/09cis480/papers/by-lncs04.pdf


class DBM:
    """DBM represents a difference bound matrix and allows for operations on
    them."""

    def __init__(self, clocks: List[str], m=None) -> None:
        """initializes the DBM by allowing an arbitrary clock valuation with all
        clocks being synchronized"""
        assert not (ZERO in clocks)

        # add the zero clock to the list of clocks
        self.clocks = {ZERO: 0}
        # index clocks
        for i in range(len(clocks)):
            self.clocks[clocks[i]] = i + 1

        self.__is_empty = False

        if not m is None:
            assert len(m) == len(self.clocks)
            self.m = m
            self.__is_canonical = False
            return

        # initialize DBM matrix
        m = []
        for i in range(len(self.clocks)):
            m.append([])
            for j in range(len(self.clocks)):
                if j == 0 and i != 0:
                    m[i].append(Bound.unbounded())
                else:
                    m[i].append(Bound.less_equal(0))
        self.m = m
        self.__is_canonical = True

    def __str__(self) -> str:
        s = "[\n"
        for i in range(len(self.clocks)):
            s += "["
            for j in range(len(self.clocks)):
                s += str(self.m[i][j]) + "\t"
            s += "]\n"
        s += "]"
        return s

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: 'DBM') -> bool:
        """Implements equality. Two DBMs are considered equal if they have the same clocks and the entries are the same (in their canonical form)"""
        if self.clocks != other.clocks:
            return False

        self.canonicalize()
        other.canonicalize()

        return self.m == other.m

    def __get_clock_names(self) -> List[str]:
        """Get the names of clocks excluding the 0 clock"""
        clocks = [key for key in self.clocks.keys()]
        clocks.remove(ZERO)
        return clocks

    def __check_constraints_satisfiable(self) -> bool:
        """Check if constraints in the DBM are satisfiable or if the set of
        clock valuations that satisfy this DBM is empty"""

        # Check for negative self-loops indicating a negative loop.
        # For self loops to be negative, the DBM has to be in the
        # canonical form.
        # See https://www.seas.upenn.edu/~lee/09cis480/papers/by-lncs04.pdf
        assert self.__is_canonical

        if self.__is_empty:
            return False

        for i in range(len(self.m)):
            for j in range(len(self.m)):
                if i == j:

                    if (self.m[i][i].get_value() < 0):
                        self.__is_empty = True
                        return False
                elif j < i:
                    if self.m[i][j] < - self.m[j][i]:
                        self.__is_empty = True
                        return False
                    # Check whether both are strictly less bounds and therefore contradicting
                    elif self.m[i][j] == - self.m[j][i]:
                        if self.m[i][j].ty == BoundType.LESS:
                            self.__is_empty = True
                            return False
        return True

    def canonicalize(self) -> bool:
        """Canonicalize the DBM by tightening all constraints and checks whether\
            the DBM is non-empty.Returns False if the DBM is empty"""
        # See https://www.seas.upenn.edu/~lee/09cis480/papers/by-lncs04.pdf
        if self.__is_empty:
            return False

        if not self.__is_canonical:
            self.m = floyd_warshall(self.m)
            self.__is_canonical = True

        return self.__check_constraints_satisfiable()

    def is_not_empty(self) -> bool:
        """Checks whether there are clock evaluations that can satisfy a DBM"""
        return self.canonicalize()

    def reset(self, clocks: List[str]) -> None:
        """Resets the given list of clocks"""
        if not (self.__is_canonical):
            self.canonicalize()

        for clock in clocks:
            c = self.clocks[clock]
            for i in range(len(self.m)):
                self.m[c][i] = self.m[0][i]
                self.m[i][c] = self.m[i][0]
            self.m[0][c] = Bound.less_equal(0)
            self.m[c][0] = Bound.less_equal(0)

    def delay(self) -> None:
        """Delays all clocks by setting their upper bound to infinity."""
        for i in range(1, len(self.m)):
            self.m[i][0] = Bound.unbounded()

    def intersect(self, other: 'DBM') -> 'DBM':
        """intersect computes the intersection between two DBMs"""
        # Defined in https://www.seas.upenn.edu/~lee/09cis480/papers/by-lncs04.pdf
        assert self.clocks == other.clocks

        self.canonicalize()
        other.canonicalize()

        m = []

        for i in range(len(self.m)):
            tmp = []
            for j in range(len(self.m[i])):
                if self.m[i][j] <= other.m[i][j]:
                    b = self.m[i][j]
                else:
                    b = other.m[i][j]
                tmp.append(copy.deepcopy(b))
            m.append(tmp)

        return DBM(self.__get_clock_names(), m)

    def and_constr(self, constr: 'Constraint') -> bool:
        """ands a constraint to the DBM"""
        # Defined in https://www.seas.upenn.edu/~lee/09cis480/papers/by-lncs04.pdf
        # TODO: Improvement: speedup emptiness by checking here
        i = self.clocks[constr.get_c_1()]
        j = self.clocks[constr.get_c_2()]

        if self.m[i][j] > constr.get_bound():
            self.m[i][j] = constr.get_bound()
            self.__is_canonical = False


def floyd_warshall(dist):
    """Executes Floyd Warshall on the graph given in matrix form"""
    for k in range(len(dist)):
        # Pick all vertices as source one by one
        for i in range(len(dist)):
            # Pick all vertices as destination for the above picked source
            for j in range(len(dist)):
                # If vertex k is on the shortest path from i to j, then update
                # the value of dist[i][j]
                if (dist[i][k] + dist[k][j] < dist[i][j]):
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
