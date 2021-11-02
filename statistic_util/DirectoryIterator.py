from glob import glob
import numpy as np
import tensorflow as tf

from statistic_util.Producer import Producer


class DirectoryIterator(Producer):

    def __init__(self, directory: str):
        self._directory = self._sanitize_path(directory)

        self._directory_files = glob(directory + "*")

        super().__init__(self, self._directory_files[:3000])

    @staticmethod
    def _sanitize_path(directory: str) -> str:
        if not directory[-1] == '\\' or not directory[-1] == '/':
            directory += '/'
        return directory
