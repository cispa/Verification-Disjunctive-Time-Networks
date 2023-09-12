""" This file contains the constraint functionality. A constraint represents a
    difference bound between two specific clocks and can be used as an entry in
    a DBM
"""
from dbm.bound import Bound

# Representation of the constantly zero clock
ZERO = "0"


class Constraint:
    """Constraint represents a single constraint over clocks a,b of the form
    a - b ≤ c / a - b < c, where `< c` is represented by a Bound object.
    """

    def __str__(self) -> str:
        return f"{self.c_1} - {self.c_2} {self.bound}"

    def __repr__(self) -> str:
        return self.__str__()

    def __init__(self, c_1: str, c_2: str, bound: "Bound"):
        """Creates a constraint over clocks c_1, c_2  with c_1 - c_2 ≤ / < c"""
        self.c_1 = c_1
        self.c_2 = c_2
        self.bound = bound

    def __eq__(self, other) -> bool:
        return (
            self.c_1 == other.c_1
            and self.c_2 == other.c_2
            and self.bound == other.bound
        )

    def get_c_1(self) -> str:
        return self.c_1

    def get_c_2(self) -> str:
        return self.c_2

    def get_bound(self) -> "Bound":
        return self.bound

    def is_upper_bound(self) -> bool:
        """Returns True if constraint is an upper bound, i.e. its second
        clock is the ZERO clock and it is not unbounded
        """
        return self.c_2 == ZERO and self.bound != Bound.unbounded()


# TODO
#    @classmethod
#    def parse(self, s: str) -> List["Constraint"]:
#        raise Exception("unimplemented")
