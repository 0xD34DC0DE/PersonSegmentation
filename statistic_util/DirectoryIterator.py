

from glob import glob
import numpy as np
import tensorflow as tf
import multiprocessing

from statistic_util.Mapper import Mapper


class DirectoryIterator(object):

    def __init__(self, directory: str):
        self.directory = self.sanitize_path(directory)

        self.directory_files = glob(directory + "*")
        self.file_iterator = iter(self.directory_files)

    def sanitize_path(self, directory: str) -> str:
        if not directory[-1] == '\\' or not directory[-1] == '/':
            directory += '/'
        return directory

    def _load_image(self, filepath: str) -> np.ndarray:
        return tf.image.decode_jpeg(tf.io.read_file(filepath)).numpy

    def __iter__(self) -> np.ndarray:
        for file_path in self.directory_files[:3000]:
            yield self._load_image(file_path)