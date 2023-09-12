""" This module implements functionality for bounds between clocks.
"""
import math
from enum import Enum


class BoundType(Enum):
    """BoundType is used to represent the constraint type in a DBM, it can
    either be ≤ / LEQ or < / LESS
    """

    LEQ = 0
    LESS = 1

    def __str__(self) -> str:
        if self == BoundType.LEQ:
            return "≤"
        else:
            return "<"


class Bound:
    """A Bound represents a bound in a DBM. It requires the difference between
    to clock valuations to be less or less equal bound to an integer value.

    All operations implemented here were formally defined in the paper
    https://www.seas.upenn.edu/~lee/09cis480/papers/by-lncs04.pdf
    """

    def __init__(self, n: int, ty: BoundType) -> None:
        self.n = n
        self.ty = ty

    def __str__(self) -> str:
        return f"({self.n},{self.ty})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        """= as defined in
        https://www.seas.upenn.edu/~lee/09cis480/papers/by-lncs04.pdf
        """
        equal = (self.n == other.n) and (self.ty == other.ty)
        inf = self.is_unbounded() and other.is_unbounded()
        return equal or inf

    def __lt__(self, other) -> bool:
        """< as defined in
        https://www.seas.upenn.edu/~lee/09cis480/papers/by-lncs04.pdf
        """
        if self.n < other.n:
            return True
        if other.is_unbounded():
            return True
        if (
            (self.n == other.n)
            and (self.ty == BoundType.LESS)
            and (other.ty == BoundType.LEQ)
        ):
            return True
        return False

    def __le__(self, other) -> bool:
        """<= derived from < and ="""
        return (self < other) or (self == other)

    def __gt__(self, other) -> bool:
        """> derived from < and ="""
        return not self <= other

    def __ge__(self, other) -> bool:
        """>= derived from <"""
        return not self < other

    def __add__(self, other) -> "Bound":
        """+ as defined in
        https://www.seas.upenn.edu/~lee/09cis480/papers/by-lncs04.pdf
        """
        if math.inf in (self.n, other.n):
            return Bound.unbounded()
        else:
            n = self.n + other.n
            if (self.ty == BoundType.LEQ) and (other.ty == BoundType.LEQ):
                ty = BoundType.LEQ
            else:
                ty = BoundType.LESS

            return Bound(n, ty)

    def __neg__(self) -> "Bound":
        """Returns a Bound with negated numeric value"""
        return Bound(-self.n, self.ty)

    def is_unbounded(self) -> bool:
        """Checks whether it is an unbounded / infinite constraint

        Returns:
            True if it is unbounded
        """
        return self.n == math.inf

    def get_value(self) -> int:
        """Returns the numeric value of the Bound

        Returns:
            the integer value of the bound
        """
        return self.n

    def get_value_abs(self) -> int:
        """Returns the absolute numeric value of the Bound

        Returns:
            the absolute integer value of the bound
        """
        if self.n < 0:
            return -self.n
        else:
            return self.n

    @classmethod
    def unbounded(cls) -> "Bound":
        """Creates a new infinite or unbounded Bound"""
        return Bound(math.inf, BoundType.LEQ)  # type: ignore

    @classmethod
    def leq(cls, n: int) -> "Bound":
        """Creates a new bound that requires the difference between two clocks
        to be smaller or equal than n, i.e. it represents a bound ≤ n

        Args:
            n (int): the numeric upper bound

        Returns:
            a new Bound object
        """
        return Bound(n, BoundType.LEQ)

    @classmethod
    def le(cls, n: int) -> "Bound":
        """Creates a new bound that requires the difference between two clocks
        to be smaller than n, i.e. it represents a bound < n

        Args:
            n (int): the numeric upper bound

        Returns:
            a new Bound object
        """
        return Bound(n, BoundType.LESS)
