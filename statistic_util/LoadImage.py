from statistic_util.Mapper import Mapper

import tensorflow as tf


class LoadImage(Mapper):
    def __init__(self):
        super().__init__()

    @staticmethod
    def _process(item):
        return tf.image.decode_jpeg(tf.io.read_file(item)).numpy()