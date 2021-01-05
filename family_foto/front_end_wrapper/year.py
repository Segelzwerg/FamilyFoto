from operator import attrgetter
from typing import List

from family_foto.front_end_wrapper.month import Month
from family_foto.models.file import File


class Year:
    """
    This contains all available files of that year.
    """

    def __init__(self, months: List[Month], year: int):
        self.months = months
        self.year = year
        self._sort()

    def __eq__(self, other):
        if not isinstance(other, Year) or self.year != other.year:
            return False
        return self.months == other.months

    def _sort(self):
        self.months = sorted(self.months, key=attrgetter('month'), reverse=True)

    def add_file(self, file: File) -> None:
        """
        Adds a file to this year.
        :param file: to be added to this year
        """
        month_no = file.month
        months = [month for month in self.months if month.month == month_no]
        if len(months) == 0:
            self.months.append(Month([file], month_no, self.year))
        else:
            months[0].add_file(file)
        self._sort()
