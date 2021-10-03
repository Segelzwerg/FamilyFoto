from typing import List, Dict, Iterator, Tuple

from family_foto.front_end_wrapper.month import Month
from family_foto.front_end_wrapper.year import Year
from family_foto.models.file import File


class Splitter:
    """
    Splits files into years and months.
    """

    def __init__(self, files: List[File]):
        self._files = files

    def split(self) -> Dict[int, Year]:
        """
        Splits the files into years.
        """
        splits = {}
        for file in self._files:
            if file.year not in splits.keys():
                month = Month([file], file.month, file.year)
                year = Year([month], file.year)
                splits.update({file.year: year})

            else:
                splits[file.year].add_file(file)

        return splits

    def sorted_years(self):
        """
        Returns the split sorted.
        """
        splits = self.split()
        # noinspection PyTypeChecker
        sorted_splits: Iterator[Tuple[int, Year]] = sorted(splits.items(), reverse=True)
        return [year[1] for year in sorted_splits]
