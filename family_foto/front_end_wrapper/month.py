from typing import List

from family_foto import File


class Month:
    """
    This contains all available files of that month
    """

    def __init__(self, files: List[File], month: int, year: int):
        self.month = month
        self.year = year
        self.files = files
