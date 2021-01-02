from typing import List

from family_foto.front_end_wrapper.month import Month


class Year:
    """
    This contains all available files of that year.
    """

    def __init__(self, months: List[Month], year: int):
        self.months = months
        self.year = year

    def __eq__(self, other):
        if not isinstance(other, Year) or self.year != other.year:
            return False
        return self.months == other.months
