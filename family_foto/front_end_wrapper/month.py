from typing import List

from family_foto import File
from family_foto.services.thumbnail_service import generate


class Month:
    """
    This contains all available files of that month
    """

    def __init__(self, files: List[File], month: int, year: int):
        self.month = month
        self.year = year
        self._files = files

    def __eq__(self, other):
        if not isinstance(other, Month) or self.month != other.month or self.year != other.year:
            return False
        return self._files == other._files

    def get_thumbnails(self, width: int, height: int) -> List[str]:
        """
        Returns the path to all thumbnails of the this month.
        :return: list of paths
        """
        return [generate(file, width, height) for file in self._files]
