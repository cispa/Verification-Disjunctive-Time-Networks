import math
from enum import Enum


class BoundType(Enum):
    """BoundType is used to represent the constraint type in a DBM, it can either
    be ≤ / LEQ or < / LESS"""
    LEQ = 0,
    LESS = 1,

    def __str__(self) -> str:

        if self == BoundType.LEQ:
            return "≤"
        else:
            return "<"


class Bound():
    """Bound represents a bound in a DBM. It can require a difference between to be less or less equal bound to an integer value."""

    def __init__(self, n: int, ty: BoundType) -> None:
        self.n = n
        self.ty = ty

    def __str__(self) -> str:
        return "({},{})".format(self.n, self.ty)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        """= as defined in
        https://www.seas.upenn.edu/~lee/09cis480/papers/by-lncs04.pdf"""
        equal = (self.n == other.n) and (self.ty == other.ty)
        inf = self.is_unbounded() and other.is_unbounded()
        return equal or inf

    def __lt__(self, other) -> bool:
        """< as defined in
        https://www.seas.upenn.edu/~lee/09cis480/papers/by-lncs04.pdf"""
        if self.n < other.n:
            return True
        if other.is_unbounded():
            return True
        if (self.n == other.n) and (self.ty == BoundType.LESS) and (other.ty == BoundType.LEQ):
            return True
        return False

    def __le__(self, other) -> bool:
        """<= derived from < and ="""
        return (self < other) or (self == other)

    def __gt__(self, other) -> bool:
        """> derived from < and ="""
        return not (self <= other)

    def __ge__(self, other) -> bool:
        """>= derived from <"""
        return not (self < other)

    def __add__(self, other) -> 'Bound':
        """+ as defined in
          https://www.seas.upenn.edu/~lee/09cis480/papers/by-lncs04.pdf"""
        if (self.n == math.inf) or (other.n == math.inf):
            return Bound.unbounded()
        else:
            n = self.n + other.n
            if (self.ty == BoundType.LEQ) and (other.ty == BoundType.LEQ):
                ty = BoundType.LEQ
            else:
                ty = BoundType.LESS

            return Bound(n, ty)

    def __neg__(self) -> 'Bound':
        """neg returns a Bound with negated numeric value"""
        return Bound(-self.n, self.ty)

    def is_unbounded(self) -> bool:
        """is_unbounded checks whether it is an unbounded / infinite constraint"""
        return self.n == math.inf

    def get_value(self) -> int:
        """get_value returns the numeric value of the Bound"""
        return self.n

    def get_value_abs(self) -> int:
        """get_value_abs returns the absolute numeric value of the Bound"""
        if self.n < 0:
            return -self.n
        else:
            return self.n

    @classmethod
    def unbounded(cls):
        """unbounded returns a bound representing an infinite or unbounded\
        constraint"""
        return Bound(math.inf, BoundType.LEQ)

    @classmethod
    def less_equal(cls, n: int):
        """less_equal returns a bound requiring the difference between two clocks 
            to be smaller or equal than n"""
        return Bound(n, BoundType.LEQ)

    @classmethod
    def less(cls, n: int):
        """less_equal returns a bound requiring the difference between two clocks 
        to be smaller than n"""
        return Bound(n, BoundType.LESS)
