from typing import List, Tuple, Iterator

from family_foto import File
from family_foto.services.thumbnail_service import generate

MONTH_NAMES = ['January', 'February', 'March', 'April', 'June', 'July', 'August', 'September',
               'October', 'November', 'December']


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

    @property
    def month_name(self) -> str:
        """
        Returns the name of the month.
        """
        if self.month == -1:
            return 'No month given'
        return MONTH_NAMES[self.month]

    def add_file(self, file: File):
        """
        Adds a file to this month.
        :param file: to be added to this year
        """
        self._files.append(file)

    def media(self, width: int, height: int) -> Iterator[Tuple[File, str]]:
        """
        Gets the thumbnail paths and the files it selves.
        :param width: of the thumbnails in pixel
        :param height: of the thumbnails in pixel
        :return: a tuple of the file list and a list of paths to the thumbnails
        """
        return zip(self._files, self.get_thumbnails(width, height))

    def get_thumbnails(self, width: int, height: int) -> List[str]:
        """
        Returns the path to all thumbnails of the this month.
        :return: list of paths
        """
        return [generate(file, width, height) for file in self._files]
